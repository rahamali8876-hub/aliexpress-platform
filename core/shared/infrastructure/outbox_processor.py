# from django.db import transaction
# from core.shared.models.outbox_event import OutboxEvent


# class OutboxProcessor:
#     def __init__(self, producer):
#         self.producer = producer

#     def process_batch(self, batch_size: int = 50):
#         events = (
#             OutboxEvent.objects.select_for_update(skip_locked=True)
#             .filter(status="PENDING")
#             .order_by("created_at")[:batch_size]
#         )

#         for event in events:
#             self._publish_event(event)

#     @transaction.atomic
#     def _publish_event(self, event: OutboxEvent):
#         try:
#             self.producer.send(
#                 topic=event.event_type,
#                 value=event.payload,
#             )
#             event.status = "PUBLISHED"
#             event.save(update_fields=["status"])
#         except Exception:
#             event.status = "FAILED"
#             event.save(update_fields=["status"])
#             raise


from django.db import transaction
from core.shared.models.outbox_event import OutboxEvent


class OutboxProcessor:
    def __init__(self, producer):
        self.producer = producer

    def process_batch(self, batch_size: int = 50):
        with transaction.atomic():
            events = (
                OutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(status="PENDING")
                .order_by("created_at")[:batch_size]
            )

            for event in events:
                self._publish_event(event)

    def _publish_event(self, event: OutboxEvent):
        try:
            self.producer.send(
                topic=event.event_type,
                value=event.payload,
            )
            event.status = "PUBLISHED"
            event.save(update_fields=["status"])

        except Exception:
            event.status = "FAILED"
            event.save(update_fields=["status"])
            raise
