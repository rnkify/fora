from types import SimpleNamespace
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.7

    routes = (
        "marketing:home",
        "marketing:services",
        "marketing:service_ai_systems",
        "marketing:service_conversion_copy",
        "marketing:service_content_systems",
        "marketing:service_automation",
        "marketing:pricing",
        "marketing:process",
        "marketing:work",
        "marketing:about",
        "marketing:faq",
        "marketing:contact",
        "marketing:start_project",
        "marketing:privacy",
        "marketing:terms",
    )

    def items(self):
        return self.routes

    def location(self, item):
        return reverse(item)

    def get_priority(self, item):
        return 1.0 if item == "marketing:home" else self.priority

    def get_urls(self, page=1, site=None, protocol=None):
        app_url = urlsplit(settings.APP_URL)
        canonical_site = SimpleNamespace(
            domain=app_url.netloc,
            name=app_url.netloc,
        )
        return super().get_urls(
            page=page,
            site=canonical_site,
            protocol=app_url.scheme or self.protocol,
        )
