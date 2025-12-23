"""
Error definitions for the user display system.
"""


class UserDisplayError(Exception):
    """Base exception for user display system."""
    pass


class ValidationError(UserDisplayError):
    """Raised when data validation fails."""
    pass


class FilterError(UserDisplayError):
    """Raised when filter operation fails."""
    pass


class FormatterError(UserDisplayError):
    """Raised when formatting operation fails."""
    pass


class PluginError(UserDisplayError):
    """Raised when plugin registration or loading fails."""
    pass


class CorruptedDataError(UserDisplayError):
    """Raised when data corruption is detected."""
    pass
