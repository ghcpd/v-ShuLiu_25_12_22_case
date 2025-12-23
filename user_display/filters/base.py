from abc import ABC, abstractmethod

class BaseFilter(ABC):
    @abstractmethod
    def match(self, user):
        pass
