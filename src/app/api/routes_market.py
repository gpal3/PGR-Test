"""Market signals API routes."""
from fastapi import APIRouter

from ..services.market_signals import market_signals_service

router = APIRouter(prefix="/v1/market", tags=["market"])


@router.get("/signals")
async def get_signals() -> dict:
    return market_signals_service.get_signals()
