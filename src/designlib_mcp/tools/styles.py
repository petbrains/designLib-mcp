from __future__ import annotations
from typing import Any

from designlib_mcp.config import CHARACTER_LIMIT
from designlib_mcp.formatting.truncate import enforce_character_limit
from designlib_mcp.models.common import Platform
from designlib_mcp.repository.base import CatalogRepository
from designlib_mcp.services.cross_links import cross_links_for_style


def list_styles_handler(
    repo: CatalogRepository, *,
    platform: str,
    family: str | None = None,
    appearance: str | None = None,
    tone: str | None = None,
    density: str | None = None,
    tags: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_styles(
        p, family=family, appearance=appearance, tone=tone,
        density=density, tags=tags, limit=limit, offset=offset,
    )
    payload = {
        "items": raw["items"],
        "total_count": raw["total_count"],
        "limit": limit,
        "offset": offset,
        "meta": {
            "schema_version": "1.0",
            "platform": platform,
            "entity_type": "style_list",
            "truncated": False,
        },
    }
    return enforce_character_limit(payload, limit=CHARACTER_LIMIT)


def get_style_handler(
    repo: CatalogRepository, *,
    style_id: str,
    include_cross_links: bool = True,
    cross_links_limit: int = 5,
) -> dict[str, Any]:
    style = repo.get_style(style_id)
    if style is None:
        return {
            "error_code": "NOT_FOUND",
            "message": f"Style '{style_id}' not found.",
            "field": "style_id",
            "suggest_tool": "list_styles",
        }
    if include_cross_links:
        style["cross_links"] = cross_links_for_style(repo, style_id, limit=cross_links_limit)
    style["meta"] = {
        "schema_version": "1.0",
        "platform": style.get("platform"),
        "entity_type": "style",
        "truncated": False,
    }
    return enforce_character_limit(style, limit=CHARACTER_LIMIT)


def list_style_facets_handler(
    repo: CatalogRepository, *, platform: str,
) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_style_facets(p)
    return {
        **raw,
        "meta": {
            "schema_version": "1.0",
            "platform": platform,
            "entity_type": "style_facets",
            "truncated": False,
        },
    }


def register(mcp, repo: CatalogRepository) -> None:
    @mcp.tool(
        name="list_styles",
        description="List design styles filtered by platform and optional facets.",
        annotations={
            "readOnlyHint": True, "destructiveHint": False,
            "idempotentHint": True, "openWorldHint": True,
        },
    )
    def list_styles(
        platform: str,
        family: str | None = None,
        appearance: str | None = None,
        tone: str | None = None,
        density: str | None = None,
        tags: list[str] | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        return list_styles_handler(
            repo, platform=platform, family=family, appearance=appearance,
            tone=tone, density=density, tags=tags, limit=limit, offset=offset,
        )

    @mcp.tool(
        name="get_style",
        description="Get a single design style with full tokens and optional cross-links.",
        annotations={
            "readOnlyHint": True, "destructiveHint": False,
            "idempotentHint": True, "openWorldHint": True,
        },
    )
    def get_style(
        style_id: str,
        include_cross_links: bool = True,
        cross_links_limit: int = 5,
    ) -> dict[str, Any]:
        return get_style_handler(
            repo, style_id=style_id,
            include_cross_links=include_cross_links,
            cross_links_limit=cross_links_limit,
        )

    @mcp.tool(
        name="list_style_facets",
        description="List available facet values for the styles catalog.",
        annotations={
            "readOnlyHint": True, "destructiveHint": False,
            "idempotentHint": True, "openWorldHint": True,
        },
    )
    def list_style_facets(platform: str) -> dict[str, Any]:
        return list_style_facets_handler(repo, platform=platform)
