
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse, JsonResponse


def healthcheck(_request):
    return JsonResponse({"status": "ok", "service": "fora"})


def readiness(_request):
    try:
        connections["default"].ensure_connection()
    except OperationalError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ready", "database": "ok"})


def robots_txt(request):
    sitemap_url = f"{settings.APP_URL.rstrip('/')}/sitemap.xml"
    return HttpResponse(
        f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /ops/\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )
