from designlib_mcp.models.font_pair import (
    FontSpec, FontPairSummary, FontPair, FontPairFacets,
)
from designlib_mcp.models.common import Platform, ResponseMeta


def test_font_spec_system_font_no_url():
    s = FontSpec(font_family="SF Pro Text", weights=[400, 500, 700], is_system_font=True)
    assert s.google_fonts_url is None


def test_font_spec_google_font_url():
    s = FontSpec(
        font_family="Inter", weights=[400, 600, 700],
        google_fonts_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
    )
    assert "Inter" in s.google_fonts_url


def test_font_pair_full():
    p = FontPair(
        id="inter-inter", name="Inter / Inter",
        platform=Platform.WEB, category_id="modern_sans", category_name="Modern Sans",
        heading=FontSpec(font_family="Inter"), body=FontSpec(font_family="Inter"),
        style_fit=["polished_modern"],
        meta=ResponseMeta(entity_type="font_pair", platform=Platform.WEB),
    )
    assert p.mono is None
