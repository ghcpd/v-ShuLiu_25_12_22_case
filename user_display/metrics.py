"""Simple in-memory metrics for the module (not Prometheus-grade)."""
from dataclasses import dataclass
from time import perf_counter


@dataclass
class Metrics:
    cache_hits: int = 0
    cache_misses: int = 0
    validation_issues: int = 0
    last_op_time_ms: float = 0.0

    def record_time(self, start: float) -> None:
        self.last_op_time_ms = (perf_counter() - start) * 1000.0
        try:
            _update_prometheus_metrics()
        except Exception:
            # Prometheus integration is optional
            pass


metrics = Metrics()

# --- Prometheus integration (optional) ---
_prom = None
try:
    from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest, start_http_server

    _reg = CollectorRegistry()
    _prom = {
        "cache_hits": Counter("user_display_cache_hits", "Cache hits", registry=_reg),
        "cache_misses": Counter("user_display_cache_misses", "Cache misses", registry=_reg),
        "validation_issues": Counter("user_display_validation_issues", "Validation issues", registry=_reg),
        "last_op_time_ms": Gauge("user_display_last_op_time_ms", "Last op time in ms", registry=_reg),
        "registry": _reg,
    }

    def _update_prometheus_metrics() -> None:
        # Counters: set by incrementing from current stored values
        # (we don't know prior state of Prometheus counters if process restarts; keep simple)
        _prom["cache_hits"]._value.set(metrics.cache_hits) if hasattr(_prom["cache_hits"], "_value") else None
        _prom["cache_misses"]._value.set(metrics.cache_misses) if hasattr(_prom["cache_misses"], "_value") else None
        _prom["validation_issues"]._value.set(metrics.validation_issues) if hasattr(_prom["validation_issues"], "_value") else None
        _prom["last_op_time_ms"].set(metrics.last_op_time_ms)

    def export_prometheus_metrics() -> bytes:
        """Return current metrics in Prometheus exposition format (bytes)."""
        # ensure latest values are pushed
        _update_prometheus_metrics()
        return generate_latest(_prom["registry"])

    def start_prometheus_http_server(port: int = 8000) -> None:
        """Start a Prometheus metrics HTTP server (non-blocking)."""
        start_http_server(port, registry=_prom["registry"])

except Exception:  # prometheus_client not available
    _prom = None

    def export_prometheus_metrics() -> bytes:
        # Fallback: export a tiny text representation
        txt = []
        txt.append(f"user_display_cache_hits {metrics.cache_hits}")
        txt.append(f"user_display_cache_misses {metrics.cache_misses}")
        txt.append(f"user_display_validation_issues {metrics.validation_issues}")
        txt.append(f"user_display_last_op_time_ms {metrics.last_op_time_ms}")
        return "\n".join(txt).encode("utf-8")

    def start_prometheus_http_server(port: int = 8000) -> None:
        raise RuntimeError("prometheus_client not installed")
