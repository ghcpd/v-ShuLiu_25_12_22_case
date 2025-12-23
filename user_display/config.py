"""
Configuration system with defaults, environment overrides, and runtime overrides.
"""

import os
from typing import Any, Dict, Optional


class Config:
    """Configuration management for the user display system."""
    
    # Default configuration
    _defaults = {
        'max_users': 200000,
        'shard_count': 4,
        'enable_caching': True,
        'cache_size': 1000,
        'enable_parallel_filtering': True,
        'parallel_worker_count': 4,
        'validation_soft_fail': True,
        'field_trim_length': None,
        'log_level': 'INFO',
        'frozen': False,
    }
    
    def __init__(self):
        self._config: Dict[str, Any] = self._defaults.copy()
        self._load_environment_overrides()
    
    def _load_environment_overrides(self):
        """Load configuration from environment variables."""
        env_mapping = {
            'USER_DISPLAY_MAX_USERS': ('max_users', int),
            'USER_DISPLAY_SHARD_COUNT': ('shard_count', int),
            'USER_DISPLAY_ENABLE_CACHING': ('enable_caching', self._parse_bool),
            'USER_DISPLAY_CACHE_SIZE': ('cache_size', int),
            'USER_DISPLAY_ENABLE_PARALLEL': ('enable_parallel_filtering', self._parse_bool),
            'USER_DISPLAY_WORKER_COUNT': ('parallel_worker_count', int),
            'USER_DISPLAY_SOFT_FAIL': ('validation_soft_fail', self._parse_bool),
            'USER_DISPLAY_LOG_LEVEL': ('log_level', str),
        }
        
        for env_var, (key, parser) in env_mapping.items():
            if env_var in os.environ:
                try:
                    self._config[key] = parser(os.environ[env_var])
                except (ValueError, TypeError):
                    pass
    
    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse boolean from string."""
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def set(self, key: str, value: Any):
        """Set configuration value (if not frozen)."""
        if self._config.get('frozen'):
            raise ValueError("Configuration is frozen and cannot be modified")
        if key not in self._defaults:
            raise KeyError(f"Unknown configuration key: {key}")
        self._config[key] = value
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def freeze(self):
        """Freeze configuration to prevent further modifications."""
        self._config['frozen'] = True
    
    def is_frozen(self) -> bool:
        """Check if configuration is frozen."""
        return self._config.get('frozen', False)
    
    def reset(self):
        """Reset configuration to defaults."""
        if self._config.get('frozen'):
            raise ValueError("Configuration is frozen and cannot be modified")
        self._config = self._defaults.copy()
        self._load_environment_overrides()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()


# Global configuration instance
_global_config = None


def get_config() -> Config:
    """Get or create global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def reset_config():
    """Reset global configuration."""
    global _global_config
    _global_config = None
