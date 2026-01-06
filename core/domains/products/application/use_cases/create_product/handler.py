# filenaeme: core/domains/products/application/use_cases/create_product/handler.py

import uuid
from django.db import transaction
from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate
from core.shared.models.outbox_event import OutboxEvent
from core.shared.observability.metrics.metrics import products_created_total


class CreateProductHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        product_id = uuid.uuid4()

        with transaction.atomic():
            aggregate = ProductAggregate.create(
                product_id=product_id,
                seller_id=command.seller_id,
                title=command.title,
            )

            self.repository.save(aggregate)

            for event in aggregate.pull_domain_events():
                OutboxEvent.objects.create(
                    aggregate_id=event.aggregate_id,
                    # event_type=event.__class__.__name__,
                    # aggregate_type = event.aggregate_type
                    event_type=event.event_type,
                    event_version=event.event_version,
                    payload=event.to_primitives(),
                )

            products_created_total.inc()

        return aggregate


# class CreateProductHandler:
#     def __init__(self, repository):
#         self.repository = repository

#     def handle(self, command):
#         product_id = uuid.uuid4()

#         with transaction.atomic():
#             # 1️⃣ Create aggregate
#             aggregate = ProductAggregate.create(
#                 product_id=product_id,
#                 seller_id=command.seller_id,
#                 title=command.title,
#             )

#             # 2️⃣ Persist aggregate
#             self.repository.save(aggregate)

#             # 3️⃣ Persist domain events into shared outbox
#             for event in aggregate.pull_events():
#                 OutboxEvent.objects.create(
#                     aggregate_id=product_id,
#                     event_type=event.event_type,
#                     event_version=event.event_version,  # ✅ NEW
#                     payload=event.to_primitives(),  # ✅ must use to_primitives()
#                 )

#             # 4️⃣ Metrics
#             products_created_total.inc()

#         return aggregate
