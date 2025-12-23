from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    @abstractmethod
    def format(self, users, fields=None):
        pass
