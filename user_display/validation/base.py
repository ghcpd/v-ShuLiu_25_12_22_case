"""Validator base class."""
from typing import Dict, Any


class BaseValidator:
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
