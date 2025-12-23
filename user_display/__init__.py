"""
User Display System - High-performance, modular user management.
"""

from .store import UserStore
from .index import UserIndex
from .formatters import CompactFormatter, JSONFormatter, TableFormatter
from .filters import RegexFilter, CompositeFilter
from .validation import DefaultValidator
from .config import config
from .logging_utils import logger
from .metrics import metrics
from .plugins import registry
from .errors import UserDisplayError

__version__ = "1.0.0"

__all__ = [
    'UserStore',
    'UserIndex',
    'CompactFormatter',
    'JSONFormatter',
    'TableFormatter',
    'RegexFilter',
    'CompositeFilter',
    'DefaultValidator',
    'config',
    'logger',
    'metrics',
    'registry',
    'UserDisplayError',
]