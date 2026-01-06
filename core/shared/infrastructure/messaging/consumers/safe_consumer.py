# # filename : core/shared/infrastructure/messaging/consumers/safe_consumer.py
# import time

# from core.shared.infrastructure.messaging.dlq.dlq_producer import DLQProducer
# from core.shared.infrastructure.messaging.schemas.validators import (
#     JsonSchemaValidator,
#     SchemaValidationError,
# )
# from core.shared.observability.metrics.metrics import ConsumerMetrics
# from django.conf import settings


# class SafeConsumer:
#     MAX_RETRIES = 3
#     RETRY_DELAY_SECONDS = 2

#     def __init__(self, topic: str):
#         self.topic = topic
#         # self.dlq_producer = DLQProducer()
#         self.dlq_producer = DLQProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

#     def process(self, message: dict):
#         # 1️⃣ Schema validation
#         try:
#             JsonSchemaValidator.validate(message)
#         except SchemaValidationError as e:
#             ConsumerMetrics.increment_dlq(self.topic, "schema_error")
#             self.dlq_producer.send_to_dlq(self.topic, message, reason=str(e))
#             return

#         # 2️⃣ Retry loop
#         for attempt in range(1, self.MAX_RETRIES + 1):
#             try:
#                 self.handle(message)
#                 return
#             except Exception as e:
#                 ConsumerMetrics.increment_retry(self.topic)

#                 if attempt >= self.MAX_RETRIES:
#                     ConsumerMetrics.increment_dlq(self.topic, "retry_exhausted")
#                     self.dlq_producer.send_to_dlq(self.topic, message, reason=str(e))
#                     return

#                 time.sleep(self.RETRY_DELAY_SECONDS)

#     def handle(self, message: dict):
#         """
#         Implemented by concrete consumers
#         """
#         raise NotImplementedError

# filename : core/shared/infrastructure/messaging/consumers/safe_consumer.py

import time
from django.conf import settings

from core.shared.infrastructure.messaging.dlq.dlq_producer import DLQProducer
from core.shared.infrastructure.messaging.schemas.validators import (
    JsonSchemaValidator,
    SchemaValidationError,
)
from core.shared.observability.metrics.consumer_metrics import ConsumerMetrics


class SafeConsumer:
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    def __init__(self, topic: str):
        self.topic = topic
        self.dlq_producer = DLQProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )

    def process(self, message: dict):
        # 1️⃣ Schema validation
        try:
            JsonSchemaValidator.validate(message)
        except SchemaValidationError as e:
            ConsumerMetrics.increment_dlq(self.topic, "schema_error")
            self.dlq_producer.send_to_dlq(self.topic, message, reason=str(e))
            return

        # 2️⃣ Retry loop
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                self.handle(message)
                return
            except Exception as e:
                ConsumerMetrics.increment_retry(self.topic)

                if attempt >= self.MAX_RETRIES:
                    ConsumerMetrics.increment_dlq(self.topic, "retry_exhausted")
                    self.dlq_producer.send_to_dlq(self.topic, message, reason=str(e))
                    return

                time.sleep(self.RETRY_DELAY_SECONDS)

    def handle(self, message: dict):
        raise NotImplementedError
