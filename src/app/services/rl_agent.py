"""Reinforcement learning stubs for negotiation decisioning."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from ..utils.config import load_settings
from ..utils.logger import get_logger

LOGGER = get_logger(__name__)


@dataclass
class StateVector:
    parsed_bom_cost: float
    similarity_score: float
    market_benchmark_delta: float
    supplier_reliability: float
    last_offer_delta: float

    def as_array(self) -> np.ndarray:
        return np.array(
            [
                self.parsed_bom_cost,
                self.similarity_score,
                self.market_benchmark_delta,
                self.supplier_reliability,
                self.last_offer_delta,
            ]
        )


ACTIONS = {
    0: {"label": "accept", "adjustment": 0.0},
    1: {"label": "reject", "adjustment": 0.0},
    2: {"label": "counter_-3", "adjustment": -0.03},
    3: {"label": "counter_-5", "adjustment": -0.05},
    4: {"label": "counter_+2", "adjustment": 0.02},
}


class NegotiationEnvironment:
    """Simple simulator with stochastic supplier responses."""

    def __init__(self) -> None:
        self.state = None

    def reset(self, state: StateVector) -> StateVector:
        self.state = state
        return state

    def step(self, action_id: int) -> Tuple[StateVector, float, bool, Dict[str, float]]:
        if self.state is None:
            raise RuntimeError("Environment not initialized")
        action = ACTIONS[action_id]
        reward = -abs(action["adjustment"] - self.state.market_benchmark_delta)
        done = random.random() > 0.6
        info = {"supplier_confidence": random.uniform(0.5, 1.0)}
        new_state = StateVector(
            parsed_bom_cost=max(self.state.parsed_bom_cost * (1 + action["adjustment"]), 0.1),
            similarity_score=self.state.similarity_score,
            market_benchmark_delta=self.state.market_benchmark_delta * 0.5,
            supplier_reliability=self.state.supplier_reliability,
            last_offer_delta=action["adjustment"],
        )
        self.state = new_state
        return new_state, reward, done, info


class RLAgentService:
    """DQN/Policy Gradient hybrid stub with heuristics."""

    def __init__(self) -> None:
        self.settings = load_settings().get("rl", {})
        self.environment = NegotiationEnvironment()
        self.weights = np.array([0.2, 0.3, 0.25, 0.15, 0.1])

    def evaluate_state(self, state: StateVector) -> Dict[int, float]:
        features = state.as_array()
        q_values = {}
        for action_id, action in ACTIONS.items():
            adjustment = action["adjustment"]
            bonus = -abs(adjustment - state.market_benchmark_delta)
            q_values[action_id] = float(np.dot(features, self.weights) + bonus)
        return q_values

    def select_action(self, state: StateVector) -> int:
        epsilon = self.settings.get("dqn", {}).get("epsilon_end", 0.1)
        if random.random() < epsilon:
            return random.choice(list(ACTIONS.keys()))
        q_values = self.evaluate_state(state)
        return max(q_values, key=q_values.get)

    def propose_counter_offer(self, state: StateVector) -> Dict[str, float | str]:
        action_id = self.select_action(state)
        action = ACTIONS[action_id]
        rationale = (
            f"Action {action['label']} selected based on similarity {state.similarity_score:.2f} "
            f"and market delta {state.market_benchmark_delta:.2f}."
        )
        return {
            "recommended_action": action["label"],
            "cost_adjustment_pct": action["adjustment"],
            "lead_time_days": int(max(0, 30 + state.last_offer_delta * 10)),
            "rationale": rationale,
        }

    def buyer_approval(self, action: str, rationale: str) -> bool:
        LOGGER.info("Buyer approval requested for action %s with rationale %s", action, rationale)
        return action != "reject"


rl_agent_service = RLAgentService()
