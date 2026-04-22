from __future__ import annotations
from typing import Any

from designlib_mcp.models.common import Platform
from designlib_mcp.repository.base import CatalogRepository


def cross_links_for_style(
    repo: CatalogRepository, style_id: str, *, limit: int = 5,
) -> dict[str, Any]:
    palettes = repo.palettes_used_by_style(style_id, limit=limit)
    fonts = repo.font_pairs_used_by_style(style_id, limit=limit)
    domain_scores = repo.style_domain_scores(style_id, limit=limit)
    return {
        "palettes": [{"palette_id": p["id"], "name": p["name"], "score": None} for p in palettes],
        "font_pairs": [{"font_pair_id": f["id"], "name": f["name"], "score": None} for f in fonts],
        "domains": [
            {"domain_id": d["domain_id"], "name": d["name"],
             "category_id": d["category_id"], "score": d["score"]}
            for d in domain_scores
        ],
    }


def recommendations_for_domain(
    repo: CatalogRepository, domain_id: str, platform: Platform, *, top_n: int = 5,
) -> dict[str, Any]:
    styles = repo.domain_top_styles(domain_id, platform, limit=top_n)
    palettes: list[dict[str, Any]] = []
    fonts: list[dict[str, Any]] = []
    for s in styles:
        palettes.extend(repo.palettes_used_by_style(s["id"], limit=2))
        fonts.extend(repo.font_pairs_used_by_style(s["id"], limit=2))
    palettes_uniq = {p["id"]: p for p in palettes}
    fonts_uniq = {f["id"]: f for f in fonts}
    return {
        "styles": [{k: v for k, v in s.items() if k != "score"} for s in styles],
        "palettes": list(palettes_uniq.values())[:top_n],
        "font_pairs": list(fonts_uniq.values())[:top_n],
    }
