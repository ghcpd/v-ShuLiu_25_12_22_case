from .base import BaseFormatter
from io import StringIO

class CompactFormatter(BaseFormatter):
    def format(self, users, fields=None):
        buf = StringIO()
        for u in users:
            parts = []
            for f in (fields or ["id", "name", "email"]):
                parts.append(f"{f.upper()}={u.get(f, '')}")
            buf.write(" | ".join(parts) + "\n")
        return buf.getvalue()
