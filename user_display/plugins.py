"""
Plugin system for dynamic registration of filters, formatters, and validators.
"""

from typing import Dict, Type, Any, Callable
from .errors import PluginError
from .logging_utils import get_logger


class PluginRegistry:
    """Registry for plugins (filters, formatters, validators)."""
    
    def __init__(self):
        self._filters: Dict[str, Type] = {}
        self._formatters: Dict[str, Type] = {}
        self._validators: Dict[str, Type] = {}
        self._logger = get_logger()
    
    def register_filter(self, name: str, filter_class: Type):
        """Register a custom filter class."""
        self._filters[name] = filter_class
        self._logger.info(f"Filter registered: {name}")
    
    def register_formatter(self, name: str, formatter_class: Type):
        """Register a custom formatter class."""
        self._formatters[name] = formatter_class
        self._logger.info(f"Formatter registered: {name}")
    
    def register_validator(self, name: str, validator_class: Type):
        """Register a custom validator class."""
        self._validators[name] = validator_class
        self._logger.info(f"Validator registered: {name}")
    
    def get_filter(self, name: str, *args, **kwargs) -> Any:
        """Get and instantiate a registered filter."""
        if name not in self._filters:
            raise PluginError(f"Filter not registered: {name}")
        return self._filters[name](*args, **kwargs)
    
    def get_formatter(self, name: str, *args, **kwargs) -> Any:
        """Get and instantiate a registered formatter."""
        if name not in self._formatters:
            raise PluginError(f"Formatter not registered: {name}")
        return self._formatters[name](*args, **kwargs)
    
    def get_validator(self, name: str, *args, **kwargs) -> Any:
        """Get and instantiate a registered validator."""
        if name not in self._validators:
            raise PluginError(f"Validator not registered: {name}")
        return self._validators[name](*args, **kwargs)
    
    def list_filters(self) -> list:
        """List registered filter names."""
        return list(self._filters.keys())
    
    def list_formatters(self) -> list:
        """List registered formatter names."""
        return list(self._formatters.keys())
    
    def list_validators(self) -> list:
        """List registered validator names."""
        return list(self._validators.keys())


# Global plugin registry
_global_registry = None


def get_plugin_registry() -> PluginRegistry:
    """Get or create global plugin registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PluginRegistry()
        # Register built-in plugins
        _register_builtins(_global_registry)
    return _global_registry


def _register_builtins(registry: PluginRegistry):
    """Register built-in plugins."""
    from .filters import (
        CriteriaFilter, CompositeFilter, RegexFilter,
        PrefixFilter, SuffixFilter, AdvancedCompositeFilter
    )
    from .formatters import JsonFormatter, CompactFormatter, TableFormatter
    from .validation import StringValidator, IntValidator, EmailValidator
    
    # Filters
    registry.register_filter('criteria', CriteriaFilter)
    registry.register_filter('composite', CompositeFilter)
    registry.register_filter('regex', RegexFilter)
    registry.register_filter('prefix', PrefixFilter)
    registry.register_filter('suffix', SuffixFilter)
    registry.register_filter('advanced_composite', AdvancedCompositeFilter)
    
    # Formatters
    registry.register_formatter('json', JsonFormatter)
    registry.register_formatter('compact', CompactFormatter)
    registry.register_formatter('table', TableFormatter)
    
    # Validators
    registry.register_validator('string', StringValidator)
    registry.register_validator('int', IntValidator)
    registry.register_validator('email', EmailValidator)
