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
