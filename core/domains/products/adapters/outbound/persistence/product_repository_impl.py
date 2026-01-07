from core.domains.products.application.ports.outbound.product_repository import (
    ProductRepository,
)
from .models.product_model import ProductModel


# class ProductRepositoryImpl(ProductRepository):
#     def save(self, aggregate):
#         ProductModel.objects.create(
#             id=aggregate.product_id,  # ✅ map explicitly
#             seller_id=aggregate.seller_id,
#             title=aggregate.title,
#         )


# core/domains/products/adapters/outbound/persistence/product_repository_impl.py

# from core.domains.products.adapters.outbound.persistence.models import ProductModel


class ProductRepositoryImpl(ProductRepository):
    def save(self, aggregate):
        product = aggregate.product  # 👈 THIS IS THE KEY

        ProductModel.objects.create(
            id=aggregate.product_id,
            seller_id=product.seller_id,
            title=product.title,
        )
