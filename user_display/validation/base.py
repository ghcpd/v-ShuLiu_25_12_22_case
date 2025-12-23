from abc import ABC, abstractmethod

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, user):
        """Return (ok: bool, user: dict)"""
        pass
