# filename : core/shared/kernel/domain_event.py
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class DomainEvent(ABC):
    aggregate_id: UUID
    occurred_at: datetime

    @property
    @abstractmethod
    def event_type(self) -> str:
        """
        Stable public contract.
        Example: 'product.created'
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def event_version(self) -> int:
        """
        Event schema version.
        MUST increase when payload structure changes.
        """
        raise NotImplementedError

    @abstractmethod
    def to_primitives(self) -> dict:
        """
        Version-specific payload.
        """
        pass
