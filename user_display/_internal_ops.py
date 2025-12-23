"""Internal helper functions: filtering and caching."""
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from .metrics import inc
from .config import Config

@lru_cache(maxsize=1024)
def _cached_filter_key(criteria_tuple):
    return criteria_tuple


def filter_users_list(users, match_fn, parallel=False):
    """Filter users efficiently, optionally in parallel."""
    inc("filter_calls")
    if parallel and Config.PARALLEL_FILTERING:
        inc("parallel_filter_calls")
        with ThreadPoolExecutor() as ex:
            results = list(ex.map(lambda u: (u, match_fn(u)), users))
            return [u for u, ok in results if ok]
    else:
        return [u for u in users if match_fn(u)]
