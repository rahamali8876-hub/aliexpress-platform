# # filename : core/shared/management/commands/process_outbox.py

from django.core.management.base import BaseCommand
from core.shared.infrastructure.messaging.outbox_publisher import OutboxPublisher


class Command(BaseCommand):
    help = "Process outbox events and publish to Kafka"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Outbox publisher (one-shot) started"))

        publisher = OutboxPublisher()
        publisher.run_once()
        # publisher.start()
