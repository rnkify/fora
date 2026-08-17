from django.contrib import admin

from apps.projects.models import Project, ProjectActivity, ProjectTask


class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "service_name_snapshot",
        "plan_name_snapshot",
        "status",
        "price_snapshot",
        "currency",
        "due_at",
        "created_at",
    )
    list_filter = ("status", "currency")
    search_fields = (
        "client__company__name",
        "service_name_snapshot",
        "plan_name_snapshot",
        "scope",
        "notes",
    )
    inlines = [ProjectTaskInline]


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "due_at", "position")
    list_filter = ("status",)
    search_fields = ("title", "project__client__company__name")


@admin.register(ProjectActivity)
class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ("project", "type", "actor", "occurred_at")
    list_filter = ("type",)
    search_fields = ("project__client__company__name", "description")
    readonly_fields = ("created_at", "updated_at")
