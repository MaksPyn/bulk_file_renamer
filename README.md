# Bulk File Renamer

A powerful and user-friendly Python GUI application for bulk renaming files with advanced features and a modular, maintainable architecture.

## Features

### Core Functionality
- **Directory Selection**: Browse and select directories to work with
- **File Type Filtering**: Filter files by extension (e.g., `.jpg, .png, .txt`)
- **Recursive Search**: Option to include files from subdirectories
- **Live Preview**: See exactly what files will be renamed before applying changes
- **Undo Functionality**: Reverse the last rename operation
- **Safe Renaming**: Prevents overwriting existing files and validates filenames
- **Comprehensive Logging**: All operations are logged to `rename.log`

### Renaming Operations
- **Prefix/Suffix**: Add text before and/or after filenames
- **Sequential Numbering**: Add numbers with customizable start value and padding
- **Find and Replace**: Replace text in filenames (case-sensitive or insensitive)
- **Date/Time Addition**: Add date information from:
  - File creation date
  - File modification date
  - EXIF data (for images with metadata)
  - Customizable date/time formats
- **Advanced Pattern Builder**: Create complex filename patterns by combining elements:
  - `{prefix}`: User-defined prefix
  - `{name}`: Original filename (without extension)
  - `{suffix}`: User-defined suffix
  - `{num}`: Sequential number
  - `{date}`: Date/time string
  - Custom separators and text

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Pillow (PIL) for EXIF date extraction from images (optional)

## Installation

1. Clone this repository or download the files
2. Install optional dependencies:
   ```bash
   pip install Pillow
   ```
   Note: Pillow is only needed for EXIF date extraction from images.

## Usage

### Quick Start

1. Run the application:
   ```bash
   python main.py
   ```

2. **Select Directory**: Click "Browse" to choose the directory containing files to rename

3. **Configure File Filtering**:
   - Enter file extensions (comma-separated, e.g., "jpg,png,gif")
   - Check "Include subdirectories" to process files in subfolders

4. **Configure Renaming Options**:
   - Use the operation controls for basic renaming
   - Use the pattern builder for advanced filename structures

5. **Preview Changes**: Click "Preview Changes" to see the new filenames

6. **Apply Changes**: Click "Rename Files" to execute the operation

7. **Undo if Needed**: Use "Undo Last Rename" to reverse the operation

### Advanced Usage

#### Pattern Builder
The pattern builder allows you to create sophisticated filename structures:

1. Add elements in your desired order
2. Use the preview to see the result
3. Rearrange elements with the up/down buttons
4. Add custom separators between elements

Example pattern: `{prefix}_{name}_{num}_{date}` might produce:
`IMG_photo_001_2024-01-15.jpg`

#### Date Formats
Customize date formats using Python's strftime codes:
- `%Y-%m-%d` → 2024-01-15
- `%Y%m%d` → 20240115
- `%Y-%m-%d_%H-%M-%S` → 2024-01-15_14-30-25

## Architecture

The application follows a clean, modular architecture:

```
bulk_file_renamer/
├── main.py                          # Application entry point
├── app.py                          # Legacy entry point (deprecated)
├── config/
│   ├── __init__.py
│   └── constants.py                # Application constants and settings
├── core/
│   ├── __init__.py
│   ├── file_manager.py            # File operations and management
│   ├── pattern_builder.py         # Pattern building logic
│   └── renamer.py                 # Main renaming engine
├── ui/
│   ├── __init__.py
│   ├── main_window.py             # Main application window
│   └── widgets/
│       ├── __init__.py
│       ├── directory_selector.py  # Directory selection widget
│       ├── file_list.py           # File list display widget
│       ├── operation_controls.py  # Renaming operation controls
│       └── pattern_builder_widget.py # Pattern builder interface
├── utils/
│   ├── __init__.py
│   ├── file_utils.py              # File system utilities
│   ├── date_utils.py              # Date/time utilities
│   └── validators.py              # Input validation utilities
├── README.md
├── LICENSE
└── .gitignore
```

