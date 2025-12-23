"""Small plugin registry for filters/formatters/validators."""
from typing import Any, Dict


class Registry:
    def __init__(self):
        self._by_kind = {"filter": {}, "formatter": {}, "validator": {}}

    def register(self, kind: str, name: str, obj: Any):
        self._by_kind.setdefault(kind, {})[name] = obj

    def get(self, kind: str, name: str):
        return self._by_kind.get(kind, {}).get(name)

    def list(self, kind: str):
        return list(self._by_kind.get(kind, {}).keys())


registry = Registry()
