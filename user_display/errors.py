class ValidationError(Exception):
    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.context = kwargs
