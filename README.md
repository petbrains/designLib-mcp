# designlib-mcp

> **A curated design-knowledge catalog for AI coding agents.**
> Stop letting Claude / Cursor / Copilot guess hex codes and font pairings. Give them a real, opinionated source of truth — over MCP.

**Live server:** `https://designlib-production.up.railway.app/mcp`
**Catalog:** 67 styles · 100 palettes · 34 font pairs · 134 domains · web + iOS
**Status:** v1, production, read-only.

---

## Why this exists

When you ask an LLM to "design a landing page for a fintech dashboard," it will happily invent `#2B7FFF`, pair Inter with Playfair, and move on. The tokens are plausible. They are also made up. Five prompts later the design has drifted, nothing matches, and you are hand-fixing colors that were never rooted in anything.

**designlib-mcp** replaces that guessing with a retrieval step. It exposes a hand-curated catalog of design styles, palettes, typography and domain recommendations through the Model Context Protocol, so any MCP-aware client (Claude Code, Claude Desktop, Cursor, IDE plugins) can fetch authoritative tokens on demand:

- Palettes with explicit role mapping (`primary`, `surface`, `text_primary`, contrast pairs) — not just five hexes.
- Font pairs with weights, fallbacks, sources and `style_fit` tags.
- Styles that bundle palette + typography + spacing + density into a cohesive token set.
- Domains (e.g. *fintech_dashboard*, *fitness_app*) with pre-computed top-N recommendations per platform.

The server is **read-only by design**. It does not write to your repo, does not call OpenAI, does not ship telemetry. It answers queries over stdio or HTTP and that's it.

---

## When to use it

Use it when:

- You are **building UI with an AI agent** and want consistent, non-hallucinated tokens across a session.
- You are **prototyping multiple styles** for the same product and want to compare them without re-authoring palettes each time.
- You are **scaffolding a design system** and need a sensible starting point keyed to a product domain.
- You are **generating marketing pages, dashboards, mobile screens** and want the agent to pick a coherent palette + typography combo instead of freestyling.

Skip it when:

- You already have a mature design system — use your own tokens.
- You need editable / writable storage — this server is read-only.
- You need brand-specific assets (logos, illustrations, icons). This catalog is about **tokens and style direction**, not brand identity.

---

## What's in the catalog

| Entity | Count | What you get |
|---|---:|---|
| **Styles** | 67 | Complete token bundles — palette + typography + spacing + density + appearance. Tagged with `family`, `tone`, `platform`. |
| **Palettes** | 100 | Role-mapped color systems (`primary` / `surface` / `text` / etc.) with pre-computed contrast pairs and mood tags. |
| **Font pairs** | 34 | Heading / body / mono triples with weights, fallbacks, licenses, and `style_fit` taxonomy. |
| **Domains** | 134 | Product contexts (fintech, fitness, academia, e-commerce…) with top-N style / palette / font recommendations per platform. |

Both **web** and **iOS** are first-class platforms. iOS styles go through a separate median pipeline so Apple-native conventions (SF family, system spacing) are preserved instead of being flattened into web assumptions.

---

## Quick start — hosted (recommended)

Zero infra, zero secrets on your machine. Point your MCP client at the hosted server:

### Claude Code

```bash
claude mcp add --transport http designlib https://designlib-production.up.railway.app/mcp
claude mcp list
```

That's it. Ask the agent:

> *"Use designlib to pick a style for a fintech dashboard on web, then show me the palette and font pair."*

### Cursor / Windsurf / other MCP-aware clients

Add an HTTP MCP server entry pointing at `https://designlib-production.up.railway.app/mcp`. Follow your client's MCP config instructions.

### Claude Desktop (stdio, local)

