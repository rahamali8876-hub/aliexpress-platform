
# core/shared/observability/metrics/consumer_metrics.py
from core.shared.observability.metrics.counters import (
    DLQ_COUNTER,
    RETRY_COUNTER,
)


class ConsumerMetrics:
    @staticmethod
    def increment_dlq(topic: str, reason: str):
        DLQ_COUNTER.labels(topic=topic, reason=reason).inc()

    @staticmethod
    def increment_retry(topic: str):
        RETRY_COUNTER.labels(topic=topic).inc()
