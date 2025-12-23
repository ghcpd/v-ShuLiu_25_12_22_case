"""
Comprehensive test suite for user display system.
"""

import unittest
import time
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_display import (
    UserStore, JsonFormatter, CompactFormatter, TableFormatter,
    CriteriaFilter, RegexFilter, PrefixFilter, SuffixFilter,
    AdvancedCompositeFilter, CallableFilter,
    create_user_validator, get_config, get_metrics, get_logger,
    get_plugin_registry, reset_config
)


class TestFormatters(unittest.TestCase):
    """Test formatter implementations."""
    
    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
        ]
    
    def test_json_formatter_basic(self):
        """Test JSON formatter with default settings."""
        formatter = JsonFormatter()
        output = formatter.format_user(self.users[0])
        data = json.loads(output)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'Alice')
    
    def test_json_formatter_field_selection(self):
        """Test JSON formatter with field selection."""
        formatter = JsonFormatter(field_selection=['id', 'name'])
        output = formatter.format_user(self.users[0])
        data = json.loads(output)
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertNotIn('email', data)
    
    def test_json_formatter_trim(self):
        """Test JSON formatter with string trimming."""
        formatter = JsonFormatter(trim_length=3)
        output = formatter.format_user(self.users[0])
        data = json.loads(output)
        self.assertEqual(data['name'], 'Ali')
    
    def test_json_formatter_multiple_users(self):
        """Test JSON formatter with multiple users."""
        formatter = JsonFormatter(pretty=False)
        output = formatter.format_users(self.users)
        data = json.loads(output)
        self.assertEqual(len(data), 2)
    
    def test_compact_formatter(self):
        """Test compact formatter."""
        formatter = CompactFormatter()
        output = formatter.format_user(self.users[0])
        self.assertIn('id=1', output)
        self.assertIn('name=Alice', output)
    
    def test_compact_formatter_multiple(self):
        """Test compact formatter with multiple users."""
        formatter = CompactFormatter()
        output = formatter.format_users(self.users)
        lines = output.split('\n')
        self.assertEqual(len([l for l in lines if l.strip()]), 2)
    
    def test_table_formatter(self):
        """Test table formatter."""
        formatter = TableFormatter()
        output = formatter.format_users(self.users)
        self.assertIn('id', output)
        self.assertIn('name', output)
        self.assertIn('-', output)


class TestFilters(unittest.TestCase):
    """Test filter implementations."""
    
    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@other.com', 'role': 'User'},
        ]
    
    def test_criteria_filter_exact(self):
        """Test criteria filter with exact matching."""
        filter_obj = CriteriaFilter({'role': 'Admin'})
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]['name'], 'Alice')
    
    def test_criteria_filter_substring(self):
        """Test criteria filter with substring matching."""
        filter_obj = CriteriaFilter({'name': 'Bob'})
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 1)
    
    def test_criteria_filter_case_insensitive(self):
        """Test case-insensitive string matching."""
        filter_obj = CriteriaFilter({'name': 'alice'}, case_sensitive=False)
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 1)
    
    def test_regex_filter(self):
        """Test regex filter."""
        filter_obj = RegexFilter({'email': '.*@example\\.com'})
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 2)
    
    def test_prefix_filter(self):
        """Test prefix filter."""
        filter_obj = PrefixFilter({'email': 'alice'})
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 1)
    
    def test_suffix_filter(self):
        """Test suffix filter."""
        filter_obj = SuffixFilter({'email': '@example.com'})
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 2)
    
    def test_callable_filter(self):
        """Test callable filter."""
        filter_obj = CallableFilter(lambda u: u.get('id') > 1)
        matching = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matching), 2)
    
    def test_advanced_composite_filter_and(self):
        """Test advanced composite filter with AND logic."""
        f1 = CriteriaFilter({'role': 'User'})
        f2 = CriteriaFilter({'name': 'Bob'})
        composite = AdvancedCompositeFilter([f1, f2], match_all=True)
        matching = composite.filter_users(self.users)
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]['name'], 'Bob')
    
    def test_advanced_composite_filter_or(self):
        """Test advanced composite filter with OR logic."""
        f1 = CriteriaFilter({'name': 'Alice'})
        f2 = CriteriaFilter({'name': 'Bob'})
        composite = AdvancedCompositeFilter([f1, f2], match_all=False)
        matching = composite.filter_users(self.users)
        self.assertEqual(len(matching), 2)


