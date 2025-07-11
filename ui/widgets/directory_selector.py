"""Directory selector widget for choosing the working directory."""

import tkinter as tk
from tkinter import filedialog, ttk
from typing import Optional, Callable

from config.constants import LABELS, PADDING


class DirectorySelector(ttk.LabelFrame):
    """Widget for selecting and displaying the current directory."""
    
    def __init__(self, parent):
        super().__init__(parent, text=LABELS["directory_selection"])
        
        self.directory_var = tk.StringVar()
        self.callback: Optional[Callable[[str], None]] = None
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self) -> None:
        """Create the directory selector widgets."""
        # Directory path entry
        self.path_entry = ttk.Entry(
            self,
            textvariable=self.directory_var,
            state="readonly",
            width=80
        )
        
        # Browse button
        self.browse_button = ttk.Button(
            self,
            text=LABELS["browse"],
            command=self._browse_directory
        )
    
    def _setup_layout(self) -> None:
        """Set up the widget layout."""
        self.grid_columnconfigure(0, weight=1)
        
        self.path_entry.grid(
            row=0, column=0,
            sticky="ew",
            padx=PADDING,
            pady=PADDING
        )
        
        self.browse_button.grid(
            row=0, column=1,
            padx=(0, PADDING),
            pady=PADDING
        )
    
    def _browse_directory(self) -> None:
        """Open directory selection dialog."""
        directory = filedialog.askdirectory(
            title="Select Directory",
            initialdir=self.directory_var.get() or "."
        )
        
        if directory:
            self.directory_var.set(directory)
            if self.callback:
                self.callback(directory)
    
    def set_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback function for directory selection."""
        self.callback = callback
    
    def get_directory(self) -> str:
        """Get the currently selected directory."""
        return self.directory_var.get()
    
    def set_directory(self, directory: str) -> None:
        """Set the directory programmatically."""
        self.directory_var.set(directory)
        if self.callback:
            self.callback(directory)
    
    def clear(self) -> None:
        """Clear the selected directory."""
        self.directory_var.set("")
