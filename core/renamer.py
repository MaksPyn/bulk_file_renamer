"""Main renaming engine that coordinates all operations."""

import logging
from typing import List, Dict, Any, Optional, Tuple, Callable

from core.file_manager import FileManager, FileItem
from core.pattern_builder import PatternBuilder
from utils.date_utils import get_date_by_type
from utils.validators import (
    validate_start_number_input,
    validate_padding_input,
    validate_date_format
)


class RenameOperation:
    """Represents a single rename operation configuration."""
    
    def __init__(self):
        self.prefix: str = ""
        self.suffix: str = ""
        self.add_numbers: bool = False
        self.start_number: int = 1
        self.padding: int = 3
        self.find_text: str = ""
        self.replace_text: str = ""
        self.case_sensitive: bool = True
        self.add_date: bool = False
        self.date_type: str = "creation"
        self.date_format: str = "%Y-%m-%d"
        self.use_pattern: bool = False
        self.pattern_builder: PatternBuilder = PatternBuilder()
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the operation configuration.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate start number
        if self.add_numbers:
            is_valid, error_msg = validate_start_number_input(str(self.start_number))
            if not is_valid:
                errors.append(f"Start number: {error_msg}")
            
            is_valid, error_msg = validate_padding_input(str(self.padding))
            if not is_valid:
                errors.append(f"Padding: {error_msg}")
        
        # Validate date format
        if self.add_date:
            is_valid, error_msg = validate_date_format(self.date_format)
            if not is_valid:
                errors.append(f"Date format: {error_msg}")
        
        # Validate pattern if using pattern builder
        if self.use_pattern:
            is_valid, error_msg = self.pattern_builder.validate_pattern()
            if not is_valid:
                errors.append(f"Pattern: {error_msg}")
        
        return len(errors) == 0, errors


