"""Stub CLI to illustrate NER training workflow."""
from __future__ import annotations

import json
from pathlib import Path

import typer

from src.app.services.ner_pipeline import ner_pipeline

app = typer.Typer(help="NER training placeholder")


@app.command()
def train(dataset: Path = typer.Argument(Path("data/historical_negotiations/transcripts.jsonl"))) -> None:
    """Pretend to fine-tune a token classifier and export artifacts."""

    samples = [json.loads(line) for line in dataset.read_text().splitlines()]
    typer.echo(f"Loaded {len(samples)} transcripts for training")
    _ = ner_pipeline.extract_entities("100% recycled polyester knitting")
    artifacts = Path(".artifacts")
    artifacts.mkdir(exist_ok=True)
    (artifacts / "ner_model.txt").write_text("NER model trained on demo dataset", encoding="utf-8")
    typer.echo("NER training completed (demo artifact created)")


if __name__ == "__main__":
    app()
