# from core.shared.infrastructure.kafka_producer import publish_event
from core.shared.infrastructure.message_broker import publish_event

DLQ_TOPIC = "dead_letter_queue"


def send_to_dlq(event: dict, reason: str):
    event["dlq_reason"] = reason
    publish_event(DLQ_TOPIC, event)
