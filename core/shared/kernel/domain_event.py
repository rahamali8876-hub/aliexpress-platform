# # from datetime import datetime
# # import uuid

# # class DomainEvent:
# #     event_id = uuid.uuid4()

# #     def __init__(self, aggregate_id):
# #         self.aggregate_id = aggregate_id
# #         self.occurred_at = datetime.utcnow()



# from dataclasses import asdict
# from uuid import UUID
# from datetime import datetime
# from core.shared.utils.json_encoder.uuid_encoder import dumps


# class DomainEvent:
#     @property
#     def event_type(self) -> str:
#         return self.__class__.__name__

#     def to_payload(self) -> dict:
#         return asdict(self)

#     def to_json(self) -> str:
#         return dumps(self.to_payload())


# filename : core/shared/kernel/domain_event.py
from abc import ABC
# from json import dumps
from uuid import UUID
from datetime import datetime


class DomainEvent(ABC):
    aggregate_id: UUID
    occurred_at: datetime

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def to_primitives(self) -> dict:
        raise NotImplementedError

    # def to_json(self) -> str:
    #     return dumps(self.to_primitives())
