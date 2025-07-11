"""File system utility functions for Bulk File Renamer."""

import os
import logging
from typing import List, Tuple, Optional
from pathlib import Path

from config.constants import LOG_FILENAME


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )


def get_files_in_directory(
    directory: str,
    file_types: List[str],
    recursive: bool = False
) -> List[str]:
    """
    Get list of files in directory matching specified file types.
    
    Args:
        directory: Path to the directory
        file_types: List of file extensions to include
        recursive: Whether to search subdirectories
        
    Returns:
        List of full file paths
    """
    if not directory or not os.path.exists(directory):
        return []
    
    files = []
    file_types_lower = [ft.lower().strip() for ft in file_types]
    
    try:
        if recursive:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if any(filename.lower().endswith(ft) for ft in file_types_lower):
                        full_path = os.path.join(root, filename)
                        files.append(full_path)
        else:
            for filename in os.listdir(directory):
                full_path = os.path.join(directory, filename)
                if os.path.isfile(full_path):
                    if any(filename.lower().endswith(ft) for ft in file_types_lower):
                        files.append(full_path)
    except (OSError, PermissionError) as e:
        logging.error(f"Error accessing directory {directory}: {e}")
        
    return sorted(files)


def parse_file_types(file_types_string: str) -> List[str]:
    """
    Parse comma-separated file types string into list.
    
    Args:
        file_types_string: Comma-separated file extensions
        
    Returns:
        List of file extensions
    """
    if not file_types_string:
        return []
    
    return [ft.strip() for ft in file_types_string.split(',') if ft.strip()]


def is_valid_filename(filename: str) -> bool:
    """
    Check if filename is valid for the current operating system.
    
    Args:
        filename: The filename to validate
        
    Returns:
        True if filename is valid, False otherwise
    """
    if not filename:
        return False
    
    # Check for invalid characters on Windows
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        return False
    
    # Check for reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = os.path.splitext(filename)[0].upper()
    if name_without_ext in reserved_names:
        return False
    
    # Check for names ending with space or period
    if filename.endswith(' ') or filename.endswith('.'):
        return False
    
    return True


def safe_rename(old_path: str, new_path: str) -> Tuple[bool, Optional[str]]:
    """
    Safely rename a file with error handling.
    
    Args:
        old_path: Current file path
        new_path: New file path
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Check if target already exists
        if os.path.exists(new_path):
            return False, f"Target file already exists: {new_path}"
        
        # Validate new filename
        new_filename = os.path.basename(new_path)
        if not is_valid_filename(new_filename):
            return False, f"Invalid filename: {new_filename}"
        
        # Ensure target directory exists
        target_dir = os.path.dirname(new_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # Perform the rename
        os.rename(old_path, new_path)
        logging.info(f"Renamed '{old_path}' to '{new_path}'")
        return True, None
        
    except (OSError, PermissionError) as e:
        error_msg = str(e)
        logging.error(f"Error renaming '{old_path}' to '{new_path}': {error_msg}")
        return False, error_msg


def get_unique_filename(file_path: str) -> str:
    """
    Generate a unique filename if the target already exists.
    
    Args:
        file_path: The desired file path
        
    Returns:
        A unique file path
    """
    if not os.path.exists(file_path):
        return file_path
    
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def backup_file(file_path: str, backup_dir: str = "backup") -> Optional[str]:
    """
    Create a backup of a file before renaming.
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backups
        
    Returns:
        Path to backup file or None if failed
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, filename)
        backup_path = get_unique_filename(backup_path)
        
        # Copy file to backup location
        import shutil
        shutil.copy2(file_path, backup_path)
        logging.info(f"Created backup: {backup_path}")
        return backup_path
        
    except Exception as e:
        logging.error(f"Failed to create backup for {file_path}: {e}")
        return None