Claude Desktop does not speak streamable-http yet. For it, self-host over stdio — see [Self-hosting](#self-hosting) below.

---

## Tools

All 12 tools are read-only. Lists are paginated (`limit` / `offset`), and every response is wrapped in a consistent envelope with `meta.schema_version`, `meta.platform`, `meta.entity_type`, and `meta.truncated`. Unknown IDs return a structured `{ error_code: "NOT_FOUND", message, field, suggest_tool }` — never an exception.

| Tool | Arguments | What it does |
|---|---|---|
| `list_style_facets` | `platform` | Enumerates valid `family` / `tone` / `density` / `appearance` / tag values for a platform |
| `list_styles` | `platform`, `family?`, `appearance?`, `tone?`, `density?`, `tags?`, `limit=50`, `offset=0` | Shortlist of styles with summaries |
| `get_style` | `style_id`, `include_cross_links=true`, `cross_links_limit=5` | Full token bundle + cross-links to palettes / fonts / domains |
| `list_palette_facets` | `platform` | Valid `family` / `mood` / `appearance` / tag values |
| `list_palettes` | `platform`, `family?`, `appearance?`, `mood?`, `tags?`, `limit`, `offset` | Shortlist of palettes |
| `get_palette` | `palette_id` | Full role mapping + contrast pairs |
| `list_font_pair_facets` | `platform` | Valid `category` / `style_fit` / tag values |
| `list_font_pairs` | `platform`, `category_id?`, `style_fit?`, `tags?`, `limit`, `offset` | Shortlist of font pairs |
| `get_font_pair` | `font_pair_id` | Heading / body / mono specs with weights, sources, fallbacks |
| `list_domain_facets` | — | Valid `category` / `audience` / `tone` values |
| `list_domains` | `category_id?`, `audience?`, `tone?`, `limit`, `offset` | Platform-agnostic domain catalog |
| `get_domain` | `domain_id`, `platform`, `top_n=5` | Domain + top-N style / palette / font recommendations for that platform |

Payloads over 25 000 characters are truncated with `meta.truncated=true`; in practice this only happens on very wide `list_*` calls — lower `limit` or paginate.

---

## Worked examples

### Domain-first: "build me a fintech dashboard"

```
1. list_domain_facets()
       → learn valid audiences / tones
2. list_domains(audience="fintech", tone="trustworthy")
       → shortlist
3. get_domain(domain_id="fintech_dashboard", platform="web", top_n=3)
       → top 3 styles + their palettes + font pairs
4. get_style(style_id=<picked>) / get_palette(palette_id=<picked>)
       → full tokens for the final pick
```

### Style-first: "show me iOS-native styles"

```
1. list_style_facets(platform="ios")
       → 10 iOS families with their tones/densities
2. list_styles(platform="ios", family="fitness_vitality", limit=5)
3. get_style(style_id="fitness_vitality_ios")
       → tokens + cross_links.palettes / font_pairs / domains
```

### Prompt patterns that work well

- **"Find a style for a fintech dashboard and give me the palette + typography"** → chains `list_domains` → `get_domain` → `get_palette` → `get_font_pair`.
- **"Show me all iOS-native styles in the `fitness_vitality` family"** → `list_styles(platform="ios", family="fitness_vitality")`.
- **"What are the tokens for `academia_classical`?"** → `get_style(style_id="academia_classical")`.
- Tell the agent to **call `list_*_facets` first** when it doesn't know valid values for `family` / `tone` / `audience`. Otherwise it tends to invent them.

### Response envelope

```json
{
  "items": [ { "id": "...", "name": "...", "summary": "...", "...": "..." } ],
  "total_count": 57,
  "limit": 50,
  "offset": 0,
  "meta": {
    "schema_version": "1.0",
    "platform": "web",
    "entity_type": "style_list",
    "truncated": false
  }
}
```

---

## Self-hosting

Run your own copy when you want to customize the catalog, keep data inside your infra, or serve Claude Desktop over stdio.

### 1. Provision Supabase

Free tier is fine. From Project Settings → API, capture `SUPABASE_URL` and `SUPABASE_ANON_KEY` (the `sb_publishable_…` format works). From Settings → Database, capture `DATABASE_URL` (used only by the migration script).

Copy `.env.example` → `.env` and fill those in.

### 2. Install

```bash
python -m venv .venv
source .venv/Scripts/activate     # Windows bash; POSIX: .venv/bin/activate
pip install -e ".[dev]"
```

### 3. Migrate + seed

```bash
python scripts/apply_migrations.py
python scripts/ingest_web.py
python scripts/compute_ios_medians.py
python scripts/ingest_ios.py
```

The `ingest_*.py` scripts write via the Supabase REST API. If RLS blocks writes after migration 001, use a service-role key for the ingest step only.

### 4. Run

```bash
# stdio — Claude Desktop and other local MCP clients
designlib-mcp

# streamable-http — Claude Code and hosted deployments
designlib-mcp --http --port 8000
# or via env:
DESIGNLIB_TRANSPORT=http PORT=8000 designlib-mcp
```

HTTP endpoint: `POST /mcp`.

### Claude Desktop config (stdio)

`~/Library/Application Support/Claude/claude_desktop_config.json` (Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "designlib": {
      "command": "designlib-mcp",
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_ANON_KEY": "sb_publishable_..."
      }
    }
  }
}
```

### Deploy to Railway

```bash
npm i -g @railway/cli
railway login
railway init                   # Empty Project
railway add                    # Empty Service — link when prompted
railway variables --set "SUPABASE_URL=https://your-project.supabase.co" \
                  --set "SUPABASE_ANON_KEY=sb_publishable_..."
