# filename : core/shared/admin/outbox_admin.py

from django.contrib import admin
from core.shared.models.outbox_event import OutboxEvent


@admin.register(OutboxEvent)
class OutboxEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "aggregate_id",
        "event_type",
        "status",
        "retry_count",
        "published_at",
        "created_at",
    )
    list_filter = ("status", "event_type", "created_at")
    search_fields = ("id", "aggregate_id", "event_type")
    ordering = ("-created_at",)
    readonly_fields = (
        "id",
        "aggregate_id",
        "event_type",
        "payload",
        "created_at",
        "published_at",
        "retry_count",
    )

    # def has_add_permission(self, request):
    #     return False  # ❌ Outbox is append-only

    # def has_delete_permission(self, request, obj=None):
    #     return False  # ❌ Never delete events

    @admin.action(description="Requeue failed events (mark as PENDING)")
    def mark_as_pending(self, request, queryset):
        queryset.filter(status="FAILED").update(status="PENDING")
