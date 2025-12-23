"""
Composite filter with advanced operations.
"""

from typing import Dict, List, Any, Callable
from .base import Filter, CompositeFilter


class AdvancedCompositeFilter(CompositeFilter):
    """Advanced composite filter with caching and parallel support."""
    
    def __init__(self, filters: List[Filter], match_all: bool = True):
        super().__init__(filters, match_all)
        self._cache: Dict[tuple, bool] = {}
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches filters."""
        return super().matches(user)
    
    def filter_users(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter users list (single-pass, efficient)."""
        return [u for u in users if self.matches(u)]
    
    def filter_users_parallel(self,
                              users: List[Dict[str, Any]],
                              num_workers: int = 4) -> List[Dict[str, Any]]:
        """Filter users in parallel (when Python GIL allows)."""
        from concurrent.futures import ThreadPoolExecutor
        
        if num_workers <= 1:
            return self.filter_users(users)
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            matches = list(executor.map(self.matches, users))
        
        return [u for u, matched in zip(users, matches) if matched]
