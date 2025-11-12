"""Negotiation API routes."""
from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, HTTPException, status

from ..adapters.data_store import data_store
from ..adapters.erp_adapter import erp_adapter
from ..services.chatbot import chatbot_service
from ..services.explainability import explain_counter_offer
from ..services.governance import prompt_guardrails, redact_pii
from ..services.graph_similarity import graph_similarity_service
from ..services.market_signals import market_signals_service
from ..services.rl_agent import StateVector, rl_agent_service
from ..utils.schemas import (
    CounterOffer,
    NegotiationStartRequest,
    NegotiationState,
    NegotiationStepRequest,
)

router = APIRouter(prefix="/v1/negotiation", tags=["negotiation"])

SESSION_CACHE: Dict[str, Dict[str, float]] = {}


def _build_state(session_id: str, supplier_id: str) -> StateVector:
    similarity = graph_similarity_service.similarity(session_id, supplier_id)
    signals = market_signals_service.get_signals()
    benchmark_values = [row.get("price_usd", 0.0) for row in signals.get("commodity_trends", [])]
    market_delta = 0.0
    if benchmark_values:
        market_delta = benchmark_values[-1] - sum(benchmark_values) / len(benchmark_values)
    supplier = erp_adapter.get_supplier(supplier_id)
    reliability = supplier.reliability if supplier else 0.7
    session_data = SESSION_CACHE.get(session_id, {})
    last_offer_delta = session_data.get("last_offer_delta", -0.02)
    parsed_cost = session_data.get("parsed_cost", 2.5)
    return StateVector(
        parsed_bom_cost=float(parsed_cost),
        similarity_score=float(similarity),
        market_benchmark_delta=float(market_delta),
        supplier_reliability=float(reliability),
        last_offer_delta=float(last_offer_delta),
    )


@router.post("/start", response_model=NegotiationState)
async def start_negotiation(payload: NegotiationStartRequest) -> NegotiationState:
    chatbot_service.start_session(payload.session_id, payload.model_dump())
    SESSION_CACHE[payload.session_id] = {
        "supplier_id": payload.supplier_id,
        "product_id": payload.product_id,
        "parsed_cost": payload.targets.cost_reduction_pct or 2.5,
    }
    state = _build_state(payload.session_id, payload.supplier_id)
    recommendation = rl_agent_service.propose_counter_offer(state)
    data_store.upsert_negotiation(
        payload.session_id,
        {
            "supplier_id": payload.supplier_id,
            "product_id": payload.product_id,
            "recommended_action": recommendation["recommended_action"],
            "rationale": recommendation["rationale"],
        },
    )
    explanation = explain_counter_offer(state)
    SESSION_CACHE[payload.session_id]["last_offer_delta"] = recommendation["cost_adjustment_pct"]
    counter = CounterOffer(
        cost_adjustment_pct=recommendation["cost_adjustment_pct"],
        lead_time_days=recommendation["lead_time_days"],
    )
    return NegotiationState(
        session_id=payload.session_id,
        system_summary="Negotiation session initialized.",
        recommended_action=recommendation["recommended_action"],
        counter_offer=counter,
        rationale=recommendation["rationale"],
        shap_values=explanation,
    )


@router.post("/step", response_model=NegotiationState)
async def negotiation_step(payload: NegotiationStepRequest) -> NegotiationState:
    if not prompt_guardrails(payload.supplier_message):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Supplier message violates guardrails")
    supplier_message = redact_pii(payload.supplier_message)
    reply = chatbot_service.step(payload.session_id, supplier_message)
    session_meta = SESSION_CACHE.get(payload.session_id)
    if not session_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not initialized")
    supplier_id = session_meta.get("supplier_id", "EcoThreads")
    state = _build_state(payload.session_id, supplier_id)
    recommendation = rl_agent_service.propose_counter_offer(state)
    explanation = explain_counter_offer(state)
    SESSION_CACHE[payload.session_id]["last_offer_delta"] = recommendation["cost_adjustment_pct"]
    counter = CounterOffer(
        cost_adjustment_pct=recommendation["cost_adjustment_pct"],
        lead_time_days=recommendation["lead_time_days"],
    )
    return NegotiationState(
        session_id=payload.session_id,
        system_summary=reply,
        recommended_action=recommendation["recommended_action"],
        counter_offer=counter,
        rationale=recommendation["rationale"],
        shap_values=explanation,
    )
