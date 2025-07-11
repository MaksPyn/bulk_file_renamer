"""Main window for the Bulk File Renamer application."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from config.constants import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, PADDING,
    LABELS, ERROR_MESSAGES, SUCCESS_MESSAGES, CONFIRMATION_MESSAGES,
    DEFAULT_FILE_TYPES, DEFAULT_START_NUMBER, DEFAULT_PADDING, DEFAULT_DATE_FORMAT
)
from core.renamer import BulkRenamer
from ui.widgets.directory_selector import DirectorySelector
from ui.widgets.file_list import FileListWidget
from ui.widgets.operation_controls import OperationControls
from ui.widgets.pattern_builder_widget import PatternBuilderWidget


class MainWindow:
    """Main application window."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.renamer = BulkRenamer()
        
        # UI Components
        self.directory_selector: Optional[DirectorySelector] = None
        self.file_list: Optional[FileListWidget] = None
        self.operation_controls: Optional[OperationControls] = None
        self.pattern_builder: Optional[PatternBuilderWidget] = None
        self.progress_bar: Optional[ttk.Progressbar] = None
        self.undo_button: Optional[ttk.Button] = None
        
        self._setup_window()
        self._create_widgets()
        self._setup_callbacks()
    
    def _setup_window(self) -> None:
        """Configure the main window."""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(800, 600)
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=PADDING)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)  # File list expands
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Directory selection
        self.directory_selector = DirectorySelector(main_frame)
        self.directory_selector.grid(row=0, column=0, sticky="ew", pady=(0, PADDING))
        
        # File filtering controls
        self._create_filter_controls(main_frame)
        
        # File list
        self.file_list = FileListWidget(main_frame)
        self.file_list.grid(row=2, column=0, sticky="nsew", pady=(0, PADDING))
        
        # Operation controls
        self.operation_controls = OperationControls(main_frame)
        self.operation_controls.grid(row=3, column=0, sticky="ew", pady=(0, PADDING))
        
        # Pattern builder
        self.pattern_builder = PatternBuilderWidget(main_frame)
        self.pattern_builder.grid(row=4, column=0, sticky="ew", pady=(0, PADDING))
        
        # Action buttons
        self._create_action_buttons(main_frame)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(main_frame, mode="determinate")
        self.progress_bar.grid(row=6, column=0, sticky="ew", pady=(0, PADDING))
        
        # Status and undo
        self._create_status_controls(main_frame)
    
    def _create_filter_controls(self, parent: ttk.Widget) -> None:
        """Create file filtering controls."""
        filter_frame = ttk.LabelFrame(parent, text=LABELS["filtering"])
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, PADDING))
        filter_frame.grid_columnconfigure(1, weight=1)
        
        # Recursive checkbox
        self.recursive_var = tk.BooleanVar()
        recursive_check = ttk.Checkbutton(
            filter_frame,
            text=LABELS["include_subdirs"],
            variable=self.recursive_var,
            command=self._on_filter_changed
        )
        recursive_check.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="w")
        
        # File types entry
        self.file_types_var = tk.StringVar(value=DEFAULT_FILE_TYPES)
        file_types_entry = ttk.Entry(filter_frame, textvariable=self.file_types_var)
        file_types_entry.grid(row=0, column=1, padx=PADDING, pady=PADDING, sticky="ew")
        file_types_entry.bind("<Return>", lambda e: self._on_filter_changed())
        file_types_entry.bind("<FocusOut>", lambda e: self._on_filter_changed())
        
        # Refresh button
        refresh_button = ttk.Button(
            filter_frame,
            text="Refresh",
            command=self._on_filter_changed
        )
        refresh_button.grid(row=0, column=2, padx=PADDING, pady=PADDING)
    
    def _create_action_buttons(self, parent: ttk.Widget) -> None:
        """Create action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, pady=(0, PADDING))
        
        # Preview button
        preview_button = ttk.Button(
            button_frame,
            text=LABELS["preview_changes"],
            command=self._on_preview_changes
        )
        preview_button.pack(side=tk.LEFT, padx=(0, PADDING))
        
        # Rename button
        rename_button = ttk.Button(
            button_frame,
            text=LABELS["rename_files"],
            command=self._on_rename_files
        )
        rename_button.pack(side=tk.LEFT, padx=(0, PADDING))
        
        # Reset button
        reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self._on_reset_operation
        )
        reset_button.pack(side=tk.LEFT)
    
    def _create_status_controls(self, parent: ttk.Widget) -> None:
        """Create status and undo controls."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=7, column=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky="w")
        
        # Undo button
        self.undo_button = ttk.Button(
            status_frame,
            text=LABELS["undo_last_rename"],
            command=self._on_undo_rename,
            state=tk.DISABLED
        )
        self.undo_button.grid(row=0, column=1, sticky="e")
    
    def _setup_callbacks(self) -> None:
        """Set up callbacks between components."""
        # Directory selector callback
        if self.directory_selector:
            self.directory_selector.set_callback(self._on_directory_selected)
        
        # Operation controls callback
        if self.operation_controls:
            self.operation_controls.set_callback(self._on_operation_changed)
        
        # Pattern builder callback
        if self.pattern_builder:
            self.pattern_builder.set_callback(self._on_pattern_changed)
        
        # Set up progress callback
        self.renamer.set_progress_callback(self._on_progress_update)
    
    def _on_directory_selected(self, directory: str) -> None:
        """Handle directory selection."""
        if self.renamer.set_directory(directory):
            self._load_files()
        else:
            messagebox.showerror("Error", ERROR_MESSAGES["no_directory"])
    
    def _on_filter_changed(self) -> None:
        """Handle filter changes."""
        self.renamer.set_file_types(self.file_types_var.get())
        self.renamer.set_recursive(self.recursive_var.get())
        self._load_files()
    
    def _on_operation_changed(self, operation_data: dict) -> None:
        """Handle operation configuration changes."""
        # Configure the renamer with new operation data
        is_valid, errors = self.renamer.configure_operation(**operation_data)
        
        if not is_valid:
            error_msg = "\n".join(errors)
            messagebox.showerror("Configuration Error", error_msg)
        
        # Auto-preview if files are loaded
        if self.renamer.get_file_count() > 0:
            self._preview_changes()
    
    def _on_pattern_changed(self, pattern_elements: list) -> None:
        """Handle pattern builder changes."""
        # Update operation to use pattern
        operation_data = self.operation_controls.get_operation_data() if self.operation_controls else {}
        operation_data.update({
            'use_pattern': True,
            'pattern_elements': pattern_elements
        })
        
        is_valid, errors = self.renamer.configure_operation(**operation_data)
        
        if not is_valid:
            error_msg = "\n".join(errors)
            messagebox.showerror("Pattern Error", error_msg)
        
        # Auto-preview if files are loaded
        if self.renamer.get_file_count() > 0:
            self._preview_changes()
    
    def _on_preview_changes(self) -> None:
        """Handle preview button click."""
        self._preview_changes()
    
    def _on_rename_files(self) -> None:
        """Handle rename button click."""
        if self.renamer.get_file_count() == 0:
            messagebox.showwarning("Warning", ERROR_MESSAGES["no_files"])
            return
        
        # Confirm operation
        if not messagebox.askyesno("Confirm", CONFIRMATION_MESSAGES["confirm_rename"]):
            return
        
        # Execute rename
        success, errors, files_renamed = self.renamer.execute_rename()
        
        if success:
            message = SUCCESS_MESSAGES["files_renamed"].format(count=files_renamed)
            messagebox.showinfo("Success", message)
            self._update_status(f"Renamed {files_renamed} files")
            
            # Update undo button state
            self.undo_button.config(state=tk.NORMAL if self.renamer.can_undo() else tk.DISABLED)
            
            # Reload files
            self._load_files()
        else:
            error_msg = "\n".join(errors)
            messagebox.showerror("Rename Errors", error_msg)
    
    def _on_undo_rename(self) -> None:
        """Handle undo button click."""
        if not messagebox.askyesno("Confirm", CONFIRMATION_MESSAGES["confirm_undo"]):
            return
        
        success, error_msg = self.renamer.undo_last_rename()
        
        if success:
            messagebox.showinfo("Success", SUCCESS_MESSAGES["operation_undone"])
            self._update_status("Undo operation completed")
            
            # Update undo button state
            self.undo_button.config(state=tk.NORMAL if self.renamer.can_undo() else tk.DISABLED)
        else:
            messagebox.showerror("Undo Error", error_msg)
    
    def _on_reset_operation(self) -> None:
        """Handle reset button click."""
        self.renamer.reset_operation()
        
        # Reset UI components
        if self.operation_controls:
            self.operation_controls.reset()
        if self.pattern_builder:
            self.pattern_builder.reset()
        if self.file_list:
            self.file_list.clear_preview()
        
        self._update_status("Operation reset")
    
    def _on_progress_update(self, current: int, total: int) -> None:
        """Handle progress updates."""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar.config(value=progress)
            self._update_status(f"Processing {current}/{total} files...")
        else:
            self.progress_bar.config(value=0)
        
        self.root.update_idletasks()
    
    def _load_files(self) -> None:
        """Load files from current directory."""
        if self.renamer.load_files():
            files = self.renamer.get_files()
            if self.file_list:
                self.file_list.update_files(files)
            
            count = len(files)
            self._update_status(f"Loaded {count} files")
        else:
            if self.file_list:
                self.file_list.clear()
            self._update_status("No files loaded")
    
    def _preview_changes(self) -> None:
        """Generate and display preview of changes."""
        try:
            changes = self.renamer.preview_changes()
            if self.file_list:
                self.file_list.update_preview(changes)
            
            count = len([c for c in changes if c[0] != c[1]])
            self._update_status(f"Preview: {count} files will be renamed")
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error generating preview: {e}")
    
    def _update_status(self, message: str) -> None:
        """Update status message."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run(self) -> None:
        """Start the application."""
        self.root.deiconify()  # Show the window
        self.root.mainloop()
    
    def close(self) -> None:
        """Close the application."""
        self.root.quit()
        self.root.destroy()
