import pytest
from django.urls import reverse

from apps.marketing.models import Inquiry


@pytest.mark.django_db
def test_contact_submission_creates_inquiry(client):
    response = client.post(
        reverse("marketing:contact"),
        {
            "name": "Example Person",
            "email": "person@example.com",
            "company": "Example Co",
            "website": "https://example.com",
            "message": "I have a general question.",
        },
    )

    assert response.status_code == 302

    inquiry = Inquiry.objects.get()

    assert inquiry.type == Inquiry.Type.CONTACT
    assert inquiry.name == "Example Person"
    assert inquiry.email == "person@example.com"
    assert inquiry.company == "Example Co"


@pytest.mark.django_db
def test_project_submission_creates_inquiry(client):
    response = client.post(
        reverse("marketing:start_project"),
        {
            "name": "Example Person",
            "email": "person@example.com",
            "company": "Example Agency",
            "website": "https://example.com",
            "service_interest_id": "ai_systems",
            "plan_interest_id": "growth",
            "message": "We want to improve our AI workflow.",
        },
    )

    assert response.status_code == 302

    inquiry = Inquiry.objects.get()

    assert inquiry.type == Inquiry.Type.PROJECT
    assert inquiry.service_interest_id == "ai_systems"
    assert inquiry.plan_interest_id == "growth"
    assert inquiry.message == "We want to improve our AI workflow."


@pytest.mark.django_db
def test_invalid_contact_submission_does_not_create_inquiry(client):
    response = client.post(
        reverse("marketing:contact"),
        {
            "name": "",
            "email": "not-an-email",
            "message": "",
        },
    )

    assert response.status_code == 200
    assert Inquiry.objects.count() == 0


@pytest.mark.django_db
def test_invalid_project_selection_is_rejected(client):
    response = client.post(
        reverse("marketing:start_project"),
        {
            "name": "Example Person",
            "email": "person@example.com",
            "service_interest_id": "not_a_real_service",
            "plan_interest_id": "growth",
            "message": "Testing.",
        },
    )

    assert response.status_code == 200
    assert Inquiry.objects.count() == 0


@pytest.mark.django_db
def test_project_submission_creates_crm_lead(client):
    from apps.leads.models import Company, Contact, Lead

    response = client.post(
        reverse("marketing:start_project"),
        {
            "name": "Jane Example",
            "email": "jane@example.com",
            "company": "Example Studio",
            "website": "https://example.com",
            "service_interest_id": "ai_systems",
            "plan_interest_id": "growth",
            "message": "We need a repeatable AI production workflow.",
        },
    )

    assert response.status_code == 302

    inquiry = Inquiry.objects.get(email="jane@example.com")
    company = Company.objects.get()
    contact = Contact.objects.get()
    lead = Lead.objects.get()

    assert inquiry.handled is True

    assert company.name == "Example Studio"
    assert company.website == "https://example.com"

    assert contact.company == company
    assert contact.name == "Jane Example"
    assert contact.email == "jane@example.com"

    assert lead.company == company
    assert lead.primary_contact == contact
    assert lead.source == Lead.Source.WEBSITE
    assert lead.status == Lead.Status.NEW
    assert lead.service_interest_id == "ai_systems"
    assert lead.plan_interest_id == "growth"


@pytest.mark.django_db
def test_repeated_project_submission_reuses_company_and_contact(client):
    from apps.leads.models import Company, Contact, Lead

    payload = {
        "name": "Jane Example",
        "email": "jane@example.com",
        "company": "Example Studio",
        "website": "https://example.com",
        "service_interest_id": "ai_systems",
        "plan_interest_id": "growth",
        "message": "First project.",
    }

    first = client.post(
        reverse("marketing:start_project"),
        payload,
    )

    payload["message"] = "Second project."

    second = client.post(
        reverse("marketing:start_project"),
        payload,
    )

    assert first.status_code == 302
    assert second.status_code == 302

    assert Inquiry.objects.count() == 2
    assert Company.objects.count() == 1
    assert Contact.objects.count() == 1
    assert Lead.objects.count() == 2


@pytest.mark.django_db
def test_same_email_at_different_company_keeps_contact_company_consistent(client):
    payload = {
        "name": "Jane Example",
        "email": "jane@example.com",
        "company": "First Company",
        "service_interest_id": "ai_systems",
        "message": "First project.",
    }
    client.post(reverse("marketing:start_project"), payload)
    payload["company"] = "Second Company"
    client.post(reverse("marketing:start_project"), payload)

    from apps.leads.models import Lead

    assert Lead.objects.count() == 2
    assert all(lead.primary_contact.company_id == lead.company_id for lead in Lead.objects.all())
