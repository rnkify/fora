import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.clients.models import Client
from apps.leads.models import Company
from apps.projects.models import Project


@pytest.mark.django_db
def test_ops_requires_authentication(client):
    response = client.get(reverse("operations:dashboard"))

    assert response.status_code == 302
    assert response.url == f'{reverse("operations:login")}?next=/ops/'


@pytest.mark.django_db
def test_ops_login_is_branded_and_rejects_non_staff(client):
    response = client.get(reverse("operations:login"))
    assert response.status_code == 200
    assert b"Staff login" in response.content
    assert b"Django administration" not in response.content

    get_user_model().objects.create_user(
        username="regular-login",
        password="test-password",
        is_staff=False,
    )
    response = client.post(
        reverse("operations:login"),
        {"username": "regular-login", "password": "test-password"},
    )
    assert response.status_code == 200
    assert b"does not have access to Fora operations" in response.content


@pytest.mark.django_db
def test_ops_login_honors_safe_next_destination(client):
    get_user_model().objects.create_user(
        username="staff-login",
        password="test-password",
        is_staff=True,
    )
    response = client.post(
        reverse("operations:login"),
        {
            "username": "staff-login",
            "password": "test-password",
            "next": reverse("operations:project_list"),
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("operations:project_list")


@pytest.mark.django_db
def test_ops_rejects_non_staff_user(client):
    user = get_user_model().objects.create_user(
        username="regular",
        password="test-password",
        is_staff=False,
    )

    client.force_login(user)

    response = client.get(reverse("operations:dashboard"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_ops_renders_for_staff_user(client):
    user = get_user_model().objects.create_user(
        username="staff",
        password="test-password",
        is_staff=True,
    )

    client.force_login(user)

    response = client.get(reverse("operations:dashboard"))

    assert response.status_code == 200
    assert b"Business overview" in response.content
    assert b"New leads" in response.content
    assert b"Active projects" in response.content
    assert response.headers["Cache-Control"] == (
        "max-age=0, no-cache, no-store, must-revalidate, private"
    )


@pytest.mark.django_db
def test_active_project_and_overdue_task_link_to_workspace(client):
    user = get_user_model().objects.create_user("staff", is_staff=True)
    company = Company.objects.create(name="Workspace Client")
    business_client = Client.objects.create(company=company)
    project = Project.objects.create(
        client=business_client,
        service_id="ai_systems",
        service_name_snapshot="AI Systems",
        scope="Build the system.",
    )
    client.force_login(user)

    response = client.get(reverse("operations:dashboard"))
    workspace_url = reverse("operations:project_detail", args=[project.pk]).encode()

    assert workspace_url in response.content
    assert b"Workspace \xe2\x86\x92" in response.content
