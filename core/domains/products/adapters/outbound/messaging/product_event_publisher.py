# from core.domains.products.application.ports.outbound.event_publisher_port import (
#     EventPublisherPort,
# )
# from core.domains.products.outbox.product_outbox_model import ProductOutbox

# # core/domains/products/adapters/outbound/messaging/product_event_publisher.py
# from core.shared.utils.json_encoder.uuid_encoder import dumps

# # class ProductEventPublisher(EventPublisherPort):

# #     def publish_all(self, events):
# #         for event in events:
# #             ProductOutbox.objects.create(
# #                 event_type=event.event_type,
# #                 payload={
# #                     "aggregate_id": event.aggregate_id,
# #                 }
# #             )


# # class ProductEventPublisher:
# #     def publish_all(self, events):
# #         for event in events:
# #             ProductOutbox.objects.create(
# #                 event_type=event.event_type,
# #                 payload=dumps(event.to_primitives())  # ✅ use centralized encoder
# #             )


# class ProductEventPublisher:
#     def publish_all(self, events):
#         for event in events:
#             ProductOutbox.objects.create(
#                 event_type=event.event_type,
#                 payload=event.to_json(),  # 🔥 canonical
#             )


from core.domains.products.outbox.product_outbox_model import ProductOutbox


class ProductEventPublisher:
    def publish_all(self, events):
        for event in events:
            ProductOutbox.objects.create(
                aggregate_id=event.aggregate_id,  # ✅ FIX
                event_type=event.event_type,
                payload=event.to_primitives(),
                status="PENDING",
            )