railway up                     # builds Dockerfile, deploys
railway domain                 # generate *.up.railway.app URL
```

Railway injects `PORT`; the Dockerfile sets `DESIGNLIB_TRANSPORT=http`; the server binds `0.0.0.0:$PORT`. Secrets live only in Railway Variables — never in the client config or on disk.

---

## Architecture

- `src/designlib_mcp/server.py` — FastMCP app, registers the 12 tools
- `src/designlib_mcp/tools/` — one module per entity (styles / palettes / font_pairs / domains)
- `src/designlib_mcp/repository/` — `CatalogRepository` Protocol + Supabase implementation
- `src/designlib_mcp/services/cross_links.py` — style→palette/font/domain cross-linking via `recommendation_scores`
- `src/designlib_mcp/models/` — Pydantic v2 response models
- `migrations/` — 4 SQL files (base schema → platform column → iOS extensions → dna columns)
- `scripts/` — migrations runner, iOS median pipeline, web/iOS ingest
- `data/` — hand-authored iOS family definitions + computed medians (checked in for reproducibility)

Source-only directories (`dump/`, `extraction/`, `researches/`) are **not shipped**; they are local working folders used to seed Supabase. End users just need a populated Supabase.

**Stack:** Python 3.11+, FastMCP 3.2, Pydantic v2, supabase-py, python-dotenv. Dev-only: psycopg[binary] for migrations, numpy + colormath2 for the iOS median pipeline.

---

## Development

```bash
pytest -m "not integration"      # unit tests, no Supabase required (87 tests)
pytest -m integration            # e2e tests against live Supabase (11 tests)
pytest                           # everything (98 tests)
ruff check src tests
```

The e2e suite (`tests/e2e/`) spins up the real FastMCP server in-memory and calls every tool through the MCP protocol against a live Supabase, including roundtrips (`list_*` → pick ID → `get_*`) and error paths (NOT_FOUND).

Design spec: `docs/superpowers/specs/2026-04-22-designlib-mcp-v1-design.md`
Implementation plan: `docs/superpowers/plans/2026-04-22-designlib-mcp-v1.md`

---

## License & data

Server code: open source. Catalog data (styles, palettes, font pairs, domains) is curated by the maintainer and intended for design exploration — it's not a substitute for brand guidelines or licensed type foundries. Font metadata references public families (Google Fonts, Apple system) with source attribution in each record.
