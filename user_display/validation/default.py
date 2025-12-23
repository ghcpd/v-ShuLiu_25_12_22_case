"""Default validator: fills missing fields, normalizes types, records issues."""
from __future__ import annotations
from .base import BaseValidator
from typing import Dict, Any
from datetime import datetime


class DefaultValidator(BaseValidator):
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # soft-recovery for missing/corrupted fields
        out = {}
        # normalize id and name; treat None as missing
        id_val = data.get("id", "")
        out["id"] = "" if id_val is None else str(id_val) if id_val != "" else ""
        name_val = data.get("name")
        out["name"] = "" if name_val is None else name_val or ""
        out["email"] = data.get("email") or ""
        ts = data.get("created_at") or data.get("created")
        if ts:
            try:
                # accept datetime or string
                if isinstance(ts, datetime):
                    out["created_at"] = ts.isoformat()
                else:
                    out["created_at"] = datetime.fromisoformat(str(ts)).isoformat()
            except Exception:
                out["created_at"] = ""
        else:
            out["created_at"] = ""
        # keep any extra fields untouched to allow extensibility
        for k, v in data.items():
            if k in out:
                continue
            out[k] = v
        return out
