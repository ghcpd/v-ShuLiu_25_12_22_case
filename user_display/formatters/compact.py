"""
Compact formatter implementation.
"""

from typing import Dict, Any, List
from .base import Formatter

class CompactFormatter(Formatter):
    """Compact, single-line user formatting."""

    def format_user(self, user: Dict[str, Any]) -> str:
        fields = []
        for field in self.get_supported_fields():
            value = user.get(field, 'N/A')
            fields.append(f"{field.upper()}={value}")
        return " | ".join(fields)

    def format_users(self, users: List[Dict[str, Any]], show_count: bool = True) -> str:
        lines = [self.format_user(user) for user in users]
        result = "\n".join(lines)
        if show_count:
            result += f"\nPROCESSED={len(users)}\n"
        return result