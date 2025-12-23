"""
Metrics collection for the user display system.
"""

import time
from collections import defaultdict, deque
from typing import Dict, Any
from .config import config

class Metrics:
    """Metrics collector for performance monitoring."""

    def __init__(self):
        self._counters = defaultdict(int)
        self._timers = defaultdict(list)
        self._gauges = {}
        self._histograms = defaultdict(list)
        self._max_samples = 1000

    def increment(self, name: str, value: int = 1):
        """Increment a counter."""
        if config.get('enable_metrics', True):
            self._counters[name] += value

    def timer_start(self, name: str) -> str:
        """Start a timer and return a token."""
        if not config.get('enable_metrics', True):
            return ''
        token = f"{name}_{time.time()}"
        self._timers[token] = [time.time()]
        return token

    def timer_stop(self, token: str):
        """Stop a timer."""
        if not config.get('enable_metrics', True) or token not in self._timers:
            return
        start_time = self._timers[token][0]
        duration = time.time() - start_time
        name = token.split('_')[0]
        self._histograms[name].append(duration)
        if len(self._histograms[name]) > self._max_samples:
            self._histograms[name].pop(0)

    def gauge(self, name: str, value: float):
        """Set a gauge value."""
        if config.get('enable_metrics', True):
            self._gauges[name] = value

    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics statistics."""
        stats = dict(self._counters)

        for name, samples in self._histograms.items():
            if samples:
                stats[f'{name}_count'] = len(samples)
                stats[f'{name}_avg'] = sum(samples) / len(samples)
                stats[f'{name}_min'] = min(samples)
                stats[f'{name}_max'] = max(samples)

        stats.update(self._gauges)
        return stats

    def reset(self):
        """Reset all metrics."""
        self._counters.clear()
        self._timers.clear()
        self._gauges.clear()
        self._histograms.clear()

# Global metrics instance
metrics = Metrics()