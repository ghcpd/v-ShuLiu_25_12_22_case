"""
Base classes for validation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..errors import ValidationError

class Validator(ABC):
    """Base validator class."""

    @abstractmethod
    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and potentially repair a user record."""
        pass

    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Return list of required fields."""
        pass