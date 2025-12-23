# from django.contrib import admin
# from core.domains.products.adapters.outbound.persistence.models.product_model import (
#     ProductModel,
# )


# @admin.register(ProductModel)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "title",
#         "seller_id",
#         # "is_published",
#         "created_at",
#     )

#     # list_filter = ("is_published",)
#     search_fields = ("title", "seller_id")
#     readonly_fields = ("id", "created_at", "updated_at")



from django.contrib import admin
from core.domains.products.adapters.outbound.persistence.models.product_model import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "seller_id",
        "title",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)
    search_fields = ("id", "seller_id", "title")

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False  # ❌ Products must be created via API

    def has_delete_permission(self, request, obj=None):
        return False  # ❌ Prevent destructive ops
