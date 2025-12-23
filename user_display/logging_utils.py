import logging
import json

logger = logging.getLogger("user_display")
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter('{"ts":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}')
    h.setFormatter(fmt)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


def log_structured(level, msg, **kwargs):
    logger.log(level, json.dumps({"msg": msg, **kwargs}))
