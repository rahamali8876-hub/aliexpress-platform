# # from core.domains.products.adapters.outbound.persistence.models.product_model import ProductModel

from django.db import models
import uuid


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_id = models.UUIDField()
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    status = models.CharField(max_length=50, default="draft")
    # is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.title
