# core/shared/infrastructure/events/event_envelope.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import UUID


@dataclass(frozen=True)
class EventEnvelope:
    event_id: UUID
    event_type: str
    event_version: int

    aggregate_type: str
    aggregate_id: str
    aggregate_version: int

    occurred_at: datetime
    published_at: datetime | None

    producer: Dict[str, str]
    trace: Dict[str, str]

    payload: Dict[str, Any]
