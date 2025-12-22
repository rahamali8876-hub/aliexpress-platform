# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from django.db import models
import uuid


class CheckoutSagaState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order_id = models.UUIDField(unique=True)

    inventory_reserved = models.BooleanField(default=False)
    payment_authorized = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
