"""
Configuration management for the user display system.
Supports defaults, environment overrides, and runtime overrides.
"""

import os
from typing import Dict, Any

class Config:
    """Configuration manager with freeze support."""

    def __init__(self):
        self._config = {
            'max_users': 200000,
            'default_format': 'compact',
            'enable_parallel_filtering': False,
            'max_parallel_workers': 4,
            'enable_caching': True,
            'cache_size': 1000,
            'log_level': 'INFO',
            'enable_metrics': True,
            'shard_count': 16,
        }
        self._frozen = False
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'USER_DISPLAY_MAX_USERS': ('max_users', int),
            'USER_DISPLAY_DEFAULT_FORMAT': ('default_format', str),
            'USER_DISPLAY_ENABLE_PARALLEL': ('enable_parallel_filtering', lambda x: x.lower() in ('true', '1', 'yes')),
            'USER_DISPLAY_MAX_WORKERS': ('max_parallel_workers', int),
            'USER_DISPLAY_ENABLE_CACHING': ('enable_caching', lambda x: x.lower() in ('true', '1', 'yes')),
            'USER_DISPLAY_CACHE_SIZE': ('cache_size', int),
            'USER_DISPLAY_LOG_LEVEL': ('log_level', str),
            'USER_DISPLAY_ENABLE_METRICS': ('enable_metrics', lambda x: x.lower() in ('true', '1', 'yes')),
            'USER_DISPLAY_SHARD_COUNT': ('shard_count', int),
        }

        for env_var, (key, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    self._config[key] = converter(value)
                except ValueError:
                    pass  # Ignore invalid values

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value if not frozen."""
        if self._frozen:
            raise RuntimeError("Configuration is frozen")
        self._config[key] = value

    def freeze(self):
        """Freeze the configuration to prevent further changes."""
        self._frozen = True

    def unfreeze(self):
        """Unfreeze the configuration."""
        self._frozen = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a copy of the configuration."""
        return self._config.copy()

# Global config instance
config = Config()