# filename : core/shared/infrastructure/messaging/event_routing.py

import logging

from core.shared.infrastructure.messaging.topics import (
    PRODUCT_EVENTS_TOPIC,
    ORDER_EVENTS_TOPIC,
)


EVENT_TOPIC_MAP = {
    "product.created": PRODUCT_EVENTS_TOPIC,
    "product.updated": PRODUCT_EVENTS_TOPIC,
    "order.placed": ORDER_EVENTS_TOPIC,
}


# below code added by my self
def route_event(event_type: str) -> str:
    """
    Routes an event type to its corresponding Kafka topic.
    Infra-only. Domains must never import this.
    """
    topic = EVENT_TOPIC_MAP.get(event_type)
    if not topic:
        logging.error(
            "No topic found for event type: %s in file: core/shared/infrastructure/messaging/event_routing.py",
            event_type,
            "below code added by my self ",
        )
        raise ValueError(f"No topic found for event type: {event_type}")
    return topic


# CALL route_event automatically when sending events to Kafka.
lambda event_type: route_event(event_type)
