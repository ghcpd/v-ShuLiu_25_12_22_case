import os
import time
from user_display_optimized import display_users, filter_users, get_user_by_id


def make_users(n):
    return [{"id": str(i), "name": f"User{i}", "email": f"user{i}@example.com"} for i in range(n)]


def test_operations_50k():
    n = 50000
    users = make_users(n)
    start = time.perf_counter()
    display_users(users=users, fmt="compact")
    display_t = (time.perf_counter() - start) * 1000.0

    start = time.perf_counter()
    out = filter_users(lambda u: u["id"].endswith("0"))
    filter_t = (time.perf_counter() - start) * 1000.0

    start = time.perf_counter()
    _ = get_user_by_id("12345")
    lookup_t = (time.perf_counter() - start) * 1000.0

    # Allow relaxing of thresholds in constrained CI
    relax = os.getenv("RELAX_PERF_TESTS", "0") == "1"

    if not relax:
        assert display_t < 120.0, f"display too slow: {display_t} ms"
        assert filter_t < 15.0, f"filter too slow: {filter_t} ms"
        assert lookup_t < 0.5, f"lookup too slow: {lookup_t} ms"
    else:
        # sanity checks when running in slower environments
        assert display_t < 2000.0
        assert filter_t < 500.0
        assert lookup_t < 50.0
