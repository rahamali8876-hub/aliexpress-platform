# # filename : core/shared/models/outbox_event.py
# from django.db import models
# import uuid
# from django.utils import timezone


# class OutboxEvent(models.Model):
#     STATUS_CHOICES = (
#         ("PENDING", "Pending"),
#         ("PUBLISHED", "Published"),
#         ("FAILED", "Failed"),
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     aggregate_id = models.UUIDField()
#     event_type = models.CharField(max_length=255)
#     payload = models.JSONField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
#     retry_count = models.IntegerField(default=0)  # ✅ Retry attempts
#     published_at = models.DateTimeField(null=True)  # ✅ Timestamp when published
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "shared_outbox_event"
#         indexes = [
#             models.Index(fields=["status", "created_at"]),
#         ]


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
    aggregate_type = models.CharField(max_length=100)

    event_type = models.CharField(max_length=255)
    event_version = models.PositiveIntegerField(default=1)

    payload = models.JSONField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    retry_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "shared_outbox_event"
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["event_type"]),
        ]


# from django.db import models


# class OutboxEvent(models.Model):
#     aggregate_id = models.UUIDField()
#     event_type = models.CharField(max_length=100)
#     event_version = models.PositiveIntegerField()  # ✅ NEW
#     payload = models.JSONField()

#     status = models.CharField(max_length=20, default="PENDING")
#     retry_count = models.PositiveIntegerField(default=0)

#     created_at = models.DateTimeField(auto_now_add=True)
#     published_at = models.DateTimeField(null=True, blank=True)
