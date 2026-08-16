from dataclasses import dataclass


@dataclass(frozen=True)
class HeroContent:
    eyebrow: str
    headline: str
    description: str
    primary_cta: str
    secondary_cta: str


@dataclass(frozen=True)
class BenefitContent:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class ProcessStepContent:
    id: str
    number: str
    title: str
    description: str


HERO = HeroContent(
    eyebrow="AI systems and growth execution",
    headline="Better systems. Better messaging. Better business outcomes.",
    description=(
        "Fora helps agencies and growing technology companies build "
        "reliable AI workflows, conversion-focused messaging, and "
        "repeatable content systems."
    ),
    primary_cta="Start a Project",
    secondary_cta="View Our Work",
)

BENEFITS = (
    BenefitContent(
        id="systemized",
        title="Built as systems",
        description=(
            "Fora creates reusable workflows and assets instead of "
            "one-off outputs that disappear after delivery."
        ),
    ),
    BenefitContent(
        id="commercial",
        title="Commercially focused",
        description=(
            "Work is designed around real business objectives rather "
            "than volume, novelty, or generic AI output."
        ),
    ),
    BenefitContent(
        id="evaluated",
        title="Tested and refined",
        description=(
            "Important variants are compared against clear criteria "
            "before the strongest direction is finalized."
        ),
    ),
)

PROCESS_STEPS = (
    ProcessStepContent(
        id="research",
        number="01",
        title="Research",
        description=(
            "We understand the audience, offer, current workflow, "
            "competitors, constraints, and success criteria."
        ),
    ),
    ProcessStepContent(
        id="build",
        number="02",
        title="Build",
        description=(
            "We create the initial system, messaging, workflow, or "
            "conversion asset with multiple directions where useful."
        ),
    ),
    ProcessStepContent(
        id="evaluate",
        number="03",
        title="Evaluate",
        description=(
            "Outputs are reviewed against accuracy, clarity, brand fit, "
            "commercial usefulness, and agreed project criteria."
        ),
    ),
    ProcessStepContent(
        id="refine",
        number="04",
        title="Refine",
        description=(
            "The strongest direction is improved, documented, and "
            "prepared for practical use."
        ),
    ),
)

FINAL_CTA_HEADLINE = "Build a system your business can actually reuse."
FINAL_CTA_DESCRIPTION = (
    "Tell Fora what you are trying to improve. We will identify the "
    "smallest useful engagement and recommend the next step."
)
FINAL_CTA_LABEL = "Start a Project"
