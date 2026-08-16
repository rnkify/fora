from django.db import models

from apps.core.models import TimeStampedModel


class AnalyticsEvent(TimeStampedModel):
    class Event(models.TextChoices):
        PAGE_VIEW = "page_view", "Page view"
        SERVICE_VIEW = "service_view", "Service view"
        PRICING_VIEW = "pricing_view", "Pricing view"
        CASE_STUDY_VIEW = "case_study_view", "Case study view"
        CTA_CLICKED = "cta_clicked", "CTA clicked"
        CONTACT_STARTED = "contact_started", "Contact started"
        CONTACT_SUBMITTED = "contact_submitted", "Contact submitted"
        PROJECT_FORM_STARTED = "project_form_started", "Project form started"
        PROJECT_FORM_SUBMITTED = (
            "project_form_submitted",
            "Project form submitted",
        )
        LEAD_QUALIFIED = "lead_qualified", "Lead qualified"
        DISCOVERY_SCHEDULED = (
            "discovery_scheduled",
            "Discovery scheduled",
        )
        PROPOSAL_CREATED = "proposal_created", "Proposal created"
        PROJECT_WON = "project_won", "Project won"
        PROJECT_DELIVERED = "project_delivered", "Project delivered"
        RETAINER_OFFERED = "retainer_offered", "Retainer offered"
        RETAINER_WON = "retainer_won", "Retainer won"

    event = models.CharField(
        max_length=50,
        choices=Event.choices,
        db_index=True,
    )

    path = models.CharField(max_length=500, blank=True)
    referrer = models.CharField(max_length=500, blank=True)

    lead_id = models.PositiveBigIntegerField(null=True, blank=True)
    project_id = models.PositiveBigIntegerField(null=True, blank=True)

    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.event
