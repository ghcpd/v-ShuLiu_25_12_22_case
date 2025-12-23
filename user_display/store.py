"""
User store with indexing, snapshotting, and thread-safe operations.
"""

import threading
import copy
from typing import Dict, Any, List, Optional
from .index import UserIndex
from .validation import DefaultValidator
from .logging_utils import logger
from .metrics import metrics
from .errors import StoreError
from .config import config

class UserStore:
    """Thread-safe user store with MVCC-like snapshotting."""

    def __init__(self, validator=None):
        self._index = UserIndex()
        self._validator = validator or DefaultValidator()
        self._lock = threading.RLock()
        self._snapshots: Dict[str, List[Dict[str, Any]]] = {}
        self._version = 0

    def add_user(self, user: Dict[str, Any]):
        """Add a user to the store."""
        with self._lock:
            try:
                validated_user = self._validator.validate(user)
                self._index.add_user(validated_user)
                self._version += 1
                metrics.increment('store_adds')
                logger.debug("User added", user_id=validated_user['id'])
            except Exception as e:
                logger.error("Failed to add user", error=str(e))
                raise StoreError(f"Failed to add user: {e}")

    def add_users(self, users: List[Dict[str, Any]]):
        """Add multiple users to the store."""
        with self._lock:
            for user in users:
                self.add_user(user)

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        with self._lock:
            return self._index.get_user(user_id)

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        with self._lock:
            return self._index.get_all_users()

    def remove_user(self, user_id: int):
        """Remove a user."""
        with self._lock:
            self._index.remove_user(user_id)
            self._version += 1
            metrics.increment('store_removes')
            logger.debug("User removed", user_id=user_id)

    def create_snapshot(self, name: str):
        """Create a snapshot of current state."""
        with self._lock:
            users = self._index.get_all_users()
            self._snapshots[name] = copy.deepcopy(users)
            logger.info("Snapshot created", name=name, user_count=len(users))

    def get_snapshot(self, name: str) -> Optional[List[Dict[str, Any]]]:
        """Get a snapshot."""
        return self._snapshots.get(name)

    def list_snapshots(self) -> List[str]:
        """List all snapshots."""
        return list(self._snapshots.keys())

    def clear(self):
        """Clear all users."""
        with self._lock:
            self._index.clear()
            self._version = 0
            metrics.increment('store_clears')
            logger.info("Store cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        with self._lock:
            index_stats = self._index.get_stats()
            return {
                **index_stats,
                'version': self._version,
                'snapshots': len(self._snapshots),
            }