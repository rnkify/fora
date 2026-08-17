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
            "Fora is a professional service business. We learn how your team "
            "works, then design, test, refine, document, and hand off AI "
            "systems, conversion copy, content systems, or automation plans. "
            "The website explains the services and collects project inquiries; "
            "it does not automatically build the solution after submission."
        ),
    ),
    FAQItem(
        id="software-or-service",
        question="Is Fora software I subscribe to?",
        answer=(
            "No. Fora sells scoped professional services rather than access to "
            "a self-service AI platform. When useful, the engagement can build "
            "around tools your team already uses and includes practical "
            "documentation and handoff."
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
