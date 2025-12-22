# from core.domains.orders.saga.management.commands.run_checkout_saga import Command

from django.core.management.base import BaseCommand
from core.domains.orders.saga.checkout_saga_consumer import run_checkout_saga

class Command(BaseCommand):
    help = "Run checkout saga"

    def handle(self, *args, **options):
        self.stdout.write("Checkout saga started")
        run_checkout_saga()
