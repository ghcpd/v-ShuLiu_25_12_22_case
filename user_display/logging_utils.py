"""
Logging utilities for structured logging and debugging.
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict, List


class StructuredLogger:
    """Structured logging with JSON output capability."""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._logs: List[Dict[str, Any]] = []
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, message: str, **metadata):
        """Log debug message with optional metadata."""
        self.logger.debug(message)
        self._record_log('DEBUG', message, metadata)
    
    def info(self, message: str, **metadata):
        """Log info message with optional metadata."""
        self.logger.info(message)
        self._record_log('INFO', message, metadata)
    
    def warning(self, message: str, **metadata):
        """Log warning message with optional metadata."""
        self.logger.warning(message)
        self._record_log('WARNING', message, metadata)
    
    def error(self, message: str, **metadata):
        """Log error message with optional metadata."""
        self.logger.error(message)
        self._record_log('ERROR', message, metadata)
    
    def _record_log(self, level: str, message: str, metadata: Dict[str, Any]):
        """Record log entry with timestamp and metadata."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'metadata': metadata
        }
        self._logs.append(entry)
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """Return all recorded logs."""
        return self._logs
    
    def clear_logs(self):
        """Clear all recorded logs."""
        self._logs.clear()
    
    def export_logs_json(self) -> str:
        """Export logs as JSON string."""
        return json.dumps(self._logs, indent=2)


# Global logger instance
_global_logger = None


def get_logger(name: str = 'user_display') -> StructuredLogger:
    """Get or create global logger."""
    global _global_logger
    if _global_logger is None:
        _global_logger = StructuredLogger(name)
    return _global_logger
