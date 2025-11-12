"""Governance utilities for safety and drift monitoring."""
from __future__ import annotations

import re
from typing import Dict, List

import numpy as np

from ..utils.config import load_settings
from ..utils.logger import get_logger

LOGGER = get_logger(__name__)

PII_PATTERN = re.compile(r"([\w.-]+@[\w.-]+|\+?\d{7,})")


def redact_pii(text: str) -> str:
    """Redact emails and long numbers to avoid storing PII."""

    return PII_PATTERN.sub("[REDACTED]", text)


def prompt_guardrails(text: str) -> bool:
    """Validate text against red team checklist keywords."""

    forbidden = ["fabricate", "confidential", "bypass"]
    return not any(keyword in text.lower() for keyword in forbidden)


def compute_psi(expected: List[float], actual: List[float]) -> float:
    """Compute a simple population stability index."""

    expected_hist, bins = np.histogram(expected, bins=5, range=(min(expected + actual), max(expected + actual)))
    actual_hist, _ = np.histogram(actual, bins=bins)
    expected_pct = expected_hist / (expected_hist.sum() + 1e-9)
    actual_pct = actual_hist / (actual_hist.sum() + 1e-9)
    psi = np.sum((actual_pct - expected_pct) * np.log((actual_pct + 1e-9) / (expected_pct + 1e-9)))
    return float(abs(psi))


def check_drift(expected: List[float], actual: List[float]) -> bool:
    settings = load_settings().get("governance", {})
    threshold = settings.get("drift_threshold", 0.2)
    psi_value = compute_psi(expected, actual)
    LOGGER.info("PSI computed at %.4f", psi_value)
    return psi_value > threshold
