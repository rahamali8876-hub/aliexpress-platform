# from django.contrib import admin
# from core.domains.products.adapters.outbound.persistence.models.variant_model import (
#     VariantModel,
# )


# @admin.register(VariantModel)
# class VariantAdmin(admin.ModelAdmin):
#     list_display = ("id", "product_id", "sku", "price", "created_at")
#     search_fields = ("sku", "product_id")
#     readonly_fields = ("id", "created_at")


from django.contrib import admin
from core.domains.products.adapters.outbound.persistence.models.variant_model import (
    VariantModel,
)


@admin.register(VariantModel)
class VariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_id",
        "sku",
        "price",
        "created_at",
    )

    list_filter = ("created_at",)
    search_fields = ("id", "product_id", "sku")

    readonly_fields = (
        "id",
        "product_id",
        "created_at",
    )

    def has_add_permission(self, request):
        return False  # ❌ Variants via domain rules only

    def has_delete_permission(self, request, obj=None):
        return False
