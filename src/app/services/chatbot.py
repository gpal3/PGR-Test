"""Negotiation chatbot wrapper around FLAN-T5 (with graceful fallback)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from ..utils.config import load_settings
from ..utils.logger import get_logger

LOGGER = get_logger(__name__)


class ChatbotService:
    """Simple session-aware wrapper for text generation."""

    def __init__(self) -> None:
        settings = load_settings()
        model_config = settings.get("model", {})
        self.model_name = model_config.get("llm_model_name", "google/flan-t5-small")
        self.fallback_model_name = model_config.get(
            "llm_fallback_model_name", "hf-internal-testing/tiny-random-t5"
        )
        self.max_new_tokens = model_config.get("max_new_tokens", 128)
        self.temperature = model_config.get("temperature", 0.7)
        self._pipeline = None
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self.system_prompt = self._load_prompt("system_prompt.txt")
        self.negotiation_prompt = self._load_prompt("negotiation_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        prompt_path = Path(__file__).resolve().parents[3] / "config" / "prompts" / filename
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        LOGGER.warning("Prompt %s not found; returning empty string", filename)
        return ""

    def _ensure_pipeline(self) -> None:
        if self._pipeline is not None:
            return
        try:
            from transformers import pipeline

            self._pipeline = pipeline(
                "text2text-generation",
                model=self.model_name,
                model_kwargs={"torch_dtype": "auto"},
            )
            LOGGER.info("Loaded LLM model %s", self.model_name)
        except Exception as exc:  # pragma: no cover - exercised only without weights
            LOGGER.warning("Failed to load %s due to %s. Falling back to tiny model.", self.model_name, exc)
            try:
                from transformers import pipeline

                self._pipeline = pipeline("text2text-generation", model=self.fallback_model_name)
                LOGGER.info("Loaded fallback model %s", self.fallback_model_name)
            except Exception as fallback_exc:  # pragma: no cover - offline stub
                LOGGER.error("Unable to load fallback model: %s", fallback_exc)
                self._pipeline = None

    def _rule_based_reply(self, session_id: str, supplier_message: str) -> str:
        history = self.sessions.get(session_id, [])
        summary = f"History turns: {len(history)}. Supplier said: {supplier_message}" if history else supplier_message
        return (
            f"Summary: {summary}. Recommended counter at 3% reduction with maintained lead time."
        )

    def start_session(self, session_id: str, seed_context: Dict[str, str]) -> None:
        self.sessions[session_id] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "context", "content": str(seed_context)},
        ]

    def step(self, session_id: str, supplier_message: str) -> str:
        if session_id not in self.sessions:
            self.start_session(session_id, {})
        conversation = self.sessions[session_id]
        conversation.append({"role": "supplier", "content": supplier_message})

        user_prompt = (
            f"{self.negotiation_prompt}\n\nSupplier message: {supplier_message}\n"
            f"History: {conversation}"
        )

        if self._pipeline is None:
            from os import getenv

            if getenv("ENABLE_LLM", "0") == "1":
                self._ensure_pipeline()

        if self._pipeline is None:
            reply = self._rule_based_reply(session_id, supplier_message)
        else:
            try:
                output = self._pipeline(
                    user_prompt,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                )
                reply = output[0]["generated_text"]
            except Exception as exc:  # pragma: no cover - fallback scenario
                LOGGER.error("LLM generation failed: %s", exc)
                reply = self._rule_based_reply(session_id, supplier_message)

        conversation.append({"role": "assistant", "content": reply})
        return reply


chatbot_service = ChatbotService()
