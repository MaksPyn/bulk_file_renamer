"""Date and time utility functions for Bulk File Renamer."""

import os
import datetime
import logging
from typing import Optional

try:
    from PIL import Image, ExifTags
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    logging.warning("Pillow not available. EXIF date extraction will be disabled.")


def get_creation_date(file_path: str, date_format: str = "%Y-%m-%d") -> Optional[str]:
    """
    Get file creation date.
    
    Args:
        file_path: Path to the file
        date_format: Format string for the date
        
    Returns:
        Formatted date string or None if failed
    """
    try:
        timestamp = os.path.getctime(file_path)
        date_obj = datetime.datetime.fromtimestamp(timestamp)
        return date_obj.strftime(date_format)
    except Exception as e:
        logging.error(f"Could not get creation date for {file_path}: {e}")
        return None


def get_modification_date(file_path: str, date_format: str = "%Y-%m-%d") -> Optional[str]:
    """
    Get file modification date.
    
    Args:
        file_path: Path to the file
        date_format: Format string for the date
        
    Returns:
        Formatted date string or None if failed
    """
    try:
        timestamp = os.path.getmtime(file_path)
        date_obj = datetime.datetime.fromtimestamp(timestamp)
        return date_obj.strftime(date_format)
    except Exception as e:
        logging.error(f"Could not get modification date for {file_path}: {e}")
        return None


def get_exif_date(file_path: str, date_format: str = "%Y-%m-%d") -> Optional[str]:
    """
    Get date from EXIF data for image files.
    
    Args:
        file_path: Path to the image file
        date_format: Format string for the date
        
    Returns:
        Formatted date string or None if failed
    """
    if not PILLOW_AVAILABLE:
        logging.warning("Pillow not available for EXIF date extraction")
        return None
    
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return None
            
            # Look for DateTimeOriginal first, then DateTime
            date_tags = ['DateTimeOriginal', 'DateTime']
            
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name in date_tags:
                    try:
                        # EXIF date format is usually 'YYYY:MM:DD HH:MM:SS'
                        dt_original = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        return dt_original.strftime(date_format)
                    except ValueError:
                        continue
            
            return None
            
    except Exception as e:
        logging.error(f"Could not get EXIF date for {file_path}: {e}")
        return None


def get_date_by_type(
    file_path: str, 
    date_type: str, 
    date_format: str = "%Y-%m-%d"
) -> Optional[str]:
    """
    Get date based on specified type.
    
    Args:
        file_path: Path to the file
        date_type: Type of date ('creation', 'modification', 'exif')
        date_format: Format string for the date
        
    Returns:
        Formatted date string or None if failed
    """
    date_type = date_type.lower()
    
    if date_type == "creation":
        return get_creation_date(file_path, date_format)
    elif date_type == "modification":
        return get_modification_date(file_path, date_format)
    elif date_type == "exif":
        return get_exif_date(file_path, date_format)
    else:
        logging.error(f"Unknown date type: {date_type}")
        return None


def is_valid_date_format(date_format: str) -> bool:
    """
    Check if date format string is valid.
    
    Args:
        date_format: Format string to validate
        
    Returns:
        True if format is valid, False otherwise
    """
    try:
        # Test with current datetime
        test_date = datetime.datetime.now()
        test_date.strftime(date_format)
        return True
    except (ValueError, TypeError):
        return False


def get_current_timestamp(date_format: str = "%Y-%m-%d_%H-%M-%S") -> str:
    """
    Get current timestamp as formatted string.
    
    Args:
        date_format: Format string for the timestamp
        
    Returns:
        Formatted timestamp string
    """
    return datetime.datetime.now().strftime(date_format)


def parse_date_from_filename(filename: str) -> Optional[datetime.datetime]:
    """
    Try to extract date from filename using common patterns.
    
    Args:
        filename: The filename to parse
        
    Returns:
        datetime object or None if no date found
    """
    import re
    
    # Common date patterns in filenames
    patterns = [
        r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
        r'(\d{4})(\d{2})(\d{2})',    # YYYYMMDD
        r'(\d{2})-(\d{2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{2})(\d{2})(\d{4})',    # DDMMYYYY
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                groups = match.groups()
                if len(groups) == 3:
                    # Determine if it's YYYY-MM-DD or DD-MM-YYYY format
                    if len(groups[0]) == 4:  # YYYY-MM-DD
                        year, month, day = groups
                    else:  # DD-MM-YYYY
                        day, month, year = groups
                    
                    return datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                continue
    
    return None
