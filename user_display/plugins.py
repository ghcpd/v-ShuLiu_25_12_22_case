"""Plugin registration for filters and formatters."""
from .formatters import register_formatter
from .filters import FilterRegistry


def register_formatter_plugin(name, cls):
    register_formatter(name, cls)


def register_filter_plugin(name, cls):
    FilterRegistry.register(name, cls)
