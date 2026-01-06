# # filename : core/shared/infrastructure/message_broker.py


# import json
# import time
# from kafka import KafkaProducer
# from kafka.errors import NoBrokersAvailable
# from django.conf import settings
# import logging

# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# _producer = None


# def get_kafka_producer():
#     global _producer

#     if _producer:
#         return _producer

#     _producer = KafkaProducer(
#         bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
#         key_serializer=lambda k: k.encode("utf-8"),
#         value_serializer=lambda v: json.dumps(v).encode("utf-8"),
#         acks="all",
#         retries=5,
#         enable_idempotence=True,
#         linger_ms=10,
#         batch_size=32768,
#     )

#     return _producer


# filename: core/shared/infrastructure/messaging/message_broker.py

import json
import time
import logging
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from django.conf import settings

logger = logging.getLogger("kafka-producer")

_producer = None


def get_kafka_producer():
    """
    Returns a singleton KafkaProducer instance.
    Retries connection automatically.
    """
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
                retries=5,
                enable_idempotence=True,
                linger_ms=10,
                batch_size=32768,
            )
            logger.info(
                "Kafka producer connected to %s",
                settings.KAFKA_BOOTSTRAP_SERVERS,
            )
            return _producer
        except NoBrokersAvailable as e:
            logger.warning(
                "Kafka broker unavailable, attempt %d/%d", attempt + 1, retries
            )
            if attempt == retries - 1:
                logger.error("Kafka broker not available after %d attempts", retries)
                raise
            time.sleep(delay)

    return _producer


def publish_event(topic: str, key: str, value: dict, wait_ack: bool = True):
    """
    Publish event to Kafka with logging and optional ACK wait
    """
    producer = get_kafka_producer()
    logger.debug("Publishing event to topic=%s key=%s value=%s", topic, key, value)

    future = producer.send(topic=topic, key=key, value=value)

    if wait_ack:
        try:
            result = future.get(timeout=10)
            logger.debug("Kafka ack received: %s", result)
        except Exception as e:
            logger.exception("Failed to get Kafka ack for topic=%s key=%s", topic, key)
            raise

    # Flush is optional; KafkaProducer auto-flushes periodically
    producer.flush()
    logger.debug("Kafka flush done for topic=%s key=%s", topic, key)
