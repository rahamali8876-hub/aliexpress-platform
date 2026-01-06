# filename: core/shared/infrastructure/messaging/outbox_processor.py

import logging
from django.db import transaction
from django.utils import timezone

from core.shared.models.outbox_event import OutboxEvent
from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
from core.shared.infrastructure.messaging.event_routing import route_event

# from core.shared.observability.metrics.prometheus import (
#     EVENTS_PROCESSED_COUNTER,
#     EVENTS_FAILED_COUNTER,
#     EVENTS_RETRY_COUNTER,
# )
from core.shared.observability.metrics.metrics import (
    EVENTS_PROCESSED_COUNTER,
    EVENTS_FAILED_COUNTER,
    EVENTS_RETRY_COUNTER,
)

logger = logging.getLogger(__name__)


class OutboxProcessor:
    """
    Low-level Outbox → Kafka publisher.
    Should be used by OutboxPublisher only.
    """

    def __init__(self, producer, max_retries: int = 5):
        self.producer = producer
        self.max_retries = max_retries

    def _publish_event(self, event: OutboxEvent):
        """
        Publish a single OutboxEvent safely:

        - Wraps payload in envelope
        - Routes to correct Kafka topic
        - Sends with aggregate_id key for ordering
        - Waits for ACK before marking PUBLISHED
        - Handles retries and failure
        """
        try:
            envelope = build_event_envelope(event)

            # Route to Kafka topic
            topic = route_event(event.event_type)

            # Send with key = aggregate_id (ensures ordering)
            future = self.producer.send(
                topic=topic,
                key=str(event.aggregate_id).encode("utf-8"),
                value=envelope,
            )

            # Force ACK (exactly-once)
            future.get(timeout=10)

            # ✅ Update Outbox atomically
            updated = OutboxEvent.objects.filter(id=event.id, status="PENDING").update(
                status="PUBLISHED", published_at=timezone.now()
            )

            if updated == 0:
                logger.warning("Outbox event already processed: %s", event.id)

            # Metrics
            EVENTS_PROCESSED_COUNTER.inc()

            logger.info(
                "Outbox event published",
                extra={
                    "event_id": event.id,
                    "aggregate_id": str(event.aggregate_id),
                    "event_type": event.event_type,
                    "topic": topic,
                    "trace_id": envelope.get("trace_id"),
                },
            )

        except Exception as exc:
            # Retry logic
            event.retry_count += 1
            EVENTS_RETRY_COUNTER.inc()

            if event.retry_count >= self.max_retries:
                event.status = "FAILED"
                EVENTS_FAILED_COUNTER.inc()
                logger.error("Outbox event moved to FAILED after retries: %s", event.id)

            event.save(update_fields=["retry_count", "status"])
            logger.exception("Failed to publish outbox event %s", event.id)
