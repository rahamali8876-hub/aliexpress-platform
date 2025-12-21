# from django.db import models
# import uuid


# class ProductOutbox(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     event_type = models.CharField(max_length=100)
#     payload = models.JSONField()
#     published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
import uuid


class ProductOutbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_outbox"
        indexes = [
            models.Index(fields=["published", "created_at"]),
        ]