class BulkRenamer:
    """Main renaming engine that coordinates all operations."""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.operation = RenameOperation()
        self.undo_stack: List[List[Tuple[str, str]]] = []
        self.progress_callback: Optional[Callable[[int, int], None]] = None
    
    def set_directory(self, directory: str) -> bool:
        """
        Set the working directory.
        
        Args:
            directory: Path to the directory
            
        Returns:
            True if directory is valid and set
        """
        return self.file_manager.set_directory(directory)
    
    def set_file_types(self, file_types: str) -> None:
        """
        Set file types to filter by.
        
        Args:
            file_types: Comma-separated file extensions
        """
        self.file_manager.set_file_types(file_types)
    
    def set_recursive(self, recursive: bool) -> None:
        """
        Set whether to search subdirectories.
        
        Args:
            recursive: True to include subdirectories
        """
        self.file_manager.set_recursive(recursive)
    
    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback for progress updates.
        
        Args:
            callback: Function that takes (current, total) parameters
        """
        self.progress_callback = callback
        self.file_manager.set_progress_callback(callback)
    
    def load_files(self) -> bool:
        """
        Load files from the current directory.
        
        Returns:
            True if files loaded successfully
        """
        return self.file_manager.load_files()
    
    def get_file_count(self) -> int:
        """Get number of loaded files."""
        return self.file_manager.get_file_count()
    
    def get_files(self) -> List[FileItem]:
        """Get list of all files."""
        return self.file_manager.get_files()
    
    def configure_operation(
        self,
        prefix: str = "",
        suffix: str = "",
        add_numbers: bool = False,
        start_number: int = 1,
        padding: int = 3,
        find_text: str = "",
        replace_text: str = "",
        case_sensitive: bool = True,
        add_date: bool = False,
        date_type: str = "creation",
        date_format: str = "%Y-%m-%d",
        use_pattern: bool = False,
        pattern_elements: Optional[List[str]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Configure the rename operation.
        
        Args:
            prefix: Prefix to add
            suffix: Suffix to add
            add_numbers: Whether to add sequential numbers
            start_number: Starting number for sequence
            padding: Number of digits for padding
            find_text: Text to find and replace
            replace_text: Replacement text
            case_sensitive: Whether find/replace is case sensitive
            add_date: Whether to add date information
            date_type: Type of date to add
            date_format: Format for date string
            use_pattern: Whether to use pattern builder
            pattern_elements: List of pattern elements if using pattern
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        self.operation.prefix = prefix
        self.operation.suffix = suffix
        self.operation.add_numbers = add_numbers
        self.operation.start_number = start_number
        self.operation.padding = padding
        self.operation.find_text = find_text
        self.operation.replace_text = replace_text
        self.operation.case_sensitive = case_sensitive
        self.operation.add_date = add_date
        self.operation.date_type = date_type
        self.operation.date_format = date_format
        self.operation.use_pattern = use_pattern
        
        if use_pattern and pattern_elements:
            self.operation.pattern_builder.set_pattern_from_list(pattern_elements)
        
        return self.operation.validate()
    
    def preview_changes(self) -> List[Tuple[str, str]]:
        """
        Generate preview of all changes.
        
        Returns:
            List of (original_name, new_name) tuples
        """
        # Reset any previous changes
        self.file_manager.reset_changes()
        
        # Apply the configured operation
        self._apply_operation()
        
        # Get preview
        return self.file_manager.preview_changes()
    
    def _apply_operation(self) -> None:
        """Apply the configured operation to all files."""
        if self.operation.use_pattern:
            self._apply_pattern_operation()
        else:
            self._apply_standard_operations()
    
    def _apply_standard_operations(self) -> None:
        """Apply standard operations in sequence."""
        # Apply find and replace first
        if self.operation.find_text:
            self.file_manager.apply_text_replacement(
                self.operation.find_text,
                self.operation.replace_text,
                self.operation.case_sensitive
            )
        
        # Apply prefix and suffix
        if self.operation.prefix or self.operation.suffix:
            self.file_manager.apply_prefix_suffix(
                self.operation.prefix,
                self.operation.suffix
            )
        
        # Apply sequential numbering
        if self.operation.add_numbers:
            self.file_manager.apply_sequential_numbering(
                self.operation.start_number,
                self.operation.padding
            )
        
        # Apply date addition
        if self.operation.add_date:
            self.file_manager.apply_date_addition(
                self.operation.date_type,
                self.operation.date_format
            )
    
    def _apply_pattern_operation(self) -> None:
        """Apply pattern-based operation."""
        def pattern_generator(file_item: FileItem, index: int) -> str:
            # Prepare values for pattern
            values = {
                'prefix': self.operation.prefix,
                'suffix': self.operation.suffix,
                'num': '',
                'date': ''
            }
            
            # Add sequential number if enabled
            if self.operation.add_numbers:
                number = self.operation.start_number + index
                values['num'] = str(number).zfill(self.operation.padding)
            
            # Add date if enabled
            if self.operation.add_date:
                date_str = get_date_by_type(
                    file_item.original_path,
                    self.operation.date_type,
                    self.operation.date_format
                )
                values['date'] = date_str or ''
            
            # Apply find and replace to original name if specified
            original_name = file_item.original_name
            if self.operation.find_text:
                if self.operation.case_sensitive:
                    original_name = original_name.replace(
                        self.operation.find_text,
                        self.operation.replace_text
                    )
                else:
                    import re
                    original_name = re.sub(
                        re.escape(self.operation.find_text),
                        self.operation.replace_text,
                        original_name,
                        flags=re.IGNORECASE
                    )
            
            # Generate filename using pattern
            return self.operation.pattern_builder.generate_filename(
                original_name,
                values,
                ""  # Extension will be added by FileItem
            )
        
        self.file_manager.apply_pattern(pattern_generator)
    
    def validate_changes(self) -> List[str]:
        """
        Validate all pending changes.
        
        Returns:
            List of error messages
        """
        return self.file_manager.validate_changes()
    
    def execute_rename(self) -> Tuple[bool, List[str], int]:
        """
        Execute the rename operation.
        
        Returns:
            Tuple of (success, error_messages, files_renamed_count)
        """
        # First generate the preview to apply changes
        self.preview_changes()
        
        # Validate changes
        validation_errors = self.validate_changes()
        if validation_errors:
            return False, validation_errors, 0
        
        # Execute the rename
        successful_renames, errors = self.file_manager.execute_rename()
        
        # Add to undo stack if any files were renamed
        if successful_renames:
            self.undo_stack.append(successful_renames)
            # Limit undo stack size
            if len(self.undo_stack) > 10:
                self.undo_stack.pop(0)
        
        success = len(errors) == 0
        files_renamed = len(successful_renames)
        
        if success:
            logging.info(f"Successfully renamed {files_renamed} files")
        else:
            logging.error(f"Rename operation completed with {len(errors)} errors")
        
        return success, errors, files_renamed
    
    def can_undo(self) -> bool:
        """Check if undo operation is available."""
        return len(self.undo_stack) > 0
    
    def undo_last_rename(self) -> Tuple[bool, Optional[str]]:
        """
        Undo the last rename operation.
        
        Returns:
            Tuple of (success, error_message)
        """
        if not self.undo_stack:
            return False, "No operations to undo"
        
        last_operation = self.undo_stack.pop()
        errors = []
        
        # Reverse the renames
        for new_path, old_path in reversed(last_operation):
            try:
                import os
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)
                    logging.info(f"Undone: '{new_path}' back to '{old_path}'")
                else:
                    errors.append(f"File not found: {new_path}")
            except Exception as e:
                error_msg = f"Could not undo rename for {new_path}: {e}"
                errors.append(error_msg)
                logging.error(error_msg)
        
        if errors:
            return False, "; ".join(errors)
        
        # Reload files to reflect changes
        self.load_files()
        return True, None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the current state.
        
        Returns:
            Dictionary with statistics
        """
        file_stats = self.file_manager.get_statistics()
        
        stats = {
            **file_stats,
            "undo_operations_available": len(self.undo_stack),
            "operation_configured": self._is_operation_configured()
        }
        
        return stats
    
    def _is_operation_configured(self) -> bool:
        """Check if any operation is configured."""
        return (
            bool(self.operation.prefix) or
            bool(self.operation.suffix) or
            self.operation.add_numbers or
            bool(self.operation.find_text) or
            self.operation.add_date or
            self.operation.use_pattern
        )
    
    def reset_operation(self) -> None:
        """Reset the current operation configuration."""
        self.operation = RenameOperation()
        self.file_manager.reset_changes()
    
    def clear_undo_stack(self) -> None:
        """Clear the undo stack."""
        self.undo_stack.clear()
    
    def sort_files(self, key: str = "name", reverse: bool = False) -> None:
        """
        Sort files by specified criteria.
        
        Args:
            key: Sort key ('name', 'path', 'extension', 'size', 'date')
            reverse: Sort in reverse order
        """
        self.file_manager.sort_files(key, reverse)
