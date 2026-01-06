# from prometheus_client import Counter

# # Total number of messages pushed to DLQ
# DLQ_COUNTER = Counter(
#     "consumer_dlq_total", "Total number of messages sent to DLQ", ["topic", "reason"]
# )

# # Total number of retry attempts
# RETRY_COUNTER = Counter(
#     "consumer_retry_total", "Total number of retries attempted per topic", ["topic"]
# )


# # ---- Outbox metrics ----

# EVENTS_PROCESSED_COUNTER = Counter(
#     "outbox_events_processed_total",
#     "Total outbox events successfully published to Kafka",
# )

# EVENTS_FAILED_COUNTER = Counter(
#     "outbox_events_failed_total",
#     "Total outbox events permanently failed",
# )

# EVENTS_RETRY_COUNTER = Counter(
#     "outbox_events_retry_total",
#     "Total outbox event publish retries",
# )


# core/shared/observability/metrics/counters.py
from prometheus_client import Counter

DLQ_COUNTER = Counter(
    "consumer_dlq_total",
    "Total number of messages sent to DLQ",
    ["topic", "reason"],
)

RETRY_COUNTER = Counter(
    "consumer_retry_total",
    "Total number of retries attempted per topic",
    ["topic"],
)
