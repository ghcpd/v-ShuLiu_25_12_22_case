"""
Plugin system for dynamic registration of filters, formatters, and validators.
"""

from typing import Dict, Type, Any, Callable
from collections import defaultdict
from .logging_utils import logger

class PluginRegistry:
    """Registry for plugins."""

    def __init__(self):
        self._filters: Dict[str, Type] = {}
        self._formatters: Dict[str, Type] = {}
        self._validators: Dict[str, Type] = {}
        self._hooks: Dict[str, list] = defaultdict(list)

    def register_filter(self, name: str, filter_class: Type):
        """Register a filter class."""
        self._filters[name] = filter_class
        logger.info(f"Registered filter: {name}")

    def get_filter(self, name: str) -> Type:
        """Get a registered filter class."""
        return self._filters.get(name)

    def list_filters(self) -> list:
        """List all registered filter names."""
        return list(self._filters.keys())

    def register_formatter(self, name: str, formatter_class: Type):
        """Register a formatter class."""
        self._formatters[name] = formatter_class
        logger.info(f"Registered formatter: {name}")

    def get_formatter(self, name: str) -> Type:
        """Get a registered formatter class."""
        return self._formatters.get(name)

    def list_formatters(self) -> list:
        """List all registered formatter names."""
        return list(self._formatters.keys())

    def register_validator(self, name: str, validator_class: Type):
        """Register a validator class."""
        self._validators[name] = validator_class
        logger.info(f"Registered validator: {name}")

    def get_validator(self, name: str) -> Type:
        """Get a registered validator class."""
        return self._validators.get(name)

    def list_validators(self) -> list:
        """List all registered validator names."""
        return list(self._validators.keys())

    def add_hook(self, hook_name: str, callback: Callable):
        """Add a hook callback."""
        self._hooks[hook_name].append(callback)

    def call_hooks(self, hook_name: str, *args, **kwargs):
        """Call all hooks for a given name."""
        for callback in self._hooks[hook_name]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Hook {hook_name} failed", error=str(e))

# Global plugin registry
registry = PluginRegistry()