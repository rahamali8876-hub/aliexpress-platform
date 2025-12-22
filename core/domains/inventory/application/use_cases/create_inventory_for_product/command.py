# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand
class CreateInventoryForProductCommand:
    def __init__(self, product_id):
        self.product_id = product_id
