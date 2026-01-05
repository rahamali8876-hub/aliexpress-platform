# filename : core/domains/products/adapters/inbound/consumer/product_event_consumer.py

import logging
from core.shared.infrastructure.messaging.kafka_consumer import create_consumer
from core.shared.infrastructure.safe_consumer import safe_handle_event
from core.shared.infrastructure.logging import get_logger
from core.shared.infrastructure.tracing import start_span
from core.domains.products.read_model.projections.product_event_projection import (
    ProductEventProjection,
)

TOPICS = ["product.events"]
GROUP_ID = "product-event-consumer"

logger = get_logger("product-event-consumer")
projection = ProductEventProjection()


def handle_product_event(event: dict):
    event_type = event["event_type"]

    with start_span("product_event_projection"):
        if event_type in ("product.created", "product.updated"):
            logging.info(
                "indexing_product",
                extra={
                    "aggregate_id": event["aggregate_id"],
                },
                filename="core/domains/products/adapters/inbound/consumer/product_event_consumer.py",
            )
            projection.index(event["payload"])

        elif event_type == "product.deleted":
            projection.delete(event["aggregate_id"])

    logger.info(
        "processing_event",
        extra={
            "event_type": event_type,
            "aggregate_id": event["aggregate_id"],
        },
        filename="core/domains/products/adapters/inbound/consumer/product_event_consumer.py",
    )


def run_product_event_consumer():
    consumer = create_consumer(TOPICS, GROUP_ID)

    for message in consumer:
        safe_handle_event(
            event=message.value,
            topic=message.topic,
            handler_fn=handle_product_event,
            consumer_name=GROUP_ID,
        )
        consumer.commit()
