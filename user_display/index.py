"""Index helpers (kept small for this exercise)."""
from __future__ import annotations

# For future: sharding / secondary indices. Keep minimal implementation so
# other modules can import index helpers without circular deps.

def make_shard_key(uid: str, shards: int = 16) -> int:
    """Deterministic shard key for a string uid."""
    return hash(uid) % max(1, shards)
