from django.urls import path
from core.domains.products.adapters.inbound.rest.product_view import CreateProductView


urlpatterns = [
    path("products/", CreateProductView.as_view()),
]
