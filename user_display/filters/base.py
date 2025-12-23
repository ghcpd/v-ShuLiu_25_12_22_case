"""
Base classes for filtering.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable
from ..errors import FilterError

class Filter(ABC):
    """Base filter class."""

    @abstractmethod
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches the filter criteria."""
        pass

    @abstractmethod
    def get_criteria(self) -> Dict[str, Any]:
        """Return the filter criteria."""
        pass

class CompositeFilter(Filter):
    """Filter that combines multiple filters."""

    def __init__(self, filters: List[Filter], operator: str = 'AND'):
        self.filters = filters
        self.operator = operator.upper()
        if self.operator not in ['AND', 'OR']:
            raise FilterError(f"Invalid operator: {operator}")

    def matches(self, user: Dict[str, Any]) -> bool:
        if self.operator == 'AND':
            return all(f.matches(user) for f in self.filters)
        else:  # OR
            return any(f.matches(user) for f in self.filters)

    def get_criteria(self) -> Dict[str, Any]:
        return {
            'type': 'composite',
            'operator': self.operator,
            'filters': [f.get_criteria() for f in self.filters]
        }