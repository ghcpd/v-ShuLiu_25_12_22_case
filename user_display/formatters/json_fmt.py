"""
JSON formatter for user display.
"""

import json
from typing import Dict, List, Any, Optional
from .base import Formatter


class JsonFormatter(Formatter):
    """Format users as JSON."""
    
    def __init__(self,
                 field_selection: Optional[List[str]] = None,
                 trim_length: Optional[int] = None,
                 pretty: bool = True):
        super().__init__(field_selection, trim_length)
        self.pretty = pretty
    
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format single user as JSON."""
        selected = self._select_fields(user)
        selected = self._trim_strings(selected)
        indent = 2 if self.pretty else None
        return json.dumps(selected, indent=indent)
    
    def format_users(self, users: List[Dict[str, Any]]) -> str:
        """Format multiple users as JSON array."""
        formatted = []
        for user in users:
            selected = self._select_fields(user)
            selected = self._trim_strings(selected)
            formatted.append(selected)
        
        indent = 2 if self.pretty else None
        return json.dumps(formatted, indent=indent)
