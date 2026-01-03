# # filename : core/shared/infrastructure/messaging/outbox_processor.py
# from django.db import transaction
# from django.utils import timezone
# import logging

# from core.shared.models.outbox_event import OutboxEvent
# from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
# from core.shared.infrastructure.messaging.event_routing import EVENT_TOPIC_MAP

# logger = logging.getLogger(__name__)


# class OutboxProcessor:
#     MAX_RETRIES = 5

#     def __init__(self, producer):
#         self.producer = producer

#     def process_batch(self, batch_size: int = 50):
#         with transaction.atomic():
#             events = list(
#                 OutboxEvent.objects.select_for_update(skip_locked=True)
#                 .filter(status="PENDING", retry_count__lt=self.MAX_RETRIES)
#                 .order_by("created_at")[:batch_size]
#             )

#         for event in events:
#             self._publish_event(event)

#     def _publish_event(self, event: OutboxEvent):
#         try:
#             envelope = build_event_envelope(event)

#             try:
#                 topic = EVENT_TOPIC_MAP[event.event_type]
#             except KeyError:
#                 raise RuntimeError(
#                     f"No Kafka topic defined for event type: {event.event_type}"
#                 )

#             self.producer.send(topic=topic, value=envelope)
#             self.producer.flush()

#             logger.info(
#                 "Event published",
#                 extra={
#                     "event_id": str(event.id),
#                     "event_type": event.event_type,
#                     "topic": topic,
#                     "trace_id": envelope["trace_id"],
#                 },
#             )

#             # 🔐 atomic status update
#             with transaction.atomic():
#                 updated = OutboxEvent.objects.filter(
#                     id=event.id, status="PENDING"
#                 ).update(
#                     status="PUBLISHED",
#                     published_at=timezone.now(),
#                 )

#                 if updated == 0:
#                     logger.warning(
#                         "Outbox event already processed: %s",
#                         event.id,
#                     )

#         except Exception as e:
#             with transaction.atomic():
#                 event.retry_count += 1
#                 if event.retry_count >= self.MAX_RETRIES:
#                     event.status = "FAILED"

#                 event.save(update_fields=["retry_count", "status"])

#             logger.exception(
#                 "Failed to publish outbox event %s",
#                 event.id,
#                 exc_info=e,
#             )

# filename : core/shared/infrastructure/messaging/outbox_processor.py
import logging
from django.db import transaction
from django.utils import timezone

from core.shared.models.outbox_event import OutboxEvent
from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
from core.shared.infrastructure.messaging.event_routing import EVENT_TOPIC_MAP

logger = logging.getLogger(__name__)


class OutboxProcessor:
    MAX_RETRIES = 5

    def __init__(self, producer):
        self.producer = producer

    def process_batch(self, batch_size: int = 50):
        with transaction.atomic():
            events = list(
                OutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(status="PENDING", retry_count__lt=self.MAX_RETRIES)
                .order_by("created_at")[:batch_size]
            )

        for event in events:
            self._publish_event(event)

    def _publish_event(self, event: OutboxEvent):
        try:
            envelope = build_event_envelope(event)

            try:
                topic = EVENT_TOPIC_MAP[event.event_type]
            except KeyError:
                raise RuntimeError(
                    f"No Kafka topic defined for event type: {event.event_type}"
                )

            self.producer.send(topic=topic, value=envelope)
            self.producer.flush()

            logger.info(
                "Event published",
                extra={
                    "event_id": event.id,
                    "event_type": event.event_type,
                    "topic": topic,
                    "trace_id": envelope["trace_id"],
                },
            )

            with transaction.atomic():
                updated = OutboxEvent.objects.filter(
                    id=event.id,
                    status="PENDING",
                ).update(
                    status="PUBLISHED",
                    published_at=timezone.now(),
                )

                if updated == 0:
                    logger.warning("Outbox event already processed: %s", event.id)

        except Exception:
            with transaction.atomic():
                event.retry_count += 1
                if event.retry_count >= self.MAX_RETRIES:
                    event.status = "FAILED"
                event.save(update_fields=["retry_count", "status"])

            logger.exception("Failed to publish outbox event %s", event.id)
