import re
from .base import BaseFilter

class RegexFilter(BaseFilter):
    def __init__(self, field, pattern, flags=0):
        self.field = field
        self.pattern = re.compile(pattern, flags)

    def match(self, user):
        val = user.get(self.field)
        if val is None:
            return False
        return bool(self.pattern.search(str(val)))
