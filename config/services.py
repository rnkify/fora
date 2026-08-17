from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceConfig:
    id: str
    name: str
    short_description: str
    path: str
    deliverables: tuple[str, ...]
    enabled: bool = True


SERVICES = {
    "ai_systems": ServiceConfig(
        id="ai_systems",
        name="AI Systems",
        short_description=(
            "Reusable AI workflows, prompts, structured outputs, "
            "evaluation systems, and internal assistants."
        ),
        path="/services/ai-systems/",
        deliverables=(
            "Workflow map",
            "Reusable prompt and workflow architecture",
            "Implementation setup",
            "Evaluation criteria",
            "Operating documentation and team handoff",
        ),
    ),
    "conversion_copy": ServiceConfig(
        id="conversion_copy",
        name="Conversion Copy",
        short_description=(
            "Landing pages, email systems, sales messaging, "
            "advertising, and conversion-focused optimization."
        ),
        path="/services/conversion-copy/",
        deliverables=(
            "Messaging framework",
            "Landing-page copy",
            "Email sequences",
            "Offer positioning",
            "Reusable messaging guidance",
        ),
    ),
    "content_systems": ServiceConfig(
        id="content_systems",
        name="Content Systems",
        short_description=(
            "Repeatable content strategy and AI-assisted production "
            "systems for consistent high-quality output."
        ),
        path="/services/content-systems/",
        deliverables=(
            "Structured content intake",
            "Reusable AI workflow and prompt templates",
            "Output templates",
            "Quality-control checklist",
            "Tested sample workflows",
            "Operating SOP and implementation documentation",
        ),
    ),
    "automation_consulting": ServiceConfig(
        id="automation_consulting",
        name="AI Automation & Consulting",
        short_description=(
            "Workflow audits, AI adoption strategy, process design, "
            "and automation planning."
        ),
        path="/services/ai-automation/",
        deliverables=(
            "Workflow audit",
            "Prioritized automation opportunities",
            "Implementation plan",
            "Configured workflows where included in scope",
            "Documentation and team handoff",
        ),
    ),
}
