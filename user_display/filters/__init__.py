from .regex_filter import RegexFilter
from .composite_filter import CompositeFilter

_REGISTRY = {
    "regex": RegexFilter,
    "composite": CompositeFilter,
}

class FilterRegistry:
    @staticmethod
    def create(name, *args, **kwargs):
        cls = _REGISTRY.get(name)
        if cls is None:
            raise ValueError(f"Unknown filter: {name}")
        return cls(*args, **kwargs)

    @staticmethod
    def register(name, cls):
        _REGISTRY[name] = cls
