from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from apps.analytics.models import AnalyticsEvent
from apps.analytics.services import record_event
from apps.leads.models import Lead
from apps.marketing.models import Inquiry
from apps.operations.auth import staff_required
from apps.operations.forms import (
    LeadActivityForm,
    LeadForm,
    ProjectActivityForm,
    ProjectDeliveryForm,
    ProjectTaskForm,
    StaffAuthenticationForm,
    TaskStatusForm,
)
from apps.operations.services import start_project_from_won_lead
from apps.projects.models import Project, ProjectActivity, ProjectTask

ACTIVE_PROJECT_STATUSES = tuple(
    value
    for value, _label in Project.Status.choices
    if value not in {Project.Status.DELIVERED, Project.Status.ARCHIVED}
)


class OperationsLoginView(LoginView):
    authentication_form = StaffAuthenticationForm
    template_name = "operations/login.html"
    next_page = "operations:dashboard"


@staff_required
@never_cache
def lead_list(request):
    leads = Lead.objects.select_related("company", "primary_contact")
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    if query:
        leads = leads.filter(
            Q(company__name__icontains=query)
            | Q(primary_contact__name__icontains=query)
            | Q(primary_contact__email__icontains=query)
            | Q(notes__icontains=query)
        )
    valid_statuses = {value for value, _label in Lead.Status.choices}
    if status in valid_statuses:
        leads = leads.filter(status=status)
    page = Paginator(leads.order_by("-updated_at"), 25).get_page(request.GET.get("page"))
    return render(request, "operations/lead_list.html", {
        "page": page,
        "query": query,
        "selected_status": status if status in valid_statuses else "",
        "status_choices": Lead.Status.choices,
    })


@staff_required
@never_cache
def lead_detail(request, lead_id):
    lead = get_object_or_404(
        Lead.objects.select_related("company", "primary_contact", "project").prefetch_related(
            "activities"
        ),
        pk=lead_id,
    )
    return render(request, "operations/lead_detail.html", _lead_context(lead))


def _lead_context(lead, *, lead_form=None, activity_form=None):
    return {
        "lead": lead,
        "lead_form": lead_form or LeadForm(instance=lead),
        "activity_form": activity_form or LeadActivityForm(),
    }


@staff_required
@require_POST
@never_cache
def update_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    previous_status = lead.status
    form = LeadForm(request.POST, instance=lead)
    if form.is_valid():
        lead = form.save(commit=False)
        if lead.status == Lead.Status.WON:
            lead.next_action_at = None
        lead.save()
        if previous_status != lead.status:
            previous_label = Lead.Status(previous_status).label
            lead.activities.create(
                type=lead.activities.model.Type.STATUS_CHANGE,
                note=(
                    f"Status changed from {previous_label} "
                    f"to {lead.get_status_display()}."
                ),
                occurred_at=timezone.now(),
            )
        messages.success(request, "Lead details updated.")
        return redirect("operations:lead_detail", lead_id=lead.pk)
    lead = Lead.objects.select_related("company", "primary_contact").prefetch_related(
        "activities"
    ).get(pk=lead.pk)
    return render(
        request,
        "operations/lead_detail.html",
        _lead_context(lead, lead_form=form),
        status=400,
    )


