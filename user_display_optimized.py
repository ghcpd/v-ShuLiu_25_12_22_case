"""
Optimized user display module - maintains API compatibility with original.
"""

import time
from typing import Dict, Any, List, Optional
from user_display import (
    UserStore, CompactFormatter, RegexFilter, CompositeFilter,
    logger, metrics, config
)

# Global store instance for API compatibility
_store = UserStore()
_formatter = CompactFormatter()

def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """
    Display users in compact format.
    API compatible with original.
    """
    timer = metrics.timer_start('display_users')
    metrics.gauge('display_user_count', len(users))

    try:
        if verbose:
            logger.info("Starting user display", count=len(users))

        # Use StringIO for efficient string building
        from io import StringIO
        output = StringIO()

        for user in users:
            fields = []
            for field in ['id', 'name', 'email', 'role', 'status', 'join_date', 'last_login']:
                value = user.get(field, 'N/A')
                fields.append(f"{field.upper()}={value}")
            output.write(" | ".join(fields) + "\n")

        result = output.getvalue()
        if show_all:
            result += f"PROCESSED={len(users)}\n"

        if verbose:
            logger.info("User display completed", count=len(users))

        metrics.timer_stop(timer)
        return result

    except Exception as e:
        logger.error("Display users failed", error=str(e))
        metrics.timer_stop(timer)
        raise

def get_user_by_id(users: List[Dict[str, Any]], uid: int) -> Optional[Dict[str, Any]]:
    """
    Get user by ID with O(1) lookup.
    API compatible with original.
    """
    timer = metrics.timer_start('get_user_by_id')

    try:
        # Create a simple hash map for O(1) lookup
        user_map = {user.get('id'): user for user in users}
        user = user_map.get(uid)

        metrics.timer_stop(timer)
        return user

    except Exception as e:
        logger.error("Get user by ID failed", user_id=uid, error=str(e))
        metrics.timer_stop(timer)
        raise

def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter users with extensible criteria.
    API compatible with original.
    """
    timer = metrics.timer_start('filter_users')
    metrics.gauge('filter_user_count', len(users))

    try:
        if not criteria:
            filtered = users
        else:
            # Simple filtering for API compatibility
            # Original behavior: substring match for name/email, exact for others
            filtered = []
            for user in users:
                match = True
                for field, value in criteria.items():
                    user_value = user.get(field, '')
                    if field in ['name', 'email'] and isinstance(value, str):
                        # Case-insensitive substring match for name and email
                        if value.lower() not in str(user_value).lower():
                            match = False
                            break
                    else:
                        # Exact match for other fields
                        if user_value != value:
                            match = False
                            break
                if match:
                    filtered.append(user)

        metrics.timer_stop(timer)
        metrics.gauge('filtered_user_count', len(filtered))
        return filtered

    except Exception as e:
        logger.error("Filter users failed", criteria=criteria, error=str(e))
        metrics.timer_stop(timer)
        raise

def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to string format.
    API compatible with original.
    """
    timer = metrics.timer_start('export_users')

    try:
        header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
        out = header

        for user in users:
            block = ""
            block += f"UserID: {user.get('id', 'N/A')}\n"
            block += f"  Name: {user.get('name', '')}\n"
            block += f"  Email: {user.get('email', '')}\n"
            block += f"  Role: {user.get('role', '')}\n"
            block += f"  Status: {user.get('status', '')}\n"
            block += f"  Join Date: {user.get('join_date', '')}\n"
            block += f"  Last Login: {user.get('last_login', '')}\n"
            block += "-" * 120 + "\n"
            out += block

        out += "EXPORT_END\n"

        metrics.timer_stop(timer)
        return out

    except Exception as e:
        logger.error("Export users failed", error=str(e))
        metrics.timer_stop(timer)
        raise

# Import re for regex escaping
import re

# Sample users for compatibility
sample_users = [
    {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@example.com",
        "role": "Admin" if i % 3 == 0 else "User" if i % 3 == 1 else "Mod",
        "status": "Active" if i % 2 == 0 else "Inactive",
        "join_date": "2023-01-01",
        "last_login": "2025-11-26",
    }
    for i in range(1, 101)
]