from __future__ import annotations
from typing import Any

from designlib_mcp.config import CHARACTER_LIMIT
from designlib_mcp.formatting.truncate import enforce_character_limit
from designlib_mcp.models.common import Platform
from designlib_mcp.repository.base import CatalogRepository


def list_domains_handler(
    repo: CatalogRepository, *,
    category_id: str | None = None, audience: str | None = None,
    tone: str | None = None, limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    raw = repo.list_domains(category_id=category_id, audience=audience,
                            tone=tone, limit=limit, offset=offset)
    payload = {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": None,
            "entity_type": "domain_list", "truncated": False,
        },
    }
    return enforce_character_limit(payload, limit=CHARACTER_LIMIT)


def get_domain_handler(
    repo: CatalogRepository, *, domain_id: str, platform: str, top_n: int = 5,
) -> dict[str, Any]:
    p = Platform(platform)
    domain = repo.get_domain(domain_id, p, top_n=top_n)
    if domain is None:
        return {
            "error_code": "NOT_FOUND",
            "message": f"Domain '{domain_id}' not found.",
            "field": "domain_id",
            "suggest_tool": "list_domains",
        }
    domain["meta"] = {
        "schema_version": "1.0", "platform": platform,
        "entity_type": "domain", "truncated": False,
    }
    return enforce_character_limit(domain, limit=CHARACTER_LIMIT)


def list_domain_facets_handler(repo: CatalogRepository) -> dict[str, Any]:
    raw = repo.list_domain_facets()
    return {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": None,
            "entity_type": "domain_facets", "truncated": False,
        },
    }


def register(mcp, repo: CatalogRepository) -> None:
    @mcp.tool(name="list_domains",
              description="List domains (platform-agnostic) filtered by category/audience/tone.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_domains(category_id: str | None = None, audience: str | None = None,
                     tone: str | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        return list_domains_handler(repo, category_id=category_id, audience=audience,
                                    tone=tone, limit=limit, offset=offset)

    @mcp.tool(name="get_domain",
              description="Get a domain with platform-filtered top-N style/palette/font recommendations.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def get_domain(domain_id: str, platform: str, top_n: int = 5) -> dict[str, Any]:
        return get_domain_handler(repo, domain_id=domain_id, platform=platform, top_n=top_n)

    @mcp.tool(name="list_domain_facets",
              description="List available facet values for the domains catalog.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_domain_facets() -> dict[str, Any]:
        return list_domain_facets_handler(repo)
