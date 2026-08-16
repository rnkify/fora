from django.db import models

from apps.core.models import TimeStampedModel


class PortfolioItem(TimeStampedModel):
    class Kind(models.TextChoices):
        DEMONSTRATION = "demonstration", "Demonstration"
        CLIENT = "client", "Client work"

    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    kind = models.CharField(
        max_length=30,
        choices=Kind.choices,
        default=Kind.DEMONSTRATION,
    )

    service_id = models.CharField(max_length=64)

    summary = models.TextField()
    situation = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    baseline = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    strategy = models.TextField(blank=True)
    improved_version = models.TextField(blank=True)
    evaluation = models.TextField(blank=True)

    published = models.BooleanField(default=False, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "-created_at"]

    def __str__(self) -> str:
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=120, blank=True)
    quote = models.TextField()

    approved = models.BooleanField(default=False, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
