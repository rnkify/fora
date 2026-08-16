from dataclasses import dataclass


@dataclass(frozen=True)
class PlanConfig:
    id: str
    name: str
    price: int
    currency: str
    billing_period: str
    highlighted: bool
    enabled: bool
    cta_label: str


PLANS = {
    "audit": PlanConfig(
        id="audit",
        name="AI & Conversion Audit",
        price=250,
        currency="USD",
        billing_period="project",
        highlighted=False,
        enabled=True,
        cta_label="Request an Audit",
    ),
    "starter": PlanConfig(
        id="starter",
        name="Starter",
        price=750,
        currency="USD",
        billing_period="project",
        highlighted=False,
        enabled=True,
        cta_label="Start a Project",
    ),
    "growth": PlanConfig(
        id="growth",
        name="Growth",
        price=1800,
        currency="USD",
        billing_period="project",
        highlighted=True,
        enabled=True,
        cta_label="Start a Project",
    ),
    "scale": PlanConfig(
        id="scale",
        name="Scale",
        price=4500,
        currency="USD",
        billing_period="project",
        highlighted=False,
        enabled=True,
        cta_label="Talk to Fora",
    ),
}
