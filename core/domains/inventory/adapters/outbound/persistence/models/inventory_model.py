# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from django.db import models


class InventoryModel(models.Model):
    product_id = models.UUIDField(primary_key=True)
    quantity = models.IntegerField(default=0)


