# # from dataclasses import dataclass
# # from uuid import UUID
# # from datetime import datetime


# # @dataclass(frozen=True)
# # class ProductCreated:
# #     product_id: UUID
# #     seller_id: UUID
# #     title: str
# #     created_at: datetime

# #     @property
# #     def event_type(self) -> str:
# #         return "ProductCreated"

# #     def to_primitives(self) -> dict:
# #         """
# #         Infrastructure-safe representation.
# #         No ORM, no JSON, no side effects.
# #         """
# #         return {
# #             "product_id": self.product_id,
# #             "seller_id": self.seller_id,
# #             "title": self.title,
# #             "created_at": self.created_at,
# #         }

# # this is new is all right now

# from dataclasses import dataclass
# from datetime import datetime
# from uuid import UUID
# from core.shared.kernel.domain_event import DomainEvent


# @dataclass(frozen=True)
# class ProductCreated(DomainEvent):
#     product_id: UUID
#     seller_id: UUID
#     title: str
#     created_at: datetime


from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from core.shared.kernel.domain_event import DomainEvent


@dataclass(frozen=True)
class ProductCreated(DomainEvent):
    aggregate_id: UUID
    seller_id: UUID
    title: str
    occurred_at: datetime

    def to_primitives(self) -> dict:
        return {
            "product_id": str(self.aggregate_id),
            "seller_id": str(self.seller_id),
            "title": self.title,
            "occurred_at": self.occurred_at.isoformat(),
        }
