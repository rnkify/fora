from dataclasses import dataclass

from content.faq import FAQS, FAQItem
from content.home import (
    BENEFITS,
    FINAL_CTA_DESCRIPTION,
    FINAL_CTA_HEADLINE,
    FINAL_CTA_LABEL,
    HERO,
    PROCESS_STEPS,
    BenefitContent,
    HeroContent,
    ProcessStepContent,
)
from content.process import PROCESS_INTRO, PROCESS_PRINCIPLE


@dataclass(frozen=True)
class HomeContent:
    hero: HeroContent
    benefits: tuple[BenefitContent, ...]
    process_steps: tuple[ProcessStepContent, ...]
    final_cta_headline: str
    final_cta_description: str
    final_cta_label: str


@dataclass(frozen=True)
class ProcessContent:
    intro: str
    principle: tuple[str, ...]


def get_home_content() -> HomeContent:
    return HomeContent(
        hero=HERO,
        benefits=BENEFITS,
        process_steps=PROCESS_STEPS,
        final_cta_headline=FINAL_CTA_HEADLINE,
        final_cta_description=FINAL_CTA_DESCRIPTION,
        final_cta_label=FINAL_CTA_LABEL,
    )


def get_faq_content() -> tuple[FAQItem, ...]:
    return FAQS


def get_process_content() -> ProcessContent:
    return ProcessContent(
        intro=PROCESS_INTRO,
        principle=PROCESS_PRINCIPLE,
    )
