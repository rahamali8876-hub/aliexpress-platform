# filename : core/shared/infrastructure/messaging/broker/kafka_producer.py
import json
import time
import logging
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from django.conf import settings

logger = logging.getLogger("kafka-producer")

_producer = None


def get_kafka_producer():
    global _producer
    if _producer:
        return _producer

    retries = 5
    delay = 3

    for attempt in range(retries):
        try:
            _producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                key_serializer=lambda k: k.encode("utf-8"),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
                enable_idempotence=True,
                retries=5,
                linger_ms=10,
                batch_size=32768,
            )
            logger.info("Kafka producer connected")
            return _producer
        except NoBrokersAvailable:
            logger.warning("Kafka unavailable (%d/%d)", attempt + 1, retries)
            time.sleep(delay)

    raise RuntimeError("Kafka not available")
