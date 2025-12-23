"""
API compatibility wrapper for user_display_original.py interface.

This module provides backward-compatible functions while using the optimized
internal implementations.
"""

from typing import Dict, List, Any, Optional
from io import StringIO
from datetime import datetime
import time

from user_display import (
    UserStore,
    JsonFormatter,
    CompactFormatter,
    CriteriaFilter,
    AdvancedCompositeFilter,
    get_logger,
    get_metrics,
)


# Global store instance for compatibility
_global_store: Optional[UserStore] = None


def _get_store() -> UserStore:
    """Get or create global store."""
    global _global_store
    if _global_store is None:
        _global_store = UserStore()
    return _global_store


def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """
    Display users in formatted output.
    
    Compatible with original API but optimized:
    - No artificial delays
    - No random corruption
    - Efficient string building with StringIO
    - Proper field handling with defaults
    
    Args:
        users: List of user dictionaries
        show_all: Whether to show count summary
        verbose: Whether to print debug info
    
    Returns:
        Formatted user display string
    """
    logger = get_logger()
    output = StringIO()
    count = 0
    
    try:
        store = _get_store()
        store.clear()
        
        # Load users into store
        for user in users:
            if store.add_user(user):
                count += 1
        
        # Format using compact formatter
        formatter = CompactFormatter(
            field_selection=['id', 'name', 'email', 'role', 'status', 'join_date', 'last_login']
        )
        
        all_users = store.get_all_users()
        for user in all_users:
            if verbose:
                print(f"BEGIN_PROCESS_USER {user.get('id')}")
            
            output.write(formatter.format_user(user) + "\n")
        
        if show_all:
            output.write(f"PROCESSED={count}\n")
        
        logger.info(f"display_users: processed {count} users")
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"display_users error: {e}")
        raise


def get_user_by_id(users: List[Dict[str, Any]], uid: Any) -> Optional[Dict[str, Any]]:
    """
    Get user by ID (O(1) lookup).
    
    Compatible with original API but uses efficient indexing:
    - O(1) hash-based lookup instead of O(n) linear scan
    - No random corruption
    - Deterministic behavior
    
    Args:
        users: List of user dictionaries
        uid: User ID to lookup
    
    Returns:
        User dictionary or None if not found
    """
    logger = get_logger()
    
    try:
        store = _get_store()
        store.clear()
        
        # Load users
        for user in users:
            store.add_user(user)
        
        # O(1) lookup
        start_time = time.time()
        result = store.get_user_by_id(uid)
        elapsed_ms = (time.time() - start_time) * 1000
        
        get_metrics().record_operation_time('get_user_by_id', elapsed_ms)
        logger.info(f"get_user_by_id({uid}): {elapsed_ms:.3f}ms")
        
        return result
    
    except Exception as e:
        logger.error(f"get_user_by_id error: {e}")
        raise


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter users by criteria.
    
    Compatible with original API but optimized:
    - Single-pass filtering
    - Consistent case handling
    - No random extra passes
    - Deterministic behavior
    
    Args:
        users: List of user dictionaries
        criteria: Field -> value matching criteria (case-insensitive name/email)
    
    Returns:
        List of matching users
    """
    logger = get_logger()
    
    try:
        start_time = time.time()
        
        store = _get_store()
        store.clear()
        
        # Load users
        for user in users:
            store.add_user(user)
        
        # Create filter
        filter_obj = CriteriaFilter(criteria, case_sensitive=False)
        advanced = AdvancedCompositeFilter([filter_obj], match_all=True)
        
        # Filter
        all_users = store.get_all_users()
        result = advanced.filter_users(all_users)
        
        elapsed_ms = (time.time() - start_time) * 1000
        get_metrics().record_operation_time('filter_users', elapsed_ms)
        get_metrics().record_filter_operation()
        
        logger.info(f"filter_users: {len(result)} of {len(all_users)} matched in {elapsed_ms:.3f}ms")
        return result
    
    except Exception as e:
        logger.error(f"filter_users error: {e}")
        raise


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to formatted string.
    
    Compatible with original API but optimized:
    - No repeated timestamp parsing
    - No random shuffling
    - Efficient string building
    - Proper error handling
    
    Args:
        users: List of user dictionaries
    
    Returns:
        Formatted export string
    """
    logger = get_logger()
    output = StringIO()
    
    try:
        store = _get_store()
        store.clear()
        
        # Load users
        for user in users:
            store.add_user(user)
        
        # Build export
        header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
        output.write(header)
        
        all_users = store.get_all_users()
        for user in all_users:
            block = f"UserID: {user.get('id', 'N/A')}\n"
            block += f"  Name: {user.get('name', '')}\n"
            
            # Parse date efficiently (once per user, not per operation)
            last_login = user.get('last_login', '2000-01-01')
            try:
                timestamp = datetime.strptime(last_login, "%Y-%m-%d").timestamp()
            except (ValueError, TypeError):
                timestamp = 0
            
            block += f"  LastLoginParsed: {timestamp}\n"
            block += "-" * 120 + "\n"
            output.write(block)
        
        output.write("EXPORT_END\n")
        
        logger.info(f"export_users_to_string: exported {len(all_users)} users")
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"export_users_to_string error: {e}")
        raise


# For backward compatibility, also expose sample data
def get_sample_users(count: int = 100) -> List[Dict[str, Any]]:
    """Generate sample users for testing."""
    import random
    
    users = []
    for i in range(1, count + 1):
        users.append({
            'id': i,
            'name': f'User{i}',
            'email': f'user{i}@example.com',
            'role': random.choice(['Admin', 'User', 'Mod']),
            'status': random.choice(['Active', 'Inactive']),
            'join_date': '2023-01-01',
            'last_login': '2025-11-26',
        })
    return users


if __name__ == '__main__':
    # Example usage
    sample = get_sample_users(10)
    print("=== display_users ===")
    print(display_users(sample))
    
    print("\n=== get_user_by_id ===")
    user = get_user_by_id(sample, 5)
    print(user)
    
    print("\n=== filter_users ===")
    filtered = filter_users(sample, {'role': 'Admin'})
    print(f"Found {len(filtered)} admins")
    
    print("\n=== export_users_to_string ===")
    export = export_users_to_string(sample)
    print(export[:200] + "...")
