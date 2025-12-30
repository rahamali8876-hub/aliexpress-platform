# # filename : core/domains/products/domain/domain_events/product_created.py
# from dataclasses import dataclass
# from uuid import UUID
# from datetime import datetime
# from core.shared.kernel.domain_event import DomainEvent


# @dataclass(frozen=True)
# class ProductCreated(DomainEvent):
#     aggregate_id: UUID
#     seller_id: UUID
#     title: str
#     occurred_at: datetime

#     def to_primitives(self) -> dict:
#         return {
#             "product_id": str(self.aggregate_id),
#             "seller_id": str(self.seller_id),
#             "title": self.title,
#             "occurred_at": self.occurred_at.isoformat(),
#         }


# filename : core/domains/products/domain/domain_events/product_created.py

from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from core.shared.kernel.domain_event import DomainEvent


@dataclass(frozen=True)
class ProductCreated(DomainEvent):
    aggregate_id: UUID
    seller_id: UUID
    title: str
    occurred_at: datetime = field(default_factory=datetime.now)

    def to_primitives(self) -> dict:
        return {
            "product_id": str(self.aggregate_id),
            "seller_id": str(self.seller_id),
            "title": self.title,
            "occurred_at": self.occurred_at.isoformat(),
        }
    
