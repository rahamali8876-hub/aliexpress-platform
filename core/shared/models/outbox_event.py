# filename : core/shared/models/outbox_event.py
from django.db import models
import uuid


class OutboxEvent(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PUBLISHED", "Published"),
        ("FAILED", "Failed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aggregate_id = models.UUIDField()
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    created_at = models.DateTimeField(auto_now_add=True)
