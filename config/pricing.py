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
    description: str
    deliverables: tuple[str, ...]


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
        description=(
            "A focused diagnostic for one workflow, prompt system, "
            "landing page, or conversion problem."
        ),
        deliverables=(
            "Focused workflow or asset review",
            "Prioritized diagnosis",
            "One improved example",
            "Actionable recommendation plan",
            "2–3 business day turnaround",
        ),
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
        description=(
            "A focused engagement for one important system, campaign, "
            "or conversion asset."
        ),
        deliverables=(
            "Research and strategic direction",
            "One focused deliverable",
            "Up to 3 useful variants",
            "Implementation documentation",
            "2 revision rounds",
            "Typical 5 business day turnaround",
        ),
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
        description=(
            "The main Fora engagement for businesses that need a "
            "complete system rather than a single isolated asset."
        ),
        deliverables=(
            "Customer and competitor research",
            "3 major deliverables or equivalent AI workflow scope",
            "Reusable prompt or content architecture",
            "Variant evaluation",
            "Implementation documentation",
            "3 revision rounds",
            "14 days post-project support",
        ),
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
        description=(
            "A larger engagement for agencies and growing teams with "
            "multiple workflows or deliverables."
        ),
        deliverables=(
            "Strategic audit",
            "Multiple workflows",
            "Up to 8 major deliverables",
            "AI workflow and prompt library",
            "Evaluation framework",
            "Training and handoff",
            "3 revision rounds",
            "30 days support",
        ),
    ),
}
