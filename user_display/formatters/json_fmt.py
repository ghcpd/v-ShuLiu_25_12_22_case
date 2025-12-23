"""JSON formatter (fast, single-pass, optional field selection)."""
from __future__ import annotations
from .base import Formatter, registry
import json
from typing import Iterable, List, Dict, Any


@Formatter.register
class JsonFormatter(Formatter):
    name = "json"

    def format_many(self, users: Iterable[Dict[str, Any]], fields: List[str] | None = None) -> str:
        if fields:
            def project(u):
                return {k: u.get(k) for k in fields}
            data = (project(u) for u in users)
        else:
            data = users
        return json.dumps(list(data), ensure_ascii=False)
