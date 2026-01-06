# # filename: core/shared/infrastructure/messaging/outbox_processor.py

# import logging
# from django.utils import timezone

# from core.shared.models.outbox_event import OutboxEvent
# from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
# from core.shared.infrastructure.messaging.event_routing import route_event
# from core.shared.observability.metrics.outbox_metrics import (
#     EVENTS_PROCESSED_COUNTER,
#     EVENTS_FAILED_COUNTER,
#     EVENTS_RETRY_COUNTER,
# )

# logger = logging.getLogger(__name__)


# class OutboxProcessor:
#     def __init__(self, producer):
#         self.producer = producer

#     def publish(self, event: OutboxEvent):
#         envelope = build_event_envelope(event)
#         topic = route_event(event.event_type)

#         future = self.producer.send(
#             topic=topic,
#             key=str(event.aggregate_id).encode("utf-8"),
#             value=envelope,
#         )

#         future.get(timeout=10)  # ACK only


# # class OutboxProcessor:
# #     """
# #     Low-level Outbox → Kafka publisher.
# #     Should be used by OutboxPublisher only.
# #     """

# #     def __init__(self, producer, max_retries: int = 5):
# #         self.producer = producer
# #         self.max_retries = max_retries

# #     def _publish_event(self, event: OutboxEvent):
# #         try:
# #             envelope = build_event_envelope(event)
# #             topic = route_event(event.event_type)

# #             future = self.producer.send(
# #                 topic=topic,
# #                 key=str(event.aggregate_id).encode("utf-8"),
# #                 value=envelope,
# #             )

# #             # Force ACK
# #             future.get(timeout=10)

# #             updated = OutboxEvent.objects.filter(id=event.id, status="PENDING").update(
# #                 status="PUBLISHED",
# #                 published_at=timezone.now(),
# #             )

# #             if updated == 0:
# #                 logger.warning("Outbox event already processed: %s", event.id)

# #             EVENTS_PROCESSED_COUNTER.inc()

# #             logger.info(
# #                 "Outbox event published",
# #                 extra={
# #                     "event_id": event.id,
# #                     "aggregate_id": str(event.aggregate_id),
# #                     "event_type": event.event_type,
# #                     "topic": topic,
# #                     "trace_id": envelope.get("trace_id"),
# #                 },
# #             )

# #         except Exception:
# #             event.retry_count += 1
# #             EVENTS_RETRY_COUNTER.inc()

# #             if event.retry_count >= self.max_retries:
# #                 event.status = "FAILED"
# #                 EVENTS_FAILED_COUNTER.inc()
# #                 logger.error("Outbox event moved to FAILED after retries: %s", event.id)

# #             event.save(update_fields=["retry_count", "status"])
# #             logger.exception("Failed to publish outbox event %s", event.id)


import logging
from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
from core.shared.infrastructure.messaging.event_routing import route_event
from core.shared.models.outbox_event import OutboxEvent

logger = logging.getLogger(__name__)


class OutboxProcessor:
    """
    Low-level Kafka publisher.
    NO retries.
    NO DB writes.
    NO metrics.
    """

    def __init__(self, producer):
        self.producer = producer

    def publish(self, event: OutboxEvent):
        logger.debug(
            "OutboxProcessor.publish called",
            extra={
                "event_id": str(event.id),
                "aggregate_id": str(event.aggregate_id),
                "event_type": event.event_type,
                "event_version": event.event_version,
            },
        )

        envelope = build_event_envelope(event)

        logger.debug(
            "Event envelope built",
            extra={
                "event_id": str(event.id),
                "trace_id": envelope.get("trace_id"),
                "payload_size": len(str(envelope.get("payload", {}))),
            },
        )

        topic = route_event(event.event_type)

        logger.debug(
            "Routing event to Kafka topic",
            extra={
                "event_id": str(event.id),
                "topic": topic,
            },
        )

        future = self.producer.send(
            topic=topic,
            key=str(event.aggregate_id).encode("utf-8"),
            value=envelope,
        )

        logger.debug(
            "Kafka send invoked, waiting for ACK",
            extra={
                "event_id": str(event.id),
                "topic": topic,
            },
        )

        record_metadata = future.get(timeout=10)

        logger.info(
            "Kafka event published successfully",
            extra={
                "event_id": str(event.id),
                "topic": record_metadata.topic,
                "partition": record_metadata.partition,
                "offset": record_metadata.offset,
            },
        )
