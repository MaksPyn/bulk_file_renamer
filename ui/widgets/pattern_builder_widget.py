"""Pattern builder widget for creating custom filename patterns."""

import tkinter as tk
from tkinter import ttk, simpledialog
from typing import Optional, Callable, List

from config.constants import LABELS, PADDING, PATTERN_PLACEHOLDERS


class PatternBuilderWidget(ttk.LabelFrame):
    """Widget for building custom filename patterns."""
    
    def __init__(self, parent):
        super().__init__(parent, text=LABELS["pattern_builder"])
        
        self.callback: Optional[Callable[[List[str]], None]] = None
        self.pattern_elements: List[str] = []
        
        self._create_widgets()
        self._setup_layout()
        self._reset_to_default()
    
    def _create_widgets(self) -> None:
        """Create all pattern builder widgets."""
        # Control buttons frame
        self.controls_frame = ttk.Frame(self)
        
        # Add element buttons
        self.add_prefix_btn = ttk.Button(
            self.controls_frame,
            text="Add Prefix",
            command=lambda: self._add_element(PATTERN_PLACEHOLDERS["prefix"])
        )
        
        self.add_name_btn = ttk.Button(
            self.controls_frame,
            text="Add Name",
            command=lambda: self._add_element(PATTERN_PLACEHOLDERS["name"])
        )
        
        self.add_suffix_btn = ttk.Button(
            self.controls_frame,
            text="Add Suffix",
            command=lambda: self._add_element(PATTERN_PLACEHOLDERS["suffix"])
        )
        
        self.add_number_btn = ttk.Button(
            self.controls_frame,
            text="Add Number",
            command=lambda: self._add_element(PATTERN_PLACEHOLDERS["number"])
        )
        
        self.add_date_btn = ttk.Button(
            self.controls_frame,
            text="Add Date",
            command=lambda: self._add_element(PATTERN_PLACEHOLDERS["date"])
        )
        
        self.add_separator_btn = ttk.Button(
            self.controls_frame,
            text="Add Separator",
            command=self._add_separator
        )
        
        # Pattern list
        self.pattern_listbox = tk.Listbox(self, height=6)
        
        # Pattern manipulation buttons
        self.manipulation_frame = ttk.Frame(self)
        
        self.move_up_btn = ttk.Button(
            self.manipulation_frame,
            text="↑ Up",
            command=self._move_up
        )
        
        self.move_down_btn = ttk.Button(
            self.manipulation_frame,
            text="↓ Down",
            command=self._move_down
        )
        
        self.remove_btn = ttk.Button(
            self.manipulation_frame,
            text="Remove",
            command=self._remove_selected
        )
        
        self.clear_btn = ttk.Button(
            self.manipulation_frame,
            text="Clear All",
            command=self._clear_all
        )
        
        # Preview frame
        self.preview_frame = ttk.Frame(self)
        
        ttk.Label(self.preview_frame, text="Preview:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.preview_var = tk.StringVar()
        self.preview_label = ttk.Label(
            self.preview_frame,
            textvariable=self.preview_var,
            relief=tk.SUNKEN,
            background="white",
            foreground="blue"
        )
    
    def _setup_layout(self) -> None:
        """Set up the widget layout."""
        # Controls frame
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=PADDING, pady=PADDING)
        
        # Pack control buttons vertically
        self.add_prefix_btn.pack(fill=tk.X, pady=(0, 2))
        self.add_name_btn.pack(fill=tk.X, pady=(0, 2))
        self.add_suffix_btn.pack(fill=tk.X, pady=(0, 2))
        self.add_number_btn.pack(fill=tk.X, pady=(0, 2))
        self.add_date_btn.pack(fill=tk.X, pady=(0, 2))
        self.add_separator_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Pattern listbox
        self.pattern_listbox.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=(0, PADDING),
            pady=PADDING
        )
        
        # Manipulation frame
        self.manipulation_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING), pady=PADDING)
        
        # Pack manipulation buttons vertically
        self.move_up_btn.pack(fill=tk.X, pady=(0, 2))
        self.move_down_btn.pack(fill=tk.X, pady=(0, 2))
        self.remove_btn.pack(fill=tk.X, pady=(0, 10))
        self.clear_btn.pack(fill=tk.X)
        
        # Preview frame at bottom
        self.preview_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))
        self.preview_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    
    def _reset_to_default(self) -> None:
        """Reset pattern to default configuration."""
        default_pattern = [
            PATTERN_PLACEHOLDERS["prefix"],
            PATTERN_PLACEHOLDERS["name"],
            PATTERN_PLACEHOLDERS["suffix"],
            PATTERN_PLACEHOLDERS["number"],
            PATTERN_PLACEHOLDERS["date"]
        ]
        self.set_pattern(default_pattern)
    
    def _add_element(self, element: str) -> None:
        """Add an element to the pattern."""
        self.pattern_elements.append(element)
        self._update_display()
        self._notify_change()
    
    def _add_separator(self) -> None:
        """Add a custom separator to the pattern."""
        separator = simpledialog.askstring(
            "Add Separator",
            "Enter separator text:",
            parent=self
        )
        
        if separator is not None:  # User didn't cancel
            self.pattern_elements.append(separator)
            self._update_display()
            self._notify_change()
    
    def _remove_selected(self) -> None:
        """Remove selected element from pattern."""
        selection = self.pattern_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.pattern_elements):
                self.pattern_elements.pop(index)
                self._update_display()
                self._notify_change()
    
    def _move_up(self) -> None:
        """Move selected element up in the pattern."""
        selection = self.pattern_listbox.curselection()
        if selection:
            index = selection[0]
            if index > 0:
                # Swap with previous element
                self.pattern_elements[index], self.pattern_elements[index - 1] = \
                    self.pattern_elements[index - 1], self.pattern_elements[index]
                
                self._update_display()
                self.pattern_listbox.selection_set(index - 1)
                self._notify_change()
    
    def _move_down(self) -> None:
        """Move selected element down in the pattern."""
        selection = self.pattern_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.pattern_elements) - 1:
                # Swap with next element
                self.pattern_elements[index], self.pattern_elements[index + 1] = \
                    self.pattern_elements[index + 1], self.pattern_elements[index]
                
                self._update_display()
                self.pattern_listbox.selection_set(index + 1)
                self._notify_change()
    
    def _clear_all(self) -> None:
        """Clear all elements from pattern."""
        self.pattern_elements.clear()
        self._update_display()
        self._notify_change()
    
    def _update_display(self) -> None:
        """Update the listbox display and preview."""
        # Update listbox
        self.pattern_listbox.delete(0, tk.END)
        for element in self.pattern_elements:
            display_text = self._get_display_text(element)
            self.pattern_listbox.insert(tk.END, display_text)
        
        # Update preview
        self._update_preview()
    
    def _get_display_text(self, element: str) -> str:
        """Get display text for an element."""
        if element == PATTERN_PLACEHOLDERS["prefix"]:
            return "Prefix"
        elif element == PATTERN_PLACEHOLDERS["name"]:
            return "Original Name"
        elif element == PATTERN_PLACEHOLDERS["suffix"]:
            return "Suffix"
        elif element == PATTERN_PLACEHOLDERS["number"]:
            return "Sequential Number"
        elif element == PATTERN_PLACEHOLDERS["date"]:
            return "Date/Time"
        else:
            return f"Text: '{element}'"
    
    def _update_preview(self) -> None:
        """Update the preview display."""
        if not self.pattern_elements:
            self.preview_var.set("(empty pattern)")
            return
        
        # Generate sample preview
        sample_values = {
            'prefix': 'IMG',
            'name': 'photo',
            'suffix': 'edited',
            'num': '001',
            'date': '2024-01-15'
        }
        
        preview_parts = []
        for element in self.pattern_elements:
            if element == PATTERN_PLACEHOLDERS["prefix"]:
                preview_parts.append(sample_values['prefix'])
            elif element == PATTERN_PLACEHOLDERS["name"]:
                preview_parts.append(sample_values['name'])
            elif element == PATTERN_PLACEHOLDERS["suffix"]:
                preview_parts.append(sample_values['suffix'])
            elif element == PATTERN_PLACEHOLDERS["number"]:
                preview_parts.append(sample_values['num'])
            elif element == PATTERN_PLACEHOLDERS["date"]:
                preview_parts.append(sample_values['date'])
            else:
                preview_parts.append(element)
        
        preview = "".join(preview_parts) + ".jpg"
        self.preview_var.set(preview)
    
    def _notify_change(self) -> None:
        """Notify callback of pattern change."""
        if self.callback:
            self.callback(self.pattern_elements.copy())
    
    def set_callback(self, callback: Callable[[List[str]], None]) -> None:
        """Set callback function for pattern changes."""
        self.callback = callback
    
    def get_pattern(self) -> List[str]:
        """Get current pattern as list of elements."""
        return self.pattern_elements.copy()
    
    def set_pattern(self, pattern: List[str]) -> None:
        """Set pattern from list of elements."""
        self.pattern_elements = pattern.copy()
        self._update_display()
        self._notify_change()
    
    def reset(self) -> None:
        """Reset pattern to default."""
        self._reset_to_default()
    
    def is_empty(self) -> bool:
        """Check if pattern is empty."""
        return len(self.pattern_elements) == 0
    
    def validate_pattern(self) -> tuple[bool, str]:
        """Validate current pattern."""
        if not self.pattern_elements:
            return False, "Pattern cannot be empty"
        
        # Check if pattern has at least one meaningful element
        has_meaningful = any(
            element in PATTERN_PLACEHOLDERS.values() or element.strip()
            for element in self.pattern_elements
        )
        
        if not has_meaningful:
            return False, "Pattern must contain at least one placeholder or text"
        
        return True, ""
    
    def export_pattern_string(self) -> str:
        """Export pattern as a single string."""
        return "".join(self.pattern_elements)
    
    def import_pattern_string(self, pattern_string: str) -> bool:
        """Import pattern from a string."""
        # This is a simplified import - in a full implementation,
        # you might want to parse placeholders from the string
        if pattern_string:
            # For now, just treat the whole string as a single text element
            self.pattern_elements = [pattern_string]
            self._update_display()
            self._notify_change()
            return True
        return False
    
    def get_pattern_summary(self) -> str:
        """Get a summary description of the current pattern."""
        if not self.pattern_elements:
            return "Empty pattern"
        
        element_counts = {}
        for element in self.pattern_elements:
            if element in PATTERN_PLACEHOLDERS.values():
                name = {v: k for k, v in PATTERN_PLACEHOLDERS.items()}[element]
                element_counts[name] = element_counts.get(name, 0) + 1
            else:
                element_counts['text'] = element_counts.get('text', 0) + 1
        
        summary_parts = []
        for element_type, count in element_counts.items():
            if count == 1:
                summary_parts.append(element_type)
            else:
                summary_parts.append(f"{element_type} (×{count})")
        
        return f"Pattern with: {', '.join(summary_parts)}"
