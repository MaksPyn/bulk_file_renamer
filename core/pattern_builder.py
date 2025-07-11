"""Pattern building functionality for filename generation."""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from config.constants import PATTERN_PLACEHOLDERS
from utils.validators import validate_pattern_placeholder


@dataclass
class PatternElement:
    """Represents a single element in a filename pattern."""
    type: str  # 'placeholder' or 'text'
    value: str
    position: int


class PatternBuilder:
    """Handles building and managing filename patterns."""
    
    def __init__(self):
        self.elements: List[PatternElement] = []
        self._reset_to_default()
    
    def _reset_to_default(self) -> None:
        """Reset pattern to default configuration."""
        default_pattern = [
            PATTERN_PLACEHOLDERS["prefix"],
            PATTERN_PLACEHOLDERS["name"],
            PATTERN_PLACEHOLDERS["suffix"],
            PATTERN_PLACEHOLDERS["number"],
            PATTERN_PLACEHOLDERS["date"]
        ]
        self.set_pattern_from_list(default_pattern)
    
    def add_element(self, element: str, position: Optional[int] = None) -> bool:
        """
        Add an element to the pattern.
        
        Args:
            element: The element to add (placeholder or text)
            position: Position to insert at (None for end)
            
        Returns:
            True if added successfully, False otherwise
        """
        is_valid, error_msg = validate_pattern_placeholder(element)
        if not is_valid:
            return False
        
        element_type = "placeholder" if element.startswith('{') and element.endswith('}') else "text"
        
        if position is None:
            position = len(self.elements)
        
        pattern_element = PatternElement(
            type=element_type,
            value=element,
            position=position
        )
        
        self.elements.insert(position, pattern_element)
        self._update_positions()
        return True
    
    def remove_element(self, position: int) -> bool:
        """
        Remove an element from the pattern.
        
        Args:
            position: Position of element to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        if 0 <= position < len(self.elements):
            self.elements.pop(position)
            self._update_positions()
            return True
        return False
    
    def move_element(self, from_position: int, to_position: int) -> bool:
        """
        Move an element to a new position.
        
        Args:
            from_position: Current position of element
            to_position: New position for element
            
        Returns:
            True if moved successfully, False otherwise
        """
        if (0 <= from_position < len(self.elements) and 
            0 <= to_position < len(self.elements)):
            
            element = self.elements.pop(from_position)
            self.elements.insert(to_position, element)
            self._update_positions()
            return True
        return False
    
    def _update_positions(self) -> None:
        """Update position values for all elements."""
        for i, element in enumerate(self.elements):
            element.position = i
    
    def get_pattern_string(self) -> str:
        """
        Get the pattern as a string.
        
        Returns:
            Pattern string with all elements concatenated
        """
        return "".join(element.value for element in self.elements)
    
    def get_pattern_list(self) -> List[str]:
        """
        Get the pattern as a list of strings.
        
        Returns:
            List of pattern elements
        """
        return [element.value for element in self.elements]
    
    def set_pattern_from_string(self, pattern_string: str) -> bool:
        """
        Set pattern from a string by parsing placeholders.
        
        Args:
            pattern_string: Pattern string to parse
            
        Returns:
            True if set successfully, False otherwise
        """
        # Parse placeholders and text from the pattern string
        placeholder_pattern = r'\{[^}]+\}'
        elements = []
        last_end = 0
        
        for match in re.finditer(placeholder_pattern, pattern_string):
            # Add text before placeholder if any
            if match.start() > last_end:
                text = pattern_string[last_end:match.start()]
                if text:
                    elements.append(text)
            
            # Add placeholder
            elements.append(match.group())
            last_end = match.end()
        
        # Add remaining text after last placeholder
        if last_end < len(pattern_string):
            text = pattern_string[last_end:]
            if text:
                elements.append(text)
        
        return self.set_pattern_from_list(elements)
    
    def set_pattern_from_list(self, pattern_list: List[str]) -> bool:
        """
        Set pattern from a list of elements.
        
        Args:
            pattern_list: List of pattern elements
            
        Returns:
            True if set successfully, False otherwise
        """
        self.elements.clear()
        
        for i, element in enumerate(pattern_list):
            is_valid, error_msg = validate_pattern_placeholder(element)
            if not is_valid:
                return False
            
            element_type = "placeholder" if element.startswith('{') and element.endswith('}') else "text"
            
            pattern_element = PatternElement(
                type=element_type,
                value=element,
                position=i
            )
            self.elements.append(pattern_element)
        
        return True
    
    def generate_filename(
        self,
        original_name: str,
        values: Dict[str, Any],
        extension: str = ""
    ) -> str:
        """
        Generate a filename using the current pattern.
        
        Args:
            original_name: Original filename (without extension)
            values: Dictionary of values for placeholders
            extension: File extension (with or without dot)
            
        Returns:
            Generated filename
        """
        # Ensure extension starts with dot
        if extension and not extension.startswith('.'):
            extension = '.' + extension
        
        # Default values
        default_values = {
            'prefix': values.get('prefix', ''),
            'name': original_name,
            'suffix': values.get('suffix', ''),
            'num': values.get('num', ''),
            'date': values.get('date', '')
        }
        
        # Build filename from pattern
        filename_parts = []
        for element in self.elements:
            if element.type == "placeholder":
                # Extract placeholder name (remove braces)
                placeholder_name = element.value[1:-1]
                value = default_values.get(placeholder_name, '')
                if value:  # Only add non-empty values
                    filename_parts.append(str(value))
            else:
                # Add text element as-is
                filename_parts.append(element.value)
        
        filename = "".join(filename_parts)
        
        # Clean up multiple separators and trim
        filename = re.sub(r'[-_\s]+', lambda m: m.group()[0], filename)
        filename = filename.strip('-_ ')
        
        # Ensure we have a valid filename
        if not filename:
            filename = original_name or "unnamed"
        
        return filename + extension
    
    def validate_pattern(self) -> tuple[bool, Optional[str]]:
        """
        Validate the current pattern.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.elements:
            return False, "Pattern cannot be empty"
        
        # Check if pattern contains at least one meaningful element
        has_meaningful_element = False
        for element in self.elements:
            if element.type == "placeholder" or element.value.strip():
                has_meaningful_element = True
                break
        
        if not has_meaningful_element:
            return False, "Pattern must contain at least one placeholder or text"
        
        return True, None
    
    def get_preview(self, sample_values: Dict[str, Any]) -> str:
        """
        Get a preview of what the pattern would generate.
        
        Args:
            sample_values: Sample values for preview
            
        Returns:
            Preview string
        """
        return self.generate_filename(
            original_name=sample_values.get('name', 'example'),
            values=sample_values,
            extension=sample_values.get('extension', '.jpg')
        )
    
    def clear(self) -> None:
        """Clear all elements from the pattern."""
        self.elements.clear()
    
    def is_empty(self) -> bool:
        """Check if pattern is empty."""
        return len(self.elements) == 0
    
    def get_element_count(self) -> int:
        """Get number of elements in pattern."""
        return len(self.elements)
    
    def get_element_at(self, position: int) -> Optional[PatternElement]:
        """Get element at specific position."""
        if 0 <= position < len(self.elements):
            return self.elements[position]
        return None
