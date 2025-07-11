"""File list widget for displaying files and preview changes."""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Optional

from config.constants import LABELS, PADDING
from core.file_manager import FileItem


class FileListWidget(ttk.LabelFrame):
    """Widget for displaying the list of files and their preview names."""
    
    def __init__(self, parent):
        super().__init__(parent, text=LABELS["files_to_rename"])
        
        self.files: List[FileItem] = []
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self) -> None:
        """Create the file list widgets."""
        # Create treeview with columns
        self.tree = ttk.Treeview(
            self,
            columns=("original", "new"),
            show="headings",
            height=15
        )
        
        # Configure columns
        self.tree.heading("original", text="Original Name")
        self.tree.heading("new", text="New Name")
        
        self.tree.column("original", width=400, minwidth=200)
        self.tree.column("new", width=400, minwidth=200)
        
        # Create scrollbars
        self.v_scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        
        self.h_scrollbar = ttk.Scrollbar(
            self,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)
        
        # Status label
        self.status_var = tk.StringVar(value="No files loaded")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
    
    def _setup_layout(self) -> None:
        """Set up the widget layout."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Treeview
        self.tree.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(PADDING, 0),
            pady=(PADDING, 0)
        )
        
        # Vertical scrollbar
        self.v_scrollbar.grid(
            row=0, column=1,
            sticky="ns",
            pady=(PADDING, 0)
        )
        
        # Horizontal scrollbar
        self.h_scrollbar.grid(
            row=1, column=0,
            sticky="ew",
            padx=(PADDING, 0)
        )
        
        # Status label
        self.status_label.grid(
            row=2, column=0,
            columnspan=2,
            sticky="w",
            padx=PADDING,
            pady=(PADDING, PADDING)
        )
    
    def update_files(self, files: List[FileItem]) -> None:
        """Update the file list with new files."""
        self.files = files.copy()
        self._refresh_display()
        
        count = len(files)
        self.status_var.set(f"{count} files loaded")
    
    def update_preview(self, changes: List[Tuple[str, str]]) -> None:
        """Update the preview column with new names."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add files with preview
        changed_count = 0
        for original, new in changes:
            # Determine if file will be changed
            will_change = original != new
            if will_change:
                changed_count += 1
            
            # Insert item with appropriate styling
            item_id = self.tree.insert("", "end", values=(original, new))
            
            # Apply styling for changed files
            if will_change:
                self.tree.set(item_id, "new", new)
                # You could add tags here for different styling if needed
        
        # Update status
        total = len(changes)
        self.status_var.set(f"{total} files, {changed_count} will be renamed")
    
    def clear_preview(self) -> None:
        """Clear the preview column, showing only original names."""
        if self.files:
            changes = [(f.original_name + f.extension, f.original_name + f.extension) 
                      for f in self.files]
            self.update_preview(changes)
        else:
            self.clear()
    
    def clear(self) -> None:
        """Clear all files from the list."""
        self.files.clear()
        
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.status_var.set("No files loaded")
    
    def get_selected_files(self) -> List[int]:
        """Get indices of selected files."""
        selected_items = self.tree.selection()
        indices = []
        
        for item in selected_items:
            # Get the index of the item
            index = self.tree.index(item)
            indices.append(index)
        
        return indices
    
    def select_all(self) -> None:
        """Select all files in the list."""
        for item in self.tree.get_children():
            self.tree.selection_add(item)
    
    def select_none(self) -> None:
        """Deselect all files."""
        self.tree.selection_remove(self.tree.selection())
    
    def _refresh_display(self) -> None:
        """Refresh the display with current files."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add files
        for file_item in self.files:
            original_name = file_item.original_name + file_item.extension
            new_name = (file_item.new_name + file_item.extension) if file_item.new_name else original_name
            
            self.tree.insert("", "end", values=(original_name, new_name))
    
    def get_file_count(self) -> int:
        """Get the number of files in the list."""
        return len(self.files)
    
    def scroll_to_top(self) -> None:
        """Scroll to the top of the list."""
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.see(first_item)
    
    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the list."""
        if self.tree.get_children():
            last_item = self.tree.get_children()[-1]
            self.tree.see(last_item)
    
    def export_list(self) -> List[Tuple[str, str]]:
        """Export the current file list as (original, new) tuples."""
        result = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if len(values) >= 2:
                result.append((values[0], values[1]))
        return result
    
    def filter_display(self, filter_func) -> None:
        """Filter the display based on a filter function."""
        # This could be implemented to show/hide certain files
        # based on criteria like extension, name pattern, etc.
        pass
    
    def sort_display(self, column: str, reverse: bool = False) -> None:
        """Sort the display by specified column."""
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children()]
        items.sort(reverse=reverse)
        
        # Rearrange items in sorted order
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)
