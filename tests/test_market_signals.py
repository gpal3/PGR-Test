from src.app.services.market_signals import market_signals_service


def test_market_signals_payload_structure() -> None:
    payload = market_signals_service.get_signals()
    assert "commodity_trends" in payload
    assert "fx_trends" in payload
    assert "forecast_summary" in payload
