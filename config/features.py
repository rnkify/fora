from dataclasses import dataclass

from config.env import env_bool


@dataclass(frozen=True)
class FeatureFlags:
    billing: bool
    blog: bool
    client_portal: bool
    booking: bool
    analytics: bool
    ai_features: bool
    digital_products: bool


FEATURES = FeatureFlags(
    billing=env_bool("ENABLE_BILLING", False),
    blog=env_bool("ENABLE_BLOG", False),
    client_portal=env_bool(
        "ENABLE_CLIENT_PORTAL",
        False,
    ),
    booking=env_bool("ENABLE_BOOKING", False),
    analytics=env_bool("ENABLE_ANALYTICS", False),
    ai_features=env_bool(
        "ENABLE_AI_FEATURES",
        False,
    ),
    digital_products=env_bool(
        "ENABLE_DIGITAL_PRODUCTS",
        False,
    ),
)
