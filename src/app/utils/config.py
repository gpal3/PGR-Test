"""Configuration utilities for the negotiation framework."""
from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, Dict

import yaml

BASE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_SETTINGS_PATH = BASE_DIR / "config" / "settings.yaml"


@functools.lru_cache(maxsize=1)
def load_settings(path: Path | None = None) -> Dict[str, Any]:
    """Load YAML settings as a dictionary.

    Parameters
    ----------
    path:
        Optional override path to the configuration file.

    Returns
    -------
    dict
        Parsed settings dictionary with string keys.
    """

    settings_path = path or DEFAULT_SETTINGS_PATH
    if not settings_path.exists():
        raise FileNotFoundError(f"Settings file not found at {settings_path}")

    with settings_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data
