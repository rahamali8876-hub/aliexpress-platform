# # from django.db import transaction
# # from core.shared.models.outbox_event import OutboxEvent


# # class OutboxProcessor:
# #     def __init__(self, producer):
# #         self.producer = producer

# #     def process_batch(self, batch_size: int = 50):
# #         events = (
# #             OutboxEvent.objects.select_for_update(skip_locked=True)
# #             .filter(status="PENDING")
# #             .order_by("created_at")[:batch_size]
# #         )

# #         for event in events:
# #             self._publish_event(event)

# #     @transaction.atomic
# #     def _publish_event(self, event: OutboxEvent):
# #         try:
# #             self.producer.send(
# #                 topic=event.event_type,
# #                 value=event.payload,
# #             )
# #             event.status = "PUBLISHED"
# #             event.save(update_fields=["status"])
# #         except Exception:
# #             event.status = "FAILED"
# #             event.save(update_fields=["status"])
# #             raise


# # # filename : core/shared/infrastructure/outbox_processor.py
# # from django.db import transaction
# # from core.shared.models.outbox_event import OutboxEvent


# # class OutboxProcessor:
# #     def __init__(self, producer):
# #         self.producer = producer

# #     def process_batch(self, batch_size: int = 50):
# #         with transaction.atomic():
# #             events = (
# #                 OutboxEvent.objects.select_for_update(skip_locked=True)
# #                 .filter(status="PENDING")
# #                 .order_by("created_at")[:batch_size]
# #             )

# #             for event in events:
# #                 self._publish_event(event)

# #     def _publish_event(self, event: OutboxEvent):
# #         try:
# #             # self.producer.send(
# #             #     topic=event.event_type,
# #             #     value=event.payload,
# #             # )
# #             self.producer.send(
# #                 topic=event.event_type,
# #                 value={
# #                     "type": event.event_type,
# #                     "aggregate_id": str(event.aggregate_id),
# #                     "payload": event.payload,
# #                 },
# #             )

# #             event.status = "PUBLISHED"
# #             event.save(update_fields=["status"])

# #         except Exception:
# #             event.status = "FAILED"
# #             event.save(update_fields=["status"])
# #             raise

# # filename : core/shared/infrastructure/outbox_processor.py

# from django.db import transaction
# from django.utils import timezone
# from core.shared.models.outbox_event import OutboxEvent


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

#     # def _publish_event(self, event: OutboxEvent):
#     #     try:
#     #         self.producer.send(
#     #             topic=event.event_type,
#     #             value={
#     #                 "type": event.event_type,
#     #                 "aggregate_id": str(event.aggregate_id),
#     #                 "payload": event.payload,
#     #             },
#     #         )
#     #         self.producer.flush()

#     #         with transaction.atomic():
#     #             event.status = "PUBLISHED"
#     #             event.published_at = timezone.now()
#     #             event.save(update_fields=["status", "published_at"])

#     #     except Exception:
#     #         with transaction.atomic():
#     #             event.retry_count += 1
#     #             if event.retry_count >= self.MAX_RETRIES:
#     #                 event.status = "FAILED"

#     #             event.save(update_fields=["retry_count", "status"])
#     #         raise

#     def _publish_event(self, event: OutboxEvent):
#         try:
#             self.producer.send(
#                 topic=event.event_type,
#                 value={
#                     "type": event.event_type,
#                     "aggregate_id": str(event.aggregate_id),
#                     "payload": event.payload,
#                 },
#             )
#             self.producer.flush()

#             event.status = "PUBLISHED"
#             event.published_at = timezone.now()
#             event.save(update_fields=["status", "published_at"])

#         except Exception as e:
#             event.retry_count += 1

#             if event.retry_count >= self.MAX_RETRIES:
#                 event.status = "FAILED"

#             event.save(update_fields=["retry_count", "status"])

#             # ❌ DO NOT re-raise
#             # just log
#             logger.exception("Failed to publish outbox event", exc_info=e)

# from django.db import transaction
# from django.utils import timezone
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
