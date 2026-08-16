from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthcheck(_request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "fora",
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("ops/", include("apps.operations.urls")),
    path("health/", healthcheck, name="healthcheck"),
    path("", include("apps.marketing.urls")),
]
