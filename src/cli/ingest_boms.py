"""CLI to ingest sample BOMs into the feature store."""
from __future__ import annotations

from pathlib import Path

import typer

from src.app.adapters.data_store import data_store
from src.app.services import bom_parser

app = typer.Typer(help="BOM ingestion utilities")


@app.command()
def ingest(directory: Path = typer.Argument(Path("data/sample_boms"))) -> None:
    """Parse BOM files and write summary rows into the feature store."""

    rows = []
    for file in directory.glob("*.*"):
        result = bom_parser.parse_bom(file.read_bytes(), file.name)
        for item in result.items:
            rows.append(
                {
                    "product_id": file.stem,
                    "supplier_id": "demo_supplier",
                    "similarity_score": 0.5,
                    "benchmark_delta": (item.unit_cost or 0.0) * 0.05,
                    "last_offer_delta": -0.02,
                }
            )
    if rows:
        data_store.insert_feature_rows(rows)
        typer.echo(f"Ingested {len(rows)} BOM rows")
    else:
        typer.echo("No BOM rows parsed")


if __name__ == "__main__":
    app()
