import os

class Config:
    DEFAULT_FORMAT = os.environ.get("USER_DISPLAY_DEFAULT_FORMAT", "compact")
    PARALLEL_FILTERING = os.environ.get("USER_DISPLAY_PARALLEL", "0") == "1"
