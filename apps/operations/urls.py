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
    path(
        "projects/<int:project_id>/",
        views.project_detail,
        name="project_detail",
    ),
    path(
        "projects/<int:project_id>/update/",
        views.update_project,
        name="update_project",
    ),
    path(
        "projects/<int:project_id>/tasks/add/",
        views.create_task,
        name="create_task",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:task_id>/status/",
        views.update_task_status,
        name="update_task_status",
    ),
]
