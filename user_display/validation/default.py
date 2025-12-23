"""
Default validators for user display data.
"""

from typing import Any, Dict, Tuple, Optional
from .base import FieldValidator


class StringValidator(FieldValidator):
    """Validate string fields."""
    
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Check if value is a string."""
        if not isinstance(value, str):
            return False, f"{self.field_name} must be a string, got {type(value).__name__}"
        return True, None
    
    def _recover_value(self, value: Any) -> Any:
        """Convert to string."""
        return str(value) if value is not None else ""
    
    def _get_default(self) -> Any:
        """Return default empty string."""
        return ""


class IntValidator(FieldValidator):
    """Validate integer fields."""
    
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Check if value is an integer."""
        if not isinstance(value, int) or isinstance(value, bool):
            return False, f"{self.field_name} must be an integer, got {type(value).__name__}"
        return True, None
    
    def _recover_value(self, value: Any) -> Any:
        """Convert to integer."""
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    def _get_default(self) -> Any:
        """Return default 0."""
        return 0


class EmailValidator(FieldValidator):
    """Validate email fields."""
    
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Check if value looks like email."""
        if not isinstance(value, str):
            return False, f"{self.field_name} must be string"
        if '@' not in value:
            return False, f"{self.field_name} must contain @"
        return True, None
    
    def _recover_value(self, value: Any) -> Any:
        """Convert to string and ensure @ exists."""
        s = str(value).strip() if value else ""
        if '@' not in s:
            s = f"{s}@example.com"
        return s
    
    def _get_default(self) -> Any:
        """Return default email."""
        return "user@example.com"


class DateValidator(FieldValidator):
    """Validate date fields (YYYY-MM-DD format)."""
    
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Check if value is valid date format."""
        if not isinstance(value, str):
            return False, f"{self.field_name} must be string"
        parts = value.split('-')
        if len(parts) != 3:
            return False, f"{self.field_name} must be YYYY-MM-DD format"
        try:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                return False, f"{self.field_name} has invalid date values"
        except (ValueError, TypeError):
            return False, f"{self.field_name} has non-numeric date parts"
        return True, None
    
    def _recover_value(self, value: Any) -> Any:
        """Attempt to recover date value."""
        if isinstance(value, str) and len(value) >= 10:
            # Try to extract YYYY-MM-DD from string
            for i in range(len(value) - 9):
                potential = value[i:i+10]
                parts = potential.split('-')
                if len(parts) == 3:
                    try:
                        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                        if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                            return potential
                    except ValueError:
                        continue
        return "2000-01-01"
    
    def _get_default(self) -> Any:
        """Return default date."""
        return "2000-01-01"


class EnumValidator(FieldValidator):
    """Validate enum fields."""
    
    def __init__(self, field_name: str, allowed_values: list, required: bool = False):
        super().__init__(field_name, required)
        self.allowed_values = allowed_values
    
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Check if value is in allowed list."""
        if value not in self.allowed_values:
            return False, f"{self.field_name} must be one of {self.allowed_values}"
        return True, None
    
    def _recover_value(self, value: Any) -> Any:
        """Use first allowed value or original."""
        if value in self.allowed_values:
            return value
        return self.allowed_values[0] if self.allowed_values else value
    
    def _get_default(self) -> Any:
        """Return first allowed value."""
        return self.allowed_values[0] if self.allowed_values else None


def create_user_validator() -> 'Validator':
    """Create a validator for user records."""
    from .base import CompositeValidator
    
    validators = [
        IntValidator('id', required=True),
        StringValidator('name', required=True),
        EmailValidator('email', required=True),
        EnumValidator('role', ['Admin', 'User', 'Mod'], required=False),
        EnumValidator('status', ['Active', 'Inactive'], required=False),
        DateValidator('join_date', required=False),
        DateValidator('last_login', required=False),
    ]
    
    return CompositeValidator(validators)
