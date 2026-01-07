# # filename : core/shared/models/outbox_event.py

from django.db import models
import uuid


class OutboxEvent(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_FAILED = "FAILED"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_FAILED, "Failed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # this below two fields not optional for production but for demo purpose we keep it optional
    processing_owner = models.CharField(max_length=100, null=True, blank=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)

    # 🔑 Identity & ordering
    aggregate_id = models.UUIDField()
    aggregate_type = models.CharField(max_length=100)

    # 📦 Event contract
    event_type = models.CharField(max_length=255)
    event_version = models.PositiveIntegerField(default=1)

    payload = models.JSONField()

    # 🚦 Delivery
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    retry_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "shared_outbox_event"
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["aggregate_id"]),
        ]
