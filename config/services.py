from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceConfig:
    id: str
    name: str
    short_description: str
    enabled: bool = True


SERVICES = {
    "ai_systems": ServiceConfig(
        id="ai_systems",
        name="AI Systems",
        short_description=(
            "Reusable AI workflows, prompts, structured outputs, "
            "evaluation systems, and internal assistants."
        ),
    ),
    "conversion_copy": ServiceConfig(
        id="conversion_copy",
        name="Conversion Copy",
        short_description=(
            "Landing pages, email systems, sales messaging, "
            "advertising, and conversion-focused optimization."
        ),
    ),
    "content_systems": ServiceConfig(
        id="content_systems",
        name="Content Systems",
        short_description=(
            "Repeatable content strategy and AI-assisted production "
            "systems for consistent high-quality output."
        ),
    ),
    "automation_consulting": ServiceConfig(
        id="automation_consulting",
        name="AI Automation & Consulting",
        short_description=(
            "Workflow audits, AI adoption strategy, process design, "
            "and automation planning."
        ),
    ),
}
