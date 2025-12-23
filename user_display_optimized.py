"""Compatibility wrapper preserving original public API."""
from user_display import UserStore, get_formatter
from user_display.validation import DefaultValidator
from user_display.filters import FilterRegistry
from user_display._internal_ops import filter_users_list
from user_display.metrics import inc
from user_display.logging_utils import log_structured
from user_display.config import Config


def display_users(users, show_all=True, verbose=False, fmt=None, fields=None):
    """Display users using formatters; accepts list or UserStore."""
    inc("display_calls")
    if isinstance(users, UserStore):
        users = users.list_snapshot()
    fmt = fmt or Config.DEFAULT_FORMAT
    formatter = get_formatter(fmt)
    out = formatter.format(users, fields=fields)
    if show_all:
        out += f"PROCESSED={len(users)}\n"
    if verbose:
        log_structured(20, "display", count=len(users))
    return out


def get_user_by_id(users, uid):
    inc("id_lookup_calls")
    if isinstance(users, UserStore):
        return users.get_by_id(uid)
    # list fallback: build index temporarily
    idx = {u.get("id"): u for u in users if u.get("id") is not None}
    return idx.get(uid)


def filter_users(users, criteria, parallel=False):
    inc("filter_interface_calls")
    if isinstance(users, UserStore):
        users = users.list_snapshot()
    # simple criteria -> matcher
    filters = []
    for k, v in criteria.items():
        if isinstance(v, dict) and v.get("type") == "regex":
            f = FilterRegistry.create("regex", k, v.get("pattern"), flags=0)
        else:
            # default equality/substring
            pattern = str(v)
            def make_match(k, pattern):
                return lambda u: pattern.lower() in str(u.get(k, "")).lower()
            f = type("_anon", (), {"match": lambda self, u, k=k, pattern=pattern: make_match(k, pattern)(u)})()
        filters.append(f)
    comp = FilterRegistry.create("composite", filters)
    return filter_users_list(users, comp.match, parallel=parallel)


def export_users_to_string(users, fmt="table", fields=None):
    # for compatibility with original heavy exporter, use table with join_date parsing avoided
    inc("export_calls")
    return display_users(users, show_all=True, verbose=False, fmt=fmt, fields=fields)
