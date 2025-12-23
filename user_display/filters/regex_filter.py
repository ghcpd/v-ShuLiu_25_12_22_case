"""Regex-based filter with multi-field targeting."""
from __future__ import annotations
from .base import BaseFilter
import re
from typing import Iterable, Dict, Any, Optional


@BaseFilter.register
class RegexFilter(BaseFilter):
    name = "regex"

    def __init__(self, pattern: str, fields: Optional[Iterable[str]] = None, flags: int = 0):
        self.pattern = pattern
        self._re = re.compile(pattern, flags)
        self.fields = list(fields) if fields else None

    def matches(self, user: Dict[str, Any]) -> bool:
        if self.fields is None:
            # search any field
            for v in user.values():
                if v is None:
                    continue
                if self._re.search(str(v)):
                    return True
            return False
        else:
            for f in self.fields:
                v = user.get(f)
                if v is None:
                    continue
                if self._re.search(str(v)):
                    return True
            return False
