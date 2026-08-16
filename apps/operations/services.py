from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.clients.models import Client
from apps.leads.models import Lead, LeadActivity
from apps.projects.models import Project
from apps.projects.services import create_project


@transaction.atomic
def start_project_from_won_lead(*, lead_id: int) -> Project:
    lead = (
        Lead.objects.select_for_update()
        .select_related("company")
        .get(pk=lead_id)
    )

    if lead.status != Lead.Status.WON:
        raise ValidationError(
            "Only a lead marked as Won can be moved into delivery."
        )

    if not lead.service_interest_id:
        raise ValidationError(
            "Choose a service for the lead before creating a project."
        )

    existing_project = Project.objects.filter(
        source_lead=lead
    ).first()

    if existing_project is not None:
        raise ValidationError(
            "A project has already been created from this lead."
        )

    client, _created = Client.objects.get_or_create(
        company=lead.company,
        defaults={
            "status": Client.Status.ACTIVE,
            "since": timezone.localdate(),
        },
    )

    client_changed = False

    if client.status != Client.Status.ACTIVE:
        client.status = Client.Status.ACTIVE
        client_changed = True

    if client.since is None:
        client.since = timezone.localdate()
        client_changed = True

    if client_changed:
        client.save(
            update_fields=[
                "status",
                "since",
                "updated_at",
            ]
        )

    project = create_project(
        client=client,
        service_id=lead.service_interest_id,
        plan_id=lead.plan_interest_id,
        scope=lead.notes or "Scope to be confirmed during onboarding.",
        notes=f"Created from CRM lead #{lead.pk}.",
    )

    project.source_lead = lead
    project.save(
        update_fields=[
            "source_lead",
            "updated_at",
        ]
    )

    LeadActivity.objects.create(
        lead=lead,
        type=LeadActivity.Type.STATUS_CHANGE,
        note=f"Lead moved into delivery as project #{project.pk}.",
        occurred_at=timezone.now(),
    )

    return project
