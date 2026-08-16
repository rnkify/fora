from django.shortcuts import render

from apps.core.configuration import (
    get_enabled_plans,
    get_enabled_services,
)
from apps.core.content import (
    get_faq_content,
    get_home_content,
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
