# # filename : core/domains/products/domain/domain_events/product_created.py

from dataclasses import dataclass, field
from uuid import UUID
from core.shared.kernel.domain_event import DomainEvent


@dataclass(frozen=True)
class ProductCreated(DomainEvent):
    aggregate_id: UUID
    seller_id: UUID
    title: str

    event_type: str = field(init=False, default="product.created")
    event_version: int = field(init=False, default=1)

    def to_primitives(self) -> dict:
        return {
            "product_id": str(self.aggregate_id),
            "seller_id": str(self.seller_id),
            "title": self.title,
            # "occurred_at": self.occurred_at.isoformat(),
        }
