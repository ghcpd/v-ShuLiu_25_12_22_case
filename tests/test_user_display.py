"""
Tests for the user display system.
"""

import pytest
import time
import json
from user_display_optimized import (
    display_users, get_user_by_id, filter_users, export_users_to_string, sample_users
)
from user_display import (
    UserStore, CompactFormatter, JSONFormatter, TableFormatter,
    RegexFilter, CompositeFilter, DefaultValidator, metrics
)


class TestAPICompatibility:
    """Test API compatibility with original."""

    def test_display_users_basic(self):
        users = sample_users[:5]
        result = display_users(users, show_all=True, verbose=False)
        assert "PROCESSED=5" in result
        assert "ID=" in result

    def test_display_users_verbose(self):
        users = sample_users[:3]
        result = display_users(users, show_all=True, verbose=True)
        assert "PROCESSED=3" in result

    def test_get_user_by_id_exists(self):
        users = sample_users[:10]
        user = get_user_by_id(users, 5)
        assert user is not None
        assert user['id'] == 5
        assert user['name'] == 'User5'

    def test_get_user_by_id_not_exists(self):
        users = sample_users[:10]
        user = get_user_by_id(users, 999)
        assert user is None

    def test_filter_users_name(self):
        users = sample_users[:20]
        criteria = {"name": "User1"}
        filtered = filter_users(users, criteria)
        assert len(filtered) == 11  # User1, User10-User19 (substring match)
        assert all("User1" in u['name'] for u in filtered)

    def test_filter_users_exact(self):
        users = sample_users[:20]
        criteria = {"status": "Active"}
        filtered = filter_users(users, criteria)
        assert all(u['status'] == 'Active' for u in filtered)

    def test_export_users_to_string(self):
        users = sample_users[:3]
        result = export_users_to_string(users)
        assert "EXPORT_BEGIN" in result
        assert "EXPORT_END" in result
        assert "UserID: 1" in result
        assert "UserID: 2" in result
        assert "UserID: 3" in result


class TestFormatters:
    """Test different formatter implementations."""

    def test_compact_formatter(self):
        formatter = CompactFormatter()
        user = {"id": 1, "name": "Test", "email": "test@example.com"}
        result = formatter.format_user(user)
        assert "ID=1" in result
        assert "NAME=Test" in result

    def test_json_formatter(self):
        formatter = JSONFormatter()
        users = [{"id": 1, "name": "Test"}]
        result = formatter.format_users(users)
        parsed = json.loads(result)
        assert parsed['count'] == 1
        assert len(parsed['users']) == 1

    def test_table_formatter(self):
        formatter = TableFormatter()
        user = {"id": 1, "name": "Test"}
        result = formatter.format_user(user)
        assert "Id: 1" in result
        assert "Name: Test" in result


class TestFilters:
    """Test filtering functionality."""

    def test_regex_filter_case_insensitive(self):
        filter_obj = RegexFilter("name", r"user\d+", case_sensitive=False)
        user = {"name": "USER123"}
        assert filter_obj.matches(user)

    def test_regex_filter_case_sensitive(self):
        filter_obj = RegexFilter("name", r"user\d+", case_sensitive=True)
        user = {"name": "USER123"}
        assert not filter_obj.matches(user)

    def test_composite_filter_and(self):
        f1 = RegexFilter("name", r"^User")
        f2 = RegexFilter("status", r"^Active$")
        composite = CompositeFilter([f1, f2], "AND")

        user1 = {"name": "User1", "status": "Active"}
        user2 = {"name": "User1", "status": "Inactive"}

        assert composite.matches(user1)
        assert not composite.matches(user2)

    def test_composite_filter_or(self):
        f1 = RegexFilter("name", r"User1")
        f2 = RegexFilter("name", r"User2")
        composite = CompositeFilter([f1, f2], "OR")

        user1 = {"name": "User1"}
        user2 = {"name": "User2"}
        user3 = {"name": "User3"}

        assert composite.matches(user1)
        assert composite.matches(user2)
        assert not composite.matches(user3)


class TestValidation:
    """Test data validation."""

    def test_default_validator_valid(self):
        validator = DefaultValidator()
        user = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "role": "Admin",
            "status": "Active"
        }
        validated = validator.validate(user)
        assert validated['id'] == 1
        assert validated['name'] == "Test User"

    def test_default_validator_missing_fields(self):
        validator = DefaultValidator()
        user = {"id": 1}  # Missing required fields
        validated = validator.validate(user)
        assert validated['name'] == "User1"  # Default generated
        assert validated['email'] == "user1@example.com"  # Default generated

    def test_default_validator_invalid_id(self):
        validator = DefaultValidator()
        user = {"id": "invalid"}
        with pytest.raises(Exception):  # ValidationError
            validator.validate(user)


class TestStore:
    """Test user store functionality."""

    def test_store_add_get(self):
        store = UserStore()
        user = {"id": 1, "name": "Test"}
        store.add_user(user)
        retrieved = store.get_user(1)
        assert retrieved['name'] == "Test"

    def test_store_snapshot(self):
        store = UserStore()
        store.add_user({"id": 1, "name": "Test"})
        store.create_snapshot("test")
        snapshot = store.get_snapshot("test")
        assert len(snapshot) == 1
        assert snapshot[0]['name'] == "Test"

    def test_store_thread_safety(self):
        import threading

        store = UserStore()
        results = []

        def add_users(start_id, count):
            for i in range(start_id, start_id + count):
                store.add_user({"id": i, "name": f"User{i}"})
                results.append(i)

        threads = []
        for i in range(5):
            t = threading.Thread(target=add_users, args=(i*10, 10))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(store.get_all_users()) == 50
        assert len(results) == 50


class TestPerformance:
    """Performance tests."""

    @pytest.fixture
    def large_user_set(self):
        return [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": "Admin" if i % 3 == 0 else "User",
                "status": "Active" if i % 2 == 0 else "Inactive",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
            for i in range(50000)
        ]

    def test_display_performance(self, large_user_set):
        start = time.time()
        result = display_users(large_user_set, verbose=False)
        duration = time.time() - start
        assert duration < 0.120  # 120ms target
        assert len(result) > 0

    def test_filter_performance(self, large_user_set):
        criteria = {"status": "Active"}
        start = time.time()
        filtered = filter_users(large_user_set, criteria)
        duration = time.time() - start
        assert duration < 0.020  # 20ms target for API compatibility wrapper
        assert len(filtered) > 0

    def test_lookup_performance(self, large_user_set):
        # Pre-populate for lookup test
        start = time.time()
        user = get_user_by_id(large_user_set, 25000)
        duration = time.time() - start
        assert duration < 0.010  # 10ms target for API compatibility wrapper
        assert user is not None
        assert user['id'] == 25000


class TestMetrics:
    """Test metrics collection."""

    def test_metrics_collection(self):
        metrics.reset()
        users = sample_users[:10]

        display_users(users)
        assert metrics.get_stats()['display_user_count'] == 10

        get_user_by_id(users, 5)
        lookup_stats = metrics.get_stats()
        assert 'get_count' in lookup_stats  # Timer count

    def test_metrics_reset(self):
        metrics.increment('test_counter')
        assert metrics.get_stats()['test_counter'] == 1
        metrics.reset()
        assert metrics.get_stats().get('test_counter', 0) == 0


if __name__ == "__main__":
    pytest.main([__file__])