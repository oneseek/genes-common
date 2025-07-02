import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import settings


def setup_logging(name: str) -> logging.Logger:
    """Set up logging for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
