"""
Base filter classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable


class Filter(ABC):
    """Base filter class."""
    
    @abstractmethod
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches filter criteria."""
        pass


class CriteriaFilter(Filter):
    """Filter by matching criteria fields."""
    
    def __init__(self, criteria: Dict[str, Any], case_sensitive: bool = False):
        """
        Initialize filter.
        
        Args:
            criteria: Dict of field_name -> value to match
            case_sensitive: Whether string comparison is case-sensitive
        """
        self.criteria = criteria
        self.case_sensitive = case_sensitive
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all criteria."""
        for field, expected in self.criteria.items():
            actual = user.get(field)
            
            if not self._values_match(actual, expected):
                return False
        
        return True
    
    def _values_match(self, actual: Any, expected: Any) -> bool:
        """Check if actual value matches expected."""
        if actual is None:
            return expected is None
        
        # String comparison
        if isinstance(actual, str) and isinstance(expected, str):
            if self.case_sensitive:
                return expected in actual
            else:
                return expected.lower() in actual.lower()
        
        # Direct comparison
        return actual == expected


class CompositeFilter(Filter):
    """Composite filter combining multiple filters."""
    
    def __init__(self, filters: List[Filter], match_all: bool = True):
        """
        Initialize composite filter.
        
        Args:
            filters: List of filters to combine
            match_all: True=AND logic, False=OR logic
        """
        self.filters = filters
        self.match_all = match_all
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches filters."""
        if self.match_all:
            return all(f.matches(user) for f in self.filters)
        else:
            return any(f.matches(user) for f in self.filters)


class CallableFilter(Filter):
    """Filter using a custom callable."""
    
    def __init__(self, func: Callable[[Dict[str, Any]], bool]):
        """Initialize with a callable."""
        self.func = func
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Apply callable filter."""
        try:
            return bool(self.func(user))
        except Exception:
            return False
