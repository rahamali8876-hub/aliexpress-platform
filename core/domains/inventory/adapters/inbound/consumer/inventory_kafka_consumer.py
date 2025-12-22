# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from core.shared.infrastructure.kafka_consumer import create_consumer
from .product_created_handler import ProductCreatedHandler

TOPICS = ["product.created"]
GROUP_ID = "inventory-service"


def run_inventory_consumer():
    consumer = create_consumer(TOPICS, GROUP_ID)
    handler = ProductCreatedHandler()

    for message in consumer:
        try:
            handler.handle(message.value)
            consumer.commit()
        except Exception:
            # log + retry later (do NOT commit)
            continue
