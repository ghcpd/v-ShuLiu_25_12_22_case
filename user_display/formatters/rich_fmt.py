"""Rich pretty-print table formatter using the `rich` library."""
from __future__ import annotations
from .base import Formatter, registry
from typing import Iterable, List, Dict, Any
from io import StringIO

@Formatter.register
class RichFormatter(Formatter):
    name = "rich"

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        # import lazily so formatter works even if `rich` was installed after module import
        try:
            from rich.table import Table
            from rich.console import Console
        except Exception:
            raise RuntimeError("rich is not available")
        users_list = list(users)
        if fields is None:
            fields = ["id", "name", "email"]
        table = Table(show_header=True, header_style="bold magenta")
        for f in fields:
            table.add_column(f)
        for u in users_list:
            table.add_row(*(str(u.get(f, "")) for f in fields))
        buf = StringIO()
        console = Console(file=buf, record=False, width=120)
        console.print(table)
        return buf.getvalue().rstrip("\n")
