# from django.apps import AppConfig

# class ProductsConfig(AppConfig):
#     name = "core.domains.products"
#     label = "products"


from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.domains.products"
    label = "products"

    def ready(self):
        # import models so Django sees them
        from .adapters.outbound.persistence import models
