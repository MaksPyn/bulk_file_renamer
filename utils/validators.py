"""Input validation utilities for Bulk File Renamer."""

import re
from typing import Tuple, Optional


def validate_number_input(value: str, min_value: int = 0, max_value: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate numeric input.
    
    Args:
        value: String value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value (None for no limit)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value.strip():
        return False, "Value cannot be empty"
    
    try:
        num = int(value)
        if num < min_value:
            return False, f"Value must be at least {min_value}"
        if max_value is not None and num > max_value:
            return False, f"Value must be at most {max_value}"
        return True, None
    except ValueError:
        return False, "Value must be a valid number"


def validate_padding_input(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate padding input for sequential numbering.
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    return validate_number_input(value, min_value=1, max_value=10)


def validate_start_number_input(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate start number input for sequential numbering.
    
    Args:
        value: String value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    return validate_number_input(value, min_value=0, max_value=999999)


def validate_filename_pattern(pattern: str) -> Tuple[bool, Optional[str]]:
    """
    Validate filename pattern for invalid characters.
    
    Args:
        pattern: Pattern string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pattern:
        return False, "Pattern cannot be empty"
    
    # Check for invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        if char in pattern:
            return False, f"Pattern contains invalid character: '{char}'"
    
    # Check for control characters
    if any(ord(char) < 32 for char in pattern):
        return False, "Pattern contains invalid control characters"
    
    return True, None


def validate_regex_pattern(pattern: str) -> Tuple[bool, Optional[str]]:
    """
    Validate regular expression pattern.
    
    Args:
        pattern: Regex pattern to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pattern:
        return True, None  # Empty pattern is valid (no replacement)
    
    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, f"Invalid regex pattern: {str(e)}"


def validate_date_format(date_format: str) -> Tuple[bool, Optional[str]]:
    """
    Validate date format string.
    
    Args:
        date_format: Date format string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_format:
        return False, "Date format cannot be empty"
    
    try:
        import datetime
        # Test with current datetime
        test_date = datetime.datetime.now()
        test_date.strftime(date_format)
        return True, None
    except (ValueError, TypeError) as e:
        return False, f"Invalid date format: {str(e)}"


def validate_file_extension(extension: str) -> Tuple[bool, Optional[str]]:
    """
    Validate file extension format.
    
    Args:
        extension: File extension to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not extension:
        return False, "Extension cannot be empty"
    
    # Remove leading dot if present
    if extension.startswith('.'):
        extension = extension[1:]
    
    if not extension:
        return False, "Extension cannot be just a dot"
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?* '
    for char in invalid_chars:
        if char in extension:
            return False, f"Extension contains invalid character: '{char}'"
    
    return True, None


def validate_file_extensions_list(extensions_string: str) -> Tuple[bool, Optional[str]]:
    """
    Validate comma-separated list of file extensions.
    
    Args:
        extensions_string: Comma-separated extensions string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not extensions_string.strip():
        return False, "File extensions list cannot be empty"
    
    extensions = [ext.strip() for ext in extensions_string.split(',')]
    
    for ext in extensions:
        is_valid, error_msg = validate_file_extension(ext)
        if not is_valid:
            return False, f"Invalid extension '{ext}': {error_msg}"
    
    return True, None


def validate_directory_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate directory path.
    
    Args:
        path: Directory path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path.strip():
        return False, "Directory path cannot be empty"
    
    import os
    
    if not os.path.exists(path):
        return False, "Directory does not exist"
    
    if not os.path.isdir(path):
        return False, "Path is not a directory"
    
    try:
        # Test if we can read the directory
        os.listdir(path)
        return True, None
    except PermissionError:
        return False, "Permission denied to access directory"
    except Exception as e:
        return False, f"Error accessing directory: {str(e)}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing or replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"
    
    # Replace invalid characters with underscore
    invalid_chars = '<>:"/\\|?*'
    sanitized = filename
    
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove control characters
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"
    
    # Check for reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = sanitized.split('.')[0].upper()
    if name_without_ext in reserved_names:
        sanitized = f"file_{sanitized}"
    
    return sanitized


def validate_pattern_placeholder(placeholder: str) -> Tuple[bool, Optional[str]]:
    """
    Validate pattern placeholder format.
    
    Args:
        placeholder: Placeholder string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not placeholder:
        return False, "Placeholder cannot be empty"
    
    # Check if it's a valid placeholder format
    valid_placeholders = ['{prefix}', '{name}', '{suffix}', '{num}', '{date}']
    
    if placeholder.startswith('{') and placeholder.endswith('}'):
        if placeholder in valid_placeholders:
            return True, None
        else:
            return False, f"Unknown placeholder: {placeholder}"
    
    # If it's not a placeholder, validate as regular text
    return validate_filename_pattern(placeholder)
