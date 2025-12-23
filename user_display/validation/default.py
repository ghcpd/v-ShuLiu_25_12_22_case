"""Default validator with soft-failure recovery and metrics reporting."""
from __future__ import annotations
from typing import Any, Dict, Tuple
from ..metrics import Metrics
from ..logging_utils import get_logger

_logger = get_logger("user_display.validation")
_metrics = Metrics()


class DefaultValidator:
    """Basic, fast validation that fills missing fields with safe defaults."""

    REQUIRED = ("id", "name", "email")

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        out = {}
        issues = False
        # coerce to dict-like
        if not isinstance(data, dict):
            _metrics.increment("validation_error_non_dict")
            _logger.warning("non_dict_user", extra={"source": str(type(data))})
            return False, {"id": None}
        for k in ("id", "name", "email", "role", "status", "join_date", "last_login"):
            v = data.get(k)
            if v is None:
                issues = True
                out[k] = "" if k != "id" else None
            else:
                out[k] = v
        if out.get("id") is None:
            _metrics.increment("validation_missing_id")
            _logger.debug("missing_id", extra={"user": out})
            return False, out
        if issues:
            _metrics.increment("validation_partial")
            _logger.info("partial_recovery", extra={"id": out.get("id")})
        return not issues, out
