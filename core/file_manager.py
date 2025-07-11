"""File management functionality for Bulk File Renamer."""

import os
import logging
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass

from utils.file_utils import get_files_in_directory, parse_file_types, safe_rename
from utils.date_utils import get_date_by_type
from config.constants import DEFAULT_FILE_TYPES


@dataclass
class FileItem:
    """Represents a file to be renamed."""
    original_path: str
    original_name: str
    new_name: str = ""
    extension: str = ""
    directory: str = ""
    
    def __post_init__(self):
        """Initialize computed fields."""
        self.directory = os.path.dirname(self.original_path)
        self.original_name = os.path.basename(self.original_path)
        name, ext = os.path.splitext(self.original_name)
        self.original_name = name
        self.extension = ext
    
    @property
    def new_path(self) -> str:
        """Get the new full path for the file."""
        if self.new_name:
            return os.path.join(self.directory, self.new_name + self.extension)
        return self.original_path


class FileManager:
    """Manages file operations and maintains file list."""
    
    def __init__(self):
        self.files: List[FileItem] = []
        self.current_directory: str = ""
        self.file_types: List[str] = parse_file_types(DEFAULT_FILE_TYPES)
        self.recursive: bool = False
        self.progress_callback: Optional[Callable[[int, int], None]] = None
    
    def set_directory(self, directory: str) -> bool:
        """
        Set the current working directory.
        
        Args:
            directory: Path to the directory
            
        Returns:
            True if directory is valid and set, False otherwise
        """
        if not directory or not os.path.exists(directory) or not os.path.isdir(directory):
            return False
        
        self.current_directory = directory
        return True
    
    def set_file_types(self, file_types_string: str) -> None:
        """
        Set file types to filter by.
        
        Args:
            file_types_string: Comma-separated file extensions
        """
        self.file_types = parse_file_types(file_types_string)
    
    def set_recursive(self, recursive: bool) -> None:
        """
        Set whether to search subdirectories.
        
        Args:
            recursive: True to include subdirectories
        """
        self.recursive = recursive
    
    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback function for progress updates.
        
        Args:
            callback: Function that takes (current, total) parameters
        """
        self.progress_callback = callback
    
    def load_files(self) -> bool:
        """
        Load files from current directory based on current settings.
        
        Returns:
            True if files loaded successfully, False otherwise
        """
        if not self.current_directory:
            return False
        
        try:
            file_paths = get_files_in_directory(
                self.current_directory,
                self.file_types,
                self.recursive
            )
            
            self.files.clear()
            for file_path in file_paths:
                file_item = FileItem(original_path=file_path)
                self.files.append(file_item)
            
            logging.info(f"Loaded {len(self.files)} files from {self.current_directory}")
            return True
            
        except Exception as e:
            logging.error(f"Error loading files: {e}")
            return False
    
    def get_file_count(self) -> int:
        """Get number of loaded files."""
        return len(self.files)
    
    def get_files(self) -> List[FileItem]:
        """Get list of all files."""
        return self.files.copy()
    
    def get_file_at(self, index: int) -> Optional[FileItem]:
        """Get file at specific index."""
        if 0 <= index < len(self.files):
            return self.files[index]
        return None
    
    def clear_files(self) -> None:
        """Clear all loaded files."""
        self.files.clear()
    
    def apply_text_replacement(
        self,
        find_text: str,
        replace_text: str,
        case_sensitive: bool = True
    ) -> None:
        """
        Apply find and replace to all file names.
        
        Args:
            find_text: Text to find
            replace_text: Text to replace with
            case_sensitive: Whether replacement is case sensitive
        """
        if not find_text:
            return
        
        import re
        
        for file_item in self.files:
            name = file_item.original_name
            
            if case_sensitive:
                new_name = name.replace(find_text, replace_text)
            else:
                new_name = re.sub(
                    re.escape(find_text),
                    replace_text,
                    name,
                    flags=re.IGNORECASE
                )
            
            file_item.new_name = new_name
    
    def apply_prefix_suffix(self, prefix: str = "", suffix: str = "") -> None:
        """
        Apply prefix and/or suffix to all file names.
        
        Args:
            prefix: Prefix to add
            suffix: Suffix to add
        """
        for file_item in self.files:
            name = file_item.original_name
            new_name = f"{prefix}{name}{suffix}"
            file_item.new_name = new_name
    
    def apply_sequential_numbering(
        self,
        start_number: int = 1,
        padding: int = 3
    ) -> None:
        """
        Apply sequential numbering to all files.
        
        Args:
            start_number: Starting number
            padding: Number of digits (zero-padded)
        """
        for i, file_item in enumerate(self.files):
            number = str(start_number + i).zfill(padding)
            # If new_name is already set, append number, otherwise use original name
            base_name = file_item.new_name if file_item.new_name else file_item.original_name
            file_item.new_name = f"{base_name}_{number}"
    
    def apply_date_addition(
        self,
        date_type: str = "creation",
        date_format: str = "%Y-%m-%d"
    ) -> None:
        """
        Add date information to all file names.
        
        Args:
            date_type: Type of date ('creation', 'modification', 'exif')
            date_format: Format string for the date
        """
        for file_item in self.files:
            date_str = get_date_by_type(file_item.original_path, date_type, date_format)
            if date_str:
                base_name = file_item.new_name if file_item.new_name else file_item.original_name
                file_item.new_name = f"{base_name}_{date_str}"
    
    def apply_pattern(
        self,
        pattern_generator: Callable[[FileItem, int], str]
    ) -> None:
        """
        Apply a custom pattern to all files.
        
        Args:
            pattern_generator: Function that takes (file_item, index) and returns new name
        """
        for i, file_item in enumerate(self.files):
            try:
                new_name = pattern_generator(file_item, i)
                file_item.new_name = new_name
            except Exception as e:
                logging.error(f"Error applying pattern to {file_item.original_path}: {e}")
    
    def preview_changes(self) -> List[Tuple[str, str]]:
        """
        Get preview of all changes.
        
        Returns:
            List of (original_name, new_name) tuples
        """
        changes = []
        for file_item in self.files:
            original = file_item.original_name + file_item.extension
            new = (file_item.new_name + file_item.extension) if file_item.new_name else original
            changes.append((original, new))
        return changes
    
    def validate_changes(self) -> List[str]:
        """
        Validate all pending changes and return list of errors.
        
        Returns:
            List of error messages
        """
        errors = []
        new_names = set()
        
        for file_item in self.files:
            if not file_item.new_name:
                continue
            
            new_full_name = file_item.new_name + file_item.extension
            
            # Check for duplicate names
            if new_full_name in new_names:
                errors.append(f"Duplicate filename: {new_full_name}")
            else:
                new_names.add(new_full_name)
            
            # Check if target file already exists
            new_path = file_item.new_path
            if os.path.exists(new_path) and new_path != file_item.original_path:
                errors.append(f"Target file already exists: {new_full_name}")
        
        return errors
    
    def execute_rename(self) -> Tuple[List[Tuple[str, str]], List[str]]:
        """
        Execute the rename operation for all files.
        
        Returns:
            Tuple of (successful_renames, errors)
        """
        successful_renames = []
        errors = []
        
        # Validate changes first
        validation_errors = self.validate_changes()
        if validation_errors:
            return successful_renames, validation_errors
        
        total_files = len([f for f in self.files if f.new_name])
        current_file = 0
        
        for file_item in self.files:
            if not file_item.new_name:
                continue
            
            current_file += 1
            
            # Update progress
            if self.progress_callback:
                self.progress_callback(current_file, total_files)
            
            old_path = file_item.original_path
            new_path = file_item.new_path
            
            success, error_msg = safe_rename(old_path, new_path)
            
            if success:
                successful_renames.append((old_path, new_path))
                # Update the file item with new path
                file_item.original_path = new_path
                file_item.original_name = file_item.new_name
                file_item.new_name = ""
            else:
                errors.append(f"Failed to rename {os.path.basename(old_path)}: {error_msg}")
        
        return successful_renames, errors
    
    def reset_changes(self) -> None:
        """Reset all pending changes."""
        for file_item in self.files:
            file_item.new_name = ""
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about loaded files.
        
        Returns:
            Dictionary with file statistics
        """
        stats = {
            "total_files": len(self.files),
            "files_with_changes": len([f for f in self.files if f.new_name]),
            "unique_extensions": len(set(f.extension for f in self.files)),
            "directories": len(set(f.directory for f in self.files))
        }
        return stats
    
    def filter_files_by_extension(self, extensions: List[str]) -> None:
        """
        Filter loaded files by extensions.
        
        Args:
            extensions: List of extensions to keep
        """
        extensions_lower = [ext.lower() for ext in extensions]
        self.files = [
            f for f in self.files 
            if f.extension.lower() in extensions_lower
        ]
    
    def sort_files(self, key: str = "name", reverse: bool = False) -> None:
        """
        Sort files by specified criteria.
        
        Args:
            key: Sort key ('name', 'path', 'extension', 'size', 'date')
            reverse: Sort in reverse order
        """
        if key == "name":
            self.files.sort(key=lambda f: f.original_name, reverse=reverse)
        elif key == "path":
            self.files.sort(key=lambda f: f.original_path, reverse=reverse)
        elif key == "extension":
            self.files.sort(key=lambda f: f.extension, reverse=reverse)
        elif key == "size":
            self.files.sort(
                key=lambda f: os.path.getsize(f.original_path) if os.path.exists(f.original_path) else 0,
                reverse=reverse
            )
        elif key == "date":
            self.files.sort(
                key=lambda f: os.path.getmtime(f.original_path) if os.path.exists(f.original_path) else 0,
                reverse=reverse
            )
