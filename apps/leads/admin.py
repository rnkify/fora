from django.contrib import admin

from apps.leads.models import Company, Contact, Lead, LeadActivity


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "size_band", "country", "created_at")
    search_fields = ("name", "website", "industry", "country")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "role", "created_at")
    search_fields = ("name", "email", "role", "company__name")
    list_filter = ("company",)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "status",
        "source",
        "score",
        "estimated_value",
        "next_action_at",
        "created_at",
    )
    list_filter = ("status", "source")
    search_fields = (
        "company__name",
        "primary_contact__name",
        "primary_contact__email",
        "notes",
    )


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ("lead", "type", "occurred_at", "created_at")
    list_filter = ("type",)
    search_fields = ("lead__company__name", "note")
