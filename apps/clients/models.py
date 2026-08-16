from django.db import models

from apps.core.models import TimeStampedModel
from apps.leads.models import Company


class Client(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        ARCHIVED = "archived", "Archived"

    company = models.OneToOneField(
        Company,
        on_delete=models.PROTECT,
        related_name="client",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    since = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["company__name"]

    def __str__(self) -> str:
        return self.company.name
