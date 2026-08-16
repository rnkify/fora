from django.db import transaction

from apps.leads.models import Company, Contact, Lead
from apps.marketing.models import Inquiry


def _find_or_create_company(inquiry):
    website = (inquiry.website or "").strip()
    name = (inquiry.company or "").strip()

    if website:
        company = Company.objects.filter(website__iexact=website).first()
        if company:
            return company

    if name:
        company = Company.objects.filter(name__iexact=name).first()
        if company:
            return company

    return Company.objects.create(
        name=name or inquiry.name,
        website=website,
    )


def _find_or_create_contact(*, inquiry, company):
    contact = Contact.objects.filter(email__iexact=inquiry.email).first()

    if contact:
        return contact

    return Contact.objects.create(
        company=company,
        name=inquiry.name,
        email=inquiry.email,
    )


@transaction.atomic
def convert_project_inquiry_to_lead(inquiry):
    if inquiry.type != Inquiry.Type.PROJECT:
        raise ValueError("Only project inquiries can be converted to CRM leads.")

    company = _find_or_create_company(inquiry)
    contact = _find_or_create_contact(
        inquiry=inquiry,
        company=company,
    )

    lead = Lead.objects.create(
        company=company,
        primary_contact=contact,
        source=Lead.Source.WEBSITE,
        status=Lead.Status.NEW,
        service_interest_id=inquiry.service_interest_id,
        plan_interest_id=inquiry.plan_interest_id,
        notes=inquiry.message,
        utm_source=inquiry.utm_source,
        utm_medium=inquiry.utm_medium,
        utm_campaign=inquiry.utm_campaign,
    )

    inquiry.handled = True
    inquiry.save(update_fields=["handled", "updated_at"])

    return lead
