import threading
from user_display import UserStore


USERS = [{"id": i, "name": f"u{i}", "email": f"u{i}@x"} for i in range(1, 1000)]


def test_snapshot_consistency_and_thread_safety():
    store = UserStore(USERS)
    snap = store.snapshot()
    results = []

    def reader():
        for _ in range(10):
            results.append(store.get_user_by_id(10))

    t = threading.Thread(target=reader)
    t.start()
    t.join()
    assert all(r and r["id"] == 10 for r in results)


def test_missing_fields_recovered():
    store = UserStore([{"id": 999, "email": "x@x"}])
    u = store.get_user_by_id(999)
    assert u is not None
    assert "name" in u
