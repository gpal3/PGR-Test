"""Market signal loaders and lightweight forecasting stubs."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd

from ..utils.config import load_settings
from ..utils.logger import get_logger

LOGGER = get_logger(__name__)


@dataclass
class MarketForecast:
    metric: str
    forecast: List[Dict[str, float]]


class MarketSignalsService:
    """Loads benchmark CSVs and returns structured responses."""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parents[3]
        self.commodity_path = base_dir / "data" / "market_signals" / "commodity_prices.csv"
        self.fx_path = base_dir / "data" / "market_signals" / "fx_rates.csv"
        self.settings = load_settings().get("market", {})

    def _load_csv(self, path: Path) -> pd.DataFrame:
        if not path.exists():
            LOGGER.warning("Market signal file missing: %s", path)
            return pd.DataFrame()
        return pd.read_csv(path, parse_dates=["date"])

    def _simple_forecast(self, series: pd.Series, horizon: int) -> List[Dict[str, float]]:
        if series.empty:
            return []
        rolling = series.tail(3).mean()
        forecasts = []
        for step in range(1, horizon + 1):
            forecasts.append({"step": step, "value": float(rolling)})
        return forecasts

    def get_signals(self) -> Dict[str, List[Dict[str, str]]]:
        commodity_df = self._load_csv(self.commodity_path)
        fx_df = self._load_csv(self.fx_path)

        commodity_records = commodity_df.sort_values("date").tail(5).to_dict(orient="records")
        fx_records = fx_df.sort_values("date").tail(5).to_dict(orient="records")

        horizon = int(self.settings.get("forecast_horizon_days", 30) / 7)
        forecast = self._simple_forecast(
            commodity_df.set_index("date")[self.settings.get("commodity_price_column", "price_usd")]
            if not commodity_df.empty
            else pd.Series(dtype=float),
            horizon,
        )

        return {
            "commodity_trends": commodity_records,
            "fx_trends": fx_records,
            "forecast_summary": {
                "horizon_weeks": horizon,
                "forecast": forecast,
            },
        }


market_signals_service = MarketSignalsService()
