from django.contrib import admin

from apps.marketing.models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "company",
        "type",
        "handled",
        "created_at",
    )
    list_filter = ("type", "handled")
    search_fields = (
        "name",
        "email",
        "company",
        "website",
        "message",
    )
