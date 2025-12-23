"""Regex-based filter (optionally case-sensitive)."""
from __future__ import annotations
from typing import Any, Dict, Iterable, List, Pattern
import re
from .base import Filter


class RegexFilter(Filter):
    def __init__(self, flags: int = re.IGNORECASE):
        self.flags = flags

    def apply(self, users: Iterable[Dict[str, Any]], criteria: Dict[str, Any], *, parallel: bool = False) -> List[Dict[str, Any]]:
        patterns = {k: re.compile(v, self.flags) for k, v in criteria.items()}
        res = []
        for u in users:
            ok = True
            for k, p in patterns.items():
                val = u.get(k, "")
                if not isinstance(val, str) or not p.search(val):
                    ok = False
                    break
            if ok:
                res.append(u)
        return res
