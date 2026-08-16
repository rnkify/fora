from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessConfig:
    primary_market: str
    secondary_market: str
    category: str
    currency: str


BUSINESS = BusinessConfig(
    primary_market="Boutique digital and marketing agencies",
    secondary_market="Founder-led SaaS and B2B technology companies",
    category="AI Systems & Growth Studio",
    currency="USD",
)
