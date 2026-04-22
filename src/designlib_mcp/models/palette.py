from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import Platform, Appearance, ResponseMeta


class ColorRole(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    hex: str
    p3_hex: str | None = None


class ContrastPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    foreground_role: str
    background_role: str
    ratio: float
    wcag_aa_normal: bool
    wcag_aa_large: bool
    wcag_aaa_normal: bool


class PaletteSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    platform: Platform
    appearance: Appearance
    main_swatches: list[str] = Field(default_factory=list, max_length=5)


class Palette(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    description: str | None = None
    platform: Platform
    appearance: Appearance
    roles: list[ColorRole]
    background_mode: str | None = None
    p3_likely: bool = False
    mood: Literal["warm", "cool", "neutral", "mixed"] | None = None
    tags: list[str] = Field(default_factory=list)
    contrast_pairs: list[ContrastPair] = Field(default_factory=list)
    source: Literal["curated", "ios_aggregated"] = "curated"
    reference_apps: list[str] = Field(default_factory=list)
    used_by_styles: list[str] = Field(default_factory=list)
    meta: ResponseMeta


class PaletteFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    families: list
    moods: list
    appearances: list
    background_modes: list
    meta: ResponseMeta
