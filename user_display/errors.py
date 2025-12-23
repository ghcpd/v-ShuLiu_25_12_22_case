"""
Custom exceptions for the user display system.
"""

class UserDisplayError(Exception):
    """Base exception for user display operations."""
    pass

class ValidationError(UserDisplayError):
    """Raised when user data validation fails."""
    pass

class FilterError(UserDisplayError):
    """Raised when filtering operations fail."""
    pass

class FormatterError(UserDisplayError):
    """Raised when formatting operations fail."""
    pass

class StoreError(UserDisplayError):
    """Raised when storage operations fail."""
    pass