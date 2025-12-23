"""Formatter base classes and small helpers."""
from __future__ import annotations
from typing import Any, Dict, Iterable, List
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, users: Iterable[Dict[str, Any]], *, show_all: bool = True) -> str:
        ...


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, dict)):
        try:
            import json

            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    return str(v)
