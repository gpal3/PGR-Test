"""Data store wrapper around SQLite for demo purposes."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable

from ..utils.config import load_settings
from ..utils.logger import get_logger

LOGGER = get_logger(__name__)


class DataStore:
    """Lightweight repository for demo artifacts."""

    def __init__(self) -> None:
        settings = load_settings().get("data", {})
        db_path = settings.get("sqlite_path", "data/demo.db")
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS negotiations (
                    session_id TEXT PRIMARY KEY,
                    supplier_id TEXT,
                    product_id TEXT,
                    recommended_action TEXT,
                    rationale TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feature_store (
                    product_id TEXT,
                    supplier_id TEXT,
                    similarity_score REAL,
                    benchmark_delta REAL,
                    last_offer_delta REAL
                )
                """
            )
            conn.commit()

    def upsert_negotiation(self, session_id: str, payload: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO negotiations(session_id, supplier_id, product_id, recommended_action, rationale)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    supplier_id=excluded.supplier_id,
                    product_id=excluded.product_id,
                    recommended_action=excluded.recommended_action,
                    rationale=excluded.rationale
                """,
                (
                    session_id,
                    payload.get("supplier_id"),
                    payload.get("product_id"),
                    payload.get("recommended_action"),
                    payload.get("rationale"),
                ),
            )
            conn.commit()

    def insert_feature_rows(self, rows: Iterable[Dict[str, Any]]) -> None:
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO feature_store(product_id, supplier_id, similarity_score, benchmark_delta, last_offer_delta)
                VALUES (:product_id, :supplier_id, :similarity_score, :benchmark_delta, :last_offer_delta)
                """,
                list(rows),
            )
            conn.commit()


data_store = DataStore()
