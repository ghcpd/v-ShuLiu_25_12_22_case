"""JSON formatter with stable ordering and optional field selection."""
from __future__ import annotations
from typing import Dict, Iterable, List, Optional
import json
from .base import Formatter


class JsonFormatter(Formatter):
    def __init__(self, fields: Optional[List[str]] = None):
        self.fields = fields

    def format(self, users: Iterable[Dict], *, show_all: bool = True) -> str:
        out = []
        for u in users:
            if self.fields:
                obj = {k: u.get(k) for k in self.fields}
            else:
                obj = dict(u)
            out.append(obj)
        payload = {"count": len(out), "users": out}
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
