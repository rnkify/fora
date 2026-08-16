import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from apps.marketing.models import Inquiry


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    INQUIRY_NOTIFICATION_EMAIL="ops@example.com",
)
def test_contact_inquiry_sends_notification(client):
    response = client.post(
        reverse("marketing:contact"),
        {
            "name": "Jane Example",
            "email": "jane@example.com",
            "company": "Example Co",
            "website": "https://example.com",
            "message": "I have a question.",
        },
    )

    assert response.status_code == 302
    assert Inquiry.objects.count() == 1
    assert len(mail.outbox) == 1

    message = mail.outbox[0]

    assert message.to == ["ops@example.com"]
    assert "contact inquiry" in message.subject.lower()
    assert "Jane Example" in message.body
    assert "I have a question." in message.body


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    INQUIRY_NOTIFICATION_EMAIL="ops@example.com",
)
def test_project_inquiry_sends_notification(client):
    response = client.post(
        reverse("marketing:start_project"),
        {
            "name": "Jane Example",
            "email": "jane@example.com",
            "company": "Example Agency",
            "website": "https://example.com",
            "service_interest_id": "ai_systems",
            "plan_interest_id": "growth",
            "message": "We need a better AI workflow.",
        },
    )

    assert response.status_code == 302
    assert len(mail.outbox) == 1

    message = mail.outbox[0]

    assert "project inquiry" in message.subject.lower()
    assert "ai_systems" in message.body
    assert "growth" in message.body


@pytest.mark.django_db
@override_settings(
    INQUIRY_NOTIFICATION_EMAIL="",
)
def test_missing_notification_email_does_not_break_submission(client):
    response = client.post(
        reverse("marketing:contact"),
        {
            "name": "Jane Example",
            "email": "jane@example.com",
            "message": "Testing.",
        },
    )

    assert response.status_code == 302
    assert Inquiry.objects.count() == 1
