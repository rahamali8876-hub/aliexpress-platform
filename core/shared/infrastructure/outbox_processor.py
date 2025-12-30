# filename : core/shared/infrastructure/outbox_processor.py

from core.shared.models.outbox_event import OutboxEvent
from django.db import transaction
from django.utils import timezone
import logging

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
            self.producer.send(
                topic=event.event_type,
                value={
                    "type": event.event_type,
                    "aggregate_id": str(event.aggregate_id),
                    "payload": event.payload,
                },
            )
            self.producer.flush()

            # 🔐 atomic status update
            with transaction.atomic():
                updated = (
                    OutboxEvent.objects
                    .filter(id=event.id, status="PENDING")
                    .update(
                        status="PUBLISHED",
                        published_at=timezone.now(),
                    )
                )

                if updated == 0:
                    logger.warning("Outbox event already processed: %s", event.id)

        except Exception as e:
            with transaction.atomic():
                event.retry_count += 1
                if event.retry_count >= self.MAX_RETRIES:
                    event.status = "FAILED"

                event.save(update_fields=["retry_count", "status"])

            logger.exception("Failed to publish outbox event", exc_info=e)
