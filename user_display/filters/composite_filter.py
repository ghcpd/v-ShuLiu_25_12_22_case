"""Compose multiple filters with AND/OR semantics."""
from __future__ import annotations
from .base import BaseFilter
from typing import Iterable, Dict, Any, List


@BaseFilter.register
class CompositeFilter(BaseFilter):
    name = "composite"

    def __init__(self, filters: Iterable[BaseFilter], op: str = "and"):
        self.filters: List[BaseFilter] = list(filters)
        self.op = op.lower()

    def matches(self, user: Dict[str, Any]) -> bool:
        if self.op == "and":
            for f in self.filters:
                if not f.matches(user):
                    return False
            return True
        elif self.op == "or":
            for f in self.filters:
                if f.matches(user):
                    return True
            return False
        else:
            raise ValueError("unsupported op")
