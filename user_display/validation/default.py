"""
Default validator implementation.
"""

from typing import Dict, Any, List
from datetime import datetime
from .base import Validator
from ..errors import ValidationError
from ..logging_utils import logger

class DefaultValidator(Validator):
    """Default validator with fallback recovery."""

    def get_required_fields(self) -> List[str]:
        return ['id', 'name', 'email']

    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user data with recovery."""
        validated = user.copy()

        # Validate and repair ID
        if 'id' not in validated or validated['id'] is None:
            raise ValidationError("Missing required field: id")
        try:
            validated['id'] = int(validated['id'])
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid id format: {validated['id']}")

        # Validate and repair name
        if 'name' not in validated or not validated['name']:
            logger.warning("Missing name field, using default", user_id=validated['id'])
            validated['name'] = f"User{validated['id']}"

        # Validate and repair email
        if 'email' not in validated or not validated['email']:
            logger.warning("Missing email field, generating default", user_id=validated['id'])
            validated['email'] = f"user{validated['id']}@example.com"

        # Validate role
        if 'role' not in validated:
            validated['role'] = 'User'

        # Validate status
        if 'status' not in validated:
            validated['status'] = 'Active'

        # Validate dates
        for date_field in ['join_date', 'last_login']:
            if date_field in validated:
                try:
                    datetime.strptime(validated[date_field], '%Y-%m-%d')
                except (ValueError, TypeError):
                    logger.warning(f"Invalid {date_field} format, using default", user_id=validated['id'])
                    validated[date_field] = '2023-01-01'

        return validated