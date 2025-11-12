"""BOM parsing utilities for CSV, XLSX, and PDF placeholders."""
from __future__ import annotations

import io
import mimetypes
from pathlib import Path
from typing import List

import pandas as pd

from ..utils.logger import get_logger
from ..utils.schemas import BOMItem, BOMParseResponse

LOGGER = get_logger(__name__)

EXPECTED_COLUMNS = {
    "material": "material",
    "composition": "composition",
    "gsm": "gsm",
    "process": "process",
    "unit_cost": "unit_cost",
    "moq": "moq",
    "lead_time": "lead_time",
}


def _load_dataframe(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Load supported BOM files into a DataFrame."""

    suffix = Path(filename).suffix.lower()
    if suffix in {".csv"}:
        return pd.read_csv(io.BytesIO(file_bytes))
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(io.BytesIO(file_bytes))
    if suffix == ".pdf":
        LOGGER.warning("PDF parsing not implemented; returning empty DataFrame. Consider pdfplumber usage.")
        # Example placeholder for future implementation:
        # import pdfplumber
        # with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        #     ...
        return pd.DataFrame(columns=EXPECTED_COLUMNS.keys())
    raise ValueError(f"Unsupported file type: {suffix}")


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and dtypes."""

    df = df.rename(columns={col: col.strip().lower() for col in df.columns})
    for src, target in EXPECTED_COLUMNS.items():
        if src not in df.columns and target in df.columns:
            continue
    df = df.rename(columns={col: EXPECTED_COLUMNS.get(col, col) for col in df.columns})

    for column in ["gsm", "unit_cost"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ["moq", "lead_time"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    for column in EXPECTED_COLUMNS.values():
        if column not in df.columns:
            df[column] = None
    return df[list(EXPECTED_COLUMNS.values())].fillna({})


def parse_bom(file_bytes: bytes, filename: str) -> BOMParseResponse:
    """Parse a BOM file and return normalized items."""

    df = _load_dataframe(file_bytes, filename)
    if df.empty:
        LOGGER.info("No rows found in BOM file %s", filename)
        items: List[BOMItem] = []
    else:
        normalized = _normalize_dataframe(df)
        items = [BOMItem(**{k: (None if pd.isna(v) else v) for k, v in row.items()}) for row in normalized.to_dict(orient="records")]
    return BOMParseResponse(items=items)


def detect_mime_type(filename: str) -> str:
    """Return MIME type for FastAPI responses."""

    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"
