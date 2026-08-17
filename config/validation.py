from config.brand import BRAND
from config.pricing import PLANS
from config.services import SERVICES


def validate_configuration() -> None:
    if not BRAND.name.strip():
        raise RuntimeError("Brand name cannot be empty.")

    if len(SERVICES) != len(set(SERVICES)):
        raise RuntimeError("Duplicate service IDs detected.")

    if len(PLANS) != len(set(PLANS)):
        raise RuntimeError("Duplicate plan IDs detected.")

    for key, service in SERVICES.items():
        if key != service.id:
            raise RuntimeError(
                f"Service key {key!r} does not match ID {service.id!r}."
            )

        if not service.name.strip():
            raise RuntimeError(
                f"Service {service.id!r} has no public name."
            )

        if not service.path.startswith("/services/"):
            raise RuntimeError(
                f"Service {service.id!r} must define a public service path."
            )

    for key, plan in PLANS.items():
        if key != plan.id:
            raise RuntimeError(
                f"Plan key {key!r} does not match ID {plan.id!r}."
            )

        if plan.price < 0:
            raise RuntimeError(
                f"Plan {plan.id!r} cannot have a negative price."
            )

        if not plan.currency:
            raise RuntimeError(
                f"Plan {plan.id!r} must define a currency."
            )
