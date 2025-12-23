"""Validator interface and common utilities."""
from __future__ import annotations
from typing import Any, Dict, Tuple
from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        ...
