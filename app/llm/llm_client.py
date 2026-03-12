from __future__ import annotations

import json
from typing import Any

from openai import AsyncOpenAI
from pydantic import ValidationError

from app.config.settings import get_settings
from app.models.response_models import RootCauseReport


class LLMClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.dummy = settings.llm_dummy
        self._client: AsyncOpenAI | None = None
        if self.provider == "openai":
            self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, prompt: str) -> RootCauseReport:
        if self.dummy or self.provider != "openai" or self._client is None:
            return RootCauseReport(
                primary_cause="Dummy response (LLM disabled)",
                contributing_factors=[],
                timeline=[],
                evidence=[],
                confidence=0.0,
                next_steps=["Set LLM_DUMMY=false and configure API key"],
            )

        schema = {
            "type": "object",
            "properties": {
                "primary_cause": {"type": "string"},
                "contributing_factors": {"type": "array", "items": {"type": "string"}},
                "timeline": {"type": "array", "items": {"type": "string"}},
                "evidence": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "number"},
                "next_steps": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["primary_cause", "confidence"],
            "additionalProperties": False,
        }

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Return JSON only that matches the provided schema.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "root_cause_report",
                    "schema": schema,
                    "strict": True,
                },
            },
        )

        content = response.choices[0].message.content or "{}"
        try:
            data: dict[str, Any] = json.loads(content)
            return RootCauseReport(**data)
        except (json.JSONDecodeError, ValidationError):
            return RootCauseReport(
                primary_cause="Failed to parse LLM response",
                contributing_factors=[],
                timeline=[],
                evidence=[content],
                confidence=0.0,
                next_steps=["Inspect raw LLM response"],
            )
