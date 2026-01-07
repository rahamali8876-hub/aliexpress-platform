# # filename : core/domains/products/domain/aggregates/product_aggregate.py

# from core.shared.kernel.base_aggregate import BaseAggregate
# from ..entities.product import Product
# from ..domain_events.product_created import ProductCreated


# class ProductAggregate(BaseAggregate):
#     @classmethod
#     def create(cls, *, product_id, seller_id, title):
#         product = Product.create(
#             product_id=product_id,
#             seller_id=seller_id,
#             title=title,
#         )

#         # aggregate = cls(product_id)
#         aggregate = cls(aggregate_id=product_id)

#         # aggregate = cls(aggregate_id=product_id)

#         aggregate.product = product

#         aggregate.raise_event(
#             ProductCreated(
#                 aggregate_id=product_id,
#                 seller_id=seller_id,
#                 title=title,
#                 # occurred_at=datetime.now(),
#             )
#         )

#         return aggregate


# core/domains/products/domain/aggregates/product_aggregate.py

from core.shared.kernel.base_aggregate import BaseAggregate
from ..entities.product import Product
from ..domain_events.product_created import ProductCreated


class ProductAggregate(BaseAggregate):
    @classmethod
    def create(cls, *, product_id, seller_id, title):
        product = Product.create(
            product_id=product_id,
            seller_id=seller_id,
            title=title,
        )

        aggregate = cls(aggregate_id=product_id)
        aggregate.product = product

        aggregate.raise_event(
            ProductCreated(
                aggregate_id=product_id,
                seller_id=seller_id,
                title=title,
            )
        )

        return aggregate

    @property
    def product_id(self):
        """
        Explicit identity for Product aggregate.
        Avoids `.id` ambiguity across layers.
        """
        return self.aggregate_id
