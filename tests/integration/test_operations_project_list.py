import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.clients.models import Client
from apps.leads.models import Company
from apps.projects.models import Project


def make_project(*, company_name, status):
    company = Company.objects.create(name=company_name)
    client = Client.objects.create(company=company)
    return Project.objects.create(
        client=client,
        service_id="ai_systems",
        service_name_snapshot="AI Systems",
        scope="Reusable prompt workflow",
        status=status,
    )


@pytest.mark.django_db
def test_project_list_requires_staff(client):
    response = client.get(reverse("operations:project_list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_project_list_defaults_to_active_and_links_workspace(client):
    staff = get_user_model().objects.create_user("staff", is_staff=True)
    active = make_project(company_name="Active Client", status=Project.Status.RESEARCH)
    make_project(company_name="Delivered Client", status=Project.Status.DELIVERED)
    client.force_login(staff)

    response = client.get(reverse("operations:project_list"))

    assert response.status_code == 200
    assert b"Active Client" in response.content
    assert b"Delivered Client" not in response.content
    assert reverse("operations:project_detail", args=[active.pk]).encode() in response.content


@pytest.mark.django_db
def test_project_list_filters_by_state_search_and_status(client):
    staff = get_user_model().objects.create_user("staff", is_staff=True)
    make_project(company_name="Alpha Studio", status=Project.Status.DELIVERED)
    make_project(company_name="Beta Studio", status=Project.Status.ARCHIVED)
    client.force_login(staff)
    url = reverse("operations:project_list")

    delivered = client.get(url, {"state": "delivered", "q": "Alpha"})
    archived = client.get(url, {"state": "all", "status": Project.Status.ARCHIVED})

    assert b"Alpha Studio" in delivered.content
    assert b"Beta Studio" not in delivered.content
    assert b"Beta Studio" in archived.content
    assert b"Alpha Studio" not in archived.content
