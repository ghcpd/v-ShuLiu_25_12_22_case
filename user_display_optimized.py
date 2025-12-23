"""Compatibility wrapper exposing the original public API but backed by the new implementation."""
from typing import Any, Dict, Iterable, List, Optional
from user_display import default_store, UserStore
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JsonFormatter
from user_display.filters.regex_filter import RegexFilter


# preserve function signatures
def display_users(users: Iterable[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    # accept either raw iterable or a UserStore
    if isinstance(users, UserStore):
        return users.display_users(show_all=show_all)
    return default_store.display_users(users, show_all=show_all)


def get_user_by_id(users: Iterable[Dict[str, Any]] | UserStore, uid: Any) -> Optional[Dict[str, Any]]:
    if isinstance(users, UserStore):
        return users.get_user_by_id(uid)
    # fall back to original behavior: scan provided iterable
    tmp = UserStore(users)
    return tmp.get_user_by_id(uid)


def filter_users(users: Iterable[Dict[str, Any]] | UserStore, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(users, UserStore):
        return users.filter_users(criteria)
    tmp = UserStore(users)
    return tmp.filter_users(criteria)


def export_users_to_string(users: Iterable[Dict[str, Any]] | UserStore) -> str:
    if isinstance(users, UserStore):
        return users.export_users_to_string()
    tmp = UserStore(users)
    return tmp.export_users_to_string()
