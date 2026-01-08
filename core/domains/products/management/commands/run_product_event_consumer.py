# filename : core/domains/products/management/commands/run_product_event_consumer.py
import logging
from django.core.management.base import BaseCommand
from core.domains.products.adapters.inbound.consumer.product_event_consumer import (
    run_product_event_consumer,
)


class Command(BaseCommand):
    help = "Run product event consumer (Kafka)"

    def handle(self, *args, **options):
        self.stdout.write("Product Event Consumer started")
        logging.info(
            "Run product event consumer Calling -> into this file :- ",
            filename="core/domains/products/management/commands/run_product_event_consumer.py",
        )
        run_product_event_consumer()
