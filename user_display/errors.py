"""Error types used across the package."""
class UserDisplayError(Exception):
    pass


class NotFoundError(UserDisplayError):
    pass


class ValidationError(UserDisplayError):
    pass
