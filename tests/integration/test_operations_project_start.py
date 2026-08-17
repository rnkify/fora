from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.clients.models import Client
from apps.leads.models import Company, Contact, Lead, LeadActivity
from apps.projects.models import Project, ProjectActivity


def create_staff_user():
    return get_user_model().objects.create_user(
        username="ops-staff",
        password="test-password",
        is_staff=True,
    )


def create_lead(*, status):
    company = Company.objects.create(
        name="Example Agency",
        website="https://example.com",
    )

    contact = Contact.objects.create(
        company=company,
        name="Jane Example",
        email="jane@example.com",
    )

    return Lead.objects.create(
        company=company,
        primary_contact=contact,
        source=Lead.Source.WEBSITE,
        status=status,
        service_interest_id="ai_systems",
        plan_interest_id="growth",
        notes="Build a reliable AI workflow.",
    )


@pytest.mark.django_db
def test_won_lead_can_create_client_and_project(client):
    user = create_staff_user()
    lead = create_lead(status=Lead.Status.WON)

    client.force_login(user)

    response = client.post(
        reverse(
            "operations:start_project",
            args=[lead.pk],
        )
    )

    assert response.status_code == 302

    created_client = Client.objects.get(
        company=lead.company
    )
    project = Project.objects.get()
    assert response.url == reverse(
        "operations:project_detail",
        args=[project.pk],
    )

    assert created_client.status == Client.Status.ACTIVE
    assert created_client.since == timezone.localdate()

    assert project.client == created_client
    assert project.source_lead == lead
    assert project.service_id == "ai_systems"
    assert project.plan_id == "growth"
    assert project.plan_name_snapshot == "Growth"
    assert project.price_snapshot == Decimal("1800")

    assert LeadActivity.objects.filter(
        lead=lead,
        type=LeadActivity.Type.STATUS_CHANGE,
    ).exists()
    activity = ProjectActivity.objects.get(project=project)
    assert activity.type == ProjectActivity.Type.CREATED
    assert activity.actor == user


@pytest.mark.django_db
def test_non_won_lead_cannot_create_project(client):
    user = create_staff_user()
    lead = create_lead(status=Lead.Status.NEW)

    client.force_login(user)

    response = client.post(
        reverse(
            "operations:start_project",
            args=[lead.pk],
        )
    )

    assert response.status_code == 302
    assert Project.objects.count() == 0
    assert Client.objects.count() == 0
    assert response.url == reverse("operations:lead_detail", args=[lead.pk])


@pytest.mark.django_db
def test_same_won_lead_cannot_create_two_projects(client):
    user = create_staff_user()
    lead = create_lead(status=Lead.Status.WON)

    client.force_login(user)

    url = reverse(
        "operations:start_project",
        args=[lead.pk],
    )

    first = client.post(url)
    second = client.post(url)

    assert first.status_code == 302
    assert second.status_code == 302

    assert Project.objects.count() == 1
    assert Client.objects.count() == 1
    project = Project.objects.get()
    assert first.url == reverse("operations:project_detail", args=[project.pk])
    assert second.url == reverse("operations:lead_detail", args=[lead.pk])


@pytest.mark.django_db
def test_project_start_requires_post(client):
    user = create_staff_user()
    lead = create_lead(status=Lead.Status.WON)

    client.force_login(user)

    response = client.get(
        reverse(
            "operations:start_project",
            args=[lead.pk],
        )
    )

    assert response.status_code == 405
    assert Project.objects.count() == 0
