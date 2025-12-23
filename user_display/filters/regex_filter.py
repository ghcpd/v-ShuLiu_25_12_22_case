"""
Regex-based filter.
"""

import re
from typing import Dict, Any, List
from .base import Filter


class RegexFilter(Filter):
    """Filter users using regex patterns."""
    
    def __init__(self, patterns: Dict[str, str]):
        """
        Initialize regex filter.
        
        Args:
            patterns: Dict of field_name -> regex_pattern
        """
        self.patterns = {}
        for field, pattern in patterns.items():
            try:
                self.patterns[field] = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex for field {field}: {e}")
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all regex patterns."""
        for field, regex in self.patterns.items():
            value = user.get(field)
            if value is None:
                return False
            
            if not regex.search(str(value)):
                return False
        
        return True


class PrefixFilter(Filter):
    """Filter users by field value prefixes."""
    
    def __init__(self, prefixes: Dict[str, str], case_sensitive: bool = False):
        """
        Initialize prefix filter.
        
        Args:
            prefixes: Dict of field_name -> prefix
            case_sensitive: Whether comparison is case-sensitive
        """
        self.prefixes = prefixes
        self.case_sensitive = case_sensitive
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all prefixes."""
        for field, prefix in self.prefixes.items():
            value = user.get(field)
            if value is None:
                return False
            
            value_str = str(value)
            prefix_str = str(prefix)
            
            if self.case_sensitive:
                if not value_str.startswith(prefix_str):
                    return False
            else:
                if not value_str.lower().startswith(prefix_str.lower()):
                    return False
        
        return True


class SuffixFilter(Filter):
    """Filter users by field value suffixes."""
    
    def __init__(self, suffixes: Dict[str, str], case_sensitive: bool = False):
        """
        Initialize suffix filter.
        
        Args:
            suffixes: Dict of field_name -> suffix
            case_sensitive: Whether comparison is case-sensitive
        """
        self.suffixes = suffixes
        self.case_sensitive = case_sensitive
    
    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all suffixes."""
        for field, suffix in self.suffixes.items():
            value = user.get(field)
            if value is None:
                return False
            
            value_str = str(value)
            suffix_str = str(suffix)
            
            if self.case_sensitive:
                if not value_str.endswith(suffix_str):
                    return False
            else:
                if not value_str.lower().endswith(suffix_str.lower()):
                    return False
        
        return True
