from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import Platform, ResponseMeta


class FontSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    font_family: str
    weights: list[int] = Field(default_factory=list)
    fallbacks: list[str] = Field(default_factory=list)
    google_fonts_url: str | None = None
    is_system_font: bool = False


class FontPairSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    platform: Platform
    category_id: str
    heading_family: str
    body_family: str


class FontPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    description: str | None = None
    platform: Platform
    category_id: str
    category_name: str
    heading: FontSpec
    body: FontSpec
    mono: FontSpec | None = None
    style_fit: list[str] = Field(default_factory=list)
    domain_fit: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    compatible_styles: list[str] = Field(default_factory=list)
    meta: ResponseMeta


class FontPairFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    categories: list
    tags: list
    meta: ResponseMeta
