git from django.core.management.base import BaseCommand
from core.domains.products.adapters.inbound.consumer.product_event_consumer import (
    run_product_search_consumer,
)


class Command(BaseCommand):
    help = "Run product search consumer (ElasticSearch)"

    def handle(self, *args, **options):
        self.stdout.write("Product Search Consumer started")
        run_product_search_consumer()
