from django.db import models

from apps.core.models import TimeStampedModel


class Company(TimeStampedModel):
    class SizeBand(models.TextChoices):
        SOLO = "solo", "Solo"
        TWO_TO_FIVE = "2_5", "2–5"
        SIX_TO_TEN = "6_10", "6–10"
        ELEVEN_TO_TWENTY_FIVE = "11_25", "11–25"
        TWENTY_SIX_TO_FIFTY = "26_50", "26–50"
        FIFTY_PLUS = "50_plus", "50+"
        UNKNOWN = "unknown", "Unknown"

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=120, blank=True)
    size_band = models.CharField(
        max_length=20,
        choices=SizeBand.choices,
        default=SizeBand.UNKNOWN,
    )
    country = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Contact(TimeStampedModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Lead(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        REPLIED = "replied", "Replied"
        QUALIFIED = "qualified", "Qualified"
        DISCOVERY = "discovery", "Discovery"
        PROPOSAL = "proposal", "Proposal"
        WON = "won", "Won"
        LOST = "lost", "Lost"
        UNQUALIFIED = "unqualified", "Unqualified"
        ARCHIVED = "archived", "Archived"

    class Source(models.TextChoices):
        OUTBOUND = "outbound", "Outbound"
        LINKEDIN = "linkedin", "LinkedIn"
        REFERRAL = "referral", "Referral"
        WEBSITE = "website", "Website"
        MARKETPLACE = "marketplace", "Marketplace"
        PARTNERSHIP = "partnership", "Partnership"
        OTHER = "other", "Other"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="leads",
    )
    primary_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_leads",
    )

    source = models.CharField(
        max_length=30,
        choices=Source.choices,
        default=Source.OTHER,
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )

    score = models.PositiveSmallIntegerField(default=0)
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    service_interest_id = models.CharField(max_length=64, blank=True)
    plan_interest_id = models.CharField(max_length=64, blank=True)

    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)

    next_action_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.company.name} — {self.get_status_display()}"


class LeadActivity(TimeStampedModel):
    class Type(models.TextChoices):
        EMAIL = "email", "Email"
        CALL = "call", "Call"
        FOLLOW_UP = "follow_up", "Follow-up"
        PROPOSAL = "proposal", "Proposal"
        STATUS_CHANGE = "status_change", "Status change"
        NOTE = "note", "Internal note"

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    type = models.CharField(
        max_length=30,
        choices=Type.choices,
        default=Type.NOTE,
    )
    note = models.TextField()
    occurred_at = models.DateTimeField()

    class Meta:
        ordering = ["-occurred_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.lead} — {self.get_type_display()}"
