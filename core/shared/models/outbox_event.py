# filename : core/shared/models/outbox_event.py

from django.db import models
import uuid
from django.utils import timezone


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

    retry_count = models.IntegerField(default=0)  # ✅ NEW
    published_at = models.DateTimeField(null=True)  # ✅ NEW

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shared_outbox_event"
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
