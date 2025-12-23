import concurrent.futures
from user_display_optimized import display_users, filter_users


SAMPLE = [{"id": str(i), "name": f"U{i}", "email": f"u{i}@ex.com"} for i in range(2000)]


def test_parallel_filter_same_as_sequential():
    display_users(users=SAMPLE)
    # filter for even ids
    def even(u):
        return int(u["id"]) % 2 == 0

    seq = filter_users(even, parallel=False)
    par = filter_users(even, parallel=True)
    assert {u['id'] for u in seq} == {u['id'] for u in par}
