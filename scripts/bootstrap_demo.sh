#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install poetry
poetry install
poetry run python scripts/seed_demo_data.py
poetry run uvicorn src.app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!
poetry run streamlit run src/ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
kill $API_PID || true
