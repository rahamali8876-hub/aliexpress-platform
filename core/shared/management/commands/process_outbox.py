# filename : core/shared/management/commands/process_outbox.py

from django.core.management.base import BaseCommand
from core.shared.infrastructure.outbox_processor import OutboxProcessor
from core.shared.infrastructure.message_broker import get_kafka_producer


class Command(BaseCommand):
    help = "Process outbox events and publish to Kafka"

    def handle(self, *args, **options):
        self.stdout.write("Outbox processor started")

        producer = get_kafka_producer()
        processor = OutboxProcessor(producer=producer)

        processor.process_batch()
