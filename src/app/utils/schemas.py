# Shared Pydantic schemas for API payloads and service responses.
from typing import List, Optional

from pydantic import BaseModel, Field


class BOMItem(BaseModel):
    """Normalized BOM line item."""

    material: str = Field(..., description="Material name")
    composition: Optional[str] = Field(None, description="Material composition details")
    gsm: Optional[float] = Field(None, description="Grams per square meter")
    process: Optional[str] = Field(None, description="Manufacturing process")
    unit_cost: Optional[float] = Field(None, description="Cost per unit")
    moq: Optional[int] = Field(None, description="Minimum order quantity")
    lead_time: Optional[int] = Field(None, description="Lead time in days")


class BOMParseResponse(BaseModel):
    items: List[BOMItem]


class NegotiationTargets(BaseModel):
    cost_reduction_pct: Optional[float] = Field(None, description="Target cost reduction percentage")
    lead_time_days: Optional[int] = Field(None, description="Desired lead time in days")


class NegotiationStartRequest(BaseModel):
    session_id: str
    supplier_id: str
    product_id: str
    targets: NegotiationTargets


class NegotiationStepRequest(BaseModel):
    session_id: str
    supplier_message: str


class CounterOffer(BaseModel):
    cost_adjustment_pct: float
    lead_time_days: Optional[int]


class NegotiationState(BaseModel):
    session_id: str
    system_summary: str
    recommended_action: str
    counter_offer: CounterOffer
    rationale: str
    shap_values: dict
