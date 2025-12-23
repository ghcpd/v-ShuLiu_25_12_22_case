from .base import BaseFormatter
import json

class JSONFormatter(BaseFormatter):
    def format(self, users, fields=None):
        if fields:
            users = [{k: u.get(k) for k in fields} for u in users]
        return json.dumps(users, default=str)
