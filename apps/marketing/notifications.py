import logging

from django.conf import settings

from apps.core.email import send_message
from apps.marketing.models import Inquiry

logger = logging.getLogger(__name__)


def _inquiry_subject(inquiry: Inquiry) -> str:
    if inquiry.type == Inquiry.Type.PROJECT:
        return f"New Fora project inquiry — {inquiry.name}"

    if inquiry.type == Inquiry.Type.PARTNERSHIP:
        return f"New Fora partnership inquiry — {inquiry.name}"

    return f"New Fora contact inquiry — {inquiry.name}"


def _inquiry_body(inquiry: Inquiry) -> str:
    lines = [
        "A new inquiry was submitted to Fora.",
        "",
        f"Type: {inquiry.get_type_display()}",
        f"Name: {inquiry.name}",
        f"Email: {inquiry.email}",
    ]

    if inquiry.company:
        lines.append(f"Company: {inquiry.company}")

    if inquiry.website:
        lines.append(f"Website: {inquiry.website}")

    if inquiry.service_interest_id:
        lines.append(
            f"Service interest: {inquiry.service_interest_id}"
        )

    if inquiry.plan_interest_id:
        lines.append(
            f"Plan interest: {inquiry.plan_interest_id}"
        )

    lines.extend(
        [
            "",
            "Message:",
            inquiry.message,
            "",
            f"Inquiry ID: {inquiry.pk}",
            f"Landing page: {inquiry.landing_page or '-'}",
            f"Referrer: {inquiry.referrer or '-'}",
        ]
    )

    return "\n".join(lines)


def notify_new_inquiry(inquiry: Inquiry) -> bool:
    recipient = getattr(
        settings,
        "INQUIRY_NOTIFICATION_EMAIL",
        "",
    ).strip()

    if not recipient:
        return False

    try:
        send_message(
            subject=_inquiry_subject(inquiry),
            body=_inquiry_body(inquiry),
            recipients=[recipient],
        )
    except Exception:
        logger.exception(
            "Failed to send notification for inquiry %s.",
            inquiry.pk,
        )
        return False

    return True
