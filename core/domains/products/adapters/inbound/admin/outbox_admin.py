
# # filename : core/domains/products/adapters/inbound/admin/outbox_admin.py
# from django.contrib import admin
# from core.domains.products.outbox.product_outbox_model import ProductOutbox


# @admin.register(ProductOutbox)
# class ProductOutboxAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "aggregate_id",
#         "event_type",
#         "status",
#         "created_at",
#     )

#     list_filter = ("status", "event_type", "created_at")
#     search_fields = ("id", "aggregate_id", "event_type")

#     ordering = ("-created_at",)

#     readonly_fields = (
#         "id",
#         "aggregate_id",
#         "event_type",
#         "payload",
#         "created_at",
#     )

#     actions = ["mark_as_pending"]

#     def has_add_permission(self, request):
#         return False  # ❌ Outbox is append-only

#     def has_delete_permission(self, request, obj=None):
#         return False  # ❌ Never delete events

#     @admin.action(description="Requeue failed events (mark as PENDING)")
#     def mark_as_pending(self, request, queryset):
#         queryset.filter(status="FAILED").update(status="PENDING")
