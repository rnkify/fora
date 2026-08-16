from unittest.mock import patch

import pytest

from apps.analytics.models import AnalyticsEvent
from apps.analytics.services import record_event
from config.features import FeatureFlags


def feature_flags(*, analytics: bool) -> FeatureFlags:
    return FeatureFlags(
        billing=False,
        blog=False,
        client_portal=False,
        booking=False,
        analytics=analytics,
        ai_features=False,
        digital_products=False,
    )


@pytest.mark.django_db
def test_record_event_returns_none_when_disabled():
    with patch(
        "apps.analytics.services.FEATURES",
        feature_flags(analytics=False),
    ):
        result = record_event(
            event=AnalyticsEvent.Event.PAGE_VIEW,
            path="/",
        )

    assert result is None
    assert AnalyticsEvent.objects.count() == 0


@pytest.mark.django_db
def test_record_event_persists_when_enabled():
    with patch(
        "apps.analytics.services.FEATURES",
        feature_flags(analytics=True),
    ):
        result = record_event(
            event=AnalyticsEvent.Event.PAGE_VIEW,
            path="/pricing/",
            utm_source="linkedin",
            metadata={"cta": "growth"},
        )

    assert result is not None
    assert result.event == AnalyticsEvent.Event.PAGE_VIEW
    assert result.path == "/pricing/"
    assert result.utm_source == "linkedin"
    assert result.metadata == {"cta": "growth"}
