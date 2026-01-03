# # # filename : core/shared/kernel/domain_event.py
# # from abc import ABC

# # # from json import dumps
# # from uuid import UUID
# # from datetime import datetime


# # class DomainEvent(ABC):
# #     aggregate_id: UUID
# #     occurred_at: datetime

# #     @property
# #     def event_type(self) -> str:
# #         return self.__class__.__name__

# #     def to_primitives(self) -> dict:
# #         raise NotImplementedError

# #     # def to_json(self) -> str:
# #     #     return dumps(self.to_primitives())

# from abc import ABC, abstractmethod
# from datetime import datetime
# from uuid import UUID


# class DomainEvent(ABC):
#     aggregate_id: UUID
#     occurred_at: datetime

#     @property
#     @abstractmethod
#     def event_type(self) -> str:
#         """
#         Stable event identifier.
#         MUST NOT depend on class name.
#         Example: 'product.created'
#         """
#         raise NotImplementedError

#     @abstractmethod
#     def to_primitives(self) -> dict:
#         raise NotImplementedError

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
