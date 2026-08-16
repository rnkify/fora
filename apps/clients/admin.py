from django.contrib import admin

from apps.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company", "status", "since", "created_at")
    list_filter = ("status",)
    search_fields = ("company__name", "company__website", "notes")
