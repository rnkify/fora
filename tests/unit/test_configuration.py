from config.brand import BRAND
from config.pricing import PLANS
from config.services import SERVICES
from config.validation import validate_configuration


def test_configuration_is_valid():
    validate_configuration()


def test_working_brand_is_fora():
    assert BRAND.name == "Fora"


def test_stable_service_ids_match_keys():
    assert all(
        key == service.id
        for key, service in SERVICES.items()
    )


def test_stable_plan_ids_match_keys():
    assert all(
        key == plan.id
        for key, plan in PLANS.items()
    )


def test_growth_is_highlighted():
    assert PLANS["growth"].highlighted is True
