from django.db import models

from apps.core.models import TimeStampedModel


class Inquiry(TimeStampedModel):
    class Type(models.TextChoices):
        CONTACT = "contact", "Contact"
        PROJECT = "project", "Project"
        PARTNERSHIP = "partnership", "Partnership"

    type = models.CharField(
        max_length=30,
        choices=Type.choices,
        default=Type.CONTACT,
        db_index=True,
    )

    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)

    service_interest_id = models.CharField(max_length=64, blank=True)
    plan_interest_id = models.CharField(max_length=64, blank=True)

    message = models.TextField()

    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    referrer = models.URLField(blank=True)
    landing_page = models.CharField(max_length=500, blank=True)

    handled = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} — {self.get_type_display()}"
