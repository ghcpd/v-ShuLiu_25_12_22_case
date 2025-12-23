"""
Table formatter implementation.
"""

from typing import Dict, Any, List
from .base import Formatter

class TableFormatter(Formatter):
    """Table-based user formatting."""

    def format_user(self, user: Dict[str, Any]) -> str:
        lines = []
        for field in self.get_supported_fields():
            value = user.get(field, 'N/A')
            lines.append(f"{field.replace('_', ' ').title()}: {value}")
        return "\n".join(lines)

    def format_users(self, users: List[Dict[str, Any]], show_count: bool = True) -> str:
        if not users:
            return "No users to display."

        result = []
        for i, user in enumerate(users):
            if i > 0:
                result.append("-" * 40)
            result.append(self.format_user(user))

        if show_count:
            result.append(f"\nTotal users: {len(users)}")

        return "\n".join(result)