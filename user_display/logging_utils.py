"""Structured, simple logging helpers used across the package."""
import logging
import json

_logger = logging.getLogger("user_display")
_logger.setLevel(logging.DEBUG)
_stream_handler = logging.StreamHandler()
_formatter = logging.Formatter('%(message)s')
_stream_handler.setFormatter(_formatter)
if not _logger.handlers:
    _logger.addHandler(_stream_handler)

_file_handler = None


def enable_file_logging(path: str) -> None:
    """Enable writing structured JSON logs to the given file path."""
    global _file_handler
    if _file_handler is not None:
        _logger.removeHandler(_file_handler)
        _file_handler.close()
    _file_handler = logging.FileHandler(path, encoding="utf-8")
    _file_handler.setFormatter(_formatter)
    _logger.addHandler(_file_handler)


def log_struct(level: str, msg: str, **kwargs) -> None:
    payload = {"message": msg, "level": level, **kwargs}
    # message is already JSON string; logger writes the string to all handlers
    _logger.log(getattr(logging, level.upper(), logging.INFO), json.dumps(payload))


def debug(msg: str, **kwargs) -> None:
    log_struct("debug", msg, **kwargs)


def info(msg: str, **kwargs) -> None:
    log_struct("info", msg, **kwargs)


def warning(msg: str, **kwargs) -> None:
    log_struct("warning", msg, **kwargs)


def error(msg: str, **kwargs) -> None:
    log_struct("error", msg, **kwargs)
