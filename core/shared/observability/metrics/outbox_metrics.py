# core/shared/observability/metrics/outbox_metrics.py
from prometheus_client import Counter

EVENTS_PROCESSED_COUNTER = Counter(
    "outbox_events_processed_total",
    "Total outbox events successfully published to Kafka",
)

EVENTS_FAILED_COUNTER = Counter(
    "outbox_events_failed_total",
    "Total outbox events permanently failed",
)

EVENTS_RETRY_COUNTER = Counter(
    "outbox_events_retry_total",
    "Total outbox event publish retries",
)
