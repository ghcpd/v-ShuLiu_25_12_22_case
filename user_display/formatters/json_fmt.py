"""
JSON formatter implementation.
"""

import json
from typing import Dict, Any, List
from .base import Formatter

class JSONFormatter(Formatter):
    """JSON-based user formatting."""

    def format_user(self, user: Dict[str, Any]) -> str:
        return json.dumps(user, indent=2, default=str)

    def format_users(self, users: List[Dict[str, Any]], show_count: bool = True) -> str:
        if show_count:
            result = {"users": users, "count": len(users)}
            return json.dumps(result, indent=2, default=str)
        else:
            return json.dumps(users, indent=2, default=str)