"""Logging utilities for consistent application logging."""
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_PATH = os.path.join(os.getcwd(), "logs", "app.log")


def setup_logging(level: int = logging.INFO, log_path: str | None = None) -> None:
    """Configure application-wide logging with rotation."""
    target_path = log_path or LOG_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    handler = RotatingFileHandler(target_path, maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[handler, console], force=True)


def get_logger(name: str) -> logging.Logger:
    """Return a logger using the configured settings."""
    if not logging.getLogger().handlers:
        setup_logging()
    return logging.getLogger(name)
