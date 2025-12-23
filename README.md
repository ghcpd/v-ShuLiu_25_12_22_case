# User Display System

A high-performance, modular, concurrent, and fault-tolerant user display system.

## Overview

This system provides a complete refactor of the original user display module, addressing performance issues, architectural problems, and reliability concerns while maintaining API compatibility.

## Key Improvements

### Performance
- **O(1) ID lookups** via sharded hash indexing
- **Single-pass operations** and buffered string building
- **Parallel filtering** for large datasets
- **Cached results** for repeated operations
- **Optimized memory usage** with minimal allocations

### Architecture
- **Modular design** with clear separation of concerns
- **Plugin system** for extensible filters, formatters, and validators
- **Thread-safe operations** with MVCC-like snapshotting
- **Structured logging** and comprehensive metrics

### Reliability
- **Fault-tolerant validation** with automatic recovery
- **Graceful handling** of malformed data
- **Comprehensive error handling** and logging
- **Data integrity** through validation layers

## Package Structure

```
user_display/
├── __init__.py          # Main package exports
├── store.py             # User storage with indexing
├── index.py             # Sharded indexing system
├── config.py            # Configuration management
├── logging_utils.py     # Structured logging
├── metrics.py           # Performance metrics
├── plugins.py           # Plugin registry
├── errors.py            # Custom exceptions
├── formatters/          # Output formatting
│   ├── __init__.py
│   ├── base.py
│   ├── compact.py
│   ├── json_fmt.py
│   └── table.py
├── filters/             # User filtering
│   ├── __init__.py
│   ├── base.py
│   ├── regex_filter.py
│   └── composite_filter.py
└── validation/          # Data validation
    ├── __init__.py
    ├── base.py
    └── default.py
```

## API Compatibility

The `user_display_optimized.py` module maintains full API compatibility with the original:

```python
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string

# All original function signatures work unchanged
result = display_users(users, show_all=True, verbose=False)
user = get_user_by_id(users, user_id)
filtered = filter_users(users, {"name": "John", "status": "Active"})
export = export_users_to_string(users)
```

## Usage Examples

### Basic Usage
```python
from user_display_optimized import display_users, sample_users

# Display users in compact format
result = display_users(sample_users[:10])
print(result)
```

### Advanced Usage with Modular Components
```python
from user_display import UserStore, JSONFormatter, RegexFilter

# Create store and add users
store = UserStore()
store.add_users(sample_users)

# Use JSON formatter
formatter = JSONFormatter()
result = formatter.format_users(store.get_all_users())
print(result)

# Use regex filtering
name_filter = RegexFilter("name", r"^User\d+$")
email_filter = RegexFilter("email", r"@example\.com$")
```

### Plugin System
```python
from user_display import registry
from user_display.filters import RegexFilter

# Register custom filter
registry.register_filter("my_filter", RegexFilter)
```

## Configuration

Configure via environment variables or runtime:

```bash
export USER_DISPLAY_MAX_USERS=200000
export USER_DISPLAY_ENABLE_PARALLEL=true
export USER_DISPLAY_LOG_LEVEL=DEBUG
```

Or programmatically:
```python
from user_display import config

config.set('enable_parallel_filtering', True)
config.set('max_parallel_workers', 8)
config.freeze()  # Lock configuration
```

## Performance Benchmarks

| Operation | Target | Status |
|-----------|--------|--------|
| Display 50,000 users | < 120ms | ✅ |
| Filter 50,000 users | < 15ms | ✅ |
| ID lookup | < 0.5ms | ✅ |

## Testing

Run the comprehensive test suite:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.ps1
```

Tests cover:
- All formatting modes (compact, JSON, table)
- Field selection and conditional display
- Multi-criteria filtering with regex support
- Case-sensitive and case-insensitive matching
- Valid/invalid ID lookups
- Handling of missing or corrupted data
- Structured logging verification
- Metrics accuracy
- Parallel filtering correctness
- Performance at scale (50,000+ users)

## Plugin Development

### Custom Formatter
```python
from user_display.formatters.base import Formatter

class CustomFormatter(Formatter):
    def format_user(self, user):
        return f"[{user['id']}] {user['name']}"

    def format_users(self, users, show_count=True):
        lines = [self.format_user(u) for u in users]
        if show_count:
            lines.append(f"Total: {len(users)}")
        return "\n".join(lines)

# Register
from user_display import registry
registry.register_formatter("custom", CustomFormatter)
```

### Custom Filter
```python
from user_display.filters.base import Filter

class AgeFilter(Filter):
    def __init__(self, min_age, max_age):
        self.min_age = min_age
        self.max_age = max_age

    def matches(self, user):
        age = user.get('age', 0)
        return self.min_age <= age <= self.max_age

# Register
registry.register_filter("age", AgeFilter)
```

## Migration from Original

The optimized version is a drop-in replacement:

1. Replace import: `from user_display_original import ...` → `from user_display_optimized import ...`
2. No code changes required
3. Immediate performance improvements
4. Enhanced reliability and features

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `user_display/` is in Python path
2. **Performance**: Check `config.enable_parallel_filtering` for large datasets
3. **Memory Usage**: Monitor via metrics for large user sets
4. **Logging**: Set `USER_DISPLAY_LOG_LEVEL=DEBUG` for detailed logs

### Debug Mode
```python
from user_display import logger, metrics

# Enable debug logging
import logging
logging.getLogger().setLevel(logging.DEBUG)

# Check metrics
stats = metrics.get_stats()
print(stats)
```

## Contributing

1. Follow modular architecture
2. Add comprehensive tests
3. Update documentation
4. Maintain API compatibility
5. Include performance benchmarks