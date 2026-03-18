from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GemOfWisdom(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    lesson: str
    param_update: dict[str, float] = Field(default_factory=dict)
    safe_to_apply: bool = True

    @field_validator("lesson")
    @classmethod
    def _lesson_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("param_update")
    @classmethod
    def _coerce_param_update(cls, value: dict[str, float]) -> dict[str, float]:
        normalized: dict[str, float] = {}

        for key, delta in value.items():
            key_text = str(key).strip()
            if not key_text:
                raise ValueError("param_update contains a blank key")
            normalized[key_text] = float(delta)

        return normalized
