"""user_display package - public API re-exports and convenience defaults."""
from .store import UserStore, default_store
from .formatters import compact, json_fmt, table
from .formatters.compact import CompactFormatter
from .formatters.json_fmt import JsonFormatter
from .formatters.table import TableFormatter
from .filters import RegexFilter, CompositeFilter
from .validation import DefaultValidator
from .plugins import registry
from .config import Config
from .errors import UserValidationError

__all__ = [
    "UserStore",
    "default_store",
    "compact",
    "json_fmt",
    "table",
    "CompactFormatter",
    "JsonFormatter",
    "TableFormatter",
    "RegexFilter",
    "CompositeFilter",
    "DefaultValidator",
    "registry",
    "Config",
    "UserValidationError",
]
