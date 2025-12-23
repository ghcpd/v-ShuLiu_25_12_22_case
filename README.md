# user_display — optimized, modular user display

Highlights
- Fast, thread-safe `UserStore` with O(1) id lookup, snapshotting and caching ✅
- Extensible formatters, filters and validators via a small plugin registry ✅
- Structured logging and lightweight metrics for observability ✅
- Compatibility wrapper `user_display_optimized.py` preserves the original API ✅

Quickstart

```py
from user_display_optimized import display_users, filter_users, get_user_by_id

users = [{"id": 1, "name": "Alice", "email": "a@x.com"}]
print(display_users(users))
```

Testing
- Unit tests: `pytest -q`
- Performance tests are skipped by default; run them with `RUN_PERF=1 pytest -q -m perf`.

Design
- `UserStore` handles validation, indexing, snapshotting and caching.
- `formatters/` provide composable output formats (compact, table, JSON).
- `filters/` provide pluggable filtering strategies (regex, composite).
- `validation/` recovers missing fields and reports issues to metrics.

Performance targets
- Display 50k users < 120 ms (best-effort, depends on environment)
- Filter 50k users < 15 ms (best-effort)
- ID lookup < 0.5 ms

For full details see the package docstrings and tests.
