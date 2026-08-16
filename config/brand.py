from dataclasses import dataclass


@dataclass(frozen=True)
class BrandConfig:
    name: str
    short_name: str
    tagline: str
    description: str
    primary_domain: str
    sales_email: str
    support_email: str


BRAND = BrandConfig(
    name="Fora",
    short_name="Fora",
    tagline="AI systems built for better business outcomes.",
    description=(
        "Fora is an AI systems and growth studio helping "
        "businesses improve workflows, messaging, and "
        "conversion-focused execution."
    ),
    primary_domain="",
    sales_email="",
    support_email="",
)
