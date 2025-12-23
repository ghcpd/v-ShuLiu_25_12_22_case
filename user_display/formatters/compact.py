"""Compact, human-friendly one-line-per-user formatter."""
from __future__ import annotations
from .base import Formatter, registry
from typing import Iterable, List, Dict, Any


@Formatter.register
class CompactFormatter(Formatter):
    name = "compact"

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        out = []
        if fields is None:
            for u in users:
                out.append(f"{u.get('id')} | {u.get('name')} | {u.get('email')}")
        else:
            for u in users:
                out.append(" | ".join(str(u.get(f)) for f in fields))
        return "\n".join(out)
