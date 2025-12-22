# from core.domains.orders.saga.checkout_saga_consumer import CheckoutSagaConsumer


from core.shared.infrastructure.kafka_consumer import create_consumer
from .checkout_saga import CheckoutSaga

TOPICS = [
    "order.created",
    "inventory.reserved",
    "payment.authorized",
    "payment.failed",
]

GROUP_ID = "checkout-saga"


def run_checkout_saga():
    saga = CheckoutSaga()
    consumer = create_consumer(TOPICS, GROUP_ID)

    for message in consumer:
        event = message.value
        event_type = event.get("type")

        try:
            if event_type == "order.created":
                saga.on_order_created(event)

            elif event_type == "inventory.reserved":
                saga.on_inventory_reserved(event)

            elif event_type == "payment.authorized":
                saga.on_payment_authorized(event)

            elif event_type == "payment.failed":
                saga.on_payment_failed(event)

            consumer.commit()
        except Exception:
            # do not commit → retry
            continue
