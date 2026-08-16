from django.http import HttpRequest

from apps.core.configuration import get_configuration


def fora_configuration(_request: HttpRequest) -> dict:
    return {
        "fora": get_configuration(),
    }
