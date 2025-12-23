"""
Base formatter classes for user display.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class Formatter(ABC):
    """Base class for user formatters."""
    
    def __init__(self, 
                 field_selection: Optional[List[str]] = None,
                 trim_length: Optional[int] = None):
        """
        Initialize formatter.
        
        Args:
            field_selection: List of fields to include (None = all)
            trim_length: Trim string fields to this length (None = no trim)
        """
        self.field_selection = field_selection
        self.trim_length = trim_length
    
    @abstractmethod
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format a single user."""
        pass
    
    @abstractmethod
    def format_users(self, users: List[Dict[str, Any]]) -> str:
        """Format multiple users."""
        pass
    
    def _select_fields(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Select relevant fields from user."""
        if self.field_selection is None:
            selected = user.copy()
        else:
            selected = {k: user.get(k) for k in self.field_selection if k in user}
        return selected
    
    def _trim_strings(self, data: Any) -> Any:
        """Trim string values if trim_length is set."""
        if self.trim_length is None:
            return data
        
        if isinstance(data, str):
            return data[:self.trim_length]
        elif isinstance(data, dict):
            return {k: self._trim_strings(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._trim_strings(v) for v in data]
        return data
