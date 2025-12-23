# # from core.domains.products.adapters.outbound.persistence.models.product_model import ProductModel

# from django.db import models


# class ProductModel(models.Model):
#     id = models.UUIDField(primary_key=True)
#     seller_id = models.UUIDField()
#     title = models.CharField(max_length=255)

# above is old code and below is new code which one should i choose, after below code facing this error 

from django.db import models
import uuid


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_id = models.UUIDField()
    title = models.CharField(max_length=255)
    # is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.title
