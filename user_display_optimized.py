"""Compatibility wrapper exposing the original public API but backed by the new modular implementation.

Public functions preserved:
- display_users
- get_user_by_id
- filter_users
- export_users_to_string
"""
from __future__ import annotations

from typing import Iterable, List, Dict, Any, Optional
from user_display import UserStore, formatter_registry, filter_registry, DefaultValidator, Config
from user_display.logging_utils import debug, info
from user_display.metrics import metrics
from concurrent.futures import ThreadPoolExecutor
import time

_store = UserStore()
_config = Config.from_env()

# Public API (backwards compatible signatures)

def _ensure_store_initialized(users: Optional[Iterable[Dict[str, Any]]]) -> None:
    if users is not None:
        _store.bulk_insert(users)


def display_users(users: Optional[Iterable[Dict[str, Any]]] = None,
                  fmt: Optional[str] = None,
                  fields: Optional[List[str]] = None,
                  limit: Optional[int] = None) -> str:
    """Display users using a formatter. Accepts same parameters as original module.

    - users: optional initial dataset to load into the store
    - fmt: one of registered formatter names
    - fields: optional field selection
    - limit: optional maximum number of rows
    """
    start = time.perf_counter()
    _ensure_store_initialized(users)
    fmt = fmt or _config.default_formatter
    formatter = formatter_registry.get(fmt)
    if not formatter:
        raise ValueError(f"unknown formatter {fmt}")
    _, snapshot = _store.snapshot()
    data = snapshot[:limit] if limit else snapshot
    out = formatter.format_many(data, fields)
    metrics.record_time(start)
    debug("display_users", fmt=fmt, count=len(data), time_ms=metrics.last_op_time_ms)
    return out


def get_user_by_id(uid: str) -> Dict[str, Any]:
    return _store.get_user_by_id(uid)


def filter_users(filter_obj, users: Optional[Iterable[Dict[str, Any]]] = None, parallel: bool = False) -> List[Dict[str, Any]]:
    """Filter users with provided filter object (instance of BaseFilter or compatible callable).

    - If users provided, loads them first (keeps compatibility with older callers that passed dataset here)
    - parallel: when True, uses ThreadPoolExecutor to evaluate filters concurrently
    """
    _ensure_store_initialized(users)
    _, snapshot = _store.snapshot()
    if callable(filter_obj) and not hasattr(filter_obj, "matches"):
        fn = filter_obj
        matcher = lambda u: bool(fn(u))
    elif hasattr(filter_obj, "matches"):
        matcher = lambda u: filter_obj.matches(u)
    else:
        raise ValueError("filter_obj must be callable or have .matches(user)")

    if parallel:
        max_workers = min(_config.max_workers, 32)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            results = list(ex.map(lambda u: (u, matcher(u)), snapshot))
            out = [u for u, ok in results if ok]
    else:
        out = [u for u in snapshot if matcher(u)]
    return out


def export_users_to_string(users: Optional[Iterable[Dict[str, Any]]] = None, fmt: str = "json", fields: Optional[List[str]] = None) -> str:
    """Export users to string in the requested format (JSON/table/compact)."""
    return display_users(users=users, fmt=fmt, fields=fields)
