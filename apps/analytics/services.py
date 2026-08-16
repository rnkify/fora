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


def record_request_event(
    *,
    request,
    event: str,
    lead_id: int | None = None,
    project_id: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> AnalyticsEvent | None:
    return record_event(
        event=event,
        path=request.path[:500],
        referrer=request.headers.get("Referer", "")[:500],
        lead_id=lead_id,
        project_id=project_id,
        utm_source=request.GET.get("utm_source", "")[:120],
        utm_medium=request.GET.get("utm_medium", "")[:120],
        utm_campaign=request.GET.get("utm_campaign", "")[:120],
        metadata=metadata,
    )
