import pytest
from pydantic import ValidationError
from designlib_mcp.models.style import (
    ColorTokens, TypographyTokens, LayoutTokens, StyleTokens,
    IosMetadata, StyleSummary, Style, StyleCrossLinks, StyleFacets,
    CrossLinkPalette, CrossLinkFontPair, CrossLinkDomain,
)
from designlib_mcp.models.common import Platform, Density, Appearance, ResponseMeta


def test_color_tokens_required_roles():
    ct = ColorTokens(
        background="#FFFFFF", surface="#FAFAFA", border="#ECECEC",
        text_primary="#111111", text_secondary="#8A8A8A", primary="#4FB0C6",
    )
    assert ct.background == "#FFFFFF"
    assert ct.extras == {}


def test_color_tokens_extras_holds_unmapped():
    ct = ColorTokens(
        background="#000", surface="#111", border="#222",
        text_primary="#FFF", text_secondary="#AAA", primary="#0F0",
        extras={"section_dark_text": "#E8DFD4"},
    )
    assert ct.extras["section_dark_text"] == "#E8DFD4"


def test_ios_metadata_minimum_shape():
    m = IosMetadata(
        liquid_glass_posture="native_fit",
        appearance_support=[Appearance.LIGHT, Appearance.DARK],
        iconography="custom_glyph_set",
    )
    assert m.surfaces_affected == []
    assert m.reference_apps == []


def test_style_summary_serializes_with_meta_omitted():
    s = StyleSummary(
        id="academia_classical", name="Academia Classical", family_id="classical",
        platform=Platform.WEB, short_description="…",
        top_signatures=["serif_double", "brass_accents", "parchment_text"],
        primary_swatch="#C9A962",
    )
    assert s.platform == Platform.WEB


def test_style_full_with_cross_links():
    tokens = StyleTokens(
        colors=ColorTokens(
            background="#FFFFFF", surface="#FAFAFA", border="#ECECEC",
            text_primary="#111111", text_secondary="#8A8A8A", primary="#4FB0C6",
        ),
        typography=TypographyTokens(heading_font="Inter", body_font="Inter"),
    )
    style = Style(
        id="x", name="X", family_id="polished", family_name="Polished",
        platform=Platform.WEB, description="d",
        visual_signatures=[], emotional_keywords=[], anti_patterns=[],
        tokens=tokens,
        cross_links=StyleCrossLinks(
            palettes=[CrossLinkPalette(palette_id="p1", name="P1", score=0.9)],
            font_pairs=[CrossLinkFontPair(font_pair_id="f1", name="F1")],
            domains=[CrossLinkDomain(domain_id="d1", name="D1", category_id="c1")],
        ),
        meta=ResponseMeta(entity_type="style", platform=Platform.WEB),
    )
    payload = style.model_dump()
    assert payload["cross_links"]["palettes"][0]["score"] == 0.9


def test_style_facets_payload_shape():
    facets = StyleFacets(
        families=[], tones=[], densities=[], appearances=[], tag_vocabulary=[],
        meta=ResponseMeta(entity_type="style_facets", platform=Platform.IOS),
    )
    assert facets.meta.platform == Platform.IOS
