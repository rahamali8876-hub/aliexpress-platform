# filename : core/shared/kernel/base_aggregate.py
from uuid import UUID
from typing import List
from core.shared.kernel.domain_event import DomainEvent


class BaseAggregate:
    """
    Base class for all Aggregate Roots.

    Enforces:
    - Explicit aggregate identity
    - Domain event correctness
    - Safe event extraction for Outbox
    """

    __slots__ = ("_aggregate_id", "_domain_events")

    def __init__(self, *, aggregate_id: UUID):
        if aggregate_id is None:
            raise ValueError("aggregate_id must be provided")

        if not isinstance(aggregate_id, UUID):
            raise TypeError("aggregate_id must be a UUID")

        self._aggregate_id: UUID = aggregate_id
        self._domain_events: List[DomainEvent] = []

    @property
    def aggregate_id(self) -> UUID:
        return self._aggregate_id

    def raise_event(self, event: DomainEvent) -> None:
        if not isinstance(event, DomainEvent):
            raise TypeError("Only DomainEvent instances can be raised")

        if event.aggregate_id != self._aggregate_id:
            raise ValueError("Event aggregate_id does not match aggregate aggregate_id")

        self._domain_events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        """
        Returns and clears domain events.
        Called by application / outbox layer.
        """
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
