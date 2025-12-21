from core.domains.products.application.ports.outbound.event_publisher_port import EventPublisherPort
from core.domains.products.outbox.product_outbox_model import ProductOutbox

class ProductEventPublisher(EventPublisherPort):

    def publish_all(self, events):
        for event in events:
            ProductOutbox.objects.create(
                event_type=event.event_type,
                payload={
                    "aggregate_id": event.aggregate_id,
                }
            )

