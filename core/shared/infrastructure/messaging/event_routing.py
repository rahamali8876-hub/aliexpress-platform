# filename : core/shared/infrastructure/messaging/event_routing.py

from core.shared.infrastructure.messaging.topics import (
    PRODUCT_EVENTS_TOPIC,
    ORDER_EVENTS_TOPIC,
)

EVENT_TOPIC_MAP = {
    "product.created": PRODUCT_EVENTS_TOPIC,
    "product.updated": PRODUCT_EVENTS_TOPIC,
    "order.placed": ORDER_EVENTS_TOPIC,
}
