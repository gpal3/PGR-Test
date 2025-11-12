"""Rule-augmented NER pipeline stubs."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List

from ..utils.logger import get_logger

LOGGER = get_logger(__name__)

MATERIAL_PATTERN = re.compile(r"(recycled|organic|cotton|polyester|linen|silk)[\w\s%-]*", re.IGNORECASE)
PROCESS_PATTERN = re.compile(r"(knitting|weaving|dyeing|finishing|cutting)", re.IGNORECASE)
TRIM_PATTERN = re.compile(r"(zipper|button|snap|trim)", re.IGNORECASE)


@dataclass
class Entity:
    label: str
    value: str
    start: int
    end: int


class NERPipeline:
    """Hybrid regex + optional transformer pipeline."""

    def __init__(self) -> None:
        self._hf_pipeline = None
        self._ensure_model()

    def _ensure_model(self) -> None:
        try:
            from transformers import pipeline

            self._hf_pipeline = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")
            LOGGER.info("Loaded Hugging Face NER pipeline")
        except Exception as exc:  # pragma: no cover - offline fallback
            LOGGER.warning("Falling back to regex-based NER due to: %s", exc)
            self._hf_pipeline = None

    def _regex_entities(self, text: str) -> List[Entity]:
        entities: List[Entity] = []
        for pattern, label in [
            (MATERIAL_PATTERN, "MATERIAL"),
            (PROCESS_PATTERN, "PROCESS"),
            (TRIM_PATTERN, "TRIM"),
        ]:
            for match in pattern.finditer(text):
                entities.append(Entity(label=label, value=match.group().strip(), start=match.start(), end=match.end()))
        return entities

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Return detected entities for downstream enrichment."""

        entities = [
            {
                "label": entity.label,
                "value": entity.value,
                "start": entity.start,
                "end": entity.end,
                "source": "regex",
            }
            for entity in self._regex_entities(text)
        ]

        if self._hf_pipeline is not None:
            try:
                hf_entities = self._hf_pipeline(text)
                for ent in hf_entities:
                    entities.append(
                        {
                            "label": ent.get("entity_group", "HF"),
                            "value": ent.get("word", ""),
                            "start": ent.get("start", 0),
                            "end": ent.get("end", 0),
                            "source": "hf",
                        }
                    )
            except Exception as exc:  # pragma: no cover - runtime fallback
                LOGGER.error("HF NER pipeline failed: %s", exc)
        return entities


ner_pipeline = NERPipeline()
