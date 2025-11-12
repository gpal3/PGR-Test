"""Stub CLI to simulate RL training episodes."""
from __future__ import annotations

import random

import typer

from src.app.services.rl_agent import ACTIONS, NegotiationEnvironment, StateVector, rl_agent_service

app = typer.Typer(help="RL training utilities")


@app.command()
def train(episodes: int = typer.Option(5, help="Number of demo episodes")) -> None:
    env = NegotiationEnvironment()
    total_reward = 0.0
    for episode in range(episodes):
        state = env.reset(
            StateVector(
                parsed_bom_cost=2.5 + random.random(),
                similarity_score=random.uniform(0, 1),
                market_benchmark_delta=random.uniform(-0.05, 0.05),
                supplier_reliability=random.uniform(0.6, 0.9),
                last_offer_delta=-0.02,
            )
        )
        done = False
        while not done:
            action_id = rl_agent_service.select_action(state)
            state, reward, done, info = env.step(action_id)
            total_reward += reward
        typer.echo(f"Episode {episode + 1}: reward={reward:.3f}, last_action={ACTIONS[action_id]['label']}")
    typer.echo(f"Total reward: {total_reward:.3f}")


if __name__ == "__main__":
    app()
