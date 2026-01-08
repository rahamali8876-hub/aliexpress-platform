class OrderCreatedEvent:
    type = "order.created"
    event_version = 1

    def __init__(self, order):
        self.payload = {
            "order_id": str(order.id),
            "buyer_id": str(order.buyer_id),  # UUID only
            "total_amount": order.total.amount,
            "currency": order.total.currency,
            "status": order.status.value,
            "created_at": order.created_at.isoformat(),
        }
