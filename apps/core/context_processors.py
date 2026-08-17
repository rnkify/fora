from django.conf import settings
from django.http import HttpRequest

from apps.core.configuration import get_configuration
from config.seo import PUBLIC_PAGE_SEO, SEO
from config.services import SERVICES


def fora_configuration(request: HttpRequest) -> dict:
    view_name = request.resolver_match.view_name if request.resolver_match else ""
    social_title, social_description = PUBLIC_PAGE_SEO.get(
        view_name,
        (SEO.default_title, SEO.default_description),
    )

    service_routes = {
        "marketing:service_ai_systems": "ai_systems",
        "marketing:service_conversion_copy": "conversion_copy",
        "marketing:service_content_systems": "content_systems",
        "marketing:service_automation": "automation_consulting",
    }
    service_id = service_routes.get(view_name)
    if service_id:
        service = SERVICES[service_id]
        social_title = f"{service.name} — Fora"
        social_description = service.short_description

    return {
        "fora": get_configuration(),
        "app_url": settings.APP_URL.rstrip("/"),
        "is_operations": view_name.startswith("operations:"),
        "social_title": social_title,
        "social_description": social_description,
    }
