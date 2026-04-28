from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import ResponseMeta

Category = Literal["background", "hero", "loader", "text_effect",
                   "element", "cursor_effect", "overlay", "decoration"]
Framework = Literal["react", "vanilla_html"]
Interactivity = Literal["static", "hover", "click", "cursor_track",
                        "scroll", "mount_only"]
Complexity = Literal["light", "medium", "heavy"]


class AnimationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    description: str
    category: Category
    framework: Framework
    complexity: Complexity
    style_tags: list[str] = Field(default_factory=list)


class Animation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    description: str
    use_when: list[str] = Field(default_factory=list)
    category: Category
    framework: Framework
    libraries: list[str] = Field(default_factory=list)
    interactivity: Interactivity
    complexity: Complexity
    style_tags: list[str] = Field(default_factory=list)
    placement: list[str] = Field(default_factory=list)
    keyword: list[str] = Field(default_factory=list)
    component_filename: str
    prompt_text: str
    meta: ResponseMeta


class AnimationFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    categories: list
    frameworks: list
    libraries: list
    interactivity: list
    complexity: list
    style_tags: list
    placement: list
    use_when: list
    meta: ResponseMeta
