# filename : core/shared/infrastructure/messaging/dlq/dlq_producer.py
import json
import os
from kafka import KafkaProducer

DLQ_TOPIC_PREFIX = os.getenv("DLQ_TOPIC_PREFIX", "dlq.")
GROUP_ID = "product-dlq-consumer-group"


class DLQProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_to_dlq(self, original_topic, envelope, reason):
        dlq_topic = f"{DLQ_TOPIC_PREFIX}{original_topic}"

        message = {
            "original_topic": original_topic,
            "event_id": envelope.get("event_id"),
            "event_type": envelope.get("event_type"),
            "version": envelope.get("version"),
            "occurred_at": envelope.get("occurred_at"),
            "payload": envelope.get("payload"),
            "reason": reason,
        }

        self.producer.send(dlq_topic, message)
        self.producer.flush()
