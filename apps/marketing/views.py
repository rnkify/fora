from django.http import Http404
from django.shortcuts import redirect, render

from apps.core.configuration import (
    get_enabled_plans,
    get_enabled_services,
)
from apps.core.content import (
    get_faq_content,
    get_home_content,
    get_process_content,
)
from apps.marketing.forms import ContactForm, ProjectInquiryForm
from apps.marketing.services import (
    create_contact_inquiry,
    create_project_inquiry,
)


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "home": get_home_content(),
            "services": get_enabled_services(),
            "plans": get_enabled_plans(),
            "faqs": get_faq_content(),
        },
    )


def services(request):
    return render(
        request,
        "pages/services.html",
        {
            "services": get_enabled_services(),
        },
    )


def _service_page(request, service_id):
    services_by_id = {
        service.id: service
        for service in get_enabled_services()
    }

    service = services_by_id.get(service_id)

    if service is None:
        raise Http404("Service not found.")

    return render(
        request,
        "pages/service_detail.html",
        {
            "service": service,
        },
    )


def service_ai_systems(request):
    return _service_page(request, "ai_systems")


def service_conversion_copy(request):
    return _service_page(request, "conversion_copy")


def service_content_systems(request):
    return _service_page(request, "content_systems")


def service_automation(request):
    return _service_page(request, "automation_consulting")


def pricing(request):
    return render(
        request,
        "pages/pricing.html",
        {
            "plans": get_enabled_plans(),
        },
    )


def process(request):
    return render(
        request,
        "pages/process.html",
        {
            "process": get_process_content(),
            "home": get_home_content(),
        },
    )


def work(request):
    return render(
        request,
        "pages/work.html",
    )


def about(request):
    return render(
        request,
        "pages/about.html",
    )


def faq(request):
    return render(
        request,
        "pages/faq.html",
        {
            "faqs": get_faq_content(),
        },
    )



def contact(request):
    submitted = request.GET.get("submitted") == "1"

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            create_contact_inquiry(
                request=request,
                cleaned_data=form.cleaned_data,
            )
            return redirect("/contact/?submitted=1")
    else:
        form = ContactForm()

    return render(
        request,
        "pages/contact.html",
        {
            "form": form,
            "submitted": submitted,
        },
    )



def start_project(request):
    submitted = request.GET.get("submitted") == "1"

    if request.method == "POST":
        form = ProjectInquiryForm(request.POST)

        if form.is_valid():
            create_project_inquiry(
                request=request,
                cleaned_data=form.cleaned_data,
            )
            return redirect("/start/?submitted=1")
    else:
        form = ProjectInquiryForm()

    return render(
        request,
        "pages/start.html",
        {
            "form": form,
            "submitted": submitted,
            "services": get_enabled_services(),
            "plans": get_enabled_plans(),
        },
    )
