"""
Validation base module.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Optional


class Validator(ABC):
    """Base validator class."""
    
    @abstractmethod
    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate data.
        Returns (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def recover(self, data: Any) -> Any:
        """Attempt to recover/fix invalid data."""
        pass


class FieldValidator(Validator):
    """Base class for field-level validators."""
    
    def __init__(self, field_name: str, required: bool = False):
        self.field_name = field_name
        self.required = required
    
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate field in dictionary."""
        if self.field_name not in data:
            if self.required:
                return False, f"Required field missing: {self.field_name}"
            return True, None
        
        return self._validate_value(data[self.field_name])
    
    @abstractmethod
    def _validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate the actual value."""
        pass
    
    def recover(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover invalid data."""
        if self.field_name not in data:
            data[self.field_name] = self._get_default()
        else:
            data[self.field_name] = self._recover_value(data[self.field_name])
        return data
    
    @abstractmethod
    def _recover_value(self, value: Any) -> Any:
        """Recover/fix invalid value."""
        pass
    
    @abstractmethod
    def _get_default(self) -> Any:
        """Get default value for missing field."""
        pass


class CompositeValidator(Validator):
    """Composite validator combining multiple validators."""
    
    def __init__(self, validators: list):
        self.validators = validators
    
    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        """Validate using all validators."""
        for validator in self.validators:
            is_valid, error_msg = validator.validate(data)
            if not is_valid:
                return False, error_msg
        return True, None
    
    def recover(self, data: Any) -> Any:
        """Recover using all validators."""
        for validator in self.validators:
            data = validator.recover(data)
        return data
