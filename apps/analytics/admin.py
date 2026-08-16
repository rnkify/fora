from django.contrib import admin

from apps.analytics.models import AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "path",
        "lead_id",
        "project_id",
        "created_at",
    )
    list_filter = ("event",)
    search_fields = (
        "path",
        "referrer",
        "utm_source",
        "utm_medium",
        "utm_campaign",
    )
    readonly_fields = ("created_at", "updated_at")
