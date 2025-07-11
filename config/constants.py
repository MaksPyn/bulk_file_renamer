"""Application constants for Bulk File Renamer."""

# Application metadata
APP_NAME = "Bulk File Renamer"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Bulk File Renamer Team"

# UI Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PADDING = 10
BUTTON_PADDING = 5

# File operation constants
DEFAULT_FILE_TYPES = ".jpg, .jpeg, .png, .gif, .bmp, .tiff, .raw"
DEFAULT_START_NUMBER = 1
DEFAULT_PADDING = 3
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
LOG_FILENAME = "rename.log"

# Pattern placeholders
PATTERN_PLACEHOLDERS = {
    "prefix": "{prefix}",
    "name": "{name}",
    "suffix": "{suffix}",
    "number": "{num}",
    "date": "{date}"
}

# Date types
DATE_TYPES = ["creation", "modification", "exif"]

# UI Labels
LABELS = {
    "directory_selection": "Directory Selection",
    "filtering": "Filtering",
    "files_to_rename": "Files to Rename",
    "renaming_operations": "Renaming Operations",
    "pattern_builder": "Pattern Builder",
    "browse": "Browse...",
    "include_subdirs": "Include Subdirectories",
    "prefix": "Prefix:",
    "suffix": "Suffix:",
    "add_numbers": "Add Sequential Numbers",
    "start_at": "Start at:",
    "padding": "Padding:",
    "find": "Find:",
    "replace": "Replace:",
    "case_sensitive": "Case Sensitive",
    "add_date": "Add Date/Time",
    "format": "Format:",
    "preview_changes": "Preview Changes",
    "rename_files": "Rename Files",
    "undo_last_rename": "Undo Last Rename",
    "new_name": "New Name"
}

# Error messages
ERROR_MESSAGES = {
    "no_directory": "Please select a directory first.",
    "no_files": "No files found matching the criteria.",
    "rename_failed": "Could not rename {old_path}:\n{error}",
    "undo_failed": "Could not undo rename for {new_path}:\n{error}",
    "invalid_number": "Please enter a valid number.",
    "invalid_padding": "Padding must be a positive integer.",
    "date_extraction_failed": "Could not get date for {file_path}: {error}"
}

# Success messages
SUCCESS_MESSAGES = {
    "files_renamed": "Successfully renamed {count} files.",
    "operation_undone": "Successfully undone the last rename operation."
}

# Confirmation messages
CONFIRMATION_MESSAGES = {
    "confirm_rename": "Are you sure you want to rename these files?",
    "confirm_undo": "Are you sure you want to undo the last rename operation?"
}
