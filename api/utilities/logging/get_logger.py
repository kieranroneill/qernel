import logging
import os


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")

    logger.setLevel(os.environ["LOG_LEVEL"] or logging.ERROR)

    return logger
