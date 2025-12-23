"""Filter base class and registry."""
from typing import Callable, Dict, Any

registry: Dict[str, Callable] = {}

class BaseFilter:
    name = "base"

    def matches(self, user: Dict[str, Any]) -> bool:
        raise NotImplementedError

    @classmethod
    def register(cls, impl):
        registry[impl.name] = impl
        return impl
