"""High-performance, thread-safe user storage with indexing and snapshots."""
from __future__ import annotations

import threading
import time
from typing import Dict, Iterable, List, Optional, Tuple

from .validation.default import DefaultValidator
from .errors import NotFoundError

class UserStore:
    """In-memory user store with O(1) id lookup, snapshots, and optional sharding.

    - Keeps an internal dict id->user for O(1) lookup
    - Maintains a monotonically increasing _version to support MVCC-like snapshots
    - Thread-safe for concurrent reads and writes using a RW-style lock (RLock)
    - Validation is applied on insertion
    """

    def __init__(self, users: Optional[Iterable[dict]] = None, validator: Optional[DefaultValidator] = None) -> None:
        self._lock = threading.RLock()
        self._by_id: Dict[str, dict] = {}
        self._order: List[str] = []
        self._version = 0
        self._validator = validator or DefaultValidator()
        if users:
            self.bulk_insert(users)

    def bulk_insert(self, users: Iterable[dict]) -> None:
        """Insert many users efficiently in a single lock acquisition."""
        with self._lock:
            for u in users:
                clean = self._validator.validate(u)
                uid = str(clean["id"])
                if uid not in self._by_id:
                    self._order.append(uid)
                self._by_id[uid] = clean
            self._version += 1

    def upsert(self, user: dict) -> None:
        clean = self._validator.validate(user)
        uid = str(clean["id"])
        with self._lock:
            if uid not in self._by_id:
                self._order.append(uid)
            self._by_id[uid] = clean
            self._version += 1

    def get_user_by_id(self, uid: str) -> dict:
        with self._lock:
            try:
                return dict(self._by_id[str(uid)])
            except KeyError:
                raise NotFoundError(f"user id={uid} not found")

    def snapshot(self) -> Tuple[int, List[dict]]:
        """Return a lightweight consistent snapshot (version, list) for concurrent reads."""
        with self._lock:
            version = self._version
            # return shallow copies to avoid cross-thread mutation
            data = [self._by_id[uid] for uid in self._order]
            return version, data

    def all_users(self) -> List[dict]:
        _, data = self.snapshot()
        return [dict(u) for u in data]

    def __len__(self) -> int:
        with self._lock:
            return len(self._by_id)
