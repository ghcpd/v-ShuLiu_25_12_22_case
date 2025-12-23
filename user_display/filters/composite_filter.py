"""Composite filter that composes multiple filter strategies."""
from __future__ import annotations
from typing import Any, Dict, Iterable, List
from .base import Filter


class CompositeFilter(Filter):
    def __init__(self, filters: Iterable[Filter]):
        self._filters = list(filters)

    def apply(self, users: Iterable[Dict[str, Any]], criteria: Dict[str, Any], *, parallel: bool = False) -> List[Dict[str, Any]]:
        res = list(users)
        for f in self._filters:
            res = f.apply(res, criteria, parallel=parallel)
        return res
