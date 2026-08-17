import pytest
from django.test import RequestFactory, override_settings
from django.urls import reverse
from django.views.defaults import server_error

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
    "marketing:privacy",
    "marketing:terms",
)


@pytest.mark.django_db
@pytest.mark.parametrize("route_name", PUBLIC_ROUTES)
def test_public_route_returns_success(client, route_name):
    response = client.get(reverse(route_name))

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("route_name", "service_id"),
    (
        ("marketing:service_ai_systems", "ai_systems"),
        ("marketing:service_conversion_copy", "conversion_copy"),
        ("marketing:service_content_systems", "content_systems"),
        ("marketing:service_automation", "automation_consulting"),
    ),
)
def test_service_detail_ctas_prefill_the_matching_service(client, route_name, service_id):
    response = client.get(reverse(route_name))

    expected = f'{reverse("marketing:start_project")}?service={service_id}'
    assert expected.encode() in response.content


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_custom_404_is_rendered(client):
    response = client.get("/definitely-not-a-public-route/")

    assert response.status_code == 404
    assert b"This page could not be found." in response.content


@override_settings(DEBUG=False)
def test_custom_500_template_renders_safely():
    response = server_error(RequestFactory().get("/safe-error-test/"))

    assert response.status_code == 500
    assert b"Something went wrong." in response.content
