from django.core.management.base import BaseCommand
from core.domains.inventory.adapters.inbound.consumer.inventory_kafka_consumer import (
    run_inventory_consumer,
)


class Command(BaseCommand):
    help = "Run inventory Kafka consumer"

    def handle(self, *args, **options):
        self.stdout.write("Inventory consumer started")
        run_inventory_consumer()
