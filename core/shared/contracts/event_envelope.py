# filename : core/shared/contracts/event_envelope.py
from datetime import datetime


def build_event(
    *,
    event_type: str,
    aggregate_id: str,
    payload: dict,
    version: int = 1,
    retry_count: int = 0,
):
    return {
        "type": event_type,
        "aggregate_id": aggregate_id,
        "payload": payload,
        "version": version,
        "retry_count": retry_count,
        "occurred_at": datetime.utcnow().isoformat(),
    }
