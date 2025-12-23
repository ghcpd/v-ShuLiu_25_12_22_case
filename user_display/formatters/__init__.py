from .compact import CompactFormatter
from .json_fmt import JSONFormatter
from .table import TableFormatter

_FORMATTERS = {
    "compact": CompactFormatter,
    "json": JSONFormatter,
    "table": TableFormatter,
}

def get_formatter(name):
    cls = _FORMATTERS.get(name)
    if cls is None:
        raise ValueError(f"Unknown formatter: {name}")
    return cls()

def register_formatter(name, cls):
    _FORMATTERS[name] = cls
