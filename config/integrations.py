from dataclasses import dataclass

from config.env import env


@dataclass(frozen=True)
class IntegrationConfig:
    analytics_provider: str
    payment_provider: str
    ai_provider: str
    email_provider: str


INTEGRATIONS = IntegrationConfig(
    analytics_provider=env(
        "ANALYTICS_PROVIDER",
        "disabled",
    )
    or "disabled",
    payment_provider=env(
        "PAYMENT_PROVIDER",
        "disabled",
    )
    or "disabled",
    ai_provider=env(
        "AI_PROVIDER",
        "disabled",
    )
    or "disabled",
    email_provider=env(
        "EMAIL_PROVIDER",
        "console",
    )
    or "console",
)
