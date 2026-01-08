# filename : core/shared/infrastructure/messaging/envelope/event_envelope.py
from uuid import uuid4
from datetime import datetime, timezone


def build_event_envelope(outbox_event):
    return {
        "event_id": str(uuid4()),
        "event_type": outbox_event.event_type,
        "aggregate_id": str(outbox_event.aggregate_id),  # 🔑 REQUIRED
        "version": outbox_event.event_version,
        "occurred_at": datetime.now(tz=timezone.utc).isoformat(),
        "payload": outbox_event.payload,
        # "metadata": {
        #     "source": outbox_event.source,
        # },
    }


# def build_event_envelope(outbox_event):
#     return {
#         "event_id": str(uuid4()),
#         "event_type": outbox_event.event_type,
#         "version": outbox_event.event_version,
#         "occurred_at": datetime.now(tz=timezone.utc).isoformat(),
#         "payload": outbox_event.payload,
#     }
