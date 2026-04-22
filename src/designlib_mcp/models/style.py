from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import (
    Platform, Appearance, Density, ResponseMeta,
)


class ColorTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    background: str
    background_subtle: str | None = None
    surface: str
    surface_hover: str | None = None
    border: str
    border_subtle: str | None = None
    text_primary: str
    text_secondary: str
    text_muted: str | None = None
    primary: str
    primary_hover: str | None = None
    text_on_primary: str | None = None
    success: str | None = None
    warning: str | None = None
    error: str | None = None
    section_alt: str | None = None
    section_dark: str | None = None
    section_accent: str | None = None
    extras: dict[str, str] = Field(default_factory=dict)


class TypographyTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    heading_font: str
    heading_weight: str | None = None
    body_font: str
    body_weight: str | None = None
    mono_font: str | None = None
    base_size_px: int | None = None
    scale_ratio: float | None = None
    letter_spacing_heading: str | None = None


class LayoutTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    density: Density | None = None
    corner_radius_card_px: int | None = None
    corner_radius_button_px: int | None = None
    container_max_width_px: int | None = None
    grid_columns: int | None = None


class InputTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    height_px: int | None = None
    padding_x_px: int | None = None
    padding_y_px: int | None = None
    font_size_px: int | None = None
    focus_style: str | None = None
    focus_ring: str | None = None


class MediaTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    icon_style: str | None = None
    icon_weight: str | None = None
    avatar_shape: str | None = None
    image_aspect_ratio: str | None = None
    illustration_style: str | None = None


class MotionTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    duration_base_ms: int | None = None
    easing: str | None = None


class StyleTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    colors: ColorTokens
    typography: TypographyTokens
    layout: LayoutTokens | None = None
    inputs: InputTokens | None = None
    media: MediaTokens | None = None
    motion: MotionTokens | None = None


class IosMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    liquid_glass_posture: Literal["native_fit", "selective", "none", "unclear"]
    surfaces_affected: list[str] = Field(default_factory=list)
    list_style_dominant: str | None = None
    density_typical: Density | None = None
    appearance_support: list[Appearance] = Field(default_factory=list)
    corner_radius_cards_pt_median: float | None = None
    iconography: Literal[
        "sf_symbols_only", "custom_glyph_set", "mixed", "photographic", "unclear"
    ]
    reference_apps: list[str] = Field(default_factory=list)


class StyleSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    family_id: str
    platform: Platform
    short_description: str
    top_signatures: list[str] = Field(default_factory=list, max_length=3)
    primary_swatch: str


class CrossLinkPalette(BaseModel):
    model_config = ConfigDict(extra="forbid")
    palette_id: str
    name: str
    score: float | None = None
    reason: str | None = None


class CrossLinkFontPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    font_pair_id: str
    name: str
    score: float | None = None


class CrossLinkDomain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    domain_id: str
    name: str
    category_id: str
    score: float | None = None


class StyleCrossLinks(BaseModel):
    model_config = ConfigDict(extra="forbid")
    palettes: list[CrossLinkPalette] = Field(default_factory=list)
    font_pairs: list[CrossLinkFontPair] = Field(default_factory=list)
    domains: list[CrossLinkDomain] = Field(default_factory=list)


class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    family_id: str
    family_name: str
    platform: Platform
    description: str
    visual_signatures: list[str] = Field(default_factory=list)
    emotional_keywords: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)
    tokens: StyleTokens
    ios_metadata: IosMetadata | None = None
    cross_links: StyleCrossLinks | None = None
    meta: ResponseMeta


class StyleFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    families: list
    tones: list
    densities: list
    appearances: list
    tag_vocabulary: list
    meta: ResponseMeta