### Key Components

- **Core Engine** (`core/renamer.py`): Coordinates all renaming operations
- **File Manager** (`core/file_manager.py`): Handles file discovery and operations
- **Pattern Builder** (`core/pattern_builder.py`): Manages filename pattern creation
- **UI Components** (`ui/`): Modular user interface widgets
- **Utilities** (`utils/`): Reusable utility functions for validation, file operations, and date handling

## Examples

### Example 1: Basic Prefix and Numbering
- Original: `photo.jpg`, `image.png`, `document.txt`
- Settings: Prefix="IMG_", Sequential numbering starting at 1
- Result: `IMG_photo_001.jpg`, `IMG_image_002.png`, `IMG_document_003.txt`

### Example 2: Find and Replace
- Original: `vacation_2023_beach.jpg`, `vacation_2023_mountain.jpg`
- Settings: Find="2023", Replace="2024"
- Result: `vacation_2024_beach.jpg`, `vacation_2024_mountain.jpg`

### Example 3: Date-based Renaming
- Original: `photo.jpg` (created on 2024-01-15)
- Settings: Add creation date with format "%Y-%m-%d"
- Result: `photo_2024-01-15.jpg`

### Example 4: Complex Pattern
- Pattern: `{date}_{prefix}_{name}_{num}`
- Settings: Prefix="IMG", Date format="%Y%m%d", Start number=1
- Result: `20240115_IMG_photo_001.jpg`

## Safety Features

- **Preview Mode**: Always shows changes before applying them
- **Input Validation**: Validates all user inputs and settings
- **Filename Validation**: Checks for invalid characters and reserved names
- **Duplicate Prevention**: Prevents creating duplicate filenames
- **Backup Prevention**: Won't overwrite existing files
- **Undo Functionality**: Can reverse the most recent operation
- **Error Handling**: Graceful handling of permission errors and other issues
- **Logging**: Comprehensive logging of all operations and errors

## Troubleshooting

### Common Issues

1. **"No files found"**: 
   - Check directory path is correct
   - Verify file extensions match existing files
   - Ensure you have read permissions

2. **Permission errors**: 
   - Run as administrator if needed
   - Close files that might be open in other applications
   - Check directory write permissions

3. **EXIF date not working**: 
   - Install Pillow: `pip install Pillow`
   - Ensure image files contain EXIF metadata
   - Try using creation/modification date instead

4. **Undo not available**: 
   - Undo only works for the most recent operation
   - Files must not have been moved or deleted since renaming

### Error Messages

- **"Invalid filename"**: Generated name contains invalid characters
- **"File already exists"**: New filename would overwrite existing file
- **"Permission denied"**: Insufficient permissions for the operation
- **"Pattern validation failed"**: Pattern contains invalid elements

## Development

### Running from Source

1. Clone the repository
2. Install dependencies: `pip install Pillow`
3. Run: `python main.py`

### Code Structure

The codebase follows these principles:
- **Separation of Concerns**: UI, business logic, and utilities are separated
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new renaming operations or UI components
- **Testability**: Clean interfaces make unit testing straightforward

### Adding New Features

1. **New Renaming Operation**: Add to `core/file_manager.py` and update UI
2. **New UI Widget**: Create in `ui/widgets/` and integrate with main window
3. **New Utility Function**: Add to appropriate module in `utils/`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 2.0.0 (Current)
- **Major Refactoring**: Complete architectural overhaul
- **Modular Design**: Separated concerns into logical modules
- **Enhanced Pattern Builder**: More flexible filename pattern creation
- **Improved Error Handling**: Better validation and error messages
- **Code Quality**: Better documentation and maintainability
- **New Entry Point**: `main.py` replaces `app.py`

### Version 1.0.0
- Initial release with basic renaming functionality
- GUI interface with tkinter
- Preview and undo capabilities
- Support for prefix/suffix, numbering, find/replace, and date addition
