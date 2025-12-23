"""Lightweight in-process metrics for testing and basic observability."""
from __future__ import annotations
import time
from collections import Counter
from contextlib import contextmanager
from threading import Lock


class Metrics:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._c = Counter()
            cls._instance._timings = {}
            cls._instance._lock = Lock()
        return cls._instance

    def increment(self, key: str, n: int = 1):
        with self._lock:
            self._c[key] += n

    def get(self, key: str) -> int:
        return self._c.get(key, 0)

    def timing(self, key: str, value: float):
        with self._lock:
            self._timings.setdefault(key, []).append(value)

    def get_timings(self, key: str):
        return list(self._timings.get(key, []))


@contextmanager
def timed(key: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        dur = (time.perf_counter() - start) * 1000.0
        Metrics().timing(key, dur)


# decorator
def timed(name: str):
    def _dec(fn):
        def _wrapped(*a, **k):
            start = time.perf_counter()
            try:
                return fn(*a, **k)
            finally:
                Metrics().timing(name, (time.perf_counter() - start) * 1000.0)
        _wrapped.__name__ = fn.__name__
        return _wrapped
    return _dec
