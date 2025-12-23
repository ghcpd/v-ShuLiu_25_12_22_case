"""
Compact formatter for user display.
"""

from typing import Dict, List, Any, Optional
from io import StringIO
from .base import Formatter


class CompactFormatter(Formatter):
    """Format users in compact pipe-separated format."""
    
    def __init__(self,
                 field_selection: Optional[List[str]] = None,
                 trim_length: Optional[int] = None,
                 separator: str = " | "):
        super().__init__(field_selection, trim_length)
        self.separator = separator
    
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format single user in compact format."""
        selected = self._select_fields(user)
        selected = self._trim_strings(selected)
        
        parts = [f"{k}={v}" for k, v in selected.items()]
        return self.separator.join(parts)
    
    def format_users(self, users: List[Dict[str, Any]]) -> str:
        """Format multiple users with one per line."""
        lines = []
        for user in users:
            selected = self._select_fields(user)
            selected = self._trim_strings(selected)
            parts = [f"{k}={v}" for k, v in selected.items()]
            lines.append(self.separator.join(parts))
        
        return "\n".join(lines)
