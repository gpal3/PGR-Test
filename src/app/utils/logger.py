"""Logging utilities for consistent instrumentation."""
from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from .config import load_settings


def configure_logging() -> None:
    """Configure logging using YAML configuration if available."""

    settings = load_settings()
    log_config_path = settings.get("app", {}).get("log_config")
    if log_config_path:
        config_path = Path(log_config_path)
        if not config_path.is_absolute():
            config_path = Path(__file__).resolve().parents[3] / config_path
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as f:
                import yaml

                config_dict = yaml.safe_load(f)
            logging.config.dictConfig(config_dict)
            return

    logging.basicConfig(level=logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured for the given name."""

    configure_logging()
    return logging.getLogger(name)
