from __future__ import annotations

from typing import Any

from apps.analytics.models import AnalyticsEvent
from config.features import FEATURES


def record_event(
    *,
    event: str,
    path: str = "",
    referrer: str = "",
    lead_id: int | None = None,
    project_id: int | None = None,
    utm_source: str = "",
    utm_medium: str = "",
    utm_campaign: str = "",
    metadata: dict[str, Any] | None = None,
) -> AnalyticsEvent | None:
    if not FEATURES.analytics:
        return None

    return AnalyticsEvent.objects.create(
        event=event,
        path=path,
        referrer=referrer,
        lead_id=lead_id,
        project_id=project_id,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        metadata=metadata or {},
    )
