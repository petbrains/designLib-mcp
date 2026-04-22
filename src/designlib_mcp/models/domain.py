from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import ResponseMeta
from designlib_mcp.models.style import StyleSummary
from designlib_mcp.models.palette import PaletteSummary
from designlib_mcp.models.font_pair import FontPairSummary


class DomainRecommendations(BaseModel):
    model_config = ConfigDict(extra="forbid")
    styles: list[StyleSummary] = Field(default_factory=list)
    palettes: list[PaletteSummary] = Field(default_factory=list)
    font_pairs: list[FontPairSummary] = Field(default_factory=list)


class DomainSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    category_id: str
    audience: str | None = None
    tone: str | None = None
    data_density: str | None = None


class Domain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    category_id: str
    category_name: str
    description: str
    audience: str | None = None
    tone: str | None = None
    data_density: str | None = None
    ui_patterns: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    recommendations: DomainRecommendations
    meta: ResponseMeta


class DomainFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    categories: list
    audiences: list
    tones: list
    data_densities: list
    ui_patterns: list
    meta: ResponseMeta
