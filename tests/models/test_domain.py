from designlib_mcp.models.domain import (
    DomainSummary, Domain, DomainRecommendations, DomainFacets,
)
from designlib_mcp.models.common import Platform, ResponseMeta


def test_domain_summary_minimum():
    d = DomainSummary(id="travel-airbnb", name="Travel: Airbnb", category_id="travel")
    assert d.tone is None


def test_domain_full_with_recommendations():
    d = Domain(
        id="x", name="X", category_id="c", category_name="C", description="desc",
        ui_patterns=["search", "card_grid"], examples=["airbnb"],
        recommendations=DomainRecommendations(),
        meta=ResponseMeta(entity_type="domain", platform=Platform.WEB),
    )
    assert d.recommendations.styles == []
