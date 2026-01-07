
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
