import os
import tempfile
from user_display import logging_utils, metrics


def test_file_logging_writes_json(tmp_path):
    p = tmp_path / "ud.log"
    logging_utils.enable_file_logging(str(p))
    logging_utils.info("hello", tag="test")
    content = p.read_text(encoding="utf-8")
    assert "hello" in content and '"tag": "test"' in content


def test_prometheus_export_contains_metrics():
    # ensure metrics reflect current state
    metrics.cache_hits = 5
    metrics.cache_misses = 2
    out = metrics.export_prometheus_metrics().decode("utf-8")
    assert "user_display_cache_hits" in out or "user_display_cache_misses" in out
