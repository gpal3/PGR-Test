"""Seed demo data for the negotiation framework."""
from __future__ import annotations

import json
from pathlib import Path

from src.app.adapters.data_store import data_store


def seed_negotiations() -> None:
    transcripts_path = Path("data/historical_negotiations/transcripts.jsonl")
    sessions = []
    for line in transcripts_path.read_text().splitlines():
        record = json.loads(line)
        sessions.append(
            {
                "session_id": record["session_id"],
                "supplier_id": record["supplier"],
                "product_id": "P-" + record["session_id"].split("-")[-1],
                "recommended_action": "counter_-3",
                "rationale": "Seeded historical negotiation",
            }
        )
    for session in sessions:
        data_store.upsert_negotiation(session["session_id"], session)


def main() -> None:
    seed_negotiations()
    print("Demo data seeded successfully.")


if __name__ == "__main__":
    main()
