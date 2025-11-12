from src.app.services.explainability import explain_counter_offer
from src.app.services.rl_agent import StateVector


def test_explainability_returns_top_features() -> None:
    state = StateVector(2.5, 0.5, 0.02, 0.8, -0.01)
    explanation = explain_counter_offer(state)
    assert "shap_values" in explanation
    assert explanation["top_features"], "Top features should not be empty"
