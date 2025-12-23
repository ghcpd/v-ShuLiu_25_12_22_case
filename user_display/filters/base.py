"""Filter base class and simple utilities."""
from __future__ import annotations
from typing import Any, Dict, Iterable, List
from abc import ABC, abstractmethod
import re


class Filter(ABC):
    @abstractmethod
    def apply(self, users: Iterable[Dict[str, Any]], criteria: Dict[str, Any], *, parallel: bool = False) -> List[Dict[str, Any]]:
        ...


class SimpleFilter(Filter):
    def apply(self, users, criteria, *, parallel: bool = False):
        res = []
        for u in users:
            ok = True
            for k, v in criteria.items():
                val = u.get(k)
                if val is None:
                    ok = False
                    break
                if isinstance(v, str) and isinstance(val, str):
                    if v.lower() not in val.lower():
                        ok = False
                        break
                else:
                    if val != v:
                        ok = False
                        break
            if ok:
                res.append(u)
        return res
