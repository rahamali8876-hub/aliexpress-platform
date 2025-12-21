from core.domains.products.application.ports.outbound.product_repository import (
    ProductRepository,
)
from .models.product_model import ProductModel


class ProductRepositoryImpl(ProductRepository):
    def save(self, aggregate):
        ProductModel.objects.create(
            id=aggregate.id,
            seller_id=aggregate.product.seller_id,
            title=aggregate.product.title,
        )
