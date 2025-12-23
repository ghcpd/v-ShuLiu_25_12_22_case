"""Thread-safe, indexed user storage with snapshotting, caching and parallel filtering."""
from __future__ import annotations
import threading
from typing import Any, Dict, Iterable, List, Optional, Tuple
from collections import defaultdict
from functools import lru_cache
import time
import json
from .index import build_index
from .formatters.base import Formatter
from .validation.default import DefaultValidator
from .filters.base import Filter
from .metrics import Metrics, timed
from .logging_utils import get_logger

_logger = get_logger("user_display.store")
_metrics = Metrics()

class UserStore:
    """In-memory user store with O(1) id lookup and snapshot support."""

    def __init__(self, users: Optional[Iterable[Dict[str, Any]]] = None, validator: Optional[DefaultValidator] = None):
        self._lock = threading.RLock()
        self._users: List[Dict[str, Any]] = []
        self._id_index: Dict[Any, int] = {}
        self._validator = validator or DefaultValidator()
        self._cache = {}  # simple cache: criteria_key -> list of ids
        if users:
            self.load(list(users))

    def load(self, users: List[Dict[str, Any]]) -> None:
        """Load or replace the store contents (thread-safe)."""
        with self._lock:
            validated = []
            issues = 0
            for u in users:
                ok, out = self._validator.validate(u)
                if not ok:
                    issues += 1
                validated.append(out)
            self._users = validated
            self._id_index = build_index(self._users)
            self._cache.clear()
        _logger.info("loaded_users", extra={"count": len(self._users), "validation_issues": issues})

    def snapshot(self) -> List[Dict[str, Any]]:
        """Return a shallow copy suitable for concurrent reads."""
        with self._lock:
            return list(self._users)

    def get_user_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        with self._lock:
            idx = self._id_index.get(uid)
            if idx is None:
                _metrics.increment("lookup_miss")
                return None
            _metrics.increment("lookup_hit")
            return dict(self._users[idx])  # return a copy

    @timed("filter")
    def filter_users(self, criteria: Dict[str, Any], fmt: Optional[Filter] = None, *, parallel: bool = False) -> List[Dict[str, Any]]:
        """Filter users using a Filter strategy. Results are cached by criteria key."""
        key = self._criteria_key(criteria)
        with self._lock:
            if key in self._cache:
                _metrics.increment("cache_hit")
                ids = self._cache[key]
                return [self.get_user_by_id(i) for i in ids]
        users = self.snapshot()
        # delegate to provided filter or default simple match
        if fmt is None:
            # simple single-pass matcher
            res = []
            for u in users:
                if self._match(u, criteria):
                    res.append(u)
        else:
            res = fmt.apply(users, criteria, parallel=parallel)
        ids = [u["id"] for u in res]
        with self._lock:
            self._cache[key] = ids
        return [dict(u) for u in res]

    def _match(self, u: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        for k, v in criteria.items():
            val = u.get(k)
            if val is None:
                return False
            if isinstance(v, str) and isinstance(val, str):
                if v.lower() not in val.lower():
                    return False
            else:
                if val != v:
                    return False
        return True

    def display_users(self, users: Optional[Iterable[Dict[str, Any]]] = None, *, formatter: Optional[Formatter] = None, show_all: bool = True) -> str:
        users = list(users) if users is not None else self.snapshot()
        if formatter is None:
            from .formatters.compact import CompactFormatter

            formatter = CompactFormatter()
        return formatter.format(users, show_all=show_all)

    def export_users_to_string(self, users: Optional[Iterable[Dict[str, Any]]] = None, *, formatter: Optional[Formatter] = None) -> str:
        users = list(users) if users is not None else self.snapshot()
        if formatter is None:
            from .formatters.json_fmt import JsonFormatter

            formatter = JsonFormatter()
        return formatter.format(users, show_all=True)

    def _criteria_key(self, criteria: Dict[str, Any]) -> str:
        # stable, hashable representation for caching
        try:
            return json.dumps(criteria, sort_keys=True, default=str)
        except Exception:
            return str(sorted(criteria.items()))


# default global store for backwards compatibility
default_store = UserStore()

# convenience functions that mirror the original module-level API
def display_users(users, show_all=True, verbose=False):
    # keep verbose param for compatibility but route to new implementation
    return default_store.display_users(users, show_all=show_all)


def get_user_by_id(users, uid):
    # original accepted a list; support both list and global store lookup
    if isinstance(users, UserStore):
        return users.get_user_by_id(uid)
    # otherwise assume it's an iterable
    tmp = UserStore(users)
    return tmp.get_user_by_id(uid)


def filter_users(users, criteria):
    if isinstance(users, UserStore):
        return users.filter_users(criteria)
    tmp = UserStore(users)
    return tmp.filter_users(criteria)


def export_users_to_string(users):
    if isinstance(users, UserStore):
        return users.export_users_to_string()
    tmp = UserStore(users)
    return tmp.export_users_to_string()
