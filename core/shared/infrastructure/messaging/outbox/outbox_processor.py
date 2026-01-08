# # # filename: core/shared/infrastructure/messaging/outbox_processor.py
# import logging
# from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
# from core.shared.infrastructure.messaging.event_routing import route_event
# from core.shared.models.outbox_event import OutboxEvent


# logger = logging.getLogger(__name__)


# class OutboxProcessor:
#     """
#     Low-level Kafka publisher.
#     NO retries.
#     NO DB writes.
#     NO metrics.
#     """

#     def __init__(self, producer):
#         self.producer = producer

#     def publish(self, event: OutboxEvent):
#         logger.debug(
#             "OutboxProcessor.publish called",
#             extra={
#                 "event_id": str(event.id),
#                 "aggregate_id": str(event.aggregate_id),
#                 "event_type": event.event_type,
#                 "event_version": event.event_version,
#             },
#         )

#         envelope = build_event_envelope(event)

#         logger.debug(
#             "Event envelope built",
#             extra={
#                 "event_id": str(event.id),
#                 "trace_id": envelope.get("trace_id"),
#                 "payload_size": len(str(envelope.get("payload", {}))),
#             },
#         )

#         topic = route_event(event.event_type)

#         logger.debug(
#             "Routing event to Kafka topic",
#             extra={
#                 "event_id": str(event.id),
#                 "topic": topic,
#             },
#         )

#         future = self.producer.send(
#             topic=topic,
#             key=str(event.aggregate_id),  # ✅ STRING
#             value=envelope,
#         )

#         logger.debug(
#             "Kafka send invoked, waiting for ACK",
#             extra={
#                 "event_id": str(event.id),
#                 "topic": topic,
#             },
#         )

#         record_metadata = future.get(timeout=10)

#         logger.info(
#             "Kafka event published successfully",
#             extra={
#                 "event_id": str(event.id),
#                 "topic": record_metadata.topic,
#                 "partition": record_metadata.partition,
#                 "offset": record_metadata.offset,
#             },
#         )


import logging
from core.shared.infrastructure.messaging.envelope.event_envelope import (
    build_event_envelope,
)

from core.shared.infrastructure.messaging.routing.event_routing import route_event

logger = logging.getLogger(__name__)


class OutboxProcessor:
    def __init__(self, producer):
        self.producer = producer

    def publish(self, event):
        envelope = build_event_envelope(event)
        topic = route_event(event.event_type)

        future = self.producer.send(
            topic=topic,
            key=str(event.aggregate_id),
            value=envelope,
        )

        future.get(timeout=10)
        logger.info("Published event %s to %s", event.event_type, topic)
