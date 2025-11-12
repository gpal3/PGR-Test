from src.app.services.rl_agent import StateVector, rl_agent_service


def test_rl_agent_produces_recommendation() -> None:
    state = StateVector(
        parsed_bom_cost=2.5,
        similarity_score=0.6,
        market_benchmark_delta=0.02,
        supplier_reliability=0.8,
        last_offer_delta=-0.01,
    )
    recommendation = rl_agent_service.propose_counter_offer(state)
    assert "recommended_action" in recommendation
    assert "cost_adjustment_pct" in recommendation
