"""Formatter base class and simple registry."""
from __future__ import annotations
from typing import Iterable, List, Dict, Any

registry = {}

class Formatter:
    name = "base"

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        raise NotImplementedError

    @classmethod
    def register(cls, impl):
        registry[impl.name] = impl()
        return impl