@staff_required
@require_POST
@never_cache
def create_lead_activity(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    form = LeadActivityForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.lead = lead
        activity.occurred_at = timezone.now()
        activity.save()
        messages.success(request, "Activity added.")
        return redirect("operations:lead_detail", lead_id=lead.pk)
    lead = Lead.objects.select_related("company", "primary_contact").prefetch_related(
        "activities"
    ).get(pk=lead.pk)
    return render(
        request,
        "operations/lead_detail.html",
        _lead_context(lead, activity_form=form),
        status=400,
    )


@staff_required
@never_cache
def project_list(request):
    projects = Project.objects.select_related("client", "client__company")
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    state = request.GET.get("state", "active").strip()

    if query:
        projects = projects.filter(
            Q(client__company__name__icontains=query)
            | Q(service_name_snapshot__icontains=query)
            | Q(plan_name_snapshot__icontains=query)
            | Q(scope__icontains=query)
        )

    valid_statuses = {value for value, _label in Project.Status.choices}
    if status in valid_statuses:
        projects = projects.filter(status=status)
    elif state == "delivered":
        projects = projects.filter(status=Project.Status.DELIVERED)
    elif state == "archived":
        projects = projects.filter(status=Project.Status.ARCHIVED)
    elif state == "all":
        pass
    else:
        state = "active"
        projects = projects.filter(status__in=ACTIVE_PROJECT_STATUSES)

    projects = projects.order_by("due_at", "-created_at")
    page = Paginator(projects, 25).get_page(request.GET.get("page"))

    return render(
        request,
        "operations/project_list.html",
        {
            "page": page,
            "query": query,
            "selected_status": status if status in valid_statuses else "",
            "selected_state": state,
            "status_choices": Project.Status.choices,
            "today": timezone.localdate(),
        },
    )


@staff_required
@never_cache
def dashboard(request):
    now = timezone.now()
    upcoming_window = now + timedelta(days=7)

    pipeline = (
        Lead.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    new_leads = (
        Lead.objects.select_related(
            "company",
            "primary_contact",
        )
        .filter(status=Lead.Status.NEW)
        .order_by("-created_at")[:8]
    )

    won_leads_ready = (
        Lead.objects.select_related(
            "company",
            "primary_contact",
        )
        .filter(
            status=Lead.Status.WON,
            project__isnull=True,
        )
        .order_by("-updated_at")[:8]
    )

    upcoming_followups = (
        Lead.objects.select_related(
            "company",
            "primary_contact",
        )
        .filter(
            next_action_at__isnull=False,
            next_action_at__gte=now,
            next_action_at__lte=upcoming_window,
        )
        .exclude(status=Lead.Status.WON)
        .order_by("next_action_at")[:8]
    )

    active_projects = (
        Project.objects.select_related("client", "client__company")
        .exclude(
            status__in=[
                Project.Status.DELIVERED,
                Project.Status.ARCHIVED,
            ]
        )
        .order_by("due_at", "-created_at")[:8]
    )

    overdue_tasks = (
        ProjectTask.objects.select_related(
            "project",
            "project__client",
            "project__client__company",
        )
        .exclude(status=ProjectTask.Status.DONE)
        .filter(
            due_at__isnull=False,
            due_at__lt=timezone.localdate(),
        )
        .order_by("due_at")[:8]
    )

    recent_inquiries = Inquiry.objects.order_by("-created_at")[:8]

    analytics_counts = {
        event: total
        for event, total in (
            AnalyticsEvent.objects.values_list("event")
            .annotate(total=Count("id"))
        )
    }

    won_project_value = (
        Project.objects.filter(
            source_lead__isnull=False,
        )
        .aggregate(total=Sum("price_snapshot"))
        .get("total")
    )

    context = {
        "pipeline": pipeline,
        "new_leads": new_leads,
        "won_leads_ready": won_leads_ready,
        "upcoming_followups": upcoming_followups,
        "active_projects": active_projects,
        "overdue_tasks": overdue_tasks,
        "recent_inquiries": recent_inquiries,
        "analytics": {
            "page_views": analytics_counts.get(
                AnalyticsEvent.Event.PAGE_VIEW,
                0,
            ),
            "pricing_views": analytics_counts.get(
                AnalyticsEvent.Event.PRICING_VIEW,
                0,
            ),
            "project_form_started": analytics_counts.get(
                AnalyticsEvent.Event.PROJECT_FORM_STARTED,
                0,
            ),
            "project_form_submitted": analytics_counts.get(
                AnalyticsEvent.Event.PROJECT_FORM_SUBMITTED,
                0,
            ),
            "project_won": analytics_counts.get(
                AnalyticsEvent.Event.PROJECT_WON,
                0,
            ),
            "project_delivered": analytics_counts.get(
                AnalyticsEvent.Event.PROJECT_DELIVERED,
                0,
            ),
            "won_project_value": won_project_value or 0,
        },
        "metrics": {
            "new_leads": Lead.objects.filter(
                status=Lead.Status.NEW
            ).count(),
            "active_projects": Project.objects.exclude(
                status__in=[
                    Project.Status.DELIVERED,
                    Project.Status.ARCHIVED,
                ]
            ).count(),
            "overdue_tasks": ProjectTask.objects.exclude(
                status=ProjectTask.Status.DONE
            )
            .filter(
                due_at__isnull=False,
                due_at__lt=timezone.localdate(),
            )
            .count(),
            "unhandled_inquiries": Inquiry.objects.filter(
                handled=False
            ).count(),
        },
    }

    return render(
        request,
        "operations/dashboard.html",
        context,
    )


@staff_required
@require_POST
@never_cache
def start_project(request, lead_id):
    try:
        project = start_project_from_won_lead(
            lead_id=lead_id,
            actor=request.user,
        )
    except Lead.DoesNotExist:
        messages.error(
            request,
            "That lead no longer exists.",
        )
    except ValidationError as exc:
        messages.error(
            request,
            "; ".join(exc.messages),
        )
    else:
        messages.success(
            request,
            f"Project #{project.pk} created successfully.",
        )

        return redirect(
            "operations:project_detail",
            project_id=project.pk,
        )

    return redirect("operations:lead_detail", lead_id=lead_id)


@staff_required
@never_cache
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related(
            "client",
            "client__company",
            "source_lead",
            "source_lead__primary_contact",
        ).prefetch_related("tasks", "activities__actor"),
        pk=project_id,
    )

    return render(
        request,
        "operations/project_detail.html",
        _project_context(project),
    )


def _project_context(
    project,
    *,
    project_form=None,
    task_form=None,
    activity_form=None,
):
    return {
        "project": project,
        "project_form": project_form or ProjectDeliveryForm(instance=project),
        "task_form": task_form or ProjectTaskForm(),
        "project_activity_form": activity_form or ProjectActivityForm(),
        "task_status_choices": ProjectTask.Status.choices,
    }


@staff_required
@require_POST
@never_cache
def update_project(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    previous_status = project.status
    previous_due_at = project.due_at

    was_delivered = (
        project.status == Project.Status.DELIVERED
    )

    form = ProjectDeliveryForm(
        request.POST,
        instance=project,
    )

    if form.is_valid():
        project = form.save()

        if (
            project.status == Project.Status.DELIVERED
            and project.delivered_at is None
        ):
            project.delivered_at = timezone.localdate()
            project.save(
                update_fields=[
                    "delivered_at",
                    "updated_at",
                ]
            )

        if (
            project.status != Project.Status.DELIVERED
            and project.status != Project.Status.ARCHIVED
            and project.delivered_at is not None
        ):
            project.delivered_at = None
            project.save(update_fields=["delivered_at", "updated_at"])

        if (
            project.status == Project.Status.DELIVERED
            and not was_delivered
        ):
            record_event(
                event=AnalyticsEvent.Event.PROJECT_DELIVERED,
                lead_id=(
                    project.source_lead_id
                    if project.source_lead_id
                    else None
                ),
                project_id=project.pk,
                metadata={
                    "service_id": project.service_id,
                    "plan_id": project.plan_id,
                },
            )

        if previous_status != project.status:
            if project.status == Project.Status.DELIVERED:
                activity_type = ProjectActivity.Type.DELIVERED
                description = "Project marked as Delivered."
            elif previous_status == Project.Status.DELIVERED:
                activity_type = ProjectActivity.Type.REOPENED
                description = (
                    f"Project reopened in {project.get_status_display()}."
                )
            else:
                activity_type = ProjectActivity.Type.STATUS_CHANGE
                previous_label = Project.Status(previous_status).label
                description = (
                    f"Status changed from {previous_label} "
                    f"to {project.get_status_display()}."
                )
            _record_project_activity(
                project=project,
                activity_type=activity_type,
                description=description,
                actor=request.user,
            )

        if previous_due_at != project.due_at:
            due_label = (
                project.due_at.strftime("%b. %-d, %Y")
                if project.due_at
                else "No due date"
            )
            _record_project_activity(
                project=project,
                activity_type=ProjectActivity.Type.DUE_DATE_CHANGE,
                description=f"Due date changed to {due_label}.",
                actor=request.user,
            )

        messages.success(
            request,
            "Project details updated.",
        )
    else:
        messages.error(
            request,
            "Correct the highlighted project details and try again.",
        )
        return render(
            request,
            "operations/project_detail.html",
            _project_context(project, project_form=form),
        )

    return redirect(
        "operations:project_detail",
        project_id=project_id,
    )


@staff_required
@require_POST
@never_cache
def create_task(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    form = ProjectTaskForm(request.POST)

    if form.is_valid():
        task = form.save(commit=False)
        task.project = project

        last_position = (
            project.tasks.order_by("-position")
            .values_list("position", flat=True)
            .first()
        )

        task.position = (
            last_position + 1
            if last_position is not None
            else 0
        )

        task.save()

        _record_project_activity(
            project=project,
            activity_type=ProjectActivity.Type.TASK_CREATED,
            description=f'Task created: “{task.title}”.',
            actor=request.user,
        )

        messages.success(
            request,
            "Task added.",
        )
    else:
        messages.error(
            request,
            "Correct the highlighted task details and try again.",
        )
        return render(
            request,
            "operations/project_detail.html",
            _project_context(project, task_form=form),
        )

    return redirect(
        "operations:project_detail",
        project_id=project_id,
    )


@staff_required
@require_POST
@never_cache
def update_task_status(request, project_id, task_id):
    task = get_object_or_404(
        ProjectTask,
        pk=task_id,
        project_id=project_id,
    )

    form = TaskStatusForm(request.POST)

    if form.is_valid():
        previous_status = task.status
        task.status = form.cleaned_data["status"]
        task.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        if previous_status != task.status:
            previous_label = ProjectTask.Status(previous_status).label
            _record_project_activity(
                project=task.project,
                activity_type=ProjectActivity.Type.TASK_STATUS_CHANGE,
                description=(
                    f'“{task.title}” changed from {previous_label} '
                    f"to {task.get_status_display()}."
                ),
                actor=request.user,
            )

        messages.success(
            request,
            "Task status updated.",
        )
    else:
        messages.error(
            request,
            "Invalid task status.",
        )

    return redirect(
        "operations:project_detail",
        project_id=project_id,
    )


def _record_project_activity(*, project, activity_type, description, actor):
    return ProjectActivity.objects.create(
        project=project,
        type=activity_type,
        description=description,
        occurred_at=timezone.now(),
        actor=actor,
    )


@staff_required
@require_POST
@never_cache
def create_project_activity(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectActivityForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.project = project
        activity.type = ProjectActivity.Type.NOTE
        activity.occurred_at = timezone.now()
        activity.actor = request.user
        activity.save()
        messages.success(request, "Project activity added.")
        return redirect("operations:project_detail", project_id=project.pk)

    project = (
        Project.objects.select_related(
            "client",
            "client__company",
            "source_lead",
            "source_lead__primary_contact",
        )
        .prefetch_related("tasks", "activities__actor")
        .get(pk=project.pk)
    )
    messages.error(request, "Add a project note before submitting.")
    return render(
        request,
        "operations/project_detail.html",
        _project_context(project, activity_form=form),
        status=400,
    )
