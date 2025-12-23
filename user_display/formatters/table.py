"""
Table formatter for user display.
"""

from typing import Dict, List, Any, Optional
from io import StringIO
from .base import Formatter


class TableFormatter(Formatter):
    """Format users as ASCII table."""
    
    def __init__(self,
                 field_selection: Optional[List[str]] = None,
                 trim_length: Optional[int] = None,
                 col_width: int = 15):
        super().__init__(field_selection, trim_length)
        self.col_width = col_width
    
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format single user as a table."""
        selected = self._select_fields(user)
        selected = self._trim_strings(selected)
        
        lines = []
        for key, value in selected.items():
            val_str = str(value)[:self.col_width]
            lines.append(f"  {key:<{self.col_width}}: {val_str}")
        
        return "\n".join(lines)
    
    def format_users(self, users: List[Dict[str, Any]]) -> str:
        """Format multiple users as ASCII table."""
        if not users:
            return "No users to display"
        
        # Get column headers from first user
        first = self._select_fields(users[0])
        first = self._trim_strings(first)
        columns = list(first.keys())
        
        # Build table
        output = StringIO()
        
        # Header
        header_parts = [col[:self.col_width].ljust(self.col_width) for col in columns]
        header = " | ".join(header_parts)
        output.write(header + "\n")
        output.write("-" * len(header) + "\n")
        
        # Rows
        for user in users:
            selected = self._select_fields(user)
            selected = self._trim_strings(selected)
            
            row_parts = []
            for col in columns:
                val = str(selected.get(col, ""))[:self.col_width]
                row_parts.append(val.ljust(self.col_width))
            
            output.write(" | ".join(row_parts) + "\n")
        
        return output.getvalue()
