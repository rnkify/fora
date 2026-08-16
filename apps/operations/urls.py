from django.urls import path

from apps.operations import views

app_name = "operations"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "leads/<int:lead_id>/start-project/",
        views.start_project,
        name="start_project",
    ),
]
