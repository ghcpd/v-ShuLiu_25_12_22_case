"""
Indexing system for fast user lookups.
"""

import hashlib
from typing import Dict, Any, List, Optional
from collections import defaultdict
from .config import config
from .logging_utils import logger
from .metrics import metrics

class UserIndex:
    """Sharded hash-based index for user lookups."""

    def __init__(self, shard_count: Optional[int] = None):
        self.shard_count = shard_count or config.get('shard_count', 16)
        self.shards: List[Dict[int, Dict[str, Any]]] = [{} for _ in range(self.shard_count)]
        self._reverse_index: Dict[int, int] = {}  # user_id -> shard_index

    def _get_shard(self, user_id: int) -> int:
        """Get shard index for a user ID."""
        return user_id % self.shard_count

    def add_user(self, user: Dict[str, Any]):
        """Add a user to the index."""
        user_id = user.get('id')
        if user_id is None:
            return

        shard_idx = self._get_shard(user_id)
        self.shards[shard_idx][user_id] = user
        self._reverse_index[user_id] = shard_idx
        metrics.increment('index_adds')

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        metrics.increment('index_lookups')
        timer = metrics.timer_start('index_lookup')

        shard_idx = self._reverse_index.get(user_id)
        if shard_idx is not None:
            user = self.shards[shard_idx].get(user_id)
            metrics.timer_stop(timer)
            if user:
                metrics.increment('index_hits')
            else:
                metrics.increment('index_misses')
            return user

        metrics.timer_stop(timer)
        metrics.increment('index_misses')
        return None

    def remove_user(self, user_id: int):
        """Remove a user from the index."""
        shard_idx = self._reverse_index.get(user_id)
        if shard_idx is not None:
            if user_id in self.shards[shard_idx]:
                del self.shards[shard_idx][user_id]
                del self._reverse_index[user_id]
                metrics.increment('index_removes')

    def clear(self):
        """Clear all users from the index."""
        for shard in self.shards:
            shard.clear()
        self._reverse_index.clear()
        logger.info("Index cleared")

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the index."""
        users = []
        for shard in self.shards:
            users.extend(shard.values())
        return users

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        total_users = sum(len(shard) for shard in self.shards)
        return {
            'total_users': total_users,
            'shard_count': self.shard_count,
            'avg_users_per_shard': total_users / self.shard_count if self.shard_count > 0 else 0,
            'max_users_per_shard': max(len(shard) for shard in self.shards),
            'min_users_per_shard': min(len(shard) for shard in self.shards),
        }