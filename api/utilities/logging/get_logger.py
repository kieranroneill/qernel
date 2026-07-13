import logging
import os


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")

    logger.setLevel(os.environ["LOG_LEVEL"] or logging.ERROR)

    for handler in logger.handlers:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"))

    return logger
