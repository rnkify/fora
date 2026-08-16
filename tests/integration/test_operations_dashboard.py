import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_ops_requires_authentication(client):
    response = client.get(reverse("operations:dashboard"))

    assert response.status_code == 302
    assert "/admin/login/" in response.url


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
