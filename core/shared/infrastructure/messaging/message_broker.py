# filename : core/shared/infrastructure/message_broker.py


import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from django.conf import settings
import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

_producer = None


def get_kafka_producer():
    global _producer

    if _producer:
        return _producer

    retries = 5
    delay = 3  # seconds

    for attempt in range(retries):
        try:
            _producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=5,
            )
            logging.info(
                "Kafka producer connected to %s",
                settings.KAFKA_BOOTSTRAP_SERVERS,
                filename="core/shared/infrastructure/messaging/message_broker.py",
            )
            return _producer
        except NoBrokersAvailable:
            if attempt == retries - 1:
                raise
            time.sleep(delay)

    return _producer


def publish_event(topic: str, event: dict):
    producer = get_kafka_producer()
    producer.send(topic, event)
    producer.flush()
