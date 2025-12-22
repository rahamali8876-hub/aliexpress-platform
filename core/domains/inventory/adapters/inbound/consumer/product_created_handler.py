# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from core.domains.inventory.application.use_cases.create_inventory_for_product.handler import (
    CreateInventoryForProductHandler,
)
from core.domains.inventory.application.use_cases.create_inventory_for_product.command import (
    CreateInventoryForProductCommand,
)
from core.domains.inventory.adapters.outbound.persistence.inventory_repository_impl import (
    InventoryRepositoryImpl,
)


class ProductCreatedHandler:
    def handle(self, event):
        command = CreateInventoryForProductCommand(product_id=event["aggregate_id"])

        handler = CreateInventoryForProductHandler(repository=InventoryRepositoryImpl())

        handler.handle(command)
