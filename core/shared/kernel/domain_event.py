# # filename : core/shared/kernel/domain_event.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent(ABC):
    aggregate_id: UUID
    occurred_at: datetime = field(
        default_factory=datetime.utcnow,
        init=False,  # ✅ KEY FIX
        repr=True,
    )

    @property
    @abstractmethod
    def event_type(self) -> str:
        pass

    @property
    @abstractmethod
    def event_version(self) -> int:
        pass

    @abstractmethod
    def to_primitives(self) -> dict:
        pass
