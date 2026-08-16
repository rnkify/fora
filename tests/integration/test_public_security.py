import pytest
from django.urls import reverse

from apps.marketing.models import Inquiry


@pytest.mark.django_db
def test_contact_page_contains_csrf_token(client):
    response = client.get(reverse("marketing:contact"))

    assert response.status_code == 200
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_start_page_contains_csrf_token(client):
    response = client.get(reverse("marketing:start_project"))

    assert response.status_code == 200
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_contact_rejects_invalid_email(client):
    response = client.post(
        reverse("marketing:contact"),
        {
            "name": "Example",
            "email": "not-an-email",
            "message": "Testing",
        },
    )

    assert response.status_code == 200
    assert Inquiry.objects.count() == 0


@pytest.mark.django_db
def test_start_rejects_unknown_service(client):
    response = client.post(
        reverse("marketing:start_project"),
        {
            "name": "Example",
            "email": "example@example.com",
            "service_interest_id": "does_not_exist",
            "plan_interest_id": "",
            "message": "Testing",
        },
    )

    assert response.status_code == 200
    assert Inquiry.objects.count() == 0
