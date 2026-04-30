# designlib-mcp

> **A curated design-knowledge catalog for AI coding agents.**
> Stop letting Claude / Cursor / Copilot guess hex codes and font pairings. Give them a real, opinionated source of truth — over MCP.

**Live server:** `https://designlib-production.up.railway.app/mcp`
**Catalog:** 67 styles · 100 palettes · 34 font pairs · 134 domains · 25 chart types · 34 landing patterns · 105 icons · 405 inspiration pages · 120 animations · web + iOS
**Status:** v1, production, read-only.

---

## Why this exists

When you ask an LLM to "design a landing page for a fintech dashboard," it will happily invent `#2B7FFF`, pair Inter with Playfair, and move on. The tokens are plausible. They are also made up. Five prompts later the design has drifted, nothing matches, and you are hand-fixing colors that were never rooted in anything.

**designlib-mcp** replaces that guessing with a retrieval step. It exposes a hand-curated catalog of design styles, palettes, typography, domain recommendations, real-world references and animation snippets through the Model Context Protocol, so any MCP-aware client (Claude Code, Claude Desktop, Cursor, IDE plugins) can fetch authoritative tokens on demand:

- **Palettes** with explicit role mapping (`primary`, `surface`, `text_primary`, contrast pairs) — not just five hexes.
- **Font pairs** with weights, fallbacks, sources and `style_fit` tags.
- **Styles** that bundle palette + typography + spacing + density into a cohesive token set.
- **Domains** (e.g. *fintech_dashboard*, *fitness_app*) with pre-computed top-N recommendations per platform.
- **Chart types** with when-to-use / when-NOT-to-use guidance, accessibility grades and library recommendations.
- **Landing patterns** with section order, CTA placement and conversion optimization notes.
- **Icons** keyed to library, category and style, with ready-to-paste import code and usage snippets.
- **Inspiration pages** — curated real-world page references tagged by style family, industry, mood and signature.
- **Animations** with library, category, complexity and ready-to-paste snippets.

The server is **read-only by design**. It does not write to your repo, does not call OpenAI, does not ship telemetry. It answers MCP queries and that's it.

## When to use it

Use it when:

- You are **building UI with an AI agent** and want consistent, non-hallucinated tokens across a session.
- You are **prototyping multiple styles** for the same product and want to compare them without re-authoring palettes each time.
- You are **scaffolding a design system** and need a sensible starting point keyed to a product domain.
- You are **generating marketing pages, dashboards, mobile screens** and want the agent to pick a coherent palette + typography combo instead of freestyling.

Skip it when:

- You already have a mature design system — use your own tokens.
- You need editable / writable storage — this server is read-only.
- You need brand-specific assets (logos, illustrations, custom icons). This catalog is about **tokens and style direction**, not brand identity.

---

## Install

Zero infra, zero secrets on your machine. Just point your MCP client at the hosted server.

### Claude Code

```bash
claude mcp add --transport http designlib https://designlib-production.up.railway.app/mcp
claude mcp list
```

### Cursor / Windsurf / other MCP-aware clients

Add an HTTP MCP server entry pointing at `https://designlib-production.up.railway.app/mcp`.

### Claude Desktop

Claude Desktop does not speak streamable-http natively — bridge it with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote). Edit `claude_desktop_config.json`:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "designlib": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://designlib-production.up.railway.app/mcp"]
    }
  }
}
```

Restart Claude Desktop and the `designlib` tools should appear.

---

## Tools

All 27 tools are read-only and platform-aware where applicable. Every `list_*` supports `limit` / `offset`; every `get_*` returns a `NOT_FOUND` payload when the id does not exist.

| Tool | Purpose | Key args |
|---|---|---|
| `list_styles` · `get_style` · `list_style_facets` | Complete design styles (palette + typography + density) | `platform`, `family`, `tone`, `density`, `tags` |
| `list_palettes` · `get_palette` · `list_palette_facets` | Palettes with role mapping and contrast pairs | `platform`, `family`, `mood`, `appearance` |
| `list_font_pairs` · `get_font_pair` · `list_font_pair_facets` | Heading + body + mono font pairings | `platform`, `category_id`, `style_fit` |
| `list_domains` · `get_domain` · `list_domain_facets` | Product domains with top-N style/palette/font recommendations | `category_id`, `audience`, `tone`, `top_n` |
| `list_chart_types` · `get_chart_type` · `list_chart_type_facets` | Chart types with when-to-use, accessibility grades, library picks | `data_type`, `a11y_grade`, `library`, `keyword` |
| `list_landing_patterns` · `get_landing_pattern` · `list_landing_pattern_facets` | Landing page layouts with section order and CTA placement | `keyword`, `cta_placement` |
| `list_icons` · `get_icon` · `list_icon_facets` | Individual icons with import code and usage snippets | `category`, `library`, `style`, `keyword` |
| `list_inspiration_pages` · `get_inspiration_page` · `list_inspiration_page_facets` | Curated real-world page references | `page_type`, `style_family`, `industry`, `mood`, `keyword` |
| `list_animations` · `get_animation` · `list_animation_facets` | Animation snippets with library, category, complexity | `category`, `framework`, `complexity`, `library`, `keyword` |
