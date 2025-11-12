"""FastAPI application entrypoint."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import routes_bom, routes_health, routes_market, routes_negotiation
from .utils.config import load_settings
from .utils.logger import configure_logging

configure_logging()
settings = load_settings()

app = FastAPI(title=settings.get("app", {}).get("name", "AI Negotiation Framework"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router)
app.include_router(routes_bom.router)
app.include_router(routes_market.router)
app.include_router(routes_negotiation.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Negotiation Framework is running"}


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    spec_path = Path(__file__).resolve().parents[2] / "openapi" / "spec.yaml"
    if spec_path.exists():
        with spec_path.open("r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        app.openapi_schema = spec
        return spec
    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=settings.get("app", {}).get("name", "AI Negotiation Framework"),
        version=settings.get("app", {}).get("version", "0.1.0"),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
