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


@pytest.mark.django_db
@pytest.mark.parametrize("route", ("marketing:contact", "marketing:start_project"))
def test_success_query_cannot_spoof_a_submission(client, route):
    response = client.get(reverse(route), {"submitted": "1"})

    assert response.status_code == 200
    assert b"csrfmiddlewaretoken" in response.content
    assert b"has been submitted" not in response.content


@pytest.mark.django_db
def test_invalid_fields_reference_accessible_error_messages(client):
    response = client.post(
        reverse("marketing:contact"),
        {"name": "", "email": "invalid", "message": ""},
    )

    assert b'aria-invalid="true"' in response.content
    assert b'aria-describedby="id_email_error"' in response.content
    assert b'id="id_email_error"' in response.content
    assert b'role="alert"' in response.content
