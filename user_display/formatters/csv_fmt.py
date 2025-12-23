"""CSV formatter for user_display."""
from __future__ import annotations
from .base import Formatter, registry
from typing import Iterable, List, Dict, Any
from io import StringIO
import csv


@Formatter.register
class CSVFormatter(Formatter):
    name = "csv"

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        users_list = list(users)
        if fields is None:
            fields = ["id", "name", "email"]
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(fields)
        for u in users_list:
            writer.writerow([u.get(f, "") if u.get(f, "") is not None else "" for f in fields])
        return buf.getvalue().rstrip("\n")
