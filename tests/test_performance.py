import os
import time
import pytest
from user_display import UserStore, CompactFormatter


RUN_PERF = os.environ.get("RUN_PERF", "0") == "1"


@pytest.mark.perf
@pytest.mark.skipif(not RUN_PERF, reason="performance tests are skipped by default; set RUN_PERF=1 to run")
def test_filter_and_display_50k_meet_targets():
    n = 50000
    users = [{"id": i, "name": f"User{i}", "email": f"u{i}@x.com", "role": "User", "status": "Active", "last_login": "2025-01-01"} for i in range(1, n+1)]
    store = UserStore(users)

    t0 = time.perf_counter()
    out = store.display_users(store.snapshot(), formatter=CompactFormatter())
    display_ms = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    res = store.filter_users({"name": "User49999"})
    filter_ms = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    u = store.get_user_by_id(49999)
    lookup_ms = (time.perf_counter() - t0) * 1000.0

    print(f"display_ms={display_ms:.1f} filter_ms={filter_ms:.1f} lookup_ms={lookup_ms:.3f}")

    # allow a small multiplier for CI variability
    mult = float(os.environ.get("PERF_MULT", "1.5"))
    assert display_ms * mult < 120.0 * 2
    assert filter_ms * mult < 15.0 * 2
    assert lookup_ms * mult < 0.5 * 5
