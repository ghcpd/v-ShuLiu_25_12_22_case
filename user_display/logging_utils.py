"""Small structured-logging helper used by the package."""
import logging
import json
from typing import Any, Dict


class _JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {"ts": self.formatTime(record), "level": record.levelname, "msg": record.getMessage()}
        extra = getattr(record, "extra", None)
        if extra:
            payload.update(extra)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


_handler = logging.StreamHandler()
_handler.setFormatter(_JSONFormatter())


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(_handler)
        logger.setLevel(logging.INFO)
    return logger
