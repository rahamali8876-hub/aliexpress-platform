# from core.domains.inventory.application.use_cases.create_inventory_for_product.handler import CreateInventoryForProductHandler


class CreateInventoryForProductHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        self.repository.create_empty_inventory(command.product_id)
