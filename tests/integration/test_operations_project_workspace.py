import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.clients.models import Client
from apps.leads.models import Company
from apps.projects.models import Project, ProjectTask


def make_staff():
    return get_user_model().objects.create_user(
        username="delivery-staff",
        password="test-password",
        is_staff=True,
    )


def make_project():
    company = Company.objects.create(
        name="Delivery Client",
    )

    client = Client.objects.create(
        company=company,
    )

    return Project.objects.create(
        client=client,
        service_id="ai_systems",
        plan_id="growth",
        service_name_snapshot="AI Systems",
        plan_name_snapshot="Growth",
        price_snapshot="1800.00",
        currency="USD",
        scope="Build a reusable AI workflow.",
    )


@pytest.mark.django_db
def test_project_workspace_requires_staff(client):
    project = make_project()

    response = client.get(
        reverse(
            "operations:project_detail",
            args=[project.pk],
        )
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_staff_can_view_project_workspace(client):
    user = make_staff()
    project = make_project()

    client.force_login(user)

    response = client.get(
        reverse(
            "operations:project_detail",
            args=[project.pk],
        )
    )

    assert response.status_code == 200
    assert b"Delivery Client" in response.content
    assert b"Delivery checklist" in response.content


@pytest.mark.django_db
def test_staff_can_update_project(client):
    user = make_staff()
    project = make_project()

    client.force_login(user)

    response = client.post(
        reverse(
            "operations:update_project",
            args=[project.pk],
        ),
        {
            "status": Project.Status.RESEARCH,
            "started_at": "2026-08-16",
            "due_at": "2026-08-30",
            "delivered_at": "",
            "revision_count": 1,
            "notes": "Research started.",
        },
    )

    assert response.status_code == 302

    project.refresh_from_db()

    assert project.status == Project.Status.RESEARCH
    assert str(project.due_at) == "2026-08-30"
    assert project.revision_count == 1
    assert project.notes == "Research started."


@pytest.mark.django_db
def test_project_rejects_due_date_before_start_date(client):
    user = make_staff()
    project = make_project()
    client.force_login(user)

    response = client.post(
        reverse("operations:update_project", args=[project.pk]),
        {
            "status": Project.Status.RESEARCH,
            "started_at": "2026-08-30",
            "due_at": "2026-08-20",
            "delivered_at": "",
            "revision_count": 0,
            "notes": "",
        },
    )

    project.refresh_from_db()
    assert response.status_code == 200
    assert b"Due date cannot be before the start date." in response.content
    assert project.started_at is None
    assert project.due_at is None


@pytest.mark.django_db
def test_reopening_delivered_project_clears_delivery_date(client):
    user = make_staff()
    project = make_project()
    project.status = Project.Status.DELIVERED
    project.delivered_at = "2026-08-16"
    project.save()
    client.force_login(user)

    client.post(
        reverse("operations:update_project", args=[project.pk]),
        {
            "status": Project.Status.REVISION,
            "started_at": "",
            "due_at": "",
            "delivered_at": "2026-08-16",
            "revision_count": 1,
            "notes": "Reopened.",
        },
    )

    project.refresh_from_db()
    assert project.delivered_at is None


@pytest.mark.django_db
def test_staff_can_add_project_task(client):
    user = make_staff()
    project = make_project()

    client.force_login(user)

    response = client.post(
        reverse(
            "operations:create_task",
            args=[project.pk],
        ),
        {
            "title": "Complete customer research",
            "due_at": "2026-08-20",
        },
    )

    assert response.status_code == 302

    task = ProjectTask.objects.get()

    assert task.project == project
    assert task.title == "Complete customer research"


@pytest.mark.django_db
def test_staff_can_update_task_status(client):
    user = make_staff()
    project = make_project()

    task = ProjectTask.objects.create(
        project=project,
        title="Draft workflow",
    )

    client.force_login(user)

    response = client.post(
        reverse(
            "operations:update_task_status",
            args=[project.pk, task.pk],
        ),
        {
            "status": ProjectTask.Status.DONE,
        },
    )

    assert response.status_code == 302

    task.refresh_from_db()

    assert task.status == ProjectTask.Status.DONE
