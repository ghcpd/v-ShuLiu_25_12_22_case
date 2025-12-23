"""Plugin registry for filters/formatters/validators."""
from typing import Dict, Callable

plugins: Dict[str, Callable] = {}


def register(name: str, fn: Callable) -> None:
    plugins[name] = fn


def get(name: str):
    return plugins.get(name)
