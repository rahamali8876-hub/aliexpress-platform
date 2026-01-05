# filename : core/shared/infrastructure/kafka_consumer.py

from kafka import KafkaConsumer
import json
from django.conf import settings


def create_consumer(topics, group_id):
    return KafkaConsumer(
        *topics,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        enable_auto_commit=False,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
    )
