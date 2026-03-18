from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from prgx_ag.schemas.enums import AuditStatus, IntentType


class AkashicEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender_id: str
    intent_type: IntentType
    payload: dict[str, Any] = Field(default_factory=dict)
    audit_status: AuditStatus = AuditStatus.PENDING
    integrity_hash: str = ""
    topic: str | None = None

    @field_validator("sender_id")
    @classmethod
    def _sender_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("topic")
    @classmethod
    def _normalize_topic(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    def compute_hash(self) -> str:
        serialized = json.dumps(
            {
                "id": self.id,
                "timestamp": self.timestamp.isoformat(),
                "sender_id": self.sender_id,
                "intent_type": self.intent_type.value,
                "payload": self.payload,
                "audit_status": self.audit_status.value,
                "topic": self.topic,
            },
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )
        self.integrity_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return self.integrity_hash
