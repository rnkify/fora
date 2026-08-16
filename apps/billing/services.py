from apps.billing.providers import BillingProvider, NullBillingProvider
from config.features import FEATURES
from config.integrations import INTEGRATIONS


def get_billing_provider() -> BillingProvider:
    if not FEATURES.billing:
        return NullBillingProvider()

    if INTEGRATIONS.payment_provider == "disabled":
        return NullBillingProvider()

    raise RuntimeError(
        "Configured billing provider is not implemented."
    )
