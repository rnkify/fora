import pytest
from django.test import override_settings
from django.urls import reverse


@pytest.mark.django_db
def test_health_and_readiness(client):
    health = client.get(reverse("healthcheck"))
    ready = client.get(reverse("readiness"))

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert ready.status_code == 200
    assert ready.json()["database"] == "ok"


@pytest.mark.django_db
def test_robots_and_sitemap(client):
    robots = client.get(reverse("robots_txt"))
    sitemap = client.get(reverse("sitemap"))

    assert robots.status_code == 200
    assert b"Disallow: /ops/" in robots.content
    assert b"Sitemap:" in robots.content
    assert sitemap.status_code == 200
    assert b"/privacy/" in sitemap.content
    assert b"/terms/" in sitemap.content


@pytest.mark.django_db
@override_settings(
    APP_URL="https://www.fora.example",
    ALLOWED_HOSTS=["internal.railway.app"],
)
def test_canonical_and_sitemap_use_configured_public_url(client):
    page = client.get(reverse("marketing:pricing"), HTTP_HOST="internal.railway.app")
    sitemap = client.get(reverse("sitemap"), HTTP_HOST="internal.railway.app")
    robots = client.get(reverse("robots_txt"), HTTP_HOST="internal.railway.app")

    assert b'<link rel="canonical" href="https://www.fora.example/pricing/">' in page.content
    assert b"https://www.fora.example/pricing/" in sitemap.content
    assert b"Sitemap: https://www.fora.example/sitemap.xml" in robots.content


@pytest.mark.django_db
def test_page_specific_social_metadata(client):
    pricing = client.get(reverse("marketing:pricing"))
    service = client.get(reverse("marketing:service_ai_systems"))

    assert b'<meta property="og:title" content="Pricing \xe2\x80\x94 Fora">' in pricing.content
    assert b'<meta name="twitter:title" content="Pricing \xe2\x80\x94 Fora">' in pricing.content
    assert b'<meta property="og:title" content="AI Systems \xe2\x80\x94 Fora">' in service.content
    assert b"Reusable AI workflows, prompts, structured outputs" in service.content


@pytest.mark.django_db
@pytest.mark.parametrize("route", ("marketing:privacy", "marketing:terms"))
def test_legal_pages_render(client, route):
    response = client.get(reverse(route))
    assert response.status_code == 200
    assert b'name="robots"' in response.content


@pytest.mark.django_db
def test_start_page_accepts_valid_prefill(client):
    response = client.get(
        reverse("marketing:start_project"),
        {"service": "ai_systems", "plan": "growth"},
    )
    assert b'<option value="ai_systems" selected>' in response.content
    assert b'<option value="growth" selected>' in response.content
