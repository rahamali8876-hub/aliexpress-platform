# filename : core/domains/inventory/adapters/outbound/persistence/inventory_repository_impl.py

from core.domains.inventory.application.ports.outbound.inventory_repository import (
    InventoryRepository,
)
from .models.inventory_model import InventoryModel


class InventoryRepositoryImpl(InventoryRepository):
    def create_empty_inventory(self, product_id):
        InventoryModel.objects.get_or_create(
            product_id=product_id,
            defaults={"quantity": 0},
        )
