import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # capture all levels

    if not logger.handlers:  # prevent duplicate handlers
        logger.propagate = False
        formatter = logging.Formatter(LOG_FORMAT)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        app_handler = TimedRotatingFileHandler(
            filename=os.path.join(LOG_DIR, "app.log"),
            when="midnight",
            interval=1,
            backupCount=7
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(formatter)

        error_handler = TimedRotatingFileHandler(
            filename=os.path.join(LOG_DIR, "error.log"),
            when="midnight",
            interval=1,
            backupCount=7
        )
        error_handler.setLevel(logging.ERROR)  # only ERROR+
        error_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(app_handler)
        logger.addHandler(error_handler)

    return logger