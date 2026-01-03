# filename: core/shared/infrastructure/messaging/event_envelope.py

from django.conf import settings
from core.shared.infrastructure.tracing import get_trace_id


def build_event_envelope(outbox_event):
    """
    Converts an OutboxEvent DB row into a Kafka-safe event envelope.
    Infra-only. Domains must never import this.
    """
    print(  # Debugging purposes
        "Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py : ",
        outbox_event.event_type,
    )
    return {
        "event_id": str(outbox_event.id),
        "event_type": outbox_event.event_type,  # e.g. product.created
        # "event_version": outbox_event.version,
        "event_version": outbox_event.event_version,  # ✅ INCLUDED
        "aggregate_type": outbox_event.aggregate_type,
        "aggregate_id": str(outbox_event.aggregate_id),
        "occurred_at": outbox_event.created_at.isoformat(),
        "producer": settings.SERVICE_NAME,
        "trace_id": get_trace_id(),
        "payload": outbox_event.payload,
    }
