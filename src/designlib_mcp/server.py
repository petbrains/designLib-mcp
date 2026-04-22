from __future__ import annotations
from fastmcp import FastMCP

from designlib_mcp.config import Settings
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.tools import styles, palettes, font_pairs, domains


def build_server() -> FastMCP:
    settings = Settings.from_env()
    repo = SupabaseRepository.from_settings(settings)
    mcp = FastMCP("designlib-mcp")
    styles.register(mcp, repo)
    palettes.register(mcp, repo)
    font_pairs.register(mcp, repo)
    domains.register(mcp, repo)
    return mcp
