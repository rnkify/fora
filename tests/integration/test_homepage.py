import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_renders_configured_business_content(client):
    response = client.get(reverse("marketing:home"))

    assert response.status_code == 200

    content = response.content.decode()

    assert "Fora" in content
    assert "AI Systems" in content
    assert "Growth" in content
    assert "Better systems. Better messaging." in content
