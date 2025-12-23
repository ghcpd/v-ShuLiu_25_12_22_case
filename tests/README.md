# Tests for user_display module

This directory contains comprehensive tests for the user display system.

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_user_display.py::TestFormatters -v

# Run with coverage
python -m pytest tests/ --cov=user_display
```

## Test Coverage

### TestFormatters
- JSON formatting (basic, field selection, trimming, multiple users)
- Compact formatting
- Table formatting

### TestFilters
- Criteria filtering (exact match, substring, case-insensitive)
- Regex filtering
- Prefix/suffix filtering
- Callable filtering
- Composite filters (AND/OR logic)

### TestValidation
- User validation (valid data, missing fields, recovery)
- Email validation
- Field-specific validators

### TestUserStore
- Adding users
- O(1) ID lookup
- Removing/updating users
- Snapshot creation and management
- Caching functionality

### TestMetrics
- Cache hit/miss tracking
- Operation time recording

### TestPlugins
- Plugin registry and discovery
- Built-in plugin instantiation

### TestPerformance
- Display 50,000 users: < 120ms
- Single ID lookup: < 0.5ms
- Filter 50,000 users: < 15ms

### TestCompatibilityWrapper
- Original API compatibility (display_users, get_user_by_id, filter_users, export_users_to_string)
