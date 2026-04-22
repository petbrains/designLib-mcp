from scripts.ingest_ios import (
    build_style_family_row, build_design_style_row,
    build_palette_rows, IOS_FONT_PAIRS,
)


def test_build_style_family_row_minimum():
    defn = {
        "name_en": "Demo",
        "description": "Demo family.",
        "visual_signatures": [], "emotional_keywords": [], "anti_patterns": [],
    }
    row = build_style_family_row("demo_family", defn, sort_order=14)
    assert row["id"] == "demo_family"
    assert row["platform"] == "ios"
    assert row["sort_order"] == 14


def test_build_design_style_row_uses_medians_and_definitions():
    defn = {
        "name_en": "Demo Family",
        "description": "Demo description.",
        "visual_signatures": ["foo"], "emotional_keywords": ["bar"], "anti_patterns": ["baz"],
    }
    medians = {
        "palette_light": {
            "background": "#FAFAFA", "surface_card": "#FFFFFF",
            "text_primary": "#111111", "text_secondary": "#8A8A8A",
            "accent_primary": "#4FB0C6", "separator": "#ECECEC",
        },
        "palette_dark": None,
        "typography": {"body_classification": "sf_pro_text", "heading_classification": "sf_pro_display",
                       "mono_present": False, "tabular_numerics_present": False},
        "layout": {"density_typical": "comfortable", "list_style_dominant": "plain",
                   "corner_radius_cards_pt_median": 18.0},
        "liquid_glass": {"posture": "native_fit", "surfaces_affected": ["tab_bar"]},
        "iconography": "custom_glyph_set",
        "reference_apps": ["alpha"],
    }
    row = build_design_style_row("demo_family", defn, medians)
    assert row["id"] == "demo_family_ios"
    assert row["family_id"] == "demo_family"
    assert row["platform"] == "ios"
    assert row["tokens"]["colors"]["background"] == "#FAFAFA"
    assert row["ios_metadata"]["liquid_glass_posture"] == "native_fit"
    assert row["ios_metadata"]["appearance_support"] == ["light"]
    assert row["ios_metadata"]["reference_apps"] == ["alpha"]


def test_build_palette_rows_returns_light_only_when_dark_missing():
    medians = {
        "palette_light": {"background": "#FAFAFA", "text_primary": "#111", "accent_primary": "#4FB0C6"},
        "palette_dark": None,
        "reference_apps": ["alpha"],
    }
    rows = build_palette_rows("demo_family", "Demo Family", medians)
    assert len(rows) == 1
    assert rows[0]["id"] == "demo_family_ios_light"
    assert rows[0]["platform"] == "ios"


def test_ios_font_pairs_count_matches_spec():
    assert len(IOS_FONT_PAIRS) == 6
    ids = {p["id"] for p in IOS_FONT_PAIRS}
    assert "ios_sf_pro_text_display" in ids
    assert "ios_sf_pro_text_new_york" in ids
