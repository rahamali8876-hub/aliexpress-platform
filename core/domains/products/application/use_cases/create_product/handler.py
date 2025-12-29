# filename : core/domains/products/application/use_cases/create_product/handler.py

import uuid
from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate
from core.shared.observability.metrics.metrics import products_created_total


class CreateProductHandler:
    def __init__(self, repository, event_publisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command):
        product_id = uuid.uuid4()  # ✅ SYSTEM GENERATES ID

        aggregate = ProductAggregate.create(
            product_id=product_id,
            seller_id=command.seller_id,
            title=command.title,
        )

        self.repository.save(aggregate)
        self.event_publisher.publish_all(aggregate.pull_events())
        # sending metrics to prometheus
        products_created_total.inc()  # 👈 THIS IS THE KEY

        return aggregate  # optional but useful
