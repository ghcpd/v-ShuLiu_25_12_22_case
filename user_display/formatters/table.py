"""Simple table formatter optimized for speed (uses single-pass, precomputed widths)."""
from __future__ import annotations
from .base import Formatter, registry
from typing import Iterable, List, Dict, Any
from io import StringIO


@Formatter.register
class TableFormatter(Formatter):
    name = "table"

    def _compute_widths(self, users: Iterable[Dict[str, Any]], fields: List[str]) -> Dict[str, int]:
        widths = {f: len(f) for f in fields}
        for u in users:
            for f in fields:
                widths[f] = max(widths[f], len(str(u.get(f, ""))))
        return widths

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        if fields is None:
            fields = ["id", "name", "email"]
        users_list = list(users)  # need to iterate twice to compute widths
        widths = self._compute_widths(users_list, fields)
        buf = StringIO()
        # header
        header = " | ".join(f.ljust(widths[f]) for f in fields)
        sep = "-+-".join("-" * widths[f] for f in fields)
        buf.write(header)
        buf.write("\n")
        buf.write(sep)
        buf.write("\n")
        for u in users_list:
            row = " | ".join(str(u.get(f, "")).ljust(widths[f]) for f in fields)
            buf.write(row)
            buf.write("\n")
        return buf.getvalue().rstrip("\n")
