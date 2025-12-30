# filename : core/domains/products/outbox/product_outbox_model.py
from django.db import models
import uuid


class ProductOutbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    aggregate_id = models.UUIDField()
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PUBLISHED", "Published"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_outbox"
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
