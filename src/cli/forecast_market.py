"""CLI to generate market forecasts."""
from __future__ import annotations

import json
from pathlib import Path

import typer

from src.app.services.market_signals import market_signals_service

app = typer.Typer(help="Market signals forecasting")


@app.command()
def forecast(output: Path = typer.Argument(Path(".artifacts/market_forecast.json"))) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    signals = market_signals_service.get_signals()
    output.write_text(json.dumps(signals, indent=2), encoding="utf-8")
    typer.echo(f"Forecast saved to {output}")


if __name__ == "__main__":
    app()
