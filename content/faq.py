from dataclasses import dataclass


@dataclass(frozen=True)
class FAQItem:
    id: str
    question: str
    answer: str


FAQS = (
    FAQItem(
        id="what-fora-does",
        question="What does Fora actually do?",
        answer=(
            "Fora designs AI systems, conversion-focused copy, content "
            "systems, and automation strategies for agencies and growing "
            "technology businesses."
        ),
    ),
    FAQItem(
        id="project-or-retainer",
        question="Do you work on projects or retainers?",
        answer=(
            "Both. Most new clients begin with a focused project. "
            "Ongoing optimization and agency fulfillment can then move "
            "to a monthly retainer."
        ),
    ),
    FAQItem(
        id="ai-only",
        question="Is Fora only a prompt engineering service?",
        answer=(
            "No. Prompt engineering is one capability inside a broader "
            "AI systems and growth offering that includes workflows, "
            "messaging, content systems, and consulting."
        ),
    ),
    FAQItem(
        id="white-label",
        question="Can agencies use Fora as a white-label partner?",
        answer=(
            "Yes. Fora can provide behind-the-scenes fulfillment for "
            "agencies that need additional AI, copy, or content-system "
            "capacity."
        ),
    ),
    FAQItem(
        id="revisions",
        question="How are revisions handled?",
        answer=(
            "Revision allowances depend on the selected package. "
            "Additional work outside the agreed scope is quoted "
            "separately."
        ),
    ),
)
