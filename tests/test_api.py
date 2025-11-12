from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_market_signals_endpoint() -> None:
    response = client.get("/v1/market/signals")
    assert response.status_code == 200
    assert "commodity_trends" in response.json()


def test_negotiation_flow() -> None:
    start_payload = {
        "session_id": "test-session",
        "supplier_id": "EcoThreads",
        "product_id": "P-001",
        "targets": {"cost_reduction_pct": 2.5, "lead_time_days": 25},
    }
    start_resp = client.post("/v1/negotiation/start", json=start_payload)
    assert start_resp.status_code == 200
    step_resp = client.post(
        "/v1/negotiation/step",
        json={"session_id": "test-session", "supplier_message": "Offering 5% discount"},
    )
    assert step_resp.status_code == 200
    body = step_resp.json()
    assert "recommended_action" in body
    assert "counter_offer" in body
