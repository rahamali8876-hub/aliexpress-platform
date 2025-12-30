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
        from core.domains.products.adapters.inbound.admin.product_admin import (
            ProductAdmin,
        )
        from core.domains.products.adapters.inbound.admin.variant_admin import (
            VariantAdmin,
        )

        # from core.domains.products.adapters.inbound.admin.outbox_admin import (
        #     ProductOutboxAdmin,
        # )
