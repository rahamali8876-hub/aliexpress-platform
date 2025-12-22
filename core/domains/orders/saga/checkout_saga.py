# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from .models.checkout_saga_state import CheckoutSagaState
from .events.commands import (
    reserve_inventory_command,
    request_payment_command,
    confirm_order_command,
    cancel_order_command,
    release_inventory_command,
)
from .publishers.saga_command_publisher import publish


class CheckoutSaga:
    def on_order_created(self, event):
        state, _ = CheckoutSagaState.objects.get_or_create(
            order_id=event["aggregate_id"]
        )

        self.reserve_inventory(event["aggregate_id"])

    def on_inventory_reserved(self, event):
        state = CheckoutSagaState.objects.get(order_id=event["order_id"])
        state.inventory_reserved = True
        state.save()

        self.request_payment(event["order_id"])

    def on_payment_authorized(self, event):
        state = CheckoutSagaState.objects.get(order_id=event["order_id"])
        state.payment_authorized = True
        state.completed = True
        state.save()

        self.confirm_order(event["order_id"])

    def on_payment_failed(self, event):
        self.release_inventory(event["order_id"])
        self.cancel_order(event["order_id"])

    # ---- Commands (outgoing) ----

    # ---- Commands (outgoing) ----

    def reserve_inventory(self, order_id):
        publish(reserve_inventory_command(order_id))

    def request_payment(self, order_id):
        publish(request_payment_command(order_id))

    def confirm_order(self, order_id):
        publish(confirm_order_command(order_id))

    def cancel_order(self, order_id):
        publish(cancel_order_command(order_id))

    def release_inventory(self, order_id):
        publish(release_inventory_command(order_id))
