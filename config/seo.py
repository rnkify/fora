from dataclasses import dataclass


@dataclass(frozen=True)
class SEOConfig:
    default_title: str
    title_suffix: str
    default_description: str
    robots_index: bool


SEO = SEOConfig(
    default_title="Fora",
    title_suffix="Fora",
    default_description=(
        "AI systems, conversion copy, content systems, "
        "and automation consulting for growing businesses."
    ),
    robots_index=True,
)


PUBLIC_PAGE_SEO = {
    "marketing:home": (
        "Fora — Better systems. Better messaging. Better growth.",
        SEO.default_description,
    ),
    "marketing:services": (
        "Services — Fora",
        "Explore Fora's AI systems, conversion copy, content systems, and AI automation services.",
    ),
    "marketing:pricing": (
        "Pricing — Fora",
        "Fora project pricing for AI systems, conversion copy, content systems, "
        "and larger growth engagements.",
    ),
    "marketing:process": (
        "Process — Fora",
        "How Fora researches, builds, evaluates, refines, and delivers AI systems "
        "and conversion-focused work.",
    ),
    "marketing:work": (
        "Work — Fora",
        "Selected Fora work, demonstration projects, and examples of AI systems, "
        "conversion work, and structured content systems.",
    ),
    "marketing:about": (
        "About — Fora",
        "Fora is an AI systems and growth studio focused on reusable systems, "
        "stronger communication, and practical business outcomes.",
    ),
    "marketing:faq": (
        "FAQ — Fora",
        "Common questions about Fora projects, AI systems, conversion work, revisions, "
        "white-label delivery, and ongoing engagements.",
    ),
    "marketing:contact": (
        "Contact — Fora",
        "Contact Fora about AI systems, conversion work, partnerships, or general questions.",
    ),
    "marketing:start_project": (
        "Start a Project — Fora",
        "Start a project with Fora for AI systems, conversion copy, content systems, "
        "or automation consulting.",
    ),
    "marketing:privacy": (
        "Privacy — Fora",
        "How Fora handles information submitted through this website.",
    ),
    "marketing:terms": (
        "Terms — Fora",
        "The terms that apply when using the Fora website and engaging Fora for services.",
    ),
}
