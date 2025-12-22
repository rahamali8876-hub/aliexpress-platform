# from core.domains.orders.saga.publishers.saga_command_publisher import SagaCommandPublisher


from core.shared.infrastructure.message_broker import get_kafka_producer

producer = get_kafka_producer()


def publish(command):
    producer.send(command["type"], command)
