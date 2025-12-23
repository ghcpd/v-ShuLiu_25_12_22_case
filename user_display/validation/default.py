from .base import BaseValidator

class DefaultValidator(BaseValidator):
    required = ["id", "name", "email"]

    def validate(self, user):
        # Soft-repair missing fields
        u = dict(user)
        for r in self.required:
            if r not in u or u.get(r) is None:
                u[r] = "" if r != "id" else None
        # ID must be int or None
        try:
            if u.get("id") is not None:
                u["id"] = int(u["id"])
        except Exception:
            u["id"] = None
        return True, u
