"""
Regex-based filter implementation.
"""

import re
from typing import Dict, Any
from .base import Filter

class RegexFilter(Filter):
    """Filter using regex patterns."""

    def __init__(self, field: str, pattern: str, case_sensitive: bool = False):
        self.field = field
        self.pattern = pattern
        self.case_sensitive = case_sensitive
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            self.regex = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

    def matches(self, user: Dict[str, Any]) -> bool:
        value = user.get(self.field, '')
        if not isinstance(value, str):
            value = str(value)
        return bool(self.regex.search(value))

    def get_criteria(self) -> Dict[str, Any]:
        return {
            'type': 'regex',
            'field': self.field,
            'pattern': self.pattern,
            'case_sensitive': self.case_sensitive
        }