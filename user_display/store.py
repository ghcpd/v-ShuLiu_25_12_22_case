"""Thread-safe user store with O(1) id lookup and snapshotting."""
from threading import RLock
from copy import deepcopy
from collections import defaultdict
from .errors import ValidationError

class UserStore:
    def __init__(self, users=None, validator=None):
        self._lock = RLock()
        self._users = [] if users is None else list(users)
        # id -> user mapping for O(1) lookups
        self._index = {u.get("id"): u for u in self._users if u.get("id") is not None}
        self.validator = validator

    def add(self, user):
        with self._lock:
            if self.validator:
                ok, repaired = self.validator.validate(user)
                if not ok:
                    raise ValidationError("Invalid user", user=repr(user))
                user = repaired
            uid = user.get("id")
            self._users.append(user)
            if uid is not None:
                self._index[uid] = user

    def get_by_id(self, uid):
        with self._lock:
            return deepcopy(self._index.get(uid))

    def list_snapshot(self):
        """Return a consistent shallow copy snapshot (fast copy)."""
        with self._lock:
            return [deepcopy(u) for u in self._users]

    def replace_all(self, users):
        with self._lock:
            self._users = list(users)
            self._index = {u.get("id"): u for u in self._users if u.get("id") is not None}

    def __len__(self):
        with self._lock:
            return len(self._users)
