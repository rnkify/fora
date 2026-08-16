from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.clients.models import Client
from apps.projects.models import Project
from config.pricing import PLANS
from config.services import SERVICES


@transaction.atomic
def create_project(
    *,
    client: Client,
    service_id: str,
    plan_id: str = "",
    scope: str,
    notes: str = "",
) -> Project:
    try:
        service = SERVICES[service_id]
    except KeyError as exc:
        raise ValidationError(
            {"service_id": f"Unknown service ID: {service_id}"}
        ) from exc

    if not service.enabled:
        raise ValidationError(
            {"service_id": "This service is currently unavailable."}
        )

    plan = None

    if plan_id:
        try:
            plan = PLANS[plan_id]
        except KeyError as exc:
            raise ValidationError(
                {"plan_id": f"Unknown plan ID: {plan_id}"}
            ) from exc

        if not plan.enabled:
            raise ValidationError(
                {"plan_id": "This plan is currently unavailable."}
            )

    return Project.objects.create(
        client=client,
        service_id=service.id,
        plan_id=plan.id if plan else "",
        service_name_snapshot=service.name,
        plan_name_snapshot=plan.name if plan else "",
        price_snapshot=(
            Decimal(plan.price)
            if plan is not None
            else None
        ),
        currency=(
            plan.currency
            if plan is not None
            else "USD"
        ),
        scope=scope,
        notes=notes,
    )
