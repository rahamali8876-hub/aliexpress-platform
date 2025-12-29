# filename : core/domains/products/adapters/inbound/consumer/product_search_consumer.py

from core.shared.infrastructure.kafka_consumer import create_consumer
from core.shared.infrastructure.safe_consumer import safe_handle_event
from core.shared.infrastructure.logging import get_logger
from core.shared.infrastructure.tracing import start_span
from core.domains.products.read_model.projections.product_search_projection import (
    ProductSearchProjection,
)

TOPICS = ["product.created", "product.updated", "product.deleted"]
GROUP_ID = "product-search-consumer"

logger = get_logger("product-search-consumer")
projection = ProductSearchProjection()


def handle_product_event(event: dict):
    event_type = event["type"]

    with start_span("product_search_projection"):
        if event_type in ("product.created", "product.updated"):
            projection.index(event["payload"])

        elif event_type == "product.deleted":
            projection.delete(event["aggregate_id"])

    logger.info(
        "processing_event",
        extra={
            "event_type": event_type,
            "aggregate_id": event["aggregate_id"],
            "retry_count": event.get("retry_count", 0),
        },
    )


def run_product_event_consumer():
    consumer = create_consumer(TOPICS, GROUP_ID)

    for message in consumer:
        safe_handle_event(
            event=message.value,
            topic=message.topic,
            handler_fn=handle_product_event,
            consumer_name="product-search-consumer",
        )
        consumer.commit()


# # filename : core/domains/products/adapters/inbound/consumer/product_search_consumer.py

# from core.shared.infrastructure.kafka_consumer import create_consumer
# from core.shared.infrastructure.safe_consumer import safe_handle_event
# from core.shared.infrastructure.logging import get_logger
# from core.shared.infrastructure.tracing import start_span
# from core.domains.products.read_model.projections.product_search_projection import (
#     ProductSearchProjection,
# )

# TOPICS = ["product.created", "product.updated", "product.deleted"]
# GROUP_ID = "product-search-consumer"

# logger = get_logger("product-search-consumer")
# projection = ProductSearchProjection()


# def handle_product_event(event: dict):
#     event_type = event["type"]

#     with start_span("product_search_projection"):
#         if event_type in ("product.created", "product.updated"):
#             projection.index(event["payload"])

#         elif event_type == "product.deleted":
#             projection.delete(event["aggregate_id"])

#     logger.info(
#         "processing_event",
#         extra={
#             "event_type": event_type,
#             "aggregate_id": event["aggregate_id"],
#             "retry_count": event.get("retry_count", 0),
#         },
#     )


# def run_product_event_consumer():
#     consumer = create_consumer(TOPICS, GROUP_ID)

#     for message in consumer:
#         safe_handle_event(
#             event=message.value,
#             topic=message.topic,
#             handler_fn=handle_product_event,
#             consumer_name="product-search-consumer",
#         )
#         consumer.commit()


# # # below is newcodebase above is old codebase

# # from core.shared.infrastructure.kafka_consumer import create_consumer

# # def run_product_event_consumer():
# #     consumer = create_consumer(
# #         topics=["product.created"],
# #         group_id="debug-product-consumer",
# #     )

# #     for message in consumer:
# #         print("EVENT RECEIVED:", message.value)
# #         consumer.commit()
