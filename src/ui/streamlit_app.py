"""Streamlit dashboard for the negotiation framework."""
from __future__ import annotations

import json
from pathlib import Path

import httpx
import pandas as pd
import streamlit as st

from src.app.utils.config import load_settings

settings = load_settings()
API_URL = settings.get("ui", {}).get("api_url", "http://localhost:8000")

st.set_page_config(page_title="AI Negotiation Framework", layout="wide")
st.title("AI-Driven Negotiation Control Tower")

nav = st.sidebar.radio(
    "Navigate",
    ["Negotiations", "BOM Parser", "Signals & Forecasts", "Explainability"],
)

client = httpx.Client(base_url=API_URL)


def render_negotiations() -> None:
    st.header("Run a Negotiation Step")
    session_id = st.text_input("Session ID", value="demo-session")
    supplier_id = st.text_input("Supplier ID", value="EcoThreads")
    product_id = st.text_input("Product ID", value="P-001")
    supplier_message = st.text_area("Supplier Message", value="Can we reduce MOQ for faster lead time?")

    if st.button("Start Session"):
        payload = {
            "session_id": session_id,
            "supplier_id": supplier_id,
            "product_id": product_id,
            "targets": {"cost_reduction_pct": 2.5, "lead_time_days": 25},
        }
        resp = client.post("/v1/negotiation/start", json=payload)
        st.write(resp.json())

    if st.button("Send Supplier Message"):
        resp = client.post(
            "/v1/negotiation/step",
            json={"session_id": session_id, "supplier_message": supplier_message},
        )
        st.write(resp.json())


def render_bom_parser() -> None:
    st.header("Parse a Bill of Materials")
    uploaded = st.file_uploader("Upload BOM", type=["csv", "xlsx"])
    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        resp = client.post("/v1/bom/parse", files=files)
        data = resp.json()
        st.dataframe(pd.DataFrame(data.get("items", [])))


def render_signals() -> None:
    st.header("Market Signals")
    resp = client.get("/v1/market/signals")
    payload = resp.json()
    st.subheader("Commodity Benchmarks")
    st.dataframe(pd.DataFrame(payload.get("commodity_trends", [])))
    st.subheader("FX Benchmarks")
    st.dataframe(pd.DataFrame(payload.get("fx_trends", [])))
    st.subheader("Forecast Summary")
    st.json(payload.get("forecast_summary", {}))


def render_explainability() -> None:
    st.header("Explainability Demo")
    shap_path = Path(".artifacts/market_forecast.json")
    if shap_path.exists():
        st.json(json.loads(shap_path.read_text()))
    else:
        st.info("Run `poetry run python src/cli/forecast_market.py` to generate demo artifacts.")


if nav == "Negotiations":
    render_negotiations()
elif nav == "BOM Parser":
    render_bom_parser()
elif nav == "Signals & Forecasts":
    render_signals()
else:
    render_explainability()
