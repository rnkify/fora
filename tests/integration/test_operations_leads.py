import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.leads.models import Company, Contact, Lead, LeadActivity


def make_lead():
    company = Company.objects.create(name="Lead Workspace Company")
    contact = Contact.objects.create(
        company=company,
        name="Lead Contact",
        email="lead@example.com",
    )
    return Lead.objects.create(
        company=company,
        primary_contact=contact,
        service_interest_id="ai_systems",
        plan_interest_id="growth",
        notes="Initial inquiry context.",
    )


@pytest.mark.django_db
def test_lead_pages_require_staff(client):
    lead = make_lead()
    assert client.get(reverse("operations:lead_list")).status_code == 302
    assert client.get(reverse("operations:lead_detail", args=[lead.pk])).status_code == 302


@pytest.mark.django_db
def test_staff_can_search_and_update_lead(client):
    user = get_user_model().objects.create_user("lead-staff", is_staff=True)
    lead = make_lead()
    client.force_login(user)

    response = client.get(reverse("operations:lead_list"), {"q": "Lead Contact"})
    assert response.status_code == 200
    assert b"Lead Workspace Company" in response.content

    response = client.post(
        reverse("operations:update_lead", args=[lead.pk]),
        {
            "status": Lead.Status.QUALIFIED,
            "score": 75,
            "estimated_value": "1800.00",
            "service_interest_id": "ai_systems",
            "plan_interest_id": "growth",
            "next_action_at": "2026-08-20T10:30",
            "notes": "Discovery is a fit.",
        },
    )
    assert response.status_code == 302
    lead.refresh_from_db()
    assert lead.status == Lead.Status.QUALIFIED
    assert lead.score == 75
    assert lead.activities.filter(type=LeadActivity.Type.STATUS_CHANGE).exists()


@pytest.mark.django_db
def test_staff_can_add_lead_activity_and_invalid_score_is_rejected(client):
    user = get_user_model().objects.create_user("activity-staff", is_staff=True)
    lead = make_lead()
    client.force_login(user)

    response = client.post(
        reverse("operations:create_lead_activity", args=[lead.pk]),
        {"type": LeadActivity.Type.CALL, "note": "Discussed scope and timing."},
    )
    assert response.status_code == 302
    assert lead.activities.get().note == "Discussed scope and timing."

    response = client.post(
        reverse("operations:update_lead", args=[lead.pk]),
        {
            "status": Lead.Status.NEW,
            "score": 101,
            "estimated_value": "",
            "service_interest_id": "ai_systems",
            "plan_interest_id": "growth",
            "next_action_at": "",
            "notes": lead.notes,
        },
    )
    assert response.status_code == 400
    assert b"Score must be between 0 and 100." in response.content
