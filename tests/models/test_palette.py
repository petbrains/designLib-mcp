from designlib_mcp.models.palette import (
    ColorRole, ContrastPair, PaletteSummary, Palette, PaletteFacets,
)
from designlib_mcp.models.common import Platform, Appearance, ResponseMeta


def test_color_role_minimal():
    r = ColorRole(role="background", hex="#FFFFFF")
    assert r.p3_hex is None


def test_contrast_pair_flags_aaa_normal():
    p = ContrastPair(
        foreground_role="text_primary", background_role="background",
        ratio=7.2, wcag_aa_normal=True, wcag_aa_large=True, wcag_aaa_normal=True,
    )
    assert p.wcag_aaa_normal is True


def test_palette_summary_5_swatches():
    s = PaletteSummary(
        id="warm-1", name="Warm 1", platform=Platform.WEB, appearance=Appearance.LIGHT,
        main_swatches=["#A", "#B", "#C", "#D", "#E"],
    )
    assert len(s.main_swatches) == 5


def test_palette_full_with_used_by():
    p = Palette(
        id="ios-fitness-light", name="iOS Fitness Light",
        platform=Platform.IOS, appearance=Appearance.LIGHT,
        roles=[ColorRole(role="background", hex="#F8F8F8")],
        source="ios_aggregated", reference_apps=["any_distance"],
        used_by_styles=["fitness_vitality_ios"],
        meta=ResponseMeta(entity_type="palette", platform=Platform.IOS),
    )
    assert p.source == "ios_aggregated"
    assert p.reference_apps == ["any_distance"]
