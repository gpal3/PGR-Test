FROM python:3.10-slim

ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
RUN poetry install --no-root --no-interaction --without dev

COPY . .
RUN poetry install --no-interaction

EXPOSE 8000 8501

CMD ["bash", "-c", "poetry run uvicorn src.app.main:app --host 0.0.0.0 --port 8000"]