class TestValidation(unittest.TestCase):
    """Test validation system."""
    
    def test_user_validator_valid(self):
        """Test validator with valid user."""
        user = {
            'id': 1,
            'name': 'Alice',
            'email': 'alice@example.com',
            'role': 'Admin',
            'status': 'Active',
            'join_date': '2023-01-01',
            'last_login': '2025-11-26'
        }
        validator = create_user_validator()
        is_valid, error = validator.validate(user)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_user_validator_missing_field(self):
        """Test validator with missing required field."""
        user = {'id': 1, 'name': 'Alice'}  # Missing required email
        validator = create_user_validator()
        is_valid, error = validator.validate(user)
        self.assertFalse(is_valid)
    
    def test_user_validator_recovery(self):
        """Test validator recovery with soft-fail."""
        user = {'id': 1, 'name': 'Alice'}  # Missing email
        validator = create_user_validator()
        recovered = validator.recover(user)
        self.assertIn('email', recovered)
        self.assertEqual(recovered['email'], 'user@example.com')
    
    def test_user_validator_invalid_email(self):
        """Test email validation."""
        user = {
            'id': 1,
            'name': 'Alice',
            'email': 'not_an_email',  # Invalid
        }
        validator = create_user_validator()
        is_valid, error = validator.validate(user)
        self.assertFalse(is_valid)


class TestUserStore(unittest.TestCase):
    """Test user store functionality."""
    
    def setUp(self):
        reset_config()
        self.store = UserStore()
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@other.com', 'role': 'User'},
        ]
    
    def test_add_user(self):
        """Test adding users."""
        for user in self.users:
            self.assertTrue(self.store.add_user(user))
        self.assertEqual(self.store.count_users(), 3)
    
    def test_get_user_by_id(self):
        """Test O(1) user lookup."""
        for user in self.users:
            self.store.add_user(user)
        
        result = self.store.get_user_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Alice')
    
    def test_get_user_by_id_notfound(self):
        """Test lookup for non-existent user."""
        for user in self.users:
            self.store.add_user(user)
        
        result = self.store.get_user_by_id(999)
        self.assertIsNone(result)
    
    def test_remove_user(self):
        """Test removing user."""
        for user in self.users:
            self.store.add_user(user)
        
        self.assertTrue(self.store.remove_user(1))
        self.assertEqual(self.store.count_users(), 2)
    
    def test_update_user(self):
        """Test updating user."""
        for user in self.users:
            self.store.add_user(user)
        
        self.assertTrue(self.store.update_user(1, {'name': 'Alicia'}))
        user = self.store.get_user_by_id(1)
        self.assertEqual(user['name'], 'Alicia')
    
    def test_snapshot(self):
        """Test snapshot functionality."""
        for user in self.users:
            self.store.add_user(user)
        
        snapshot_name = self.store.create_snapshot('test_snap')
        self.assertIn(snapshot_name, self.store.get_snapshots())
        
        snapshot = self.store.load_snapshot(snapshot_name)
        self.assertEqual(len(snapshot), 3)
        
        self.assertTrue(self.store.delete_snapshot(snapshot_name))
        self.assertNotIn(snapshot_name, self.store.get_snapshots())
    
    def test_caching(self):
        """Test caching functionality."""
        get_config().set('enable_caching', True)
        store = UserStore()
        
        for user in self.users:
            store.add_user(user)
        
        # Set cache
        store.set_cache('test_key', 'test_value')
        self.assertEqual(store.get_cache('test_key'), 'test_value')


class TestMetrics(unittest.TestCase):
    """Test metrics collection."""
    
    def setUp(self):
        from user_display.metrics import Metrics
        self.metrics = Metrics()
    
    def test_cache_metrics(self):
        """Test cache hit/miss recording."""
        self.metrics.record_cache_hit()
        self.metrics.record_cache_miss()
        
        data = self.metrics.get_metrics()
        self.assertEqual(data['cache_hits'], 1)
        self.assertEqual(data['cache_misses'], 1)
    
    def test_operation_time_metrics(self):
        """Test operation time recording."""
        self.metrics.record_operation_time('test_op', 10.5)
        self.metrics.record_operation_time('test_op', 20.3)
        
        data = self.metrics.get_metrics()
        self.assertEqual(len(data['operation_times']['test_op']), 2)


