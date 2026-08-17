from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.marketing.crm import convert_project_inquiry_to_lead
from apps.marketing.models import Inquiry
from apps.marketing.notifications import notify_new_inquiry


def _request_metadata(request):
    return {
        "utm_source": request.GET.get("utm_source", "")[:120],
        "utm_medium": request.GET.get("utm_medium", "")[:120],
        "utm_campaign": request.GET.get("utm_campaign", "")[:120],
        "referrer": request.headers.get("Referer", "")[:200],
        "landing_page": request.path[:500],
    }


def create_contact_inquiry(*, request, cleaned_data):
    inquiry = Inquiry.objects.create(
        type=Inquiry.Type.CONTACT,
        name=cleaned_data["name"],
        email=cleaned_data["email"],
        company=cleaned_data.get("company", ""),
        website=cleaned_data.get("website", ""),
        message=cleaned_data["message"],
        **_request_metadata(request),
    )

    notify_new_inquiry(inquiry)

    return inquiry


@transaction.atomic
def create_project_inquiry(*, request, cleaned_data):
    duplicate_since = timezone.now() - timedelta(minutes=5)
    duplicate = Inquiry.objects.filter(
        type=Inquiry.Type.PROJECT,
        name__iexact=cleaned_data["name"],
        email__iexact=cleaned_data["email"],
        company__iexact=cleaned_data.get("company", ""),
        website__iexact=cleaned_data.get("website", ""),
        service_interest_id=cleaned_data.get("service_interest_id", ""),
        plan_interest_id=cleaned_data.get("plan_interest_id", ""),
        message=cleaned_data["message"],
        created_at__gte=duplicate_since,
    ).first()

    if duplicate is not None:
        return duplicate

    inquiry = Inquiry.objects.create(
        type=Inquiry.Type.PROJECT,
        name=cleaned_data["name"],
        email=cleaned_data["email"],
        company=cleaned_data.get("company", ""),
        website=cleaned_data.get("website", ""),
        service_interest_id=cleaned_data.get("service_interest_id", ""),
        plan_interest_id=cleaned_data.get("plan_interest_id", ""),
        message=cleaned_data["message"],
        **_request_metadata(request),
    )

    convert_project_inquiry_to_lead(inquiry)
    notify_new_inquiry(inquiry)

    return inquiry
