from __future__ import annotations
from typing import Any

from designlib_mcp.config import CHARACTER_LIMIT
from designlib_mcp.formatting.truncate import enforce_character_limit
from designlib_mcp.repository.base import CatalogRepository


def list_inspiration_pages_handler(
    repo: CatalogRepository, *,
    page_type: str | None = None, appearance: str | None = None,
    style_family: str | None = None, industry: str | None = None,
    density: str | None = None, mood: str | None = None,
    keyword: str | None = None, signature: str | None = None,
    good_for_product_type: str | None = None, good_for_stage: str | None = None,
    limit: int = 25, offset: int = 0,
) -> dict[str, Any]:
    raw = repo.list_inspiration_pages(
        page_type=page_type, appearance=appearance,
        style_family=style_family, industry=industry,
        density=density, mood=mood, keyword=keyword, signature=signature,
        good_for_product_type=good_for_product_type,
        good_for_stage=good_for_stage,
        limit=limit, offset=offset,
    )
    payload = {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": None,
            "entity_type": "inspiration_page_list", "truncated": False,
        },
    }
    return enforce_character_limit(payload, limit=CHARACTER_LIMIT)


def get_inspiration_page_handler(repo: CatalogRepository, *, page_id: str) -> dict[str, Any]:
    page = repo.get_inspiration_page(page_id)
    if page is None:
        return {
            "error_code": "NOT_FOUND",
            "message": f"Inspiration page '{page_id}' not found.",
            "field": "page_id",
            "suggest_tool": "list_inspiration_pages",
        }
    page["meta"] = {
        "schema_version": "1.0", "platform": None,
        "entity_type": "inspiration_page", "truncated": False,
    }
    return enforce_character_limit(page, limit=CHARACTER_LIMIT)


def list_inspiration_page_facets_handler(repo: CatalogRepository) -> dict[str, Any]:
    raw = repo.list_inspiration_page_facets()
    return {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": None,
            "entity_type": "inspiration_page_facets", "truncated": False,
        },
    }


def register(mcp, repo: CatalogRepository) -> None:
    @mcp.tool(
        name="list_inspiration_pages",
        description=(
            "List analyzed reference pages (land-book screenshots) filtered by page_type, "
            "appearance, style_family, industry, mood, visual signature, keyword, "
            "good_for_product_type or good_for_stage. Use to find inspiration for a new "
            "page before generating one."
        ),
        annotations={"readOnlyHint": True, "destructiveHint": False,
                     "idempotentHint": True, "openWorldHint": True},
    )
    def list_inspiration_pages(
        page_type: str | None = None, appearance: str | None = None,
        style_family: str | None = None, industry: str | None = None,
        density: str | None = None, mood: str | None = None,
        keyword: str | None = None, signature: str | None = None,
        good_for_product_type: str | None = None, good_for_stage: str | None = None,
        limit: int = 25, offset: int = 0,
    ) -> dict[str, Any]:
        return list_inspiration_pages_handler(
            repo, page_type=page_type, appearance=appearance,
            style_family=style_family, industry=industry,
            density=density, mood=mood, keyword=keyword, signature=signature,
            good_for_product_type=good_for_product_type,
            good_for_stage=good_for_stage,
            limit=limit, offset=offset,
        )

    @mcp.tool(
        name="get_inspiration_page",
        description=(
            "Get a single inspiration page with palette, typography, ordered sections, "
            "primary CTA, generation prompt and constraints — everything needed to "
            "reconstruct or remix the reference."
        ),
        annotations={"readOnlyHint": True, "destructiveHint": False,
                     "idempotentHint": True, "openWorldHint": True},
    )
    def get_inspiration_page(page_id: str) -> dict[str, Any]:
        return get_inspiration_page_handler(repo, page_id=page_id)

    @mcp.tool(
        name="list_inspiration_page_facets",
        description="List available facet values for the inspiration pages catalog.",
        annotations={"readOnlyHint": True, "destructiveHint": False,
                     "idempotentHint": True, "openWorldHint": True},
    )
    def list_inspiration_page_facets() -> dict[str, Any]:
        return list_inspiration_page_facets_handler(repo)
