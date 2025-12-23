"""Simple column-aligned table formatter (fast, no external deps)."""
from __future__ import annotations
from typing import Dict, Iterable, List
from .base import Formatter, _safe_str


class TableFormatter(Formatter):
    def __init__(self, columns: List[str] = None):
        self.columns = columns or ["id", "name", "email", "role", "status", "last_login"]

    def format(self, users: Iterable[Dict], *, show_all: bool = True) -> str:
        rows = []
        widths = [len(c) for c in self.columns]
        for u in users:
            row = [(_safe_str(u.get(c)) or "") for c in self.columns]
            for i, v in enumerate(row):
                widths[i] = max(widths[i], len(v))
            rows.append(row)
        # header
        hdr = " | ".join(c.ljust(widths[i]) for i, c in enumerate(self.columns))
        sep = "-+-".join("-" * w for w in widths)
        lines = [hdr, sep]
        for r in rows:
            lines.append(" | ".join(r[i].ljust(widths[i]) for i in range(len(r))))
        if show_all:
            lines.append(f"PROCESSED={len(rows)}")
        return "\n".join(lines) + "\n"
