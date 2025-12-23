"""Indexing utilities for UserStore."""
from typing import Any, Dict, List


def build_index(users: List[Dict[str, Any]]) -> Dict[Any, int]:
    """Build a simple id -> list-index map. Last-write wins for duplicates."""
    idx = {}
    for i, u in enumerate(users):
        uid = u.get("id")
        if uid is None:
            continue
        idx[uid] = i
    return idx
