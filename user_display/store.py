"""
User storage with indexing, snapshotting, and thread-safe operations.
"""

from typing import Dict, List, Any, Optional, Callable
from threading import RLock
from copy import deepcopy
from datetime import datetime
import time

from .index import ShardIndex
from .validation import create_user_validator
from .config import get_config
from .logging_utils import get_logger
from .metrics import get_metrics
from .errors import CorruptedDataError, ValidationError


class UserStore:
    """
    Thread-safe user storage with:
    - O(1) ID lookup via sharded indexing
    - Snapshotting for consistent concurrent reads
    - Validation with soft-failure recovery
    - Caching support
    """
    
    def __init__(self, validator=None):
        self._users: List[Dict[str, Any]] = []
        self._index: ShardIndex = ShardIndex(
            shard_count=get_config().get('shard_count', 4)
        )
        self._lock = RLock()
        self._snapshots: Dict[str, List[Dict[str, Any]]] = {}
        self._validator = validator or create_user_validator()
        self._logger = get_logger()
        self._metrics = get_metrics()
        self._cache: Dict[str, Any] = {}
        self._cache_enabled = get_config().get('enable_caching', True)
    
    def add_user(self, user: Dict[str, Any]) -> bool:
        """Add a user with validation."""
        with self._lock:
            # Validate
            is_valid, error_msg = self._validator.validate(user)
            
            if not is_valid:
                if get_config().get('validation_soft_fail', True):
                    self._metrics.record_validation_error()
                    user = self._validator.recover(user)
                    self._metrics.record_validation_recovery()
                    self._logger.info(
                        "User validation failed, recovered",
                        user_id=user.get('id'),
                        error=error_msg
                    )
                else:
                    self._logger.error(
                        "User validation failed",
                        user_id=user.get('id'),
                        error=error_msg
                    )
                    raise ValidationError(error_msg)
            
            # Add user
            user_id = user.get('id')
            if self._index.exists(user_id):
                return False  # Already exists
            
            self._users.append(user)
            self._index.add(user_id, len(self._users) - 1)
            self._invalidate_cache()
            return True
    
    def get_user_by_id(self, user_id: Any) -> Optional[Dict[str, Any]]:
        """Get user by ID (O(1) lookup)."""
        with self._lock:
            index = self._index.get(user_id)
            if index is not None and 0 <= index < len(self._users):
                return deepcopy(self._users[index])
            return None
    
    def remove_user(self, user_id: Any) -> bool:
        """Remove user by ID."""
        with self._lock:
            index = self._index.get(user_id)
            if index is None:
                return False
            
            # Mark as removed (for stability, don't reindex)
            self._users[index] = {'_deleted': True, 'id': user_id}
            self._index.remove(user_id)
            self._invalidate_cache()
            return True
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all non-deleted users."""
        with self._lock:
            return [
                deepcopy(u) for u in self._users
                if '_deleted' not in u
            ]
    
    def update_user(self, user_id: Any, updates: Dict[str, Any]) -> bool:
        """Update user fields."""
        with self._lock:
            index = self._index.get(user_id)
            if index is None or index >= len(self._users):
                return False
            
            user = self._users[index]
            if '_deleted' in user:
                return False
            
            user.update(updates)
            self._invalidate_cache()
            return True
    
    def create_snapshot(self, name: str) -> str:
        """Create a snapshot for consistent concurrent reads."""
        with self._lock:
            self._snapshots[name] = deepcopy([
                u for u in self._users if '_deleted' not in u
            ])
            self._logger.info(f"Snapshot created: {name}")
            return name
    
    def load_snapshot(self, name: str) -> Optional[List[Dict[str, Any]]]:
        """Load a snapshot."""
        with self._lock:
            return deepcopy(self._snapshots.get(name))
    
    def delete_snapshot(self, name: str) -> bool:
        """Delete a snapshot."""
        with self._lock:
            if name in self._snapshots:
                del self._snapshots[name]
                return True
            return False
    
    def get_snapshots(self) -> List[str]:
        """Get list of available snapshots."""
        with self._lock:
            return list(self._snapshots.keys())
    
    def _invalidate_cache(self):
        """Invalidate all cached results."""
        if self._cache_enabled:
            self._cache.clear()
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cached value."""
        if self._cache_enabled and key in self._cache:
            self._metrics.record_cache_hit()
            return self._cache[key]
        self._metrics.record_cache_miss()
        return None
    
    def set_cache(self, key: str, value: Any):
        """Cache a value."""
        if self._cache_enabled:
            max_size = get_config().get('cache_size', 1000)
            if len(self._cache) >= max_size:
                # Simple LRU: remove first item
                first_key = next(iter(self._cache))
                del self._cache[first_key]
            self._cache[key] = value
    
    def count_users(self) -> int:
        """Get count of non-deleted users."""
        with self._lock:
            return sum(1 for u in self._users if '_deleted' not in u)
    
    def get_shard_stats(self) -> Dict[int, int]:
        """Get shard distribution statistics."""
        return self._index.get_shard_stats()
    
    def clear(self):
        """Clear all users and snapshots."""
        with self._lock:
            self._users.clear()
            self._index.clear()
            self._snapshots.clear()
            self._cache.clear()
