from django.db import models


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True)
    seller_id = models.UUIDField()
    title = models.CharField(max_length=255)
