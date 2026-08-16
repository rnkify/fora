import pytest
from django.urls import reverse

PUBLIC_ROUTES = (
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
)


@pytest.mark.django_db
@pytest.mark.parametrize("route_name", PUBLIC_ROUTES)
def test_public_route_returns_success(client, route_name):
    response = client.get(reverse(route_name))

    assert response.status_code == 200
