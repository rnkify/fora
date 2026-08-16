from dataclasses import dataclass

from config.brand import BRAND, BrandConfig
from config.business import BUSINESS, BusinessConfig
from config.features import FEATURES, FeatureFlags
from config.integrations import INTEGRATIONS, IntegrationConfig
from config.navigation import PRIMARY_CTA, PRIMARY_NAVIGATION, NavItem
from config.pricing import PLANS, PlanConfig
from config.seo import SEO, SEOConfig
from config.services import SERVICES, ServiceConfig


@dataclass(frozen=True)
class ForaConfiguration:
    brand: BrandConfig
    business: BusinessConfig
    features: FeatureFlags
    integrations: IntegrationConfig
    seo: SEOConfig
    services: dict[str, ServiceConfig]
    plans: dict[str, PlanConfig]
    navigation: tuple[NavItem, ...]
    primary_cta: NavItem


def get_configuration() -> ForaConfiguration:
    return ForaConfiguration(
        brand=BRAND,
        business=BUSINESS,
        features=FEATURES,
        integrations=INTEGRATIONS,
        seo=SEO,
        services=SERVICES,
        plans=PLANS,
        navigation=PRIMARY_NAVIGATION,
        primary_cta=PRIMARY_CTA,
    )


def get_service(service_id: str) -> ServiceConfig:
    return SERVICES[service_id]


def get_plan(plan_id: str) -> PlanConfig:
    return PLANS[plan_id]


def get_enabled_services() -> tuple[ServiceConfig, ...]:
    return tuple(
        service
        for service in SERVICES.values()
        if service.enabled
    )


def get_enabled_plans() -> tuple[PlanConfig, ...]:
    return tuple(
        plan
        for plan in PLANS.values()
        if plan.enabled
    )
