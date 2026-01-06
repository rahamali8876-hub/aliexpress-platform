# # filename : core/shared/observability/metrics/metrics.py

# from prometheus_client import Counter, Histogram, Gauge
# from core.shared.observability.metrics.counters import (
#     DLQ_COUNTER,
#     RETRY_COUNTER,
# )


# EVENTS_PROCESSED = Counter(
#     "events_processed_total",
#     "Total events processed",
#     ["consumer", "event_type"],
# )

# EVENT_PROCESSING_TIME = Histogram(
#     "event_processing_seconds",
#     "Event processing time",
#     ["consumer"],
# )

# EVENT_FAILURES = Counter(
#     "event_failures_total",
#     "Total failed events",
#     ["consumer", "event_type"],
# )


# class ConsumerMetrics:
#     @staticmethod
#     def increment_dlq(topic: str, reason: str):
#         DLQ_COUNTER.labels(topic=topic, reason=reason).inc()
#         print(f"[METRICS] DLQ incremented for topic={topic}, reason={reason}")

#     @staticmethod
#     def increment_retry(topic: str):
#         RETRY_COUNTER.labels(topic=topic).inc()
#         print(f"[METRICS] Retry incremented for topic={topic}")


# # ========= PRODUCT METRICS =========
# products_created_total = Counter(
#     "products_created_total", "Total number of products created"
# )

# products_published_total = Counter(
#     "products_published_total", "Total number of products published"
# )

# # ========= ORDER METRICS =========
# orders_created_total = Counter("orders_created_total", "Total number of orders created")

# orders_failed_total = Counter("orders_failed_total", "Total number of failed orders")

# # ========= INFRA =========
# api_request_latency = Histogram(
#     "api_request_latency_seconds", "API request latency", ["method", "path"]
# )

# outbox_pending_events = Gauge(
#     "outbox_pending_events", "Number of events waiting in outbox"
# )


# core/shared/observability/metrics/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# ========= CONSUMER =========
EVENTS_PROCESSED = Counter(
    "events_processed_total",
    "Total events processed",
    ["consumer", "event_type"],
)

EVENT_FAILURES = Counter(
    "event_failures_total",
    "Total failed events",
    ["consumer", "event_type"],
)

EVENT_PROCESSING_TIME = Histogram(
    "event_processing_seconds",
    "Event processing time",
    ["consumer"],
)

# ========= PRODUCT =========
products_created_total = Counter(
    "products_created_total",
    "Total number of products created",
)

products_published_total = Counter(
    "products_published_total",
    "Total number of products published",
)

# ========= ORDER =========
orders_created_total = Counter(
    "orders_created_total",
    "Total number of orders created",
)

orders_failed_total = Counter(
    "orders_failed_total",
    "Total number of failed orders",
)

# ========= API =========
api_request_latency = Histogram(
    "api_request_latency_seconds",
    "API request latency",
    ["method", "path"],
)

# ========= OUTBOX =========
outbox_pending_events = Gauge(
    "outbox_pending_events",
    "Number of events waiting in outbox",
)
