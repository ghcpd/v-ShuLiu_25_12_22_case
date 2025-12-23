"""
Base classes for formatting.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..errors import FormatterError

class Formatter(ABC):
    """Base formatter class."""

    @abstractmethod
    def format_user(self, user: Dict[str, Any]) -> str:
        """Format a single user."""
        pass

    @abstractmethod
    def format_users(self, users: List[Dict[str, Any]], show_count: bool = True) -> str:
        """Format multiple users."""
        pass

    def get_supported_fields(self) -> List[str]:
        """Return list of supported fields."""
        return ['id', 'name', 'email', 'role', 'status', 'join_date', 'last_login']