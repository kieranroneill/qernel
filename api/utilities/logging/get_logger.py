import logging
import os


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")

    logger.setLevel(os.getenv("LOG_LEVEL", "ERROR"))

    return logger
