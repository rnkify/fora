import pytest
from django.core.exceptions import ValidationError

from apps.clients.models import Client
from apps.leads.models import Company
from apps.projects.services import create_project


@pytest.mark.django_db
def test_create_project_snapshots_current_config():
    company = Company.objects.create(name="Test Company")
    client = Client.objects.create(company=company)

    project = create_project(
        client=client,
        service_id="ai_systems",
        plan_id="growth",
        scope="Test scope",
    )

    assert project.service_id == "ai_systems"
    assert project.plan_id == "growth"

    assert project.service_name_snapshot == "AI Systems"
    assert project.plan_name_snapshot == "Growth"

    assert project.price_snapshot == 1800
    assert project.currency == "USD"


@pytest.mark.django_db
def test_create_project_rejects_unknown_service():
    company = Company.objects.create(name="Test Company")
    client = Client.objects.create(company=company)

    with pytest.raises(ValidationError):
        create_project(
            client=client,
            service_id="does_not_exist",
            scope="Test scope",
        )


@pytest.mark.django_db
def test_create_project_rejects_unknown_plan():
    company = Company.objects.create(name="Test Company")
    client = Client.objects.create(company=company)

    with pytest.raises(ValidationError):
        create_project(
            client=client,
            service_id="ai_systems",
            plan_id="does_not_exist",
            scope="Test scope",
        )
