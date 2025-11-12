"""Explainability utilities for negotiation outcomes."""
from __future__ import annotations

from typing import Dict, List

import numpy as np

from .rl_agent import StateVector


def explain_counter_offer(state: StateVector, weight_vector: np.ndarray | None = None, top_k: int = 3) -> Dict[str, List[Dict[str, float]]]:
    """Return pseudo-SHAP values derived from state weights.

    The implementation uses a deterministic dot-product decomposition to avoid
    heavy SHAP dependencies while keeping JSON-compatible output for the UI.
    """

    features = state.as_array()
    names = [
        "parsed_bom_cost",
        "similarity_score",
        "market_benchmark_delta",
        "supplier_reliability",
        "last_offer_delta",
    ]
    weights = weight_vector if weight_vector is not None else np.array([0.3, 0.2, 0.25, 0.15, 0.1])
    contributions = features * weights
    normalized = contributions / (np.sum(np.abs(contributions)) + 1e-6)
    shap_values = [
        {
            "feature": name,
            "value": float(contrib),
            "normalized_importance": float(norm),
        }
        for name, contrib, norm in zip(names, contributions, normalized)
    ]
    shap_values.sort(key=lambda x: abs(x["normalized_importance"]), reverse=True)
    return {
        "shap_values": shap_values,
        "top_features": shap_values[:top_k],
    }
