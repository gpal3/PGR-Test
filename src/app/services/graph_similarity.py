"""Graph similarity utilities for BOM and supplier relationships."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx
import pandas as pd

from ..utils.logger import get_logger

LOGGER = get_logger(__name__)


class GraphSimilarityService:
    """Wraps a NetworkX graph with helper similarity functions."""

    def __init__(self) -> None:
        self.graph = nx.Graph()
        self._load_demo_graph()

    def _load_demo_graph(self) -> None:
        base_path = Path(__file__).resolve().parents[3] / "data" / "historical_negotiations" / "transcripts.jsonl"
        if not base_path.exists():
            LOGGER.warning("No transcripts found for graph bootstrap")
            return
        df = pd.read_json(base_path, lines=True)
        for _, row in df.iterrows():
            supplier = row.get("supplier")
            session = row.get("session_id")
            if supplier and session:
                self.graph.add_node(session, type="session")
                self.graph.add_node(supplier, type="supplier")
                self.graph.add_edge(session, supplier)
        LOGGER.info("Bootstrapped graph with %d nodes", self.graph.number_of_nodes())

    def similarity(self, node_a: str, node_b: str) -> float:
        if not self.graph.has_node(node_a) or not self.graph.has_node(node_b):
            return 0.0
        if node_a == node_b:
            return 1.0
        common_neighbors = len(sorted(nx.common_neighbors(self.graph, node_a, node_b)))
        degree_product = max(self.graph.degree(node_a) * self.graph.degree(node_b), 1)
        return common_neighbors / degree_product

    def nearest_neighbors(self, node_id: str, k: int = 3) -> List[Tuple[str, float]]:
        scores: Dict[str, float] = {}
        for other in self.graph.nodes:
            if other == node_id or self.graph.nodes[other].get("type") != "supplier":
                continue
            score = self.similarity(node_id, other)
            if score > 0:
                scores[other] = score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]


graph_similarity_service = GraphSimilarityService()
