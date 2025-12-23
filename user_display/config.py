"""Runtime configuration with environment override support."""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    default_formatter: str = os.getenv("USER_DISPLAY_FMT", "table")
    max_workers: int = int(os.getenv("USER_DISPLAY_MAX_WORKERS", "4"))
    enable_caching: bool = os.getenv("USER_DISPLAY_ENABLE_CACHE", "1") != "0"
    freeze: bool = False

    @classmethod
    def from_env(cls):
        return cls()
