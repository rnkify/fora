from django.urls import path

from apps.marketing.views import home

app_name = "marketing"

urlpatterns = [
    path("", home, name="home"),
]
