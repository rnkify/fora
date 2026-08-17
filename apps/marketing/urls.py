from django.urls import path

from apps.marketing import views

app_name = "marketing"

urlpatterns = [
    path("", views.home, name="home"),

    path("services/", views.services, name="services"),
    path(
        "services/ai-systems/",
        views.service_ai_systems,
        name="service_ai_systems",
    ),
    path(
        "services/conversion-copy/",
        views.service_conversion_copy,
        name="service_conversion_copy",
    ),
    path(
        "services/content-systems/",
        views.service_content_systems,
        name="service_content_systems",
    ),
    path(
        "services/ai-automation/",
        views.service_automation,
        name="service_automation",
    ),

    path("pricing/", views.pricing, name="pricing"),
    path("process/", views.process, name="process"),
    path("work/", views.work, name="work"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("start/", views.start_project, name="start_project"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
