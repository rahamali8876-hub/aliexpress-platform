# from core.domains.orders.saga.events.commands import (
#     reserve_inventory_command,
#     request_payment_command,
#     confirm_order_command,
#     cancel_order_command,
#     release_inventory_command,
# )


def reserve_inventory_command(order_id):
    return {
        "type": "inventory.reserve",
        "order_id": order_id,
    }


def request_payment_command(order_id):
    return {
        "type": "payment.request",
        "order_id": order_id,
    }


def confirm_order_command(order_id):
    return {
        "type": "order.confirm",
        "order_id": order_id,
    }


def cancel_order_command(order_id):
    return {
        "type": "order.cancel",
        "order_id": order_id,
    }


def release_inventory_command(order_id):
    return {
        "type": "inventory.release",
        "order_id": order_id,
    }
