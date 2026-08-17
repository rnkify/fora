import os
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.browser")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.clients.models import Client  # noqa: E402
from apps.leads.models import Company, Contact, Lead  # noqa: E402
from apps.projects.models import Project, ProjectTask  # noqa: E402

call_command("flush", interactive=False, verbosity=0)

user_model = get_user_model()
user_model.objects.create_user(
    username="qa-staff",
    password="qa-browser-password",
    is_staff=True,
)
user_model.objects.create_user(
    username="qa-member",
    password="qa-browser-password",
    is_staff=False,
)

today = timezone.localdate()
main_company = Company.objects.create(name="QA Primary Client", website="https://qa.example")
main_contact = Contact.objects.create(
    company=main_company,
    name="Quinn Analyst",
    email="quinn@qa.example",
)
main_lead = Lead.objects.create(
    company=main_company,
    primary_contact=main_contact,
    source=Lead.Source.WEBSITE,
    status=Lead.Status.WON,
    service_interest_id="ai_systems",
    plan_interest_id="growth",
    notes="Build a deterministic browser QA workflow.",
)
main_client = Client.objects.create(company=main_company, since=today)
main_project = Project.objects.create(
    source_lead=main_lead,
    client=main_client,
    service_id="ai_systems",
    plan_id="growth",
    service_name_snapshot="AI Systems",
    plan_name_snapshot="Growth",
    price_snapshot="1800.00",
    currency="USD",
    scope="Build a deterministic browser QA workflow with a deliberately long scope description.",
    status=Project.Status.RESEARCH,
    started_at=today,
    due_at=today + timedelta(days=14),
)
ProjectTask.objects.create(
    project=main_project,
    title="Review responsive layouts",
    due_at=today + timedelta(days=2),
)
ProjectTask.objects.create(
    project=main_project,
    title="Verify browser interactions",
    status=ProjectTask.Status.IN_PROGRESS,
    due_at=today - timedelta(days=1),
    position=1,
)

ready_company = Company.objects.create(name="QA Won Lead")
ready_contact = Contact.objects.create(
    company=ready_company,
    name="Wendy Won",
    email="wendy@qa.example",
)
Lead.objects.create(
    company=ready_company,
    primary_contact=ready_contact,
    source=Lead.Source.WEBSITE,
    status=Lead.Status.WON,
    service_interest_id="conversion_copy",
    plan_interest_id="starter",
    notes="Create the won-lead browser QA project.",
)

for index in range(28):
    company = Company.objects.create(name=f"QA Pagination Client {index:02d}")
    client = Client.objects.create(company=company, since=today)
    Project.objects.create(
        client=client,
        service_id="content_systems",
        plan_id="starter",
        service_name_snapshot="Content Systems",
        plan_name_snapshot="Starter",
        price_snapshot="600.00",
        currency="USD",
        scope=f"Pagination fixture {index:02d}",
        status=Project.Status.REVIEW if index % 2 else Project.Status.DELIVERED,
        due_at=today + timedelta(days=index - 8),
        delivered_at=today if index % 2 == 0 else None,
    )
