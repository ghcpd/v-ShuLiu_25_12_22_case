"""
Metrics collection for performance monitoring.
"""

from typing import Dict, Any
from datetime import datetime
import time


class Metrics:
    """Collect and report metrics for the user display system."""
    
    def __init__(self):
        self._metrics: Dict[str, Any] = {
            'cache_hits': 0,
            'cache_misses': 0,
            'filter_operations': 0,
            'validation_errors': 0,
            'validation_recoveries': 0,
            'operation_times': {},
            'shard_usage': {},
            'parallel_filter_stats': {}
        }
    
    def record_cache_hit(self):
        """Record a cache hit."""
        self._metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        self._metrics['cache_misses'] += 1
    
    def record_filter_operation(self):
        """Record a filter operation."""
        self._metrics['filter_operations'] += 1
    
    def record_validation_error(self):
        """Record a validation error."""
        self._metrics['validation_errors'] += 1
    
    def record_validation_recovery(self):
        """Record a validation recovery."""
        self._metrics['validation_recoveries'] += 1
    
    def record_operation_time(self, operation: str, duration_ms: float):
        """Record operation duration."""
        if operation not in self._metrics['operation_times']:
            self._metrics['operation_times'][operation] = []
        self._metrics['operation_times'][operation].append(duration_ms)
    
    def record_shard_usage(self, shard_id: int, user_count: int):
        """Record shard usage."""
        self._metrics['shard_usage'][f'shard_{shard_id}'] = user_count
    
    def record_parallel_filter_stats(self, threads: int, duration_ms: float):
        """Record parallel filtering statistics."""
        if 'last_run' not in self._metrics['parallel_filter_stats']:
            self._metrics['parallel_filter_stats']['runs'] = 0
        self._metrics['parallel_filter_stats']['runs'] += 1
        self._metrics['parallel_filter_stats']['last_threads'] = threads
        self._metrics['parallel_filter_stats']['last_duration_ms'] = duration_ms
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return self._metrics.copy()
    
    def get_summary(self) -> str:
        """Get human-readable metrics summary."""
        metrics = self._metrics
        lines = [
            "=== Metrics Summary ===",
            f"Cache Hits: {metrics['cache_hits']}",
            f"Cache Misses: {metrics['cache_misses']}",
            f"Filter Operations: {metrics['filter_operations']}",
            f"Validation Errors: {metrics['validation_errors']}",
            f"Validation Recoveries: {metrics['validation_recoveries']}",
        ]
        
        if metrics['operation_times']:
            lines.append("\nOperation Times (ms):")
            for op, times in metrics['operation_times'].items():
                avg = sum(times) / len(times) if times else 0
                min_t = min(times) if times else 0
                max_t = max(times) if times else 0
                lines.append(f"  {op}: avg={avg:.3f}, min={min_t:.3f}, max={max_t:.3f}")
        
        if metrics['shard_usage']:
            lines.append("\nShard Usage:")
            for shard, count in metrics['shard_usage'].items():
                lines.append(f"  {shard}: {count} users")
        
        return "\n".join(lines)
    
    def reset(self):
        """Reset all metrics."""
        self._metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'filter_operations': 0,
            'validation_errors': 0,
            'validation_recoveries': 0,
            'operation_times': {},
            'shard_usage': {},
            'parallel_filter_stats': {}
        }


# Global metrics instance
_global_metrics = None


def get_metrics() -> Metrics:
    """Get or create global metrics instance."""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = Metrics()
    return _global_metrics
