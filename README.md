# Bulk File Renamer

A powerful and easy-to-use desktop application for bulk renaming files with a wide variety of options and a user-friendly interface.

## Features

*   **Directory Selection**: Browse and select a directory to load files for renaming.
*   **Recursive Search**: Optionally include files from subdirectories.
*   **File Type Filtering**: Specify which file types to include (e.g., `.jpg, .png, .gif`).
*   **Live Preview**: See the new filenames before applying any changes.
*   **Undo**: Undo the last renaming operation.
*   **Logging**: All renaming operations are logged to `rename.log`.

### Renaming Operations

*   **Prefix/Suffix**: Add a prefix and/or suffix to filenames.
*   **Sequential Numbering**: Add sequential numbers to filenames with customizable starting number and padding.
*   **Text Replacement**: Find and replace text in filenames, with an option for case-sensitive matching.
*   **Date/Time**: Add date and time information to filenames, with options for:
    *   Creation date
    *   Modification date
    *   EXIF data (for images)
    *   Customizable date/time format
*   **Pattern Builder**: Create complex filename patterns by combining different elements in any order:
    *   `{prefix}`: The specified prefix.
    *   `{name}`: The original filename (without extension).
    *   `{suffix}`: The specified suffix.
    *   `{num}`: The sequential number.
    *   `{date}`: The date/time string.
    *   Custom separators.

## How to Use

1.  **Run the application**:
    ```bash
    python app.py
    ```
2.  **Select a directory**: Click the "Browse..." button to choose the directory containing the files you want to rename.
3.  **Filter files**:
    *   Check "Include Subdirectories" to include files from subfolders.
    *   Modify the comma-separated list of file extensions to filter by file type.
4.  **Configure renaming operations**:
    *   Use the various input fields and checkboxes to define how you want to rename the files.
    *   Use the "Pattern Builder" to create a custom filename structure.
5.  **Preview changes**: Click the "Preview Changes" button to see what the new filenames will look like.
6.  **Rename files**: If you're happy with the preview, click the "Rename Files" button to apply the changes.
7.  **Undo (optional)**: If you make a mistake, click the "Undo Last Rename" button to revert the changes.

## Dependencies

*   Python 3.x
*   Tkinter (usually included with Python)
*   Pillow (for EXIF data):
    ```bash
    pip install Pillow
