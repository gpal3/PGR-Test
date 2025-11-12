"""ERP adapter interface and demo implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Supplier:
    supplier_id: str
    name: str
    reliability: float


@dataclass
class Contract:
    contract_id: str
    supplier_id: str
    product_id: str
    currency: str
    incoterms: str


class ERPAdapter:
    """Mock ERP adapter exposing typed methods."""

    def __init__(self) -> None:
        self.suppliers: Dict[str, Supplier] = {
            "EcoThreads": Supplier("EcoThreads", "Eco Threads Ltd", 0.82),
            "SustainTex": Supplier("SustainTex", "Sustain Tex Mills", 0.76),
        }
        self.contracts: Dict[str, Contract] = {
            "C-100": Contract("C-100", "EcoThreads", "P-01", "USD", "FOB"),
            "C-101": Contract("C-101", "SustainTex", "P-02", "USD", "CIF"),
        }

    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        return self.suppliers.get(supplier_id)

    def get_contracts(self, supplier_id: str) -> Dict[str, Contract]:
        return {cid: contract for cid, contract in self.contracts.items() if contract.supplier_id == supplier_id}


erp_adapter = ERPAdapter()
