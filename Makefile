.PHONY: help setup seed dev api ui test lint format clean

help:
@echo "Available targets:"
@echo "  setup      Install dependencies and setup pre-commit"
@echo "  seed       Seed the demo database"
@echo "  dev        Run API and Streamlit UI in development mode"
@echo "  api        Run FastAPI application"
@echo "  ui         Run Streamlit dashboard"
@echo "  test       Run unit tests with coverage"
@echo "  lint       Run ruff lint checks"
@echo "  format     Run black + isort"
@echo "  clean      Remove build artifacts"

setup:
poetry install
poetry run pre-commit install

seed:
poetry run python scripts/seed_demo_data.py

api:
poetry run uvicorn src.app.main:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000} --reload

ui:
poetry run streamlit run src/ui/streamlit_app.py --server.port $${UI_PORT:-8501}

# Run API and UI concurrently for local demos
# To stop, press Ctrl+C twice
# shellcheck disable=SC2038
# The nohup pattern ensures cleanup when the parent exits
# but for simplicity we rely on foreground processes.
dev:
poetry run uvicorn src.app.main:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000} --reload & \
API_PID=$$!; \
poetry run streamlit run src/ui/streamlit_app.py --server.port $${UI_PORT:-8501}; \
kill $$API_PID || true

test:
poetry run pytest

lint:
poetry run ruff check src tests

format:
poetry run isort src tests
poetry run black src tests

clean:
rm -rf .pytest_cache .mypy_cache htmlcov
find . -type d -name "__pycache__" -exec rm -rf {} +
