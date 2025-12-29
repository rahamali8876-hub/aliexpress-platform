# filename : core/shared/observability/metrics.py
# from prometheus_client import Counter, Histogram
from prometheus_client import Counter, Histogram, Gauge

EVENTS_PROCESSED = Counter(
    "events_processed_total",
    "Total events processed",
    ["consumer", "event_type"],
)

EVENT_PROCESSING_TIME = Histogram(
    "event_processing_seconds",
    "Event processing time",
    ["consumer"],
)

EVENT_FAILURES = Counter(
    "event_failures_total",
    "Total failed events",
    ["consumer", "event_type"],
)


# ========= PRODUCT METRICS =========
products_created_total = Counter(
    "products_created_total", "Total number of products created"
)

products_published_total = Counter(
    "products_published_total", "Total number of products published"
)

# ========= ORDER METRICS =========
orders_created_total = Counter("orders_created_total", "Total number of orders created")

orders_failed_total = Counter("orders_failed_total", "Total number of failed orders")

# ========= INFRA =========
api_request_latency = Histogram(
    "api_request_latency_seconds", "API request latency", ["method", "path"]
)

outbox_pending_events = Gauge(
    "outbox_pending_events", "Number of events waiting in outbox"
)