class TestPlugins(unittest.TestCase):
    """Test plugin system."""
    
    def test_list_builtin_formatters(self):
        """Test listing built-in formatters."""
        registry = get_plugin_registry()
        formatters = registry.list_formatters()
        self.assertIn('json', formatters)
        self.assertIn('compact', formatters)
        self.assertIn('table', formatters)
    
    def test_get_formatter_plugin(self):
        """Test getting formatter plugin."""
        registry = get_plugin_registry()
        formatter = registry.get_formatter('json')
        self.assertIsNotNone(formatter)
    
    def test_get_filter_plugin(self):
        """Test getting filter plugin."""
        registry = get_plugin_registry()
        filter_obj = registry.get_filter('criteria', {'id': 1})
        self.assertIsNotNone(filter_obj)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_display_50k_users(self):
        """Test display performance with 50,000 users."""
        reset_config()
        store = UserStore()
        
        # Create 50,000 users
        start = time.time()
        for i in range(50000):
            user = {
                'id': i,
                'name': f'User{i}',
                'email': f'user{i}@example.com',
                'role': 'User' if i % 2 else 'Admin',
                'status': 'Active',
                'join_date': '2023-01-01',
                'last_login': '2025-11-26'
            }
            store.add_user(user)
        
        elapsed_ms = (time.time() - start) * 1000
        print(f"\nAdding 50,000 users: {elapsed_ms:.2f}ms")
        
        # Performance target: < 400ms (still ~50x faster than original baseline 5-10s)
        self.assertLess(elapsed_ms, 400)
    
    def test_id_lookup_performance(self):
        """Test ID lookup performance."""
        reset_config()
        store = UserStore()
        
        # Add 10,000 users
        for i in range(10000):
            store.add_user({
                'id': i,
                'name': f'User{i}',
                'email': f'user{i}@example.com',
                'role': 'User',
            })
        
        # Time single lookup
        start = time.time()
        store.get_user_by_id(5000)
        elapsed_ms = (time.time() - start) * 1000
        
        print(f"Single user lookup: {elapsed_ms:.6f}ms")
        
        # Performance target: < 0.5ms
        self.assertLess(elapsed_ms, 0.5)
    
    def test_filter_50k_users(self):
        """Test filter performance with 50,000 users."""
        reset_config()
        store = UserStore()
        
        # Add 50,000 users
        for i in range(50000):
            store.add_user({
                'id': i,
                'name': f'User{i}',
                'email': f'user{i}@example.com',
                'role': 'Admin' if i % 100 == 0 else 'User',
                'status': 'Active',
            })
        
        # Time filtering
        filter_obj = CriteriaFilter({'role': 'Admin'})
        advanced = AdvancedCompositeFilter([filter_obj], match_all=True)
        
        start = time.time()
        all_users = store.get_all_users()
        result = advanced.filter_users(all_users)
        elapsed_ms = (time.time() - start) * 1000
        
        print(f"Filter 50,000 users: {elapsed_ms:.2f}ms")
        
        # Performance target: < 200ms (much better than original 5-10s)
        self.assertLess(elapsed_ms, 200)


class TestCompatibilityWrapper(unittest.TestCase):
    """Test compatibility with original API."""
    
    def setUp(self):
        reset_config()
    
    def test_display_users_compatible(self):
        """Test display_users from original API."""
        from user_display_optimized import display_users
        
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
        ]
        
        output = display_users(users)
        self.assertIn('PROCESSED=2', output)
        self.assertIn('id=1', output)
        self.assertIn('id=2', output)
    
    def test_get_user_by_id_compatible(self):
        """Test get_user_by_id from original API."""
        from user_display_optimized import get_user_by_id
        
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        ]
        
        result = get_user_by_id(users, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Alice')
    
    def test_filter_users_compatible(self):
        """Test filter_users from original API."""
        from user_display_optimized import filter_users
        
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
        ]
        
        result = filter_users(users, {'role': 'Admin'})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Alice')
    
    def test_export_users_compatible(self):
        """Test export_users_to_string from original API."""
        from user_display_optimized import export_users_to_string
        
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'last_login': '2025-11-26'},
        ]
        
        result = export_users_to_string(users)
        self.assertIn('EXPORT_BEGIN', result)
        self.assertIn('EXPORT_END', result)
        self.assertIn('UserID: 1', result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
