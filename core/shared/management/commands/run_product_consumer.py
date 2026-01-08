# filename : core/shared/management/commands/run_product_consumer
import logging
from django.core.management.base import BaseCommand
from core.shared.infrastructure.messaging.kafka_consumer import create_consumer
from core.shared.infrastructure.messaging.consumers.product_consumer import (
    ProductCreatedConsumer,
)

GROUP_ID = "product-command-consumer-group"


class Command(BaseCommand):
    help = "Run product Kafka consumer"

    def handle(self, *args, **options):
        consumer = create_consumer(
            topics=[
                "product.events",
            ],
            group_id=GROUP_ID,
        )
        handler = ProductCreatedConsumer()

        self.stdout.write("Product consumer started")
        logging.info(
            "Run product consumer Calling ->",
            filename="core/shared/management/commands/run_product_consumer.py",
        )

        for msg in consumer:
            handler.process(msg.value)
