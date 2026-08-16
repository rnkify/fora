from django.contrib import admin

from apps.portfolio.models import PortfolioItem, Testimonial


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "kind",
        "service_id",
        "published",
        "featured",
        "position",
        "created_at",
    )
    list_filter = ("kind", "published", "featured", "service_id")
    search_fields = ("title", "slug", "summary")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "role",
        "approved",
        "featured",
        "created_at",
    )
    list_filter = ("approved", "featured")
    search_fields = ("name", "company", "role", "quote")
