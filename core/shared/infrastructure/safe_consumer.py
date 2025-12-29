# from core.shared.infrastructure.retry_policy import (
#     should_retry,
#     increment_retry,
# )
# from core.shared.infrastructure.kafka_producer import publish_event
# from core.shared.infrastructure.dlq_producer import send_to_dlq


# def safe_handle_event(
#     *,
#     event: dict,
#     topic: str,
#     handler_fn,
# ):
#     try:
#         handler_fn(event)

#     except Exception as exc:
#         if should_retry(event):
#             retry_event = increment_retry(event)
#             publish_event(topic, retry_event)
#         else:
#             send_to_dlq(event, str(exc))

# below is new code base and above is old code base

# import time
# from core.shared.infrastructure.metrics import (
#     EVENTS_PROCESSED,
#     EVENT_PROCESSING_TIME,
#     EVENT_FAILURES,
# )


# def safe_handle_event(*, event, topic, handler_fn, consumer_name):
#     start = time.time()

#     try:
#         handler_fn(event)

#         EVENTS_PROCESSED.labels(
#             consumer=consumer_name,
#             event_type=event["type"],
#         ).inc()

#     except Exception:
#         EVENT_FAILURES.labels(
#             consumer=consumer_name,
#             event_type=event["type"],
#         ).inc()
#         raise

#     finally:
#         EVENT_PROCESSING_TIME.labels(
#             consumer=consumer_name,
#         ).observe(time.time() - start)


import time
from core.shared.infrastructure.retry_policy import (
    should_retry,
    increment_retry,
)

# from core.shared.infrastructure.kafka_producer import publish_event
from core.shared.infrastructure.message_broker import publish_event
from core.shared.infrastructure.dlq_producer import send_to_dlq
from core.shared.observability.metrics.metrics import (
    EVENTS_PROCESSED,
    EVENT_PROCESSING_TIME,
    EVENT_FAILURES,
)


def safe_handle_event(
    *,
    event: dict,
    topic: str,
    handler_fn,
    consumer_name: str,
):
    start = time.time()

    try:
        handler_fn(event)

        EVENTS_PROCESSED.labels(
            consumer=consumer_name,
            event_type=event["type"],
        ).inc()

    except Exception as exc:
        EVENT_FAILURES.labels(
            consumer=consumer_name,
            event_type=event["type"],
        ).inc()

        if should_retry(event):
            retry_event = increment_retry(event)
            publish_event(topic, retry_event)
        else:
            send_to_dlq(event, str(exc))

    finally:
        EVENT_PROCESSING_TIME.labels(
            consumer=consumer_name,
        ).observe(time.time() - start)
