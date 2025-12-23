"""Compact human-readable formatter — efficient, single-pass, safe for missing fields."""
from __future__ import annotations
from typing import Dict, Iterable
from .base import Formatter, _safe_str
from io import StringIO


class CompactFormatter(Formatter):
    def format(self, users: Iterable[Dict], *, show_all: bool = True) -> str:
        buf = StringIO()
        cnt = 0
        write = buf.write
        for u in users:
            write(
                "ID=" + _safe_str(u.get("id"))
                + " | NAME="
                + _safe_str(u.get("name"))
                + " | EMAIL="
                + _safe_str(u.get("email"))
                + " | ROLE="
                + _safe_str(u.get("role"))
                + " | STATUS="
                + _safe_str(u.get("status"))
                + " | JOIN_DATE="
                + _safe_str(u.get("join_date"))
                + " | LAST_LOGIN="
                + _safe_str(u.get("last_login"))
                + "\n"
            )
            cnt += 1
        if show_all:
            write(f"PROCESSED={cnt}\n")
        return buf.getvalue()
