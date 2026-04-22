from __future__ import annotations
from typing import Any

from designlib_mcp.config import CHARACTER_LIMIT
from designlib_mcp.formatting.truncate import enforce_character_limit
from designlib_mcp.models.common import Platform
from designlib_mcp.repository.base import CatalogRepository


def list_font_pairs_handler(
    repo: CatalogRepository, *,
    platform: str, category_id: str | None = None,
    style_fit: list[str] | None = None, tags: list[str] | None = None,
    limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_font_pairs(p, category_id=category_id, style_fit=style_fit,
                               tags=tags, limit=limit, offset=offset)
    payload = {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": platform,
            "entity_type": "font_pair_list", "truncated": False,
        },
    }
    return enforce_character_limit(payload, limit=CHARACTER_LIMIT)


def get_font_pair_handler(repo: CatalogRepository, *, font_pair_id: str) -> dict[str, Any]:
    fp = repo.get_font_pair(font_pair_id)
    if fp is None:
        return {
            "error_code": "NOT_FOUND",
            "message": f"Font pair '{font_pair_id}' not found.",
            "field": "font_pair_id",
            "suggest_tool": "list_font_pairs",
        }
    fp["meta"] = {
        "schema_version": "1.0", "platform": fp.get("platform"),
        "entity_type": "font_pair", "truncated": False,
    }
    return enforce_character_limit(fp, limit=CHARACTER_LIMIT)


def list_font_pair_facets_handler(repo: CatalogRepository, *, platform: str) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_font_pair_facets(p)
    return {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": platform,
            "entity_type": "font_pair_facets", "truncated": False,
        },
    }


def register(mcp, repo: CatalogRepository) -> None:
    @mcp.tool(name="list_font_pairs",
              description="List font pairs filtered by platform and optional facets.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_font_pairs(platform: str, category_id: str | None = None,
                        style_fit: list[str] | None = None, tags: list[str] | None = None,
                        limit: int = 50, offset: int = 0) -> dict[str, Any]:
        return list_font_pairs_handler(repo, platform=platform, category_id=category_id,
                                       style_fit=style_fit, tags=tags,
                                       limit=limit, offset=offset)

    @mcp.tool(name="get_font_pair",
              description="Get a single font pair with full heading/body/mono specs.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def get_font_pair(font_pair_id: str) -> dict[str, Any]:
        return get_font_pair_handler(repo, font_pair_id=font_pair_id)

    @mcp.tool(name="list_font_pair_facets",
              description="List available facet values for the font pairs catalog.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_font_pair_facets(platform: str) -> dict[str, Any]:
        return list_font_pair_facets_handler(repo, platform=platform)
