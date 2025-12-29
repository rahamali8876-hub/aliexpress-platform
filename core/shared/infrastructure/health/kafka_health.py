# # from confluent_kafka import AdminClient
# # from django.conf import settings
# # from .base import HealthCheck


# # class KafkaHealthCheck(HealthCheck):
# #     name = "kafka"

# #     def check(self) -> bool:
# #         try:
# #             admin = AdminClient({
# #                 "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS
# #             })
# #             metadata = admin.list_topics(timeout=2)
# #             return bool(metadata.brokers)
# #         except Exception:
# #             return False

from kafka import KafkaAdminClient
from django.conf import settings
from .base import HealthCheck


class KafkaHealthCheck(HealthCheck):
    name = "kafka"

    def check(self) -> bool:
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                request_timeout_ms=2000,
                api_version_auto_timeout_ms=2000,
            )
            admin.list_topics()
            admin.close()
            return True
        except Exception:
            return False


# from confluent_kafka import Consumer
# from django.conf import settings
# from .base import HealthCheck


# class KafkaHealthCheck(HealthCheck):
#     name = "kafka"

#     def check(self) -> bool:
#         consumer = None
#         try:
#             consumer = Consumer(
#                 {
#                     "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
#                     "group.id": "health-check",
#                     "socket.timeout.ms": 2000,
#                     "session.timeout.ms": 2000,
#                 }
#             )

#             # Metadata fetch = broker reachable
#             metadata = consumer.list_topics(timeout=2)
#             return bool(metadata.brokers)

#         except Exception:
#             return False

#         finally:
#             if consumer:
#                 consumer.close()
