"""
User Display Package - High-performance, modular user management system.
"""

from .store import UserStore
from .index import UserIndex, ShardIndex
from .config import get_config, reset_config, Config
from .logging_utils import get_logger, StructuredLogger
from .metrics import get_metrics, Metrics
from .errors import (
    UserDisplayError,
    ValidationError,
    FilterError,
    FormatterError,
    PluginError,
    CorruptedDataError,
)
from .formatters import (
    Formatter,
    JsonFormatter,
    CompactFormatter,
    TableFormatter,
)
from .filters import (
    Filter,
    CriteriaFilter,
    CompositeFilter,
    CallableFilter,
    RegexFilter,
    PrefixFilter,
    SuffixFilter,
    AdvancedCompositeFilter,
)
from .validation import (
    Validator,
    FieldValidator,
    CompositeValidator,
    create_user_validator,
)
from .plugins import get_plugin_registry, PluginRegistry

__version__ = '1.0.0'

__all__ = [
    # Core
    'UserStore',
    'UserIndex',
    'ShardIndex',
    
    # Configuration
    'Config',
    'get_config',
    'reset_config',
    
    # Logging & Metrics
    'StructuredLogger',
    'get_logger',
    'Metrics',
    'get_metrics',
    
    # Errors
    'UserDisplayError',
    'ValidationError',
    'FilterError',
    'FormatterError',
    'PluginError',
    'CorruptedDataError',
    
    # Formatters
    'Formatter',
    'JsonFormatter',
    'CompactFormatter',
    'TableFormatter',
    
    # Filters
    'Filter',
    'CriteriaFilter',
    'CompositeFilter',
    'CallableFilter',
    'RegexFilter',
    'PrefixFilter',
    'SuffixFilter',
    'AdvancedCompositeFilter',
    
    # Validation
    'Validator',
    'FieldValidator',
    'CompositeValidator',
    'create_user_validator',
    
    # Plugins
    'PluginRegistry',
    'get_plugin_registry',
]
