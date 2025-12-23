"""
Structured logging utilities for the user display system.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
from .config import config

class StructuredLogger:
    """Logger that outputs structured JSON logs."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.get('log_level', 'INFO')))

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add JSON handler
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)

    def log(self, level: str, message: str, **kwargs):
        """Log a structured message."""
        extra = {'extra_data': kwargs}
        getattr(self.logger, level.lower())(message, extra=extra)

    def debug(self, message: str, **kwargs):
        self.log('DEBUG', message, **kwargs)

    def info(self, message: str, **kwargs):
        self.log('INFO', message, **kwargs)

    def warning(self, message: str, **kwargs):
        self.log('WARNING', message, **kwargs)

    def error(self, message: str, **kwargs):
        self.log('ERROR', message, **kwargs)

    def critical(self, message: str, **kwargs):
        self.log('CRITICAL', message, **kwargs)

class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)

        return json.dumps(log_entry)

# Global logger instance
logger = StructuredLogger('user_display')