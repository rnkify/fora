from django.db import models

from apps.clients.models import Client
from apps.core.models import TimeStampedModel


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        ONBOARDING = "onboarding", "Onboarding"
        RESEARCH = "research", "Research"
        STRATEGY = "strategy", "Strategy"
        DRAFT = "draft", "Draft"
        REVIEW = "review", "Review"
        REVISION = "revision", "Revision"
        APPROVED = "approved", "Approved"
        DELIVERED = "delivered", "Delivered"
        ARCHIVED = "archived", "Archived"

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="projects",
    )

    service_id = models.CharField(max_length=64)
    plan_id = models.CharField(max_length=64, blank=True)

    service_name_snapshot = models.CharField(max_length=200)
    plan_name_snapshot = models.CharField(max_length=200, blank=True)

    price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(max_length=3, default="USD")

    scope = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ONBOARDING,
        db_index=True,
    )

    started_at = models.DateField(null=True, blank=True)
    due_at = models.DateField(null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True)

    revision_count = models.PositiveSmallIntegerField(default=0)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.client} — {self.service_name_snapshot}"


class ProjectTask(TimeStampedModel):
    class Status(models.TextChoices):
        TODO = "todo", "To do"
        IN_PROGRESS = "in_progress", "In progress"
        BLOCKED = "blocked", "Blocked"
        DONE = "done", "Done"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        db_index=True,
    )
    due_at = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self) -> str:
        return self.title
