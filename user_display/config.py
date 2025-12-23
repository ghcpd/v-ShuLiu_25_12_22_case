"""Runtime configuration with environment overrides and freeze support."""
from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    default_formatter: str = os.environ.get("UD_DEFAULT_FORMATTER", "compact")
    max_snapshot_size: int = int(os.environ.get("UD_MAX_SNAPSHOT", "500000"))
    enable_parallel_filtering: bool = os.environ.get("UD_ENABLE_PARALLEL", "0") == "1"


DEFAULT = Config()
