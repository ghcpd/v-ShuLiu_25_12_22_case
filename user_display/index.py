"""
Indexing system for O(1) ID lookup and sharding.
"""

from typing import Dict, List, Any, Optional
from threading import RLock


class UserIndex:
    """Hash-based index for O(1) user ID lookup."""
    
    def __init__(self):
        self._index: Dict[Any, int] = {}  # Maps user_id to list index
        self._lock = RLock()
    
    def add(self, user_id: Any, list_index: int):
        """Add user to index."""
        with self._lock:
            self._index[user_id] = list_index
    
    def remove(self, user_id: Any):
        """Remove user from index."""
        with self._lock:
            self._index.pop(user_id, None)
    
    def get(self, user_id: Any) -> Optional[int]:
        """Get list index for user ID (O(1))."""
        with self._lock:
            return self._index.get(user_id)
    
    def exists(self, user_id: Any) -> bool:
        """Check if user ID exists."""
        with self._lock:
            return user_id in self._index
    
    def clear(self):
        """Clear the index."""
        with self._lock:
            self._index.clear()
    
    def size(self) -> int:
        """Get number of indexed users."""
        with self._lock:
            return len(self._index)


class ShardIndex:
    """Sharded index for distributed user storage."""
    
    def __init__(self, shard_count: int = 4):
        self.shard_count = shard_count
        self._shards: Dict[int, UserIndex] = {
            i: UserIndex() for i in range(shard_count)
        }
        self._lock = RLock()
    
    def _get_shard_id(self, user_id: Any) -> int:
        """Get shard ID for user ID."""
        return hash(user_id) % self.shard_count
    
    def add(self, user_id: Any, list_index: int):
        """Add user to appropriate shard."""
        shard_id = self._get_shard_id(user_id)
        self._shards[shard_id].add(user_id, list_index)
    
    def remove(self, user_id: Any):
        """Remove user from appropriate shard."""
        shard_id = self._get_shard_id(user_id)
        self._shards[shard_id].remove(user_id)
    
    def get(self, user_id: Any) -> Optional[int]:
        """Get list index for user ID."""
        shard_id = self._get_shard_id(user_id)
        return self._shards[shard_id].get(user_id)
    
    def exists(self, user_id: Any) -> bool:
        """Check if user ID exists."""
        shard_id = self._get_shard_id(user_id)
        return self._shards[shard_id].exists(user_id)
    
    def get_shard_stats(self) -> Dict[int, int]:
        """Get user count per shard."""
        with self._lock:
            return {i: shard.size() for i, shard in self._shards.items()}
    
    def clear(self):
        """Clear all shards."""
        with self._lock:
            for shard in self._shards.values():
                shard.clear()
