"""Operation controls widget for configuring rename operations."""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, Any

from config.constants import (
    LABELS, PADDING, DEFAULT_START_NUMBER, DEFAULT_PADDING, 
    DEFAULT_DATE_FORMAT, DATE_TYPES
)


class OperationControls(ttk.LabelFrame):
    """Widget for configuring rename operations."""
    
    def __init__(self, parent):
        super().__init__(parent, text=LABELS["renaming_operations"])
        
        self.callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
        # Variables for operation settings
        self.prefix_var = tk.StringVar()
        self.suffix_var = tk.StringVar()
        self.add_numbers_var = tk.BooleanVar()
        self.start_number_var = tk.StringVar(value=str(DEFAULT_START_NUMBER))
        self.padding_var = tk.StringVar(value=str(DEFAULT_PADDING))
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.case_sensitive_var = tk.BooleanVar(value=True)
        self.add_date_var = tk.BooleanVar()
        self.date_type_var = tk.StringVar(value=DATE_TYPES[0])
        self.date_format_var = tk.StringVar(value=DEFAULT_DATE_FORMAT)
        
        self._create_widgets()
        self._setup_layout()
        self._bind_events()
    
    def _create_widgets(self) -> None:
        """Create all operation control widgets."""
        # Prefix/Suffix frame
        self.prefix_suffix_frame = ttk.Frame(self)
        
        ttk.Label(self.prefix_suffix_frame, text=LABELS["prefix"]).pack(side=tk.LEFT, padx=(0, 5))
        self.prefix_entry = ttk.Entry(self.prefix_suffix_frame, textvariable=self.prefix_var, width=15)
        self.prefix_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(self.prefix_suffix_frame, text=LABELS["suffix"]).pack(side=tk.LEFT, padx=(0, 5))
        self.suffix_entry = ttk.Entry(self.prefix_suffix_frame, textvariable=self.suffix_var, width=15)
        self.suffix_entry.pack(side=tk.LEFT)
        
        # Numbering frame
        self.numbering_frame = ttk.Frame(self)
        
        self.add_numbers_check = ttk.Checkbutton(
            self.numbering_frame,
            text=LABELS["add_numbers"],
            variable=self.add_numbers_var,
            command=self._on_numbering_toggled
        )
        self.add_numbers_check.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(self.numbering_frame, text=LABELS["start_at"]).pack(side=tk.LEFT, padx=(0, 5))
        self.start_number_entry = ttk.Entry(
            self.numbering_frame,
            textvariable=self.start_number_var,
            width=8,
            state=tk.DISABLED
        )
        self.start_number_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(self.numbering_frame, text=LABELS["padding"]).pack(side=tk.LEFT, padx=(0, 5))
        self.padding_entry = ttk.Entry(
            self.numbering_frame,
            textvariable=self.padding_var,
            width=5,
            state=tk.DISABLED
        )
        self.padding_entry.pack(side=tk.LEFT)
        
        # Text replacement frame
        self.replace_frame = ttk.Frame(self)
        
        ttk.Label(self.replace_frame, text=LABELS["find"]).pack(side=tk.LEFT, padx=(0, 5))
        self.find_entry = ttk.Entry(self.replace_frame, textvariable=self.find_var, width=20)
        self.find_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(self.replace_frame, text=LABELS["replace"]).pack(side=tk.LEFT, padx=(0, 5))
        self.replace_entry = ttk.Entry(self.replace_frame, textvariable=self.replace_var, width=20)
        self.replace_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.case_sensitive_check = ttk.Checkbutton(
            self.replace_frame,
            text=LABELS["case_sensitive"],
            variable=self.case_sensitive_var
        )
        self.case_sensitive_check.pack(side=tk.LEFT)
        
        # Date/Time frame
        self.date_frame = ttk.Frame(self)
        
        self.add_date_check = ttk.Checkbutton(
            self.date_frame,
            text=LABELS["add_date"],
            variable=self.add_date_var,
            command=self._on_date_toggled
        )
        self.add_date_check.pack(side=tk.LEFT, padx=(0, 10))
        
        self.date_type_combo = ttk.Combobox(
            self.date_frame,
            textvariable=self.date_type_var,
            values=DATE_TYPES,
            width=12,
            state=tk.DISABLED
        )
        self.date_type_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(self.date_frame, text=LABELS["format"]).pack(side=tk.LEFT, padx=(0, 5))
        self.date_format_entry = ttk.Entry(
            self.date_frame,
            textvariable=self.date_format_var,
            width=15,
            state=tk.DISABLED
        )
        self.date_format_entry.pack(side=tk.LEFT)
    
    def _setup_layout(self) -> None:
        """Set up the widget layout."""
        self.prefix_suffix_frame.pack(fill=tk.X, padx=PADDING, pady=PADDING)
        self.numbering_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))
        self.replace_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))
        self.date_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))
    
    def _bind_events(self) -> None:
        """Bind events to trigger callbacks."""
        # Bind all variables to trigger callback
        self.prefix_var.trace_add("write", self._on_change)
        self.suffix_var.trace_add("write", self._on_change)
        self.add_numbers_var.trace_add("write", self._on_change)
        self.start_number_var.trace_add("write", self._on_change)
        self.padding_var.trace_add("write", self._on_change)
        self.find_var.trace_add("write", self._on_change)
        self.replace_var.trace_add("write", self._on_change)
        self.case_sensitive_var.trace_add("write", self._on_change)
        self.add_date_var.trace_add("write", self._on_change)
        self.date_type_var.trace_add("write", self._on_change)
        self.date_format_var.trace_add("write", self._on_change)
    
    def _on_numbering_toggled(self) -> None:
        """Handle numbering checkbox toggle."""
        enabled = self.add_numbers_var.get()
        state = tk.NORMAL if enabled else tk.DISABLED
        
        self.start_number_entry.config(state=state)
        self.padding_entry.config(state=state)
        
        self._on_change()
    
    def _on_date_toggled(self) -> None:
        """Handle date checkbox toggle."""
        enabled = self.add_date_var.get()
        state = tk.NORMAL if enabled else tk.DISABLED
        
        self.date_type_combo.config(state=state)
        self.date_format_entry.config(state=state)
        
        self._on_change()
    
    def _on_change(self, *args) -> None:
        """Handle any change in operation settings."""
        if self.callback:
            self.callback(self.get_operation_data())
    
    def get_operation_data(self) -> Dict[str, Any]:
        """Get current operation configuration as dictionary."""
        try:
            start_number = int(self.start_number_var.get()) if self.start_number_var.get() else DEFAULT_START_NUMBER
        except ValueError:
            start_number = DEFAULT_START_NUMBER
        
        try:
            padding = int(self.padding_var.get()) if self.padding_var.get() else DEFAULT_PADDING
        except ValueError:
            padding = DEFAULT_PADDING
        
        return {
            'prefix': self.prefix_var.get(),
            'suffix': self.suffix_var.get(),
            'add_numbers': self.add_numbers_var.get(),
            'start_number': start_number,
            'padding': padding,
            'find_text': self.find_var.get(),
            'replace_text': self.replace_var.get(),
            'case_sensitive': self.case_sensitive_var.get(),
            'add_date': self.add_date_var.get(),
            'date_type': self.date_type_var.get(),
            'date_format': self.date_format_var.get(),
            'use_pattern': False  # This will be overridden by pattern builder if active
        }
    
    def set_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set callback function for operation changes."""
        self.callback = callback
    
    def reset(self) -> None:
        """Reset all operation settings to defaults."""
        self.prefix_var.set("")
        self.suffix_var.set("")
        self.add_numbers_var.set(False)
        self.start_number_var.set(str(DEFAULT_START_NUMBER))
        self.padding_var.set(str(DEFAULT_PADDING))
        self.find_var.set("")
        self.replace_var.set("")
        self.case_sensitive_var.set(True)
        self.add_date_var.set(False)
        self.date_type_var.set(DATE_TYPES[0])
        self.date_format_var.set(DEFAULT_DATE_FORMAT)
        
        # Update widget states
        self._on_numbering_toggled()
        self._on_date_toggled()
    
    def set_operation_data(self, data: Dict[str, Any]) -> None:
        """Set operation configuration from dictionary."""
        self.prefix_var.set(data.get('prefix', ''))
        self.suffix_var.set(data.get('suffix', ''))
        self.add_numbers_var.set(data.get('add_numbers', False))
        self.start_number_var.set(str(data.get('start_number', DEFAULT_START_NUMBER)))
        self.padding_var.set(str(data.get('padding', DEFAULT_PADDING)))
        self.find_var.set(data.get('find_text', ''))
        self.replace_var.set(data.get('replace_text', ''))
        self.case_sensitive_var.set(data.get('case_sensitive', True))
        self.add_date_var.set(data.get('add_date', False))
        self.date_type_var.set(data.get('date_type', DATE_TYPES[0]))
        self.date_format_var.set(data.get('date_format', DEFAULT_DATE_FORMAT))
        
        # Update widget states
        self._on_numbering_toggled()
        self._on_date_toggled()
    
    def validate_inputs(self) -> tuple[bool, list[str]]:
        """Validate current input values."""
        errors = []
        
        # Validate start number
        if self.add_numbers_var.get():
            try:
                start_num = int(self.start_number_var.get())
                if start_num < 0:
                    errors.append("Start number must be non-negative")
            except ValueError:
                errors.append("Start number must be a valid integer")
            
            try:
                padding = int(self.padding_var.get())
                if padding < 1 or padding > 10:
                    errors.append("Padding must be between 1 and 10")
            except ValueError:
                errors.append("Padding must be a valid integer")
        
        # Validate date format
        if self.add_date_var.get():
            try:
                import datetime
                test_date = datetime.datetime.now()
                test_date.strftime(self.date_format_var.get())
            except (ValueError, TypeError):
                errors.append("Invalid date format")
        
        return len(errors) == 0, errors
    
    def enable_all(self) -> None:
        """Enable all controls."""
        for widget in self.winfo_children():
            self._enable_widget_recursive(widget)
    
    def disable_all(self) -> None:
        """Disable all controls."""
        for widget in self.winfo_children():
            self._disable_widget_recursive(widget)
    
    def _enable_widget_recursive(self, widget) -> None:
        """Recursively enable a widget and its children."""
        try:
            widget.config(state=tk.NORMAL)
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self._enable_widget_recursive(child)
    
    def _disable_widget_recursive(self, widget) -> None:
        """Recursively disable a widget and its children."""
        try:
            widget.config(state=tk.DISABLED)
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self._disable_widget_recursive(child)
