import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_renders_configured_business_content(client):
    response = client.get(reverse("marketing:home"))

    assert response.status_code == 200

    content = response.content.decode()

    assert "Fora" in content
    assert "AI Systems" in content
    assert "Growth" in content
    assert "Better systems. Better messaging." in content

    for service_path in (
        "/services/ai-systems/",
        "/services/conversion-copy/",
        "/services/content-systems/",
        "/services/ai-automation/",
    ):
        assert f'href="{service_path}"' in content


@pytest.mark.django_db
@pytest.mark.parametrize("route_name", ("marketing:home", "marketing:pricing"))
def test_pricing_cards_keep_description_outside_badge_heading_row(client, route_name):
    response = client.get(reverse(route_name))

    assert response.status_code == 200

    content = response.content.decode()
    growth_card_start = content.index("fora-pricing-card-recommended")
    growth_card_end = content.index("</article>", growth_card_start)
    growth_card = content[growth_card_start:growth_card_end]

    heading_start = growth_card.index("fora-pricing-card-heading")
    heading_end = growth_card.index("</div>", heading_start)
    description_start = growth_card.index("fora-pricing-card-description")

    assert "Recommended" in growth_card[heading_start:heading_end]
    assert description_start > heading_end
    assert "fora-pricing-grid" in content
