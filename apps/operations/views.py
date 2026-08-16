from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.leads.models import Lead
from apps.marketing.models import Inquiry
from apps.operations.services import start_project_from_won_lead
from apps.projects.models import Project, ProjectTask


@staff_member_required
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
            due_at__lt=now,
        )
        .order_by("due_at")[:8]
    )

    recent_inquiries = Inquiry.objects.order_by("-created_at")[:8]

    context = {
        "pipeline": pipeline,
        "new_leads": new_leads,
        "won_leads_ready": won_leads_ready,
        "upcoming_followups": upcoming_followups,
        "active_projects": active_projects,
        "overdue_tasks": overdue_tasks,
        "recent_inquiries": recent_inquiries,
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
                due_at__lt=now,
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


@staff_member_required
@require_POST
def start_project(request, lead_id):
    try:
        project = start_project_from_won_lead(
            lead_id=lead_id,
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

    return redirect("operations:dashboard")
