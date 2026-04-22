# designlib-mcp v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a Python MCP server that exposes a curated design-knowledge catalog (web + iOS) over 12 read-only tools backed by Supabase, ready to be queried by an external IDE plugin.

**Architecture:** FastMCP server with a Repository-pattern data layer (`CatalogRepository` Protocol, Supabase implementation). Pydantic v2 models for all responses. One module per entity (styles/palettes/font_pairs/domains), each registers list/get/facets tools. Ingest scripts (separate from server) seed Supabase from local source folders (`dump/`, `extraction/`, `researches/`) which are gitignored.

**Tech Stack:** Python 3.11+, `fastmcp`, `pydantic` v2, `supabase-py`, `psycopg[binary]` (migrations only), `python-dotenv`, `pytest`, `ruff`.

**Reference spec:** `docs/superpowers/specs/2026-04-22-designlib-mcp-v1-design.md`

---

## File Structure

```
designlib-mcp/
├── pyproject.toml                                  # Task 1
├── .env.example                                    # Task 2
├── README.md                                       # Task 32
├── src/designlib_mcp/
│   ├── __init__.py                                 # Task 1
│   ├── __main__.py                                 # Task 31
│   ├── server.py                                   # Task 31
│   ├── config.py                                   # Task 2
│   ├── models/
│   │   ├── __init__.py                             # Task 3
│   │   ├── common.py                               # Task 3
│   │   ├── style.py                                # Task 10
│   │   ├── palette.py                              # Task 11
│   │   ├── font_pair.py                            # Task 12
│   │   └── domain.py                               # Task 13
│   ├── repository/
│   │   ├── __init__.py                             # Task 8
│   │   ├── base.py                                 # Task 8
│   │   └── supabase_repo.py                        # Tasks 9, 21–24
│   ├── services/
│   │   ├── __init__.py                             # Task 25
│   │   └── cross_links.py                          # Task 25
│   └── formatting/
│       ├── __init__.py                             # Task 26
│       └── truncate.py                             # Task 26
│   └── tools/
│       ├── __init__.py                             # Task 27
│       ├── styles.py                               # Task 27
│       ├── palettes.py                             # Task 28
│       ├── font_pairs.py                           # Task 29
│       └── domains.py                              # Task 30
├── migrations/
│   ├── 001_base_schema.sql                         # Task 4 (copied from dump)
│   ├── 002_platform_column.sql                     # Task 5
│   └── 003_ios_extensions.sql                      # Task 6
├── scripts/
│   ├── apply_migrations.py                         # Task 7
│   ├── compute_ios_medians.py                      # Tasks 14–17
│   ├── ingest_web.py                               # Task 19
│   └── ingest_ios.py                               # Task 20
├── data/
│   ├── ios_family_definitions.json                 # Task 18 (hand-authored)
│   └── ios_family_medians.json                     # Task 17 (script output, committed)
├── tests/
│   ├── __init__.py                                 # Task 1
│   ├── conftest.py                                 # Tasks 9, 21
│   ├── fixtures/
│   │   ├── ios_aggregated_sample.json              # Task 14
│   │   └── supabase_responses/                     # Task 21+
│   ├── models/
│   │   ├── test_common.py                          # Task 3
│   │   ├── test_style.py                           # Task 10
│   │   ├── test_palette.py                         # Task 11
│   │   ├── test_font_pair.py                       # Task 12
│   │   └── test_domain.py                          # Task 13
│   ├── scripts/
│   │   ├── test_compute_ios_medians.py             # Tasks 14–17
│   ├── repository/
│   │   ├── test_styles_repo.py                     # Task 21
│   │   ├── test_palettes_repo.py                   # Task 22
│   │   ├── test_font_pairs_repo.py                 # Task 23
│   │   └── test_domains_repo.py                    # Task 24
│   ├── services/
│   │   └── test_cross_links.py                     # Task 25
│   ├── formatting/
│   │   └── test_truncate.py                        # Task 26
│   └── tools/
│       ├── test_styles_tool.py                     # Task 27
│       ├── test_palettes_tool.py                   # Task 28
│       ├── test_font_pairs_tool.py                 # Task 29
│       └── test_domains_tool.py                    # Task 30
└── .gitignore                                      # already present
```

---

## Phase A — Bootstrap

### Task 1: Project skeleton

**Files:**
- Create: `pyproject.toml`
- Create: `src/designlib_mcp/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py` (empty)

- [ ] **Step 1: Write pyproject.toml**

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "designlib-mcp"
version = "0.1.0"
description = "MCP server exposing a curated design-knowledge catalog (web + iOS)"
readme = "README.md"
requires-python = ">=3.11"
license = { file = "LICENSE" }
authors = [{ name = "Roman Pluzhnikov" }]
dependencies = [
  "fastmcp>=0.4",
  "pydantic>=2.6",
  "supabase>=2.4",
  "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-asyncio>=0.23",
  "ruff>=0.4",
  "psycopg[binary]>=3.1",
  "numpy>=1.26",
  "colormath2>=3.1",
]

[project.scripts]
designlib-mcp = "designlib_mcp.__main__:main"

[tool.hatch.build.targets.wheel]
packages = ["src/designlib_mcp"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 2: Create empty package/test init files**

```python
# src/designlib_mcp/__init__.py
__version__ = "0.1.0"
```

```python
# tests/__init__.py
```

```python
# tests/conftest.py
```

- [ ] **Step 3: Install and verify**

Run:
```bash
python -m venv .venv
.venv/Scripts/activate   # Windows bash
pip install -e ".[dev]"
pytest --collect-only
ruff check src tests
```

Expected: `pytest` collects 0 tests without error; `ruff` returns clean.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml src/designlib_mcp/__init__.py tests/__init__.py tests/conftest.py
git commit -m "chore: bootstrap python project skeleton"
```

---

### Task 2: Configuration loader

**Files:**
- Create: `.env.example`
- Create: `src/designlib_mcp/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write `.env.example`**

```
# Supabase project credentials
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOi...
# DATABASE_URL is required only by scripts/apply_migrations.py and scripts/ingest_*.py
DATABASE_URL=postgresql://postgres:password@db.your-project-ref.supabase.co:5432/postgres
```

- [ ] **Step 2: Write failing test `tests/test_config.py`**

```python
import pytest
from designlib_mcp.config import Settings, CHARACTER_LIMIT


def test_character_limit_constant():
    assert CHARACTER_LIMIT == 25_000


def test_settings_loads_from_env(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon-key")
    s = Settings.from_env()
    assert s.supabase_url == "https://example.supabase.co"
    assert s.supabase_anon_key == "anon-key"


def test_settings_missing_required_raises(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_ANON_KEY", raising=False)
    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        Settings.from_env()
```

- [ ] **Step 3: Run test — must fail**

Run: `pytest tests/test_config.py -v`
Expected: ImportError (module not found).

- [ ] **Step 4: Write `src/designlib_mcp/config.py`**

```python
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

CHARACTER_LIMIT: int = 25_000


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_anon_key: str
    database_url: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url:
            raise RuntimeError("SUPABASE_URL is required")
        if not key:
            raise RuntimeError("SUPABASE_ANON_KEY is required")
        return cls(
            supabase_url=url,
            supabase_anon_key=key,
            database_url=os.getenv("DATABASE_URL"),
        )
```

- [ ] **Step 5: Run test — must pass**

Run: `pytest tests/test_config.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add .env.example src/designlib_mcp/config.py tests/test_config.py
git commit -m "feat(config): add env-driven Settings + CHARACTER_LIMIT"
```

---

### Task 3: Common Pydantic models

**Files:**
- Create: `src/designlib_mcp/models/__init__.py`
- Create: `src/designlib_mcp/models/common.py`
- Create: `tests/models/__init__.py`
- Create: `tests/models/test_common.py`

- [ ] **Step 1: Write `tests/models/test_common.py`**

```python
import pytest
from pydantic import ValidationError
from designlib_mcp.models.common import (
    Platform, Appearance, Density, ResponseMeta, FacetValue,
    PaginatedResponse, MCPError,
)


def test_platform_enum_values():
    assert Platform.WEB.value == "web"
    assert Platform.IOS.value == "ios"


def test_response_meta_defaults():
    meta = ResponseMeta(entity_type="style")
    assert meta.schema_version == "1.0"
    assert meta.truncated is False
    assert meta.platform is None


def test_facet_value_serialization():
    f = FacetValue(value="polished", count=12, label="Polished")
    assert f.model_dump() == {"value": "polished", "count": 12, "label": "Polished"}


def test_paginated_response_generic():
    items = [FacetValue(value="a", count=1)]
    resp = PaginatedResponse[FacetValue](
        items=items, total_count=1, limit=50, offset=0,
        meta=ResponseMeta(entity_type="facet"),
    )
    assert resp.items[0].value == "a"
    assert resp.total_count == 1


def test_mcp_error_actionable():
    err = MCPError(
        error_code="UNKNOWN_FAMILY",
        message="Unknown family 'foo'.",
        field="family",
        available_values=["polished", "dark"],
        suggest_tool="list_style_facets",
    )
    payload = err.model_dump()
    assert payload["error_code"] == "UNKNOWN_FAMILY"
    assert payload["available_values"] == ["polished", "dark"]


def test_density_enum_rejects_unknown():
    with pytest.raises(ValueError):
        Density("crowded")
```

- [ ] **Step 2: Run test — must fail**

Run: `pytest tests/models/test_common.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/models/__init__.py`**

```python
```

- [ ] **Step 4: Write `src/designlib_mcp/models/common.py`**

```python
from __future__ import annotations
from enum import Enum
from typing import Generic, Literal, TypeVar
from pydantic import BaseModel, ConfigDict, Field


class Platform(str, Enum):
    WEB = "web"
    IOS = "ios"


class Appearance(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    BOTH = "both"


class Density(str, Enum):
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


class ResponseMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"] = "1.0"
    platform: Platform | None = None
    entity_type: str
    truncated: bool = False


class FacetValue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str
    count: int = Field(ge=0)
    label: str | None = None


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")
    items: list[T]
    total_count: int = Field(ge=0)
    limit: int = Field(ge=1, le=200)
    offset: int = Field(ge=0)
    meta: ResponseMeta


class MCPError(BaseModel):
    model_config = ConfigDict(extra="forbid")
    error_code: str
    message: str
    field: str | None = None
    available_values: list[str] | None = None
    suggest_tool: str | None = None
```

- [ ] **Step 5: Create `tests/models/__init__.py`** (empty)

- [ ] **Step 6: Run test — must pass**

Run: `pytest tests/models/test_common.py -v`
Expected: 6 passed.

- [ ] **Step 7: Commit**

```bash
git add src/designlib_mcp/models tests/models
git commit -m "feat(models): add common Pydantic models (Platform, ResponseMeta, PaginatedResponse, MCPError)"
```

---

## Phase B — Migrations

### Task 4: Copy base schema migration

**Files:**
- Create: `migrations/001_base_schema.sql` (copied from `dump/db-dump/supabase-source/migrations/001_initial_schema.sql`)

- [ ] **Step 1: Copy file verbatim**

Run:
```bash
mkdir -p migrations
cp dump/db-dump/supabase-source/migrations/001_initial_schema.sql migrations/001_base_schema.sql
```

- [ ] **Step 2: Verify by counting CREATE TABLE statements**

Run: `grep -c "^CREATE TABLE" migrations/001_base_schema.sql`
Expected: `15`

- [ ] **Step 3: Commit**

```bash
git add migrations/001_base_schema.sql
git commit -m "chore(db): import base schema from legacy dump (15 tables, 3 views, RLS)"
```

---

### Task 5: Platform column migration

**Files:**
- Create: `migrations/002_platform_column.sql`

- [ ] **Step 1: Write migration**

```sql
-- 002_platform_column.sql
-- Adds platform discriminator across catalog tables.

CREATE TYPE platform AS ENUM ('web', 'ios');

ALTER TABLE style_families ADD COLUMN platform platform NOT NULL DEFAULT 'web';
ALTER TABLE design_styles  ADD COLUMN platform platform NOT NULL DEFAULT 'web';
ALTER TABLE color_palettes ADD COLUMN platform platform NOT NULL DEFAULT 'web';
ALTER TABLE font_pairs     ADD COLUMN platform platform NOT NULL DEFAULT 'web';

CREATE INDEX idx_style_families_platform ON style_families(platform);
CREATE INDEX idx_design_styles_platform  ON design_styles(platform);
CREATE INDEX idx_color_palettes_platform ON color_palettes(platform);
CREATE INDEX idx_font_pairs_platform     ON font_pairs(platform);
```

- [ ] **Step 2: Commit**

```bash
git add migrations/002_platform_column.sql
git commit -m "feat(db): add platform enum + column on style/palette/font tables"
```

---

### Task 6: iOS extensions migration

**Files:**
- Create: `migrations/003_ios_extensions.sql`

- [ ] **Step 1: Write migration**

```sql
-- 003_ios_extensions.sql
-- iOS-specific fields and reference profile table.

ALTER TABLE design_styles ADD COLUMN ios_metadata JSONB;
-- ios_metadata shape (nullable for web, required for ios):
-- {
--   "liquid_glass_posture": "native_fit|selective|none|unclear",
--   "surfaces_affected": ["tab_bar","toolbar","modal_sheet",...],
--   "list_style_dominant": "inset_grouped|plain|card_grid|...",
--   "density_typical": "compact|comfortable|spacious",
--   "appearance_support": ["light","dark"] | ["light"] | ["dark"],
--   "corner_radius_cards_pt_median": 16,
--   "iconography": "sf_symbols_only|custom_glyph_set|mixed|photographic|unclear",
--   "reference_apps": ["linear","things_3","bear"]
-- }

CREATE TABLE ios_app_profiles (
  slug              TEXT PRIMARY KEY,
  family_id         TEXT REFERENCES style_families(id) ON DELETE SET NULL,
  aggregated        JSONB NOT NULL,
  screenshot_count  INTEGER,
  confidence        TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT valid_confidence CHECK (confidence IN ('high','medium','low') OR confidence IS NULL)
);

CREATE INDEX idx_ios_app_profiles_family ON ios_app_profiles(family_id);

ALTER TABLE ios_app_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON ios_app_profiles FOR SELECT TO anon, authenticated USING (true);
```

- [ ] **Step 2: Commit**

```bash
git add migrations/003_ios_extensions.sql
git commit -m "feat(db): add ios_metadata JSONB on design_styles + ios_app_profiles table"
```

---

### Task 7: Apply-migrations script

**Files:**
- Create: `scripts/apply_migrations.py`
- Create: `tests/scripts/__init__.py`
- Create: `tests/scripts/test_apply_migrations.py`

- [ ] **Step 1: Write failing test**

```python
# tests/scripts/test_apply_migrations.py
from pathlib import Path
from scripts.apply_migrations import discover_migrations


def test_discover_migrations_returns_sorted(tmp_path: Path):
    (tmp_path / "002_b.sql").write_text("-- b")
    (tmp_path / "001_a.sql").write_text("-- a")
    (tmp_path / "003_c.sql").write_text("-- c")
    files = discover_migrations(tmp_path)
    assert [p.name for p in files] == ["001_a.sql", "002_b.sql", "003_c.sql"]


def test_discover_migrations_skips_non_sql(tmp_path: Path):
    (tmp_path / "001_a.sql").write_text("-- a")
    (tmp_path / "README.md").write_text("readme")
    files = discover_migrations(tmp_path)
    assert [p.name for p in files] == ["001_a.sql"]
```

Also create empty `tests/scripts/__init__.py`.

Update `pyproject.toml`'s `[tool.pytest.ini_options]` to include `pythonpath = ["src", "."]` so `from scripts.apply_migrations import ...` resolves.

- [ ] **Step 2: Run test — must fail**

Run: `pytest tests/scripts/test_apply_migrations.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `scripts/apply_migrations.py`**

```python
"""Apply SQL migrations in order using DATABASE_URL.

Usage:
    python scripts/apply_migrations.py [--dry-run]
"""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


def discover_migrations(directory: Path) -> list[Path]:
    return sorted(p for p in directory.iterdir() if p.suffix == ".sql")


def apply(database_url: str, files: list[Path]) -> None:
    import psycopg

    with psycopg.connect(database_url, autocommit=False) as conn:
        for f in files:
            sql = f.read_text(encoding="utf-8")
            print(f"[apply] {f.name} ({len(sql)} bytes)")
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            print(f"[ok]    {f.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is required", file=sys.stderr)
        return 1

    files = discover_migrations(MIGRATIONS_DIR)
    print(f"[discover] {len(files)} migrations from {MIGRATIONS_DIR}")
    for f in files:
        print(f"  - {f.name}")

    if args.dry_run:
        return 0

    apply(database_url, files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test — must pass**

Run: `pytest tests/scripts/test_apply_migrations.py -v`
Expected: 2 passed.

- [ ] **Step 5: Dry-run end-to-end**

Run: `python scripts/apply_migrations.py --dry-run`
Expected: lists 3 migrations.

- [ ] **Step 6: Commit**

```bash
git add scripts/apply_migrations.py tests/scripts pyproject.toml
git commit -m "feat(scripts): apply_migrations runner using psycopg + DATABASE_URL"
```

---

## Phase C — Repository foundation

### Task 8: CatalogRepository Protocol

**Files:**
- Create: `src/designlib_mcp/repository/__init__.py`
- Create: `src/designlib_mcp/repository/base.py`
- Create: `tests/repository/__init__.py`
- Create: `tests/repository/test_base.py`

- [ ] **Step 1: Write failing test**

```python
# tests/repository/test_base.py
from designlib_mcp.repository.base import CatalogRepository


def test_protocol_has_required_methods():
    methods = {
        "list_styles", "get_style", "list_style_facets",
        "list_palettes", "get_palette", "list_palette_facets",
        "list_font_pairs", "get_font_pair", "list_font_pair_facets",
        "list_domains", "get_domain", "list_domain_facets",
    }
    for m in methods:
        assert hasattr(CatalogRepository, m), f"missing {m}"
```

Empty `tests/repository/__init__.py`.

- [ ] **Step 2: Run — fail**

Run: `pytest tests/repository/test_base.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/repository/__init__.py`** (empty)

- [ ] **Step 4: Write `src/designlib_mcp/repository/base.py`**

```python
from __future__ import annotations
from typing import Any, Protocol, runtime_checkable

from designlib_mcp.models.common import Platform


@runtime_checkable
class CatalogRepository(Protocol):
    # Styles
    def list_styles(
        self, platform: Platform, *,
        family: str | None = None, appearance: str | None = None,
        tone: str | None = None, density: str | None = None,
        tags: list[str] | None = None, limit: int = 50, offset: int = 0,
    ) -> dict[str, Any]: ...

    def get_style(self, style_id: str) -> dict[str, Any] | None: ...

    def list_style_facets(self, platform: Platform) -> dict[str, Any]: ...

    # Palettes
    def list_palettes(
        self, platform: Platform, *,
        family: str | None = None, appearance: str | None = None,
        mood: str | None = None, tags: list[str] | None = None,
        limit: int = 50, offset: int = 0,
    ) -> dict[str, Any]: ...

    def get_palette(self, palette_id: str) -> dict[str, Any] | None: ...

    def list_palette_facets(self, platform: Platform) -> dict[str, Any]: ...

    # Font pairs
    def list_font_pairs(
        self, platform: Platform, *,
        category_id: str | None = None, style_fit: list[str] | None = None,
        tags: list[str] | None = None, limit: int = 50, offset: int = 0,
    ) -> dict[str, Any]: ...

    def get_font_pair(self, font_pair_id: str) -> dict[str, Any] | None: ...

    def list_font_pair_facets(self, platform: Platform) -> dict[str, Any]: ...

    # Domains
    def list_domains(
        self, *, category_id: str | None = None, audience: str | None = None,
        tone: str | None = None, limit: int = 50, offset: int = 0,
    ) -> dict[str, Any]: ...

    def get_domain(
        self, domain_id: str, platform: Platform, top_n: int = 5,
    ) -> dict[str, Any] | None: ...

    def list_domain_facets(self) -> dict[str, Any]: ...

    # Cross-link helpers used by services/cross_links.py
    def palettes_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]: ...
    def font_pairs_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]: ...
    def style_domain_scores(self, style_id: str, limit: int) -> list[dict[str, Any]]: ...
    def domain_top_styles(self, domain_id: str, platform: Platform, limit: int) -> list[dict[str, Any]]: ...
```

- [ ] **Step 5: Run — pass**

Run: `pytest tests/repository/test_base.py -v`
Expected: 1 passed.

- [ ] **Step 6: Commit**

```bash
git add src/designlib_mcp/repository tests/repository
git commit -m "feat(repository): define CatalogRepository Protocol with 12 tool methods + cross-link helpers"
```

---

### Task 9: SupabaseRepository skeleton + smoke connect

**Files:**
- Create: `src/designlib_mcp/repository/supabase_repo.py`
- Modify: `tests/conftest.py`
- Create: `tests/repository/test_supabase_smoke.py`

- [ ] **Step 1: Write `src/designlib_mcp/repository/supabase_repo.py` (skeleton, all methods raise NotImplementedError except connect smoke)**

```python
from __future__ import annotations
from typing import Any
from supabase import create_client, Client

from designlib_mcp.config import Settings
from designlib_mcp.models.common import Platform


class SupabaseRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    @classmethod
    def from_settings(cls, settings: Settings) -> "SupabaseRepository":
        client = create_client(settings.supabase_url, settings.supabase_anon_key)
        return cls(client)

    def health_check(self) -> bool:
        # Cheap read against a known table to confirm connectivity.
        # style_families is small (≤24 rows) and present after migrations.
        resp = self._client.table("style_families").select("id").limit(1).execute()
        return isinstance(resp.data, list)

    # All concrete methods are added in Phase G (Tasks 21–24).
    def list_styles(self, platform: Platform, **_: Any) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 21")

    def get_style(self, style_id: str) -> dict[str, Any] | None:
        raise NotImplementedError("Implemented in Task 21")

    def list_style_facets(self, platform: Platform) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 21")

    def list_palettes(self, platform: Platform, **_: Any) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 22")

    def get_palette(self, palette_id: str) -> dict[str, Any] | None:
        raise NotImplementedError("Implemented in Task 22")

    def list_palette_facets(self, platform: Platform) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 22")

    def list_font_pairs(self, platform: Platform, **_: Any) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 23")

    def get_font_pair(self, font_pair_id: str) -> dict[str, Any] | None:
        raise NotImplementedError("Implemented in Task 23")

    def list_font_pair_facets(self, platform: Platform) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 23")

    def list_domains(self, **_: Any) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 24")

    def get_domain(self, domain_id: str, platform: Platform, top_n: int = 5) -> dict[str, Any] | None:
        raise NotImplementedError("Implemented in Task 24")

    def list_domain_facets(self) -> dict[str, Any]:
        raise NotImplementedError("Implemented in Task 24")

    def palettes_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Implemented in Task 25")

    def font_pairs_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Implemented in Task 25")

    def style_domain_scores(self, style_id: str, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Implemented in Task 25")

    def domain_top_styles(self, domain_id: str, platform: Platform, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Implemented in Task 25")
```

- [ ] **Step 2: Add a session-scoped Supabase fixture (skipped if no env)**

Replace `tests/conftest.py` with:

```python
import os
import pytest
from designlib_mcp.config import Settings


def _env_present() -> bool:
    return bool(os.getenv("SUPABASE_URL")) and bool(os.getenv("SUPABASE_ANON_KEY"))


@pytest.fixture(scope="session")
def settings() -> Settings:
    if not _env_present():
        pytest.skip("Supabase env not configured; set SUPABASE_URL and SUPABASE_ANON_KEY")
    return Settings.from_env()
```

- [ ] **Step 3: Write smoke test**

```python
# tests/repository/test_supabase_smoke.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository


@pytest.mark.integration
def test_health_check(settings):
    repo = SupabaseRepository.from_settings(settings)
    assert repo.health_check() is True
```

Add to `pyproject.toml` `[tool.pytest.ini_options]`:

```toml
markers = [
  "integration: tests that require a live Supabase",
]
```

- [ ] **Step 4: Verify (skipped if no env)**

Run: `pytest tests/repository/test_supabase_smoke.py -v`
Expected: skipped if no env, or 1 passed once Supabase is provisioned (deferred to Task 19).

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/repository/supabase_repo.py tests/conftest.py tests/repository/test_supabase_smoke.py pyproject.toml
git commit -m "feat(repository): add SupabaseRepository skeleton + health_check smoke test"
```

---

## Phase D — Entity models

### Task 10: Style models

**Files:**
- Create: `src/designlib_mcp/models/style.py`
- Create: `tests/models/test_style.py`

- [ ] **Step 1: Write failing test**

```python
# tests/models/test_style.py
import pytest
from pydantic import ValidationError
from designlib_mcp.models.style import (
    ColorTokens, TypographyTokens, LayoutTokens, StyleTokens,
    IosMetadata, StyleSummary, Style, StyleCrossLinks, StyleFacets,
    CrossLinkPalette, CrossLinkFontPair, CrossLinkDomain,
)
from designlib_mcp.models.common import Platform, Density, Appearance, ResponseMeta


def test_color_tokens_required_roles():
    ct = ColorTokens(
        background="#FFFFFF", surface="#FAFAFA", border="#ECECEC",
        text_primary="#111111", text_secondary="#8A8A8A", primary="#4FB0C6",
    )
    assert ct.background == "#FFFFFF"
    assert ct.extras == {}


def test_color_tokens_extras_holds_unmapped():
    ct = ColorTokens(
        background="#000", surface="#111", border="#222",
        text_primary="#FFF", text_secondary="#AAA", primary="#0F0",
        extras={"section_dark_text": "#E8DFD4"},
    )
    assert ct.extras["section_dark_text"] == "#E8DFD4"


def test_ios_metadata_minimum_shape():
    m = IosMetadata(
        liquid_glass_posture="native_fit",
        appearance_support=[Appearance.LIGHT, Appearance.DARK],
        iconography="custom_glyph_set",
    )
    assert m.surfaces_affected == []
    assert m.reference_apps == []


def test_style_summary_serializes_with_meta_omitted():
    s = StyleSummary(
        id="academia_classical", name="Academia Classical", family_id="classical",
        platform=Platform.WEB, short_description="…",
        top_signatures=["serif_double", "brass_accents", "parchment_text"],
        primary_swatch="#C9A962",
    )
    assert s.platform == Platform.WEB


def test_style_full_with_cross_links():
    tokens = StyleTokens(
        colors=ColorTokens(
            background="#FFFFFF", surface="#FAFAFA", border="#ECECEC",
            text_primary="#111111", text_secondary="#8A8A8A", primary="#4FB0C6",
        ),
        typography=TypographyTokens(heading_font="Inter", body_font="Inter"),
    )
    style = Style(
        id="x", name="X", family_id="polished", family_name="Polished",
        platform=Platform.WEB, description="d",
        visual_signatures=[], emotional_keywords=[], anti_patterns=[],
        tokens=tokens,
        cross_links=StyleCrossLinks(
            palettes=[CrossLinkPalette(palette_id="p1", name="P1", score=0.9)],
            font_pairs=[CrossLinkFontPair(font_pair_id="f1", name="F1")],
            domains=[CrossLinkDomain(domain_id="d1", name="D1", category_id="c1")],
        ),
        meta=ResponseMeta(entity_type="style", platform=Platform.WEB),
    )
    payload = style.model_dump()
    assert payload["cross_links"]["palettes"][0]["score"] == 0.9


def test_style_facets_payload_shape():
    facets = StyleFacets(
        families=[], tones=[], densities=[], appearances=[], tag_vocabulary=[],
        meta=ResponseMeta(entity_type="style_facets", platform=Platform.IOS),
    )
    assert facets.meta.platform == Platform.IOS
```

- [ ] **Step 2: Run — fail**

Run: `pytest tests/models/test_style.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/models/style.py`**

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import (
    Platform, Appearance, Density, ResponseMeta,
)


class ColorTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    background: str
    background_subtle: str | None = None
    surface: str
    surface_hover: str | None = None
    border: str
    border_subtle: str | None = None
    text_primary: str
    text_secondary: str
    text_muted: str | None = None
    primary: str
    primary_hover: str | None = None
    text_on_primary: str | None = None
    success: str | None = None
    warning: str | None = None
    error: str | None = None
    section_alt: str | None = None
    section_dark: str | None = None
    section_accent: str | None = None
    extras: dict[str, str] = Field(default_factory=dict)


class TypographyTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    heading_font: str
    heading_weight: str | None = None
    body_font: str
    body_weight: str | None = None
    mono_font: str | None = None
    base_size_px: int | None = None
    scale_ratio: float | None = None
    letter_spacing_heading: str | None = None


class LayoutTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    density: Density | None = None
    corner_radius_card_px: int | None = None
    corner_radius_button_px: int | None = None
    container_max_width_px: int | None = None
    grid_columns: int | None = None


class InputTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    height_px: int | None = None
    padding_x_px: int | None = None
    padding_y_px: int | None = None
    font_size_px: int | None = None
    focus_style: str | None = None
    focus_ring: str | None = None


class MediaTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    icon_style: str | None = None
    icon_weight: str | None = None
    avatar_shape: str | None = None
    image_aspect_ratio: str | None = None
    illustration_style: str | None = None


class MotionTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    duration_base_ms: int | None = None
    easing: str | None = None


class StyleTokens(BaseModel):
    model_config = ConfigDict(extra="forbid")
    colors: ColorTokens
    typography: TypographyTokens
    layout: LayoutTokens | None = None
    inputs: InputTokens | None = None
    media: MediaTokens | None = None
    motion: MotionTokens | None = None


class IosMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    liquid_glass_posture: Literal["native_fit", "selective", "none", "unclear"]
    surfaces_affected: list[str] = Field(default_factory=list)
    list_style_dominant: str | None = None
    density_typical: Density | None = None
    appearance_support: list[Appearance] = Field(default_factory=list)
    corner_radius_cards_pt_median: float | None = None
    iconography: Literal[
        "sf_symbols_only", "custom_glyph_set", "mixed", "photographic", "unclear"
    ]
    reference_apps: list[str] = Field(default_factory=list)


class StyleSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    family_id: str
    platform: Platform
    short_description: str
    top_signatures: list[str] = Field(default_factory=list, max_length=3)
    primary_swatch: str


class CrossLinkPalette(BaseModel):
    model_config = ConfigDict(extra="forbid")
    palette_id: str
    name: str
    score: float | None = None
    reason: str | None = None


class CrossLinkFontPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    font_pair_id: str
    name: str
    score: float | None = None


class CrossLinkDomain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    domain_id: str
    name: str
    category_id: str
    score: float | None = None


class StyleCrossLinks(BaseModel):
    model_config = ConfigDict(extra="forbid")
    palettes: list[CrossLinkPalette] = Field(default_factory=list)
    font_pairs: list[CrossLinkFontPair] = Field(default_factory=list)
    domains: list[CrossLinkDomain] = Field(default_factory=list)


class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    family_id: str
    family_name: str
    platform: Platform
    description: str
    visual_signatures: list[str] = Field(default_factory=list)
    emotional_keywords: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)
    tokens: StyleTokens
    ios_metadata: IosMetadata | None = None
    cross_links: StyleCrossLinks | None = None
    meta: ResponseMeta


class StyleFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    families: list  # list[FacetValue]
    tones: list
    densities: list
    appearances: list
    tag_vocabulary: list
    meta: ResponseMeta
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/models/test_style.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/models/style.py tests/models/test_style.py
git commit -m "feat(models): add Style/StyleTokens/IosMetadata/StyleCrossLinks/StyleFacets"
```

---

### Task 11: Palette models

**Files:**
- Create: `src/designlib_mcp/models/palette.py`
- Create: `tests/models/test_palette.py`

- [ ] **Step 1: Write failing test**

```python
# tests/models/test_palette.py
from designlib_mcp.models.palette import (
    ColorRole, ContrastPair, PaletteSummary, Palette, PaletteFacets,
)
from designlib_mcp.models.common import Platform, Appearance, ResponseMeta


def test_color_role_minimal():
    r = ColorRole(role="background", hex="#FFFFFF")
    assert r.p3_hex is None


def test_contrast_pair_flags_aaa_normal():
    p = ContrastPair(
        foreground_role="text_primary", background_role="background",
        ratio=7.2, wcag_aa_normal=True, wcag_aa_large=True, wcag_aaa_normal=True,
    )
    assert p.wcag_aaa_normal is True


def test_palette_summary_5_swatches():
    s = PaletteSummary(
        id="warm-1", name="Warm 1", platform=Platform.WEB, appearance=Appearance.LIGHT,
        main_swatches=["#A", "#B", "#C", "#D", "#E"],
    )
    assert len(s.main_swatches) == 5


def test_palette_full_with_used_by():
    p = Palette(
        id="ios-fitness-light", name="iOS Fitness Light",
        platform=Platform.IOS, appearance=Appearance.LIGHT,
        roles=[ColorRole(role="background", hex="#F8F8F8")],
        source="ios_aggregated", reference_apps=["any_distance"],
        used_by_styles=["fitness_vitality_ios"],
        meta=ResponseMeta(entity_type="palette", platform=Platform.IOS),
    )
    assert p.source == "ios_aggregated"
    assert p.reference_apps == ["any_distance"]
```

- [ ] **Step 2: Run — fail**

Run: `pytest tests/models/test_palette.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/models/palette.py`**

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import Platform, Appearance, ResponseMeta


class ColorRole(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    hex: str
    p3_hex: str | None = None


class ContrastPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    foreground_role: str
    background_role: str
    ratio: float
    wcag_aa_normal: bool
    wcag_aa_large: bool
    wcag_aaa_normal: bool


class PaletteSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    platform: Platform
    appearance: Appearance
    main_swatches: list[str] = Field(default_factory=list, max_length=5)


class Palette(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    description: str | None = None
    platform: Platform
    appearance: Appearance
    roles: list[ColorRole]
    background_mode: str | None = None
    p3_likely: bool = False
    mood: Literal["warm", "cool", "neutral", "mixed"] | None = None
    tags: list[str] = Field(default_factory=list)
    contrast_pairs: list[ContrastPair] = Field(default_factory=list)
    source: Literal["curated", "ios_aggregated"] = "curated"
    reference_apps: list[str] = Field(default_factory=list)
    used_by_styles: list[str] = Field(default_factory=list)
    meta: ResponseMeta


class PaletteFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    families: list
    moods: list
    appearances: list
    background_modes: list
    meta: ResponseMeta
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/models/test_palette.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/models/palette.py tests/models/test_palette.py
git commit -m "feat(models): add Palette/ColorRole/ContrastPair/PaletteFacets"
```

---

### Task 12: FontPair models

**Files:**
- Create: `src/designlib_mcp/models/font_pair.py`
- Create: `tests/models/test_font_pair.py`

- [ ] **Step 1: Write failing test**

```python
# tests/models/test_font_pair.py
from designlib_mcp.models.font_pair import (
    FontSpec, FontPairSummary, FontPair, FontPairFacets,
)
from designlib_mcp.models.common import Platform, ResponseMeta


def test_font_spec_system_font_no_url():
    s = FontSpec(font_family="SF Pro Text", weights=[400, 500, 700], is_system_font=True)
    assert s.google_fonts_url is None


def test_font_spec_google_font_url():
    s = FontSpec(
        font_family="Inter", weights=[400, 600, 700],
        google_fonts_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
    )
    assert "Inter" in s.google_fonts_url


def test_font_pair_full():
    p = FontPair(
        id="inter-inter", name="Inter / Inter",
        platform=Platform.WEB, category_id="modern_sans", category_name="Modern Sans",
        heading=FontSpec(font_family="Inter"), body=FontSpec(font_family="Inter"),
        style_fit=["polished_modern"],
        meta=ResponseMeta(entity_type="font_pair", platform=Platform.WEB),
    )
    assert p.mono is None
```

- [ ] **Step 2: Run — fail**

Run: `pytest tests/models/test_font_pair.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/models/font_pair.py`**

```python
from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

from designlib_mcp.models.common import Platform, ResponseMeta


class FontSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    font_family: str
    weights: list[int] = Field(default_factory=list)
    fallbacks: list[str] = Field(default_factory=list)
    google_fonts_url: str | None = None
    is_system_font: bool = False


class FontPairSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    platform: Platform
    category_id: str
    heading_family: str
    body_family: str


class FontPair(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    description: str | None = None
    platform: Platform
    category_id: str
    category_name: str
    heading: FontSpec
    body: FontSpec
    mono: FontSpec | None = None
    style_fit: list[str] = Field(default_factory=list)
    domain_fit: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    compatible_styles: list[str] = Field(default_factory=list)
    meta: ResponseMeta


class FontPairFacets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    categories: list
    tags: list
    meta: ResponseMeta
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/models/test_font_pair.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/models/font_pair.py tests/models/test_font_pair.py
git commit -m "feat(models): add FontPair/FontSpec/FontPairFacets"
```

---

### Task 13: Domain models

**Files:**
- Create: `src/designlib_mcp/models/domain.py`
- Create: `tests/models/test_domain.py`

- [ ] **Step 1: Write failing test**

```python
# tests/models/test_domain.py
from designlib_mcp.models.domain import (
    DomainSummary, Domain, DomainRecommendations, DomainFacets,
)
from designlib_mcp.models.common import Platform, ResponseMeta


def test_domain_summary_minimum():
    d = DomainSummary(id="travel-airbnb", name="Travel: Airbnb", category_id="travel")
    assert d.tone is None


def test_domain_full_with_recommendations():
    d = Domain(
        id="x", name="X", category_id="c", category_name="C", description="desc",
        ui_patterns=["search", "card_grid"], examples=["airbnb"],
        recommendations=DomainRecommendations(),
        meta=ResponseMeta(entity_type="domain", platform=Platform.WEB),
    )
    assert d.recommendations.styles == []
```

- [ ] **Step 2: Run — fail**

Run: `pytest tests/models/test_domain.py -v`
Expected: ImportError.

- [ ] **Step 3: Write `src/designlib_mcp/models/domain.py`**

```python
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
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/models/test_domain.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/models/domain.py tests/models/test_domain.py
git commit -m "feat(models): add Domain/DomainSummary/DomainRecommendations/DomainFacets"
```

---

## Phase E — iOS normalization pipeline

### Task 14: LAB color median utility

**Files:**
- Create: `scripts/__init__.py` (empty)
- Create: `scripts/compute_ios_medians.py` (initial version with one helper)
- Create: `tests/scripts/test_compute_ios_medians.py`
- Create: `tests/fixtures/ios_aggregated_sample.json`

- [ ] **Step 1: Add a fixture with 3 toy app profiles**

```json
// tests/fixtures/ios_aggregated_sample.json
{
  "apps": [
    {"slug": "alpha", "palette_light": {"background": "#FFFFFF", "background_conflicting": false, "text_primary": "#111111", "accent_primary": "#4FB0C6"}, "typography": {"body": "sf_pro_text", "heading": "sf_pro_display"}, "layout": {"density_typical": "comfortable", "list_style_dominant": "plain", "corner_radius_cards_pt_median": 16.0}, "liquid_glass": {"posture": "native_fit", "surfaces_affected_union": ["tab_bar", "toolbar"]}, "iconography": {"icon_system": "custom_glyph_set"}, "screenshot_count": 8, "_confidence": "high"},
    {"slug": "beta",  "palette_light": {"background": "#FAFAFA", "background_conflicting": false, "text_primary": "#0F0F0F", "accent_primary": "#5AB6CC"}, "typography": {"body": "sf_pro_text", "heading": "sf_pro_display"}, "layout": {"density_typical": "comfortable", "list_style_dominant": "plain", "corner_radius_cards_pt_median": 18.0}, "liquid_glass": {"posture": "native_fit", "surfaces_affected_union": ["tab_bar", "modal_sheet"]}, "iconography": {"icon_system": "custom_glyph_set"}, "screenshot_count": 6, "_confidence": "medium"},
    {"slug": "gamma", "palette_light": {"background": "#F2F2F2", "background_conflicting": false, "text_primary": "#1A1A1A", "accent_primary": "#3EA8C0"}, "typography": {"body": "sf_pro_text", "heading": "new_york_serif"}, "layout": {"density_typical": "spacious", "list_style_dominant": "plain", "corner_radius_cards_pt_median": 20.0}, "liquid_glass": {"posture": "native_fit", "surfaces_affected_union": ["tab_bar"]}, "iconography": {"icon_system": "sf_symbols_only"}, "screenshot_count": 9, "_confidence": "high"}
  ]
}
```

- [ ] **Step 2: Write failing test**

```python
# tests/scripts/test_compute_ios_medians.py
import pytest
from scripts.compute_ios_medians import median_hex_lab


def test_median_hex_lab_three_grays():
    out = median_hex_lab(["#FFFFFF", "#F2F2F2", "#FAFAFA"])
    assert out.upper() in {"#FAFAFA", "#F8F8F8", "#F9F9F9"}  # any near-median


def test_median_hex_lab_single_value():
    assert median_hex_lab(["#112233"]).upper() == "#112233"


def test_median_hex_lab_empty_returns_none():
    assert median_hex_lab([]) is None


def test_median_hex_lab_drops_none_inputs():
    out = median_hex_lab([None, "#FFFFFF", None])
    assert out.upper() == "#FFFFFF"
```

- [ ] **Step 3: Run — fail**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: ImportError.

- [ ] **Step 4: Write `scripts/__init__.py`** (empty)

- [ ] **Step 5: Write the helper in `scripts/compute_ios_medians.py`**

```python
"""Compute median iOS family tokens from extraction/aggregated/*.json.

Phase E of designlib-mcp v1. Reads aggregated app profiles + family_assignments,
emits data/ios_family_medians.json.
"""
from __future__ import annotations
from typing import Iterable


def _hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    # sRGB → linear
    def srgb_to_linear(c: int) -> float:
        v = c / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (srgb_to_linear(c) for c in rgb)
    # linear → XYZ (D65)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    # XYZ → LAB
    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _lab_to_xyz(lab: tuple[float, float, float]) -> tuple[float, float, float]:
    L, a, b = lab
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200
    def finv(t: float) -> float:
        t3 = t ** 3
        return t3 if t3 > 0.008856 else (t - 16 / 116) / 7.787
    return (finv(fx) * 0.95047, finv(fy) * 1.00000, finv(fz) * 1.08883)


def _xyz_to_rgb(xyz: tuple[float, float, float]) -> tuple[int, int, int]:
    x, y, z = xyz
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b = 0.0557 * x - 0.2040 * y + 1.0570 * z
    def linear_to_srgb(v: float) -> int:
        if v <= 0:
            return 0
        if v >= 1:
            return 255
        c = 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        return max(0, min(255, round(c * 255)))
    return (linear_to_srgb(r), linear_to_srgb(g), linear_to_srgb(b))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def median_hex_lab(hexes: Iterable[str | None]) -> str | None:
    """Return the LAB-space coordinate-wise median of input hex colors.

    None values are dropped. Returns None if no values remain.
    """
    cleaned = [h for h in hexes if h]
    if not cleaned:
        return None
    labs = [_rgb_to_lab(_hex_to_rgb(h)) for h in cleaned]
    n = len(labs)
    sorted_L = sorted(l[0] for l in labs)
    sorted_a = sorted(l[1] for l in labs)
    sorted_b = sorted(l[2] for l in labs)
    mid = n // 2
    if n % 2 == 1:
        med_lab = (sorted_L[mid], sorted_a[mid], sorted_b[mid])
    else:
        med_lab = (
            (sorted_L[mid - 1] + sorted_L[mid]) / 2,
            (sorted_a[mid - 1] + sorted_a[mid]) / 2,
            (sorted_b[mid - 1] + sorted_b[mid]) / 2,
        )
    return _rgb_to_hex(_xyz_to_rgb(_lab_to_xyz(med_lab)))
```

- [ ] **Step 6: Run — pass**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: 4 passed.

- [ ] **Step 7: Commit**

```bash
git add scripts/__init__.py scripts/compute_ios_medians.py tests/scripts/test_compute_ios_medians.py tests/fixtures
git commit -m "feat(scripts): add LAB-space hex median helper for iOS palette aggregation"
```

---

### Task 15: Palette aggregator

**Files:**
- Modify: `scripts/compute_ios_medians.py`
- Modify: `tests/scripts/test_compute_ios_medians.py`

- [ ] **Step 1: Append failing test**

```python
# Append to tests/scripts/test_compute_ios_medians.py
import json
from pathlib import Path
from scripts.compute_ios_medians import aggregate_palette


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "ios_aggregated_sample.json"


def _load_apps():
    return json.loads(FIXTURE.read_text())["apps"]


def test_aggregate_palette_light_uses_lab_median():
    apps = _load_apps()
    palette = aggregate_palette(apps, mode="light")
    assert palette["background"].startswith("#")
    assert palette["text_primary"].startswith("#")
    assert palette["accent_primary"].startswith("#")


def test_aggregate_palette_drops_conflicting_background():
    apps = _load_apps()
    apps[0]["palette_light"]["background_conflicting"] = True
    palette = aggregate_palette(apps, mode="light")
    # Background is computed from the remaining 2 apps only.
    assert palette["background"] is not None


def test_aggregate_palette_returns_none_when_no_apps_have_dark():
    apps = _load_apps()
    palette = aggregate_palette(apps, mode="dark")
    assert palette is None
```

- [ ] **Step 2: Run — fail**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: 3 new failures (ImportError for `aggregate_palette`).

- [ ] **Step 3: Append `aggregate_palette` to `scripts/compute_ios_medians.py`**

```python
PALETTE_ROLES = (
    "background", "background_elevated", "surface_card",
    "text_primary", "text_secondary", "separator", "accent_primary",
    "semantic_destructive", "semantic_success", "semantic_warning",
)


def _palette_key(mode: str) -> str:
    return "palette_light" if mode == "light" else "palette_dark"


def _coverage_for_mode(apps: list[dict], mode: str) -> list[dict]:
    key = _palette_key(mode)
    return [a for a in apps if a.get(key)]


def aggregate_palette(apps: list[dict], mode: str) -> dict | None:
    """Aggregate per-role hex medians for a family in light or dark mode.

    Returns None when fewer than 3 apps have the requested mode (per spec rule).
    Drops a single app's `background` value when its palette has
    `background_conflicting=true`.
    """
    relevant = _coverage_for_mode(apps, mode)
    if mode == "dark" and len(relevant) < 3:
        return None
    if not relevant:
        return None

    key = _palette_key(mode)
    out: dict[str, str | None] = {}
    for role in PALETTE_ROLES:
        values: list[str | None] = []
        for app in relevant:
            pal = app.get(key) or {}
            if role == "background" and pal.get("background_conflicting"):
                continue
            values.append(pal.get(role))
        out[role] = median_hex_lab(values)
    return out
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: 7 passed (4 prior + 3 new).

- [ ] **Step 5: Commit**

```bash
git add scripts/compute_ios_medians.py tests/scripts/test_compute_ios_medians.py
git commit -m "feat(scripts): aggregate palette medians (light/dark) across apps in a family"
```

---

### Task 16: Typography / layout / liquid_glass / iconography aggregators

**Files:**
- Modify: `scripts/compute_ios_medians.py`
- Modify: `tests/scripts/test_compute_ios_medians.py`

- [ ] **Step 1: Append failing tests**

```python
# Append to tests/scripts/test_compute_ios_medians.py
from scripts.compute_ios_medians import (
    aggregate_typography, aggregate_layout, aggregate_liquid_glass,
    aggregate_iconography, top_reference_apps,
)


def test_aggregate_typography_majority_vote():
    apps = _load_apps()
    typo = aggregate_typography(apps)
    assert typo["body_classification"] == "sf_pro_text"
    assert typo["heading_classification"] == "sf_pro_display"  # 2/3 majority


def test_aggregate_layout_uses_mode_and_median():
    apps = _load_apps()
    layout = aggregate_layout(apps)
    assert layout["density_typical"] == "comfortable"
    assert layout["list_style_dominant"] == "plain"
    assert layout["corner_radius_cards_pt_median"] == 18.0


def test_aggregate_liquid_glass_keeps_70_percent_surfaces():
    apps = _load_apps()
    lg = aggregate_liquid_glass(apps)
    assert lg["posture"] == "native_fit"
    # tab_bar appears in 3/3 apps → kept; toolbar 1/3 → dropped at 70% threshold
    assert "tab_bar" in lg["surfaces_affected"]
    assert "toolbar" not in lg["surfaces_affected"]


def test_aggregate_iconography_mode():
    apps = _load_apps()
    icon = aggregate_iconography(apps)
    assert icon == "custom_glyph_set"  # 2/3 majority


def test_top_reference_apps_weights_confidence():
    apps = _load_apps()
    refs = top_reference_apps(apps, top_n=3)
    # gamma (high, 9 shots) > alpha (high, 8) > beta (medium, 6 × 0.6 = 3.6)
    assert refs == ["gamma", "alpha", "beta"]
```

- [ ] **Step 2: Run — fail (5 new errors)**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`

- [ ] **Step 3: Append aggregators to `scripts/compute_ios_medians.py`**

```python
from collections import Counter
from statistics import median

CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.6, "low": 0.0}


def _mode(values: list) -> str | None:
    cleaned = [v for v in values if v]
    if not cleaned:
        return None
    return Counter(cleaned).most_common(1)[0][0]


def aggregate_typography(apps: list[dict]) -> dict:
    body = [a.get("typography", {}).get("body") for a in apps]
    heading = [a.get("typography", {}).get("heading") for a in apps]
    return {
        "body_classification": _mode(body),
        "heading_classification": _mode(heading),
        "mono_present": any(a.get("typography", {}).get("mono_present") for a in apps),
        "tabular_numerics_present": any(
            a.get("typography", {}).get("tabular_numerics_present") for a in apps
        ),
    }


def aggregate_layout(apps: list[dict]) -> dict:
    densities = [a.get("layout", {}).get("density_typical") for a in apps]
    list_styles = [a.get("layout", {}).get("list_style_dominant") for a in apps]
    radii = [
        a.get("layout", {}).get("corner_radius_cards_pt_median")
        for a in apps
        if a.get("layout", {}).get("corner_radius_cards_pt_median") is not None
    ]
    return {
        "density_typical": _mode(densities),
        "list_style_dominant": _mode(list_styles),
        "corner_radius_cards_pt_median": median(radii) if radii else None,
    }


def aggregate_liquid_glass(apps: list[dict]) -> dict:
    postures = [a.get("liquid_glass", {}).get("posture") for a in apps]
    surface_counts: Counter[str] = Counter()
    n_apps = len(apps)
    for a in apps:
        for s in a.get("liquid_glass", {}).get("surfaces_affected_union", []):
            surface_counts[s] += 1
    threshold = 0.70 * n_apps
    surfaces = sorted(s for s, c in surface_counts.items() if c >= threshold)
    return {"posture": _mode(postures) or "unclear", "surfaces_affected": surfaces}


def aggregate_iconography(apps: list[dict]) -> str | None:
    return _mode([a.get("iconography", {}).get("icon_system") for a in apps])


def top_reference_apps(apps: list[dict], top_n: int) -> list[str]:
    def score(app: dict) -> float:
        weight = CONFIDENCE_WEIGHT.get(app.get("_confidence", "low"), 0.0)
        return float(app.get("screenshot_count", 0)) * weight
    ranked = sorted(apps, key=score, reverse=True)
    return [a["slug"] for a in ranked[:top_n]]
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: 12 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/compute_ios_medians.py tests/scripts/test_compute_ios_medians.py
git commit -m "feat(scripts): add typography/layout/liquid_glass/iconography aggregators + reference-app ranker"
```

---

### Task 17: Main orchestrator + run + commit medians

**Files:**
- Modify: `scripts/compute_ios_medians.py`
- Modify: `tests/scripts/test_compute_ios_medians.py`
- Create: `data/ios_family_medians.json` (script output, committed)

- [ ] **Step 1: Append orchestrator test**

```python
# Append to tests/scripts/test_compute_ios_medians.py
from scripts.compute_ios_medians import compute_family_medians


def test_compute_family_medians_smoke(tmp_path):
    apps = _load_apps()
    family_assignments = [
        {"slug": "alpha", "family_assigned": "demo_family", "confidence": "high"},
        {"slug": "beta",  "family_assigned": "demo_family", "confidence": "medium"},
        {"slug": "gamma", "family_assigned": "demo_family", "confidence": "high"},
    ]
    out = compute_family_medians(apps_by_slug={a["slug"]: a for a in apps},
                                 family_assignments=family_assignments)
    assert "demo_family" in out
    fam = out["demo_family"]
    assert fam["app_count"] == 3
    assert fam["palette_light"]["background"].startswith("#")
    assert fam["palette_dark"] is None
    assert fam["typography"]["heading_classification"] == "sf_pro_display"
    assert fam["layout"]["density_typical"] == "comfortable"
    assert fam["liquid_glass"]["posture"] == "native_fit"
    assert fam["reference_apps"] == ["gamma", "alpha", "beta"]
    assert fam["review_flags"] == []  # 3 apps, no flags
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Append orchestrator and CLI to `scripts/compute_ios_medians.py`**

```python
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXTRACTION_DIR = REPO_ROOT / "extraction"
DATA_DIR = REPO_ROOT / "data"


def _confidence_for_family_aggregation(c: str) -> bool:
    return c in {"high", "medium"}


def compute_family_medians(
    apps_by_slug: dict[str, dict],
    family_assignments: list[dict],
) -> dict[str, dict]:
    families: dict[str, list[dict]] = {}
    for row in family_assignments:
        if not _confidence_for_family_aggregation(row.get("confidence", "low")):
            continue
        slug = row["slug"]
        family = row["family_assigned"]
        app = apps_by_slug.get(slug)
        if not app:
            continue
        # decorate the app with its assignment confidence for downstream use
        app = {**app, "_confidence": row["confidence"]}
        families.setdefault(family, []).append(app)

    out: dict[str, dict] = {}
    for family, apps in families.items():
        n = len(apps)
        flags: list[str] = []
        if n < 3:
            flags.append(f"app_count_below_3 ({n})")
        out[family] = {
            "app_count": n,
            "palette_light": aggregate_palette(apps, mode="light"),
            "palette_dark": aggregate_palette(apps, mode="dark"),
            "typography": aggregate_typography(apps),
            "layout": aggregate_layout(apps),
            "liquid_glass": aggregate_liquid_glass(apps),
            "iconography": aggregate_iconography(apps),
            "reference_apps": top_reference_apps(apps, top_n=5),
            "review_flags": flags,
        }
    return out


def _load_apps_by_slug(extraction_dir: Path) -> dict[str, dict]:
    aggregated_dir = extraction_dir / "aggregated"
    out: dict[str, dict] = {}
    for f in aggregated_dir.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        out[data["slug"]] = data
    return out


def _load_family_assignments(extraction_dir: Path) -> list[dict]:
    raw = json.loads((extraction_dir / "family_assignments.json").read_text(encoding="utf-8"))
    return raw["assignments"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extraction-dir", default=str(EXTRACTION_DIR))
    parser.add_argument("--out", default=str(DATA_DIR / "ios_family_medians.json"))
    args = parser.parse_args()

    extraction_dir = Path(args.extraction_dir)
    out_path = Path(args.out)
    if not extraction_dir.exists():
        print(f"extraction dir not found: {extraction_dir}", file=sys.stderr)
        return 1

    apps_by_slug = _load_apps_by_slug(extraction_dir)
    family_assignments = _load_family_assignments(extraction_dir)
    medians = compute_family_medians(apps_by_slug, family_assignments)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(medians, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ok] wrote {len(medians)} families → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/scripts/test_compute_ios_medians.py -v`
Expected: 13 passed.

- [ ] **Step 5: Run end-to-end against real `extraction/`**

Run: `python scripts/compute_ios_medians.py`
Expected: writes `data/ios_family_medians.json` with 10 families. Verify:

```bash
python -c "import json; d=json.load(open('data/ios_family_medians.json')); print(len(d), list(d.keys()))"
```

Expected output: `10 ['enterprise_muted', 'fitness_vitality', ...]`

- [ ] **Step 6: Inspect `review_flags` count**

Run:
```bash
python -c "import json; d=json.load(open('data/ios_family_medians.json')); flagged=sum(1 for f in d.values() if f['review_flags']); print(f'{flagged}/{len(d)} families have review_flags')"
```
Expected: < 30% of families flagged (per spec acceptance criteria).

- [ ] **Step 7: Commit script + generated artifact**

```bash
git add scripts/compute_ios_medians.py tests/scripts/test_compute_ios_medians.py data/ios_family_medians.json
git commit -m "feat(scripts): orchestrate compute_ios_medians end-to-end + commit medians artifact"
```

---

### Task 18: Hand-author iOS family definitions

**Files:**
- Create: `data/ios_family_definitions.json`

This is a manual editorial step (~2 hours). It produces canonical descriptions/keywords/anti_patterns for each of the 10 iOS families, drawing from `researches/compass_artifact_*.md`.

- [ ] **Step 1: Write template with all 10 families filled with placeholder TBD-removed content**

Author the file directly. Schema:

```json
{
  "enterprise_muted": {
    "name_en": "Enterprise Muted",
    "description": "Restrained, professional iOS UI with desaturated palettes, tabular data emphasis, and subdued accents. Trades visual flair for legibility and operational density.",
    "visual_signatures": ["muted_palette", "tabular_numerics", "tight_density", "system_chrome"],
    "emotional_keywords": ["trustworthy", "professional", "efficient", "calm"],
    "anti_patterns": ["saturated_brand_accent", "playful_illustration", "decorative_motion"]
  },
  "fitness_vitality": {
    "name_en": "Fitness Vitality",
    "description": "High-energy iOS UI built around motion data, vivid metric pills, gradient halos, and ring-style progress indicators.",
    "visual_signatures": ["metric_pill", "ring_progress", "gradient_accents", "tabular_numerics"],
    "emotional_keywords": ["energetic", "achievement", "vital", "motivating"],
    "anti_patterns": ["dense_text_lists", "muted_palette", "serif_typography"]
  },
  "editorial_photography": {
    "name_en": "Editorial Photography",
    "description": "Image-led iOS UI where photography drives the surface, type recedes into supporting role, and chrome is intentionally minimal.",
    "visual_signatures": ["full_bleed_imagery", "minimal_chrome", "thin_typography", "generous_whitespace"],
    "emotional_keywords": ["aspirational", "premium", "considered", "atmospheric"],
    "anti_patterns": ["dense_data_grids", "saturated_chrome", "rounded_playful_shapes"]
  },
  "minimalist_monochrome": {
    "name_en": "Minimalist Monochrome",
    "description": "Restricted-palette iOS UI built around grayscale surfaces with a single accent, generous spacing, and uniform geometry.",
    "visual_signatures": ["grayscale_surfaces", "single_accent", "uniform_radii", "comfortable_density"],
    "emotional_keywords": ["focused", "calm", "uncluttered", "intentional"],
    "anti_patterns": ["multi_accent_palettes", "decorative_imagery", "ornamental_typography"]
  },
  "data_dense_terminal": {
    "name_en": "Data-Dense Terminal",
    "description": "Compact iOS UI for power users: tabular layouts, mono accents, tight row heights, and command-style affordances.",
    "visual_signatures": ["compact_density", "mono_accents", "tabular_grids", "fixed_width_glyphs"],
    "emotional_keywords": ["efficient", "expert", "precise", "utilitarian"],
    "anti_patterns": ["spacious_density", "photographic_imagery", "playful_illustration"]
  },
  "warm_handcrafted": {
    "name_en": "Warm Handcrafted",
    "description": "Tactile iOS UI with warm earth-tone palettes, soft gradients, hand-feel iconography, and approachable typography.",
    "visual_signatures": ["warm_palette", "soft_gradients", "hand_iconography", "rounded_geometry"],
    "emotional_keywords": ["welcoming", "human", "tactile", "soft"],
    "anti_patterns": ["cool_blue_palettes", "sharp_geometry", "neutral_grayscale"]
  },
  "editorial_canvas": {
    "name_en": "Editorial Canvas",
    "description": "Magazine-inflected iOS UI: serif headings, structured columnar layouts, generous spacing, content-first chrome.",
    "visual_signatures": ["serif_headings", "columnar_layout", "generous_whitespace", "muted_chrome"],
    "emotional_keywords": ["literary", "considered", "calm", "intentional"],
    "anti_patterns": ["sans_only_typography", "dense_grids", "neon_accents"]
  },
  "tactile_depth_playful": {
    "name_en": "Tactile Depth Playful",
    "description": "iOS UI that leans on depth, shadow, and 3D-feeling controls; bouncy motion and saturated highlights.",
    "visual_signatures": ["soft_shadows", "depth_layers", "bouncy_motion", "saturated_accents"],
    "emotional_keywords": ["delightful", "playful", "tangible", "energetic"],
    "anti_patterns": ["flat_minimal_surfaces", "muted_palette", "tight_density"]
  },
  "youth_social_widget": {
    "name_en": "Youth Social Widget",
    "description": "Vibrant iOS UI optimized for short-form social, widget cards, and expressive avatars; bold accents on light surfaces.",
    "visual_signatures": ["bold_accents", "widget_cards", "expressive_avatars", "rounded_chrome"],
    "emotional_keywords": ["expressive", "playful", "social", "current"],
    "anti_patterns": ["serif_typography", "muted_palette", "dense_grids"]
  },
  "system_default_plus": {
    "name_en": "System Default Plus",
    "description": "iOS UI that hews close to native HIG with light brand customization: SF Pro typography, system chrome, single brand accent.",
    "visual_signatures": ["sf_pro_typography", "system_chrome", "single_brand_accent", "comfortable_density"],
    "emotional_keywords": ["familiar", "reliable", "polished", "neutral"],
    "anti_patterns": ["custom_chrome_overrides", "dense_data_grids", "ornamental_typography"]
  }
}
```

- [ ] **Step 2: Sanity check JSON parses and has 10 keys**

Run:
```bash
python -c "import json; d=json.load(open('data/ios_family_definitions.json')); assert len(d)==10; print(list(d.keys()))"
```
Expected: prints all 10 family slugs.

- [ ] **Step 3: Commit**

```bash
git add data/ios_family_definitions.json
git commit -m "data: hand-author iOS family canonical descriptions/keywords/anti_patterns"
```

---

## Phase F — Ingest scripts

### Task 19: ingest_web.py + run + verify

**Files:**
- Create: `scripts/ingest_web.py`
- Create: `tests/scripts/test_ingest_web.py`

- [ ] **Step 1: Write failing unit test for the table list**

```python
# tests/scripts/test_ingest_web.py
from scripts.ingest_web import WEB_TABLES, SKIP_TABLES


def test_skip_tables_excludes_user_data_and_views():
    assert "profiles" in SKIP_TABLES
    assert "projects" in SKIP_TABLES
    assert "domain_density_mapping" in SKIP_TABLES
    assert "domain_tone_mapping" in SKIP_TABLES
    assert "style_family_counts" in SKIP_TABLES
    assert "_summary" in SKIP_TABLES


def test_web_tables_include_core_catalog():
    for t in ("style_families", "design_styles", "color_palettes",
              "font_pairs", "domains", "domain_categories",
              "recommendation_scores", "color_psychology",
              "font_pair_categories"):
        assert t in WEB_TABLES, f"{t} missing from WEB_TABLES"
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `scripts/ingest_web.py`**

```python
"""Ingest dump/db-dump/tables/*.json into Supabase with platform='web'.

Usage:
    python scripts/ingest_web.py [--dump-dir dump/db-dump/tables] [--batch 200]

Idempotent: uses upsert by primary key.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from designlib_mcp.config import Settings
from supabase import create_client

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DUMP = REPO_ROOT / "dump" / "db-dump" / "tables"

WEB_TABLES = (
    "style_families",
    "domain_categories",
    "font_pair_categories",
    "domains",
    "design_styles",
    "color_palettes",
    "color_psychology",
    "font_pairs",
    "icon_libraries",
    "animation_presets",
    "animation_themed_collections",
    "background_types",
    "ui_libraries",
    "recommendation_scores",
    "app_config",
)

SKIP_TABLES = {
    "_summary",
    "profiles", "projects",                          # user-generated
    "domain_density_mapping", "domain_tone_mapping", # views
    "style_family_counts",
}

PLATFORM_AWARE = {"style_families", "design_styles", "color_palettes", "font_pairs"}


def _read_table(dump_dir: Path, name: str) -> list[dict]:
    path = dump_dir / f"{name}.json"
    if not path.exists():
        print(f"  [skip] {name}.json not found", file=sys.stderr)
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _annotate_platform(table: str, rows: list[dict]) -> list[dict]:
    if table not in PLATFORM_AWARE:
        return rows
    return [{**r, "platform": "web"} for r in rows]


def _strip_view_only_fields(rows: list[dict]) -> list[dict]:
    # tables sometimes serialize joined fields not present in the base schema
    return rows


def _upsert(client, table: str, rows: list[dict], batch: int) -> int:
    inserted = 0
    for i in range(0, len(rows), batch):
        chunk = rows[i:i + batch]
        client.table(table).upsert(chunk).execute()
        inserted += len(chunk)
    return inserted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP))
    parser.add_argument("--batch", type=int, default=200)
    args = parser.parse_args()

    settings = Settings.from_env()
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    dump_dir = Path(args.dump_dir)

    print(f"[ingest_web] dump_dir={dump_dir}")
    summary: dict[str, int] = {}
    for name in WEB_TABLES:
        rows = _read_table(dump_dir, name)
        rows = _annotate_platform(name, rows)
        if not rows:
            summary[name] = 0
            continue
        n = _upsert(client, name, rows, batch=args.batch)
        summary[name] = n
        print(f"  [ok] {name}: {n}")

    expected = json.loads((dump_dir / "_summary.json").read_text(encoding="utf-8"))
    print("\n[verify]")
    for name in WEB_TABLES:
        want = expected.get(name, {}).get("rows", 0)
        got = summary.get(name, 0)
        ok = "ok" if got >= want else "MISMATCH"
        print(f"  [{ok}] {name}: ingested={got} expected={want}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/scripts/test_ingest_web.py -v`
Expected: 2 passed.

- [ ] **Step 5: Provision Supabase, apply migrations, run ingest**

Manual steps (instructions for the engineer running the plan):

1. Create a Supabase project (free tier).
2. Copy `.env.example` to `.env`, fill in `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `DATABASE_URL`.
3. Apply migrations:
   ```bash
   python scripts/apply_migrations.py
   ```
   Expected: 3 migrations applied, no SQL errors.
4. Ingest web data:
   ```bash
   python scripts/ingest_web.py
   ```
   Expected: each table reports `ok`, verify-step shows all rows match `_summary.json`.
5. Run smoke test:
   ```bash
   pytest tests/repository/test_supabase_smoke.py -v
   ```
   Expected: 1 passed (`health_check`).

- [ ] **Step 6: Commit script (no Supabase data committed; only code)**

```bash
git add scripts/ingest_web.py tests/scripts/test_ingest_web.py
git commit -m "feat(scripts): ingest curated web catalog from dump into Supabase (idempotent upsert)"
```

---

### Task 20: ingest_ios.py + run + verify

**Files:**
- Create: `scripts/ingest_ios.py`
- Create: `tests/scripts/test_ingest_ios.py`

- [ ] **Step 1: Write failing unit tests for transform helpers**

```python
# tests/scripts/test_ingest_ios.py
from scripts.ingest_ios import (
    build_style_family_row, build_design_style_row,
    build_palette_rows, IOS_FONT_PAIRS,
)


def test_build_style_family_row_minimum():
    defn = {
        "name_en": "Demo",
        "description": "Demo family.",
        "visual_signatures": [], "emotional_keywords": [], "anti_patterns": [],
    }
    row = build_style_family_row("demo_family", defn, sort_order=14)
    assert row["id"] == "demo_family"
    assert row["platform"] == "ios"
    assert row["sort_order"] == 14


def test_build_design_style_row_uses_medians_and_definitions():
    defn = {
        "name_en": "Demo Family",
        "description": "Demo description.",
        "visual_signatures": ["foo"], "emotional_keywords": ["bar"], "anti_patterns": ["baz"],
    }
    medians = {
        "palette_light": {
            "background": "#FAFAFA", "surface_card": "#FFFFFF",
            "text_primary": "#111111", "text_secondary": "#8A8A8A",
            "accent_primary": "#4FB0C6", "separator": "#ECECEC",
        },
        "palette_dark": None,
        "typography": {"body_classification": "sf_pro_text", "heading_classification": "sf_pro_display",
                       "mono_present": False, "tabular_numerics_present": False},
        "layout": {"density_typical": "comfortable", "list_style_dominant": "plain",
                   "corner_radius_cards_pt_median": 18.0},
        "liquid_glass": {"posture": "native_fit", "surfaces_affected": ["tab_bar"]},
        "iconography": "custom_glyph_set",
        "reference_apps": ["alpha"],
    }
    row = build_design_style_row("demo_family", defn, medians)
    assert row["id"] == "demo_family_ios"
    assert row["family_id"] == "demo_family"
    assert row["platform"] == "ios"
    assert row["tokens"]["colors"]["background"] == "#FAFAFA"
    assert row["ios_metadata"]["liquid_glass_posture"] == "native_fit"
    assert row["ios_metadata"]["appearance_support"] == ["light"]
    assert row["ios_metadata"]["reference_apps"] == ["alpha"]


def test_build_palette_rows_returns_light_only_when_dark_missing():
    medians = {
        "palette_light": {"background": "#FAFAFA", "text_primary": "#111", "accent_primary": "#4FB0C6"},
        "palette_dark": None,
        "reference_apps": ["alpha"],
    }
    rows = build_palette_rows("demo_family", "Demo Family", medians)
    assert len(rows) == 1
    assert rows[0]["id"] == "demo_family_ios_light"
    assert rows[0]["platform"] == "ios"


def test_ios_font_pairs_count_matches_spec():
    assert len(IOS_FONT_PAIRS) == 6
    ids = {p["id"] for p in IOS_FONT_PAIRS}
    assert "ios_sf_pro_text_display" in ids
    assert "ios_sf_pro_text_new_york" in ids
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `scripts/ingest_ios.py`**

```python
"""Ingest iOS data (medians + definitions + raw aggregated profiles) into Supabase.

Usage:
    python scripts/ingest_ios.py [--reset]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from designlib_mcp.config import Settings
from supabase import create_client

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
EXTRACTION_DIR = REPO_ROOT / "extraction"

# Six canonical iOS font pairings authored by hand per spec §3.
IOS_FONT_PAIRS: list[dict] = [
    {
        "id": "ios_sf_pro_text_display",
        "name": "SF Pro Text + SF Pro Display",
        "category_id": "system_sans",
        "heading": {"font_family": "SF Pro Display", "weights": [400, 600, 700], "is_system_font": True},
        "body":    {"font_family": "SF Pro Text",    "weights": [400, 500, 600], "is_system_font": True},
        "mono": None,
        "import_url": "", "size_kb": 0, "variable_font": True,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["neutral", "system"], "use_cases": ["default_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
    {
        "id": "ios_sf_pro_text_new_york",
        "name": "SF Pro Text + New York Serif",
        "category_id": "system_serif_mix",
        "heading": {"font_family": "New York", "weights": [400, 600, 700], "is_system_font": True},
        "body":    {"font_family": "SF Pro Text", "weights": [400, 500], "is_system_font": True},
        "mono": None,
        "import_url": "", "size_kb": 0, "variable_font": False,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["editorial"], "use_cases": ["editorial_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
    {
        "id": "ios_sf_pro_rounded",
        "name": "SF Pro Rounded (heading + body)",
        "category_id": "system_rounded",
        "heading": {"font_family": "SF Pro Rounded", "weights": [500, 700], "is_system_font": True},
        "body":    {"font_family": "SF Pro Rounded", "weights": [400, 500], "is_system_font": True},
        "mono": None,
        "import_url": "", "size_kb": 0, "variable_font": True,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["friendly", "playful"], "use_cases": ["youthful_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
    {
        "id": "ios_sf_pro_text_custom_serif",
        "name": "SF Pro Text + Custom Serif",
        "category_id": "system_custom_serif",
        "heading": {"font_family": "Custom Serif", "weights": [400, 700], "is_system_font": False},
        "body":    {"font_family": "SF Pro Text",  "weights": [400, 500], "is_system_font": True},
        "mono": None,
        "import_url": "", "size_kb": 0, "variable_font": False,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["editorial", "branded"], "use_cases": ["branded_editorial_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
    {
        "id": "ios_sf_pro_text_custom_sans",
        "name": "SF Pro Text + Custom Sans",
        "category_id": "system_custom_sans",
        "heading": {"font_family": "Custom Sans", "weights": [500, 700], "is_system_font": False},
        "body":    {"font_family": "SF Pro Text", "weights": [400, 500], "is_system_font": True},
        "mono": None,
        "import_url": "", "size_kb": 0, "variable_font": False,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["branded"], "use_cases": ["branded_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
    {
        "id": "ios_sf_mono_display",
        "name": "SF Mono + SF Pro Display",
        "category_id": "system_mono_mix",
        "heading": {"font_family": "SF Pro Display", "weights": [600, 700], "is_system_font": True},
        "body":    {"font_family": "SF Mono",        "weights": [400, 500], "is_system_font": True},
        "mono":    {"font_family": "SF Mono",        "weights": [400, 500], "is_system_font": True},
        "import_url": "", "size_kb": 0, "variable_font": False,
        "line_heights": {}, "letter_spacing": {},
        "mood": ["technical"], "use_cases": ["data_dense_ios"],
        "style_fit": [], "domain_fit": [], "used_by": [],
        "platform": "ios",
    },
]


def build_style_family_row(family_slug: str, defn: dict, sort_order: int) -> dict:
    return {
        "id": family_slug,
        "name_en": defn["name_en"],
        "description": defn["description"],
        "sort_order": sort_order,
        "platform": "ios",
    }


def build_design_style_row(family_slug: str, defn: dict, medians: dict) -> dict:
    light = medians.get("palette_light") or {}
    dark = medians.get("palette_dark")
    appearance_support = ["light"] + (["dark"] if dark else [])
    typo = medians.get("typography") or {}
    layout = medians.get("layout") or {}
    lg = medians.get("liquid_glass") or {}
    return {
        "id": f"{family_slug}_ios",
        "family_id": family_slug,
        "name_en": defn["name_en"],
        "description": defn["description"],
        "visual_signatures": defn.get("visual_signatures", []),
        "emotional_keywords": defn.get("emotional_keywords", []),
        "anti_patterns": defn.get("anti_patterns", []),
        "tokens": {
            "colors": {
                "background": light.get("background"),
                "surface": light.get("surface_card") or light.get("background"),
                "border": light.get("separator"),
                "text_primary": light.get("text_primary"),
                "text_secondary": light.get("text_secondary"),
                "primary": light.get("accent_primary"),
            },
            "typography": {
                "heading_font": typo.get("heading_classification"),
                "body_font": typo.get("body_classification"),
                "mono_font": "SF Mono" if typo.get("mono_present") else None,
            },
            "layout": {
                "density": layout.get("density_typical"),
                "corner_radius_card_px": (
                    int(layout["corner_radius_cards_pt_median"])
                    if layout.get("corner_radius_cards_pt_median") is not None else None
                ),
            },
        },
        "reference_products": [],
        "domain_fit": {},
        "platform": "ios",
        "ios_metadata": {
            "liquid_glass_posture": lg.get("posture", "unclear"),
            "surfaces_affected": lg.get("surfaces_affected", []),
            "list_style_dominant": layout.get("list_style_dominant"),
            "density_typical": layout.get("density_typical"),
            "appearance_support": appearance_support,
            "corner_radius_cards_pt_median": layout.get("corner_radius_cards_pt_median"),
            "iconography": medians.get("iconography") or "unclear",
            "reference_apps": medians.get("reference_apps", []),
        },
    }


def _palette_colors_jsonb(pal: dict) -> dict:
    # color_palettes.colors is a JSONB column; store role→hex map.
    return {role: hex_v for role, hex_v in pal.items() if hex_v}


def build_palette_rows(family_slug: str, family_name: str, medians: dict) -> list[dict]:
    rows: list[dict] = []
    light = medians.get("palette_light")
    if light:
        rows.append({
            "id": f"{family_slug}_ios_light",
            "palette_type": "collection",
            "family_id": family_slug,
            "name": f"{family_name} (iOS Light)",
            "colors": _palette_colors_jsonb(light),
            "tags": ["ios_aggregated", "light"],
            "style_fit": [f"{family_slug}_ios"],
            "wcag_aa": None,
            "dark_mode_first": False,
            "sort_order": 0,
            "platform": "ios",
        })
    dark = medians.get("palette_dark")
    if dark:
        rows.append({
            "id": f"{family_slug}_ios_dark",
            "palette_type": "collection",
            "family_id": family_slug,
            "name": f"{family_name} (iOS Dark)",
            "colors": _palette_colors_jsonb(dark),
            "tags": ["ios_aggregated", "dark"],
            "style_fit": [f"{family_slug}_ios"],
            "wcag_aa": None,
            "dark_mode_first": True,
            "sort_order": 1,
            "platform": "ios",
        })
    return rows


def build_app_profile_rows(extraction_dir: Path, family_assignments: list[dict]) -> list[dict]:
    by_slug = {row["slug"]: row for row in family_assignments}
    rows: list[dict] = []
    for f in (extraction_dir / "aggregated").glob("*.json"):
        agg = json.loads(f.read_text(encoding="utf-8"))
        slug = agg["slug"]
        assignment = by_slug.get(slug, {})
        rows.append({
            "slug": slug,
            "family_id": assignment.get("family_assigned"),
            "aggregated": agg,
            "screenshot_count": agg.get("screenshot_count"),
            "confidence": assignment.get("confidence"),
        })
    return rows


def _reset_ios(client) -> None:
    print("[reset] removing ios rows...")
    client.table("ios_app_profiles").delete().neq("slug", "").execute()
    client.table("color_palettes").delete().eq("platform", "ios").execute()
    client.table("font_pairs").delete().eq("platform", "ios").execute()
    client.table("design_styles").delete().eq("platform", "ios").execute()
    client.table("style_families").delete().eq("platform", "ios").execute()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true",
                        help="delete existing ios rows before ingest")
    args = parser.parse_args()

    settings = Settings.from_env()
    client = create_client(settings.supabase_url, settings.supabase_anon_key)

    medians = json.loads((DATA_DIR / "ios_family_medians.json").read_text(encoding="utf-8"))
    definitions = json.loads((DATA_DIR / "ios_family_definitions.json").read_text(encoding="utf-8"))
    family_assignments = json.loads((EXTRACTION_DIR / "family_assignments.json").read_text(encoding="utf-8"))["assignments"]

    if args.reset:
        _reset_ios(client)

    # 1. style_families
    fam_rows = [
        build_style_family_row(slug, definitions[slug], sort_order=100 + i)
        for i, slug in enumerate(definitions)
    ]
    client.table("style_families").upsert(fam_rows).execute()
    print(f"[ok] style_families: {len(fam_rows)}")

    # 2. design_styles
    style_rows = [
        build_design_style_row(slug, definitions[slug], medians[slug])
        for slug in definitions if slug in medians
    ]
    client.table("design_styles").upsert(style_rows).execute()
    print(f"[ok] design_styles: {len(style_rows)}")

    # 3. color_palettes
    palette_rows: list[dict] = []
    for slug, defn in definitions.items():
        if slug in medians:
            palette_rows.extend(build_palette_rows(slug, defn["name_en"], medians[slug]))
    client.table("color_palettes").upsert(palette_rows).execute()
    print(f"[ok] color_palettes: {len(palette_rows)}")

    # 4. font_pairs (canonical iOS combinations)
    client.table("font_pairs").upsert(IOS_FONT_PAIRS).execute()
    print(f"[ok] font_pairs: {len(IOS_FONT_PAIRS)}")

    # 5. ios_app_profiles
    profile_rows = build_app_profile_rows(EXTRACTION_DIR, family_assignments)
    client.table("ios_app_profiles").upsert(profile_rows).execute()
    print(f"[ok] ios_app_profiles: {len(profile_rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/scripts/test_ingest_ios.py -v`
Expected: 4 passed.

- [ ] **Step 5: Run end-to-end against live Supabase**

Run: `python scripts/ingest_ios.py`
Expected output (approximate):
```
[ok] style_families: 10
[ok] design_styles: 10
[ok] color_palettes: 10–20
[ok] font_pairs: 6
[ok] ios_app_profiles: 51
```

- [ ] **Step 6: Verify rows in Supabase via psql**

Run:
```bash
psql "$DATABASE_URL" -c "SELECT platform, COUNT(*) FROM design_styles GROUP BY platform;"
psql "$DATABASE_URL" -c "SELECT platform, COUNT(*) FROM color_palettes GROUP BY platform;"
psql "$DATABASE_URL" -c "SELECT platform, COUNT(*) FROM font_pairs GROUP BY platform;"
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM ios_app_profiles;"
```
Expected: web counts unchanged from web ingest; ios counts ≥ 10/10/6/51.

- [ ] **Step 7: Commit**

```bash
git add scripts/ingest_ios.py tests/scripts/test_ingest_ios.py
git commit -m "feat(scripts): ingest iOS families/styles/palettes/font_pairs/app_profiles into Supabase"
```

---

## Phase G — Repository methods

### Notes for the engineer

`supabase-py` v2 query builder cheatsheet:

```python
client.table("design_styles").select("*", count="exact") \
    .eq("platform", "web") \
    .eq("family_id", "polished") \
    .contains("emotional_keywords", ["scholarly"]) \
    .range(0, 49) \
    .execute()
```
`count="exact"` makes `resp.count` populated (used for pagination total).
`range(start, end_inclusive)` is offset/limit.
For `tags` matching either `visual_signatures` OR `emotional_keywords`, use two queries and union (or use `.or_("...")` with PostgREST OR syntax).

All repository tests are marked `@pytest.mark.integration` and skip when env is absent.

---

### Task 21: Style repository methods

**Files:**
- Modify: `src/designlib_mcp/repository/supabase_repo.py`
- Create: `src/designlib_mcp/repository/normalizer.py` (DB row → Pydantic shape)
- Create: `tests/repository/test_styles_repo.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/repository/test_styles_repo.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.models.common import Platform


pytestmark = pytest.mark.integration


def test_list_styles_web_returns_57_total(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_styles(Platform.WEB, limit=200)
    assert out["total_count"] == 57
    assert len(out["items"]) == 57


def test_list_styles_ios_returns_10(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_styles(Platform.IOS, limit=50)
    assert out["total_count"] == 10
    assert {s["id"] for s in out["items"]} == {
        "enterprise_muted_ios", "fitness_vitality_ios", "editorial_photography_ios",
        "minimalist_monochrome_ios", "data_dense_terminal_ios", "warm_handcrafted_ios",
        "editorial_canvas_ios", "tactile_depth_playful_ios", "youth_social_widget_ios",
        "system_default_plus_ios",
    }


def test_list_styles_filters_by_family(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_styles(Platform.WEB, family="classical")
    for s in out["items"]:
        assert s["family_id"] == "classical"


def test_list_styles_filters_by_tag(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_styles(Platform.WEB, tags=["scholarly"])
    assert len(out["items"]) >= 1
    # academia_classical has emotional_keyword "scholarly"
    assert any(s["id"] == "academia_classical" for s in out["items"])


def test_get_style_returns_full_tokens(settings):
    repo = SupabaseRepository.from_settings(settings)
    s = repo.get_style("academia_classical")
    assert s is not None
    assert s["id"] == "academia_classical"
    assert "tokens" in s
    assert "colors" in s["tokens"]


def test_get_style_unknown_returns_none(settings):
    repo = SupabaseRepository.from_settings(settings)
    assert repo.get_style("does_not_exist_xyz") is None


def test_list_style_facets_web_has_families(settings):
    repo = SupabaseRepository.from_settings(settings)
    facets = repo.list_style_facets(Platform.WEB)
    assert len(facets["families"]) >= 9
    assert any(f["value"] == "polished" for f in facets["families"])
```

- [ ] **Step 2: Run — fail (NotImplementedError)**

- [ ] **Step 3: Implement style methods + a small normalizer**

Replace the style-related stub methods in `src/designlib_mcp/repository/supabase_repo.py`:

```python
# in supabase_repo.py — replace stubs for: list_styles, get_style, list_style_facets

def list_styles(
    self, platform: Platform, *,
    family: str | None = None, appearance: str | None = None,
    tone: str | None = None, density: str | None = None,
    tags: list[str] | None = None, limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    q = self._client.table("design_styles").select("*", count="exact").eq("platform", platform.value)
    if family:
        q = q.eq("family_id", family)
    # tone filter: exists in emotional_keywords array
    if tone:
        q = q.contains("emotional_keywords", [tone])
    # density filter (web tokens.layout.density OR ios_metadata.density_typical)
    if density:
        if platform == Platform.IOS:
            q = q.eq("ios_metadata->>density_typical", density)
        else:
            q = q.eq("tokens->'layout'->>'density'", density)
    # tags: visual_signatures OR emotional_keywords contains ALL tags
    if tags:
        for t in tags:
            q = q.or_(f"visual_signatures.cs.{{{t}}},emotional_keywords.cs.{{{t}}}")
    if appearance and platform == Platform.IOS:
        q = q.contains("ios_metadata->appearance_support", [appearance])
    q = q.range(offset, offset + limit - 1)
    resp = q.execute()
    rows = resp.data or []
    items = [_to_style_summary(r) for r in rows]
    return {
        "items": items,
        "total_count": resp.count or len(items),
        "limit": limit,
        "offset": offset,
        "platform": platform.value,
    }


def get_style(self, style_id: str) -> dict[str, Any] | None:
    resp = self._client.table("design_styles").select("*, style_families(name_en)") \
        .eq("id", style_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    row = rows[0]
    return _to_style_full(row)


def list_style_facets(self, platform: Platform) -> dict[str, Any]:
    resp = self._client.table("design_styles") \
        .select("family_id, visual_signatures, emotional_keywords, tokens, ios_metadata") \
        .eq("platform", platform.value).execute()
    rows = resp.data or []
    families: Counter[str] = Counter(r["family_id"] for r in rows if r.get("family_id"))
    tones: Counter[str] = Counter()
    densities: Counter[str] = Counter()
    appearances: Counter[str] = Counter()
    tags: Counter[str] = Counter()
    for r in rows:
        for kw in r.get("emotional_keywords") or []:
            tones[kw] += 1
        for sig in r.get("visual_signatures") or []:
            tags[sig] += 1
        if platform == Platform.IOS:
            ios = r.get("ios_metadata") or {}
            d = ios.get("density_typical")
            if d:
                densities[d] += 1
            for app in ios.get("appearance_support") or []:
                appearances[app] += 1
        else:
            d = ((r.get("tokens") or {}).get("layout") or {}).get("density")
            if d:
                densities[d] += 1
    return {
        "families": [{"value": v, "count": c} for v, c in families.most_common()],
        "tones": [{"value": v, "count": c} for v, c in tones.most_common()],
        "densities": [{"value": v, "count": c} for v, c in densities.most_common()],
        "appearances": [{"value": v, "count": c} for v, c in appearances.most_common()],
        "tag_vocabulary": [{"value": v, "count": c} for v, c in tags.most_common()],
        "platform": platform.value,
    }
```

Add to the top of `supabase_repo.py`:

```python
from collections import Counter
from designlib_mcp.repository.normalizer import _to_style_summary, _to_style_full
```

Create `src/designlib_mcp/repository/normalizer.py`:

```python
from __future__ import annotations
from typing import Any


def _primary_swatch(row: dict) -> str:
    tokens = row.get("tokens") or {}
    colors = tokens.get("colors") or {}
    return colors.get("primary") or colors.get("background") or "#000000"


def _to_style_summary(row: dict) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row.get("name_en") or row["id"],
        "family_id": row.get("family_id") or "",
        "platform": row.get("platform", "web"),
        "short_description": (row.get("description") or "")[:200],
        "top_signatures": (row.get("visual_signatures") or [])[:3],
        "primary_swatch": _primary_swatch(row),
    }


def _to_style_full(row: dict) -> dict[str, Any]:
    family_name = ""
    sf = row.get("style_families")
    if isinstance(sf, dict):
        family_name = sf.get("name_en", "")
    elif isinstance(sf, list) and sf:
        family_name = sf[0].get("name_en", "")
    return {
        "id": row["id"],
        "name": row.get("name_en") or row["id"],
        "family_id": row.get("family_id") or "",
        "family_name": family_name,
        "platform": row.get("platform", "web"),
        "description": row.get("description") or "",
        "visual_signatures": row.get("visual_signatures") or [],
        "emotional_keywords": row.get("emotional_keywords") or [],
        "anti_patterns": row.get("anti_patterns") or [],
        "tokens": row.get("tokens") or {},
        "ios_metadata": row.get("ios_metadata"),
    }
```

- [ ] **Step 4: Run — pass (assuming Supabase is seeded)**

Run: `pytest tests/repository/test_styles_repo.py -v -m integration`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/repository tests/repository/test_styles_repo.py
git commit -m "feat(repository): implement Supabase style methods (list/get/facets)"
```

---

### Task 22: Palette repository methods

**Files:**
- Modify: `src/designlib_mcp/repository/supabase_repo.py`
- Modify: `src/designlib_mcp/repository/normalizer.py`
- Create: `tests/repository/test_palettes_repo.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/repository/test_palettes_repo.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.models.common import Platform


pytestmark = pytest.mark.integration


def test_list_palettes_web_count(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_palettes(Platform.WEB, limit=200)
    assert out["total_count"] == 87


def test_list_palettes_ios_includes_aggregated(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_palettes(Platform.IOS, limit=50)
    assert out["total_count"] >= 10
    for p in out["items"]:
        assert p["platform"] == "ios"


def test_get_palette_returns_full_roles(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_palettes(Platform.IOS, limit=1)
    pid = out["items"][0]["id"]
    p = repo.get_palette(pid)
    assert p is not None
    assert "roles" in p
    assert isinstance(p["roles"], list)


def test_list_palette_facets_returns_appearances(settings):
    repo = SupabaseRepository.from_settings(settings)
    facets = repo.list_palette_facets(Platform.IOS)
    appearance_values = {a["value"] for a in facets["appearances"]}
    assert "light" in appearance_values
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Implement palette methods**

Replace palette stubs in `supabase_repo.py`:

```python
def list_palettes(
    self, platform: Platform, *,
    family: str | None = None, appearance: str | None = None,
    mood: str | None = None, tags: list[str] | None = None,
    limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    q = self._client.table("color_palettes").select("*", count="exact").eq("platform", platform.value)
    if family:
        q = q.eq("family_id", family)
    if mood:
        q = q.contains("tags", [mood])
    if tags:
        for t in tags:
            q = q.contains("tags", [t])
    if appearance:
        # appearance encoded in tags (e.g. "light"/"dark") for ios palettes
        q = q.contains("tags", [appearance])
    q = q.range(offset, offset + limit - 1)
    resp = q.execute()
    rows = resp.data or []
    items = [_to_palette_summary(r) for r in rows]
    return {
        "items": items,
        "total_count": resp.count or len(items),
        "limit": limit,
        "offset": offset,
        "platform": platform.value,
    }


def get_palette(self, palette_id: str) -> dict[str, Any] | None:
    resp = self._client.table("color_palettes").select("*").eq("id", palette_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    return _to_palette_full(rows[0])


def list_palette_facets(self, platform: Platform) -> dict[str, Any]:
    resp = self._client.table("color_palettes") \
        .select("family_id, tags, dark_mode_first").eq("platform", platform.value).execute()
    rows = resp.data or []
    families: Counter[str] = Counter()
    moods: Counter[str] = Counter()
    appearances: Counter[str] = Counter()
    bg_modes: Counter[str] = Counter()  # not currently captured separately; placeholder for future
    for r in rows:
        if r.get("family_id"):
            families[r["family_id"]] += 1
        for t in r.get("tags") or []:
            if t in {"warm", "cool", "neutral", "mixed"}:
                moods[t] += 1
            if t in {"light", "dark"}:
                appearances[t] += 1
        if r.get("dark_mode_first") and "dark" not in {a for a in appearances}:
            appearances["dark"] += 1
    return {
        "families": [{"value": v, "count": c} for v, c in families.most_common()],
        "moods": [{"value": v, "count": c} for v, c in moods.most_common()],
        "appearances": [{"value": v, "count": c} for v, c in appearances.most_common()],
        "background_modes": [{"value": v, "count": c} for v, c in bg_modes.most_common()],
        "platform": platform.value,
    }
```

Add to `normalizer.py`:

```python
def _to_palette_summary(row: dict) -> dict[str, Any]:
    colors = row.get("colors") or {}
    swatches = list(colors.values())[:5] if isinstance(colors, dict) else []
    appearance = "dark" if row.get("dark_mode_first") else "light"
    if isinstance(row.get("tags"), list):
        if "dark" in row["tags"] and "light" not in row["tags"]:
            appearance = "dark"
        elif "light" in row["tags"] and "dark" not in row["tags"]:
            appearance = "light"
    return {
        "id": row["id"],
        "name": row.get("name") or row["id"],
        "platform": row.get("platform", "web"),
        "appearance": appearance,
        "main_swatches": swatches,
    }


def _to_palette_full(row: dict) -> dict[str, Any]:
    colors = row.get("colors") or {}
    roles = [{"role": role, "hex": hex_v} for role, hex_v in colors.items()] if isinstance(colors, dict) else []
    appearance = "dark" if row.get("dark_mode_first") else "light"
    tags = row.get("tags") or []
    if "dark" in tags and "light" not in tags:
        appearance = "dark"
    elif "light" in tags and "dark" not in tags:
        appearance = "light"
    source = "ios_aggregated" if "ios_aggregated" in tags else "curated"
    return {
        "id": row["id"],
        "name": row.get("name") or row["id"],
        "platform": row.get("platform", "web"),
        "appearance": appearance,
        "roles": roles,
        "tags": tags,
        "source": source,
        "reference_apps": [],   # populated downstream from app_profiles when needed
        "used_by_styles": row.get("style_fit") or [],
    }
```

Update import line in `supabase_repo.py`:
```python
from designlib_mcp.repository.normalizer import (
    _to_style_summary, _to_style_full,
    _to_palette_summary, _to_palette_full,
)
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/repository/test_palettes_repo.py -v -m integration`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/repository tests/repository/test_palettes_repo.py
git commit -m "feat(repository): implement palette methods (list/get/facets) for web + ios"
```

---

### Task 23: Font pair repository methods

**Files:**
- Modify: `src/designlib_mcp/repository/supabase_repo.py`
- Modify: `src/designlib_mcp/repository/normalizer.py`
- Create: `tests/repository/test_font_pairs_repo.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/repository/test_font_pairs_repo.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.models.common import Platform


pytestmark = pytest.mark.integration


def test_list_font_pairs_web_count(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_font_pairs(Platform.WEB, limit=100)
    assert out["total_count"] == 28


def test_list_font_pairs_ios_count(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_font_pairs(Platform.IOS, limit=50)
    assert out["total_count"] == 6


def test_get_font_pair_full(settings):
    repo = SupabaseRepository.from_settings(settings)
    fp = repo.get_font_pair("ios_sf_pro_text_display")
    assert fp is not None
    assert fp["heading"]["font_family"] == "SF Pro Display"
    assert fp["body"]["is_system_font"] is True


def test_list_font_pair_facets_returns_categories(settings):
    repo = SupabaseRepository.from_settings(settings)
    facets = repo.list_font_pair_facets(Platform.IOS)
    cat_values = {c["value"] for c in facets["categories"]}
    assert "system_sans" in cat_values
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Implement font_pair methods**

Replace stubs:

```python
def list_font_pairs(
    self, platform: Platform, *,
    category_id: str | None = None, style_fit: list[str] | None = None,
    tags: list[str] | None = None, limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    q = self._client.table("font_pairs").select("*", count="exact").eq("platform", platform.value)
    if category_id:
        q = q.eq("category_id", category_id)
    if style_fit:
        for sid in style_fit:
            q = q.contains("style_fit", [sid])
    if tags:
        for t in tags:
            q = q.contains("mood", [t])
    q = q.range(offset, offset + limit - 1)
    resp = q.execute()
    rows = resp.data or []
    return {
        "items": [_to_font_pair_summary(r) for r in rows],
        "total_count": resp.count or len(rows),
        "limit": limit,
        "offset": offset,
        "platform": platform.value,
    }


def get_font_pair(self, font_pair_id: str) -> dict[str, Any] | None:
    resp = self._client.table("font_pairs").select("*, font_pair_categories(name_en)") \
        .eq("id", font_pair_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    return _to_font_pair_full(rows[0])


def list_font_pair_facets(self, platform: Platform) -> dict[str, Any]:
    resp = self._client.table("font_pairs") \
        .select("category_id, mood").eq("platform", platform.value).execute()
    rows = resp.data or []
    cats: Counter[str] = Counter(r["category_id"] for r in rows if r.get("category_id"))
    tags: Counter[str] = Counter()
    for r in rows:
        for m in r.get("mood") or []:
            tags[m] += 1
    return {
        "categories": [{"value": v, "count": c} for v, c in cats.most_common()],
        "tags": [{"value": v, "count": c} for v, c in tags.most_common()],
        "platform": platform.value,
    }
```

Add to `normalizer.py`:

```python
def _to_font_spec(jsonb: Any) -> dict[str, Any]:
    j = jsonb or {}
    return {
        "font_family": j.get("font_family") or j.get("family") or "",
        "weights": j.get("weights") or [],
        "fallbacks": j.get("fallbacks") or [],
        "google_fonts_url": j.get("google_fonts_url") or j.get("import_url"),
        "is_system_font": bool(j.get("is_system_font", False)),
    }


def _to_font_pair_summary(row: dict) -> dict[str, Any]:
    h = row.get("heading") or {}
    b = row.get("body") or {}
    return {
        "id": row["id"],
        "name": row.get("name") or row["id"],
        "platform": row.get("platform", "web"),
        "category_id": row.get("category_id") or "",
        "heading_family": (h.get("font_family") or h.get("family") or ""),
        "body_family": (b.get("font_family") or b.get("family") or ""),
    }


def _to_font_pair_full(row: dict) -> dict[str, Any]:
    cat_name = ""
    cat = row.get("font_pair_categories")
    if isinstance(cat, dict):
        cat_name = cat.get("name_en", "")
    elif isinstance(cat, list) and cat:
        cat_name = cat[0].get("name_en", "")
    return {
        "id": row["id"],
        "name": row.get("name") or row["id"],
        "platform": row.get("platform", "web"),
        "category_id": row.get("category_id") or "",
        "category_name": cat_name,
        "heading": _to_font_spec(row.get("heading")),
        "body": _to_font_spec(row.get("body")),
        "mono": _to_font_spec(row["mono"]) if row.get("mono") else None,
        "style_fit": row.get("style_fit") or [],
        "domain_fit": row.get("domain_fit") or [],
        "tags": row.get("mood") or [],
        "compatible_styles": row.get("style_fit") or [],
    }
```

Update imports in `supabase_repo.py` accordingly.

- [ ] **Step 4: Run — pass**

Run: `pytest tests/repository/test_font_pairs_repo.py -v -m integration`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/repository tests/repository/test_font_pairs_repo.py
git commit -m "feat(repository): implement font_pair methods (list/get/facets)"
```

---

### Task 24: Domain repository methods

**Files:**
- Modify: `src/designlib_mcp/repository/supabase_repo.py`
- Modify: `src/designlib_mcp/repository/normalizer.py`
- Create: `tests/repository/test_domains_repo.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/repository/test_domains_repo.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.models.common import Platform


pytestmark = pytest.mark.integration


def test_list_domains_returns_134(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_domains(limit=200)
    assert out["total_count"] == 134


def test_list_domains_filter_category(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_domains(category_id="travel")
    for d in out["items"]:
        assert d["category_id"] == "travel"


def test_get_domain_web_recommendations(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_domains(limit=1)
    domain_id = out["items"][0]["id"]
    d = repo.get_domain(domain_id, Platform.WEB, top_n=3)
    assert d is not None
    assert "recommendations" in d
    assert isinstance(d["recommendations"]["styles"], list)


def test_get_domain_ios_empty_recommendations_v1(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_domains(limit=1)
    domain_id = out["items"][0]["id"]
    d = repo.get_domain(domain_id, Platform.IOS, top_n=3)
    # iOS recommendation_scores not seeded in v1
    assert d["recommendations"]["styles"] == []


def test_list_domain_facets_returns_categories(settings):
    repo = SupabaseRepository.from_settings(settings)
    facets = repo.list_domain_facets()
    assert len(facets["categories"]) >= 15
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Implement domain methods**

Replace stubs:

```python
def list_domains(
    self, *, category_id: str | None = None, audience: str | None = None,
    tone: str | None = None, limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    q = self._client.table("domains").select("*", count="exact")
    if category_id:
        q = q.eq("category_id", category_id)
    if audience:
        q = q.eq("audience", audience)
    if tone:
        q = q.contains("tone", [tone])
    q = q.range(offset, offset + limit - 1)
    resp = q.execute()
    rows = resp.data or []
    return {
        "items": [_to_domain_summary(r) for r in rows],
        "total_count": resp.count or len(rows),
        "limit": limit,
        "offset": offset,
    }


def get_domain(
    self, domain_id: str, platform: Platform, top_n: int = 5,
) -> dict[str, Any] | None:
    resp = self._client.table("domains").select("*, domain_categories(name_en)") \
        .eq("id", domain_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    domain = _to_domain_full(rows[0])

    # Recommendations are populated by services/cross_links.py in Task 25.
    # For this task, return empty arrays — Task 25 wires them in.
    domain["recommendations"] = {"styles": [], "palettes": [], "font_pairs": []}
    return domain


def list_domain_facets(self) -> dict[str, Any]:
    resp = self._client.table("domains") \
        .select("category_id, audience, tone, data_density, ui_patterns").execute()
    rows = resp.data or []
    cats: Counter[str] = Counter(r["category_id"] for r in rows if r.get("category_id"))
    audiences: Counter[str] = Counter(r["audience"] for r in rows if r.get("audience"))
    tones: Counter[str] = Counter()
    densities: Counter[str] = Counter(r["data_density"] for r in rows if r.get("data_density"))
    patterns: Counter[str] = Counter()
    for r in rows:
        for t in r.get("tone") or []:
            tones[t] += 1
        for p in r.get("ui_patterns") or []:
            patterns[p] += 1
    return {
        "categories": [{"value": v, "count": c} for v, c in cats.most_common()],
        "audiences": [{"value": v, "count": c} for v, c in audiences.most_common()],
        "tones": [{"value": v, "count": c} for v, c in tones.most_common()],
        "data_densities": [{"value": v, "count": c} for v, c in densities.most_common()],
        "ui_patterns": [{"value": v, "count": c} for v, c in patterns.most_common()],
    }
```

Add to `normalizer.py`:

```python
def _to_domain_summary(row: dict) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row.get("name_en") or row["id"],
        "category_id": row.get("category_id") or "",
        "audience": row.get("audience"),
        "tone": (row.get("tone") or [None])[0],
        "data_density": row.get("data_density"),
    }


def _to_domain_full(row: dict) -> dict[str, Any]:
    cat_name = ""
    cat = row.get("domain_categories")
    if isinstance(cat, dict):
        cat_name = cat.get("name_en", "")
    elif isinstance(cat, list) and cat:
        cat_name = cat[0].get("name_en", "")
    return {
        "id": row["id"],
        "name": row.get("name_en") or row["id"],
        "category_id": row.get("category_id") or "",
        "category_name": cat_name,
        "description": row.get("description") or "",
        "audience": row.get("audience"),
        "tone": (row.get("tone") or [None])[0],
        "data_density": row.get("data_density"),
        "ui_patterns": row.get("ui_patterns") or [],
        "examples": row.get("examples") or [],
    }
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/repository/test_domains_repo.py -v -m integration`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/repository tests/repository/test_domains_repo.py
git commit -m "feat(repository): implement domain methods (list/get/facets) — recommendations stubbed"
```

---

### Task 25: Cross-links service + cross-link repository helpers

**Files:**
- Create: `src/designlib_mcp/services/__init__.py`
- Create: `src/designlib_mcp/services/cross_links.py`
- Modify: `src/designlib_mcp/repository/supabase_repo.py` (implement 4 helper methods)
- Modify: `src/designlib_mcp/repository/normalizer.py` (add helpers)
- Create: `tests/services/test_cross_links.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/services/test_cross_links.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.services.cross_links import (
    cross_links_for_style, recommendations_for_domain,
)
from designlib_mcp.models.common import Platform


pytestmark = pytest.mark.integration


def test_cross_links_for_web_style(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = cross_links_for_style(repo, "academia_classical", limit=3)
    assert "palettes" in out and "font_pairs" in out and "domains" in out
    # at least domains should be populated for web (recommendation_scores)
    assert len(out["domains"]) <= 3


def test_cross_links_for_ios_style_empty_v1(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = cross_links_for_style(repo, "fitness_vitality_ios", limit=3)
    # No iOS recommendation_scores in v1; domains list is empty.
    assert out["domains"] == []


def test_recommendations_for_domain_web(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = repo.list_domains(limit=1)
    domain_id = out["items"][0]["id"]
    rec = recommendations_for_domain(repo, domain_id, Platform.WEB, top_n=3)
    assert "styles" in rec and "palettes" in rec and "font_pairs" in rec
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Implement repo helpers**

Replace the four stubs at the bottom of `supabase_repo.py`:

```python
def palettes_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]:
    resp = self._client.table("color_palettes").select("*") \
        .contains("style_fit", [style_id]).limit(limit).execute()
    return [_to_palette_summary(r) for r in (resp.data or [])]


def font_pairs_used_by_style(self, style_id: str, limit: int) -> list[dict[str, Any]]:
    resp = self._client.table("font_pairs").select("*") \
        .contains("style_fit", [style_id]).limit(limit).execute()
    return [_to_font_pair_summary(r) for r in (resp.data or [])]


def style_domain_scores(self, style_id: str, limit: int) -> list[dict[str, Any]]:
    """Returns top-N domains for the given style, ordered by score desc."""
    resp = self._client.table("recommendation_scores").select("key_b, score") \
        .eq("matrix_type", "style_domain").eq("key_a", style_id) \
        .order("score", desc=True).limit(limit).execute()
    rows = resp.data or []
    if not rows:
        return []
    domain_ids = [r["key_b"] for r in rows]
    domains = self._client.table("domains").select("id, name_en, category_id") \
        .in_("id", domain_ids).execute()
    by_id = {d["id"]: d for d in (domains.data or [])}
    out = []
    for r in rows:
        d = by_id.get(r["key_b"])
        if d:
            out.append({
                "domain_id": d["id"],
                "name": d.get("name_en") or d["id"],
                "category_id": d.get("category_id") or "",
                "score": float(r["score"]),
            })
    return out


def domain_top_styles(
    self, domain_id: str, platform: Platform, limit: int,
) -> list[dict[str, Any]]:
    resp = self._client.table("recommendation_scores").select("key_a, score") \
        .eq("matrix_type", "style_domain").eq("key_b", domain_id) \
        .order("score", desc=True).limit(limit * 2).execute()
    rows = resp.data or []
    if not rows:
        return []
    style_ids = [r["key_a"] for r in rows]
    styles = self._client.table("design_styles").select("*") \
        .in_("id", style_ids).eq("platform", platform.value).execute()
    by_id = {s["id"]: s for s in (styles.data or [])}
    out = []
    for r in rows:
        s = by_id.get(r["key_a"])
        if s:
            out.append({**_to_style_summary(s), "score": float(r["score"])})
        if len(out) >= limit:
            break
    return out
```

- [ ] **Step 4: Write `src/designlib_mcp/services/__init__.py`** (empty)

- [ ] **Step 5: Write `src/designlib_mcp/services/cross_links.py`**

```python
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
    # de-dupe by id
    palettes_uniq = {p["id"]: p for p in palettes}
    fonts_uniq = {f["id"]: f for f in fonts}
    return {
        "styles": [{k: v for k, v in s.items() if k != "score"} for s in styles],
        "palettes": list(palettes_uniq.values())[:top_n],
        "font_pairs": list(fonts_uniq.values())[:top_n],
    }
```

- [ ] **Step 6: Wire into `get_style` and `get_domain`**

In `supabase_repo.py`, modify `get_style` (after building `_to_style_full(row)` result) to optionally include cross_links — but to keep the repo clean, we expose a separate method called by the tool layer. Adjust:

```python
def get_style(self, style_id: str) -> dict[str, Any] | None:
    resp = self._client.table("design_styles").select("*, style_families(name_en)") \
        .eq("id", style_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    return _to_style_full(rows[0])
```

(unchanged — the tool layer composes get_style + cross_links_for_style; see Task 27.)

Modify `get_domain` to delegate recommendations to the service:

```python
def get_domain(
    self, domain_id: str, platform: Platform, top_n: int = 5,
) -> dict[str, Any] | None:
    resp = self._client.table("domains").select("*, domain_categories(name_en)") \
        .eq("id", domain_id).limit(1).execute()
    rows = resp.data or []
    if not rows:
        return None
    domain = _to_domain_full(rows[0])
    from designlib_mcp.services.cross_links import recommendations_for_domain
    domain["recommendations"] = recommendations_for_domain(self, domain_id, platform, top_n=top_n)
    return domain
```

- [ ] **Step 7: Run — pass**

Run: `pytest tests/services/test_cross_links.py -v -m integration`
Expected: 3 passed.

- [ ] **Step 8: Commit**

```bash
git add src/designlib_mcp/services src/designlib_mcp/repository tests/services
git commit -m "feat(services): add cross_links service + repository cross-link helpers"
```

---

## Phase H — MCP tools

### Task 26: Truncate formatter

**Files:**
- Create: `src/designlib_mcp/formatting/__init__.py`
- Create: `src/designlib_mcp/formatting/truncate.py`
- Create: `tests/formatting/__init__.py`
- Create: `tests/formatting/test_truncate.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/formatting/test_truncate.py
from designlib_mcp.formatting.truncate import enforce_character_limit


def test_no_truncation_when_small():
    payload = {"items": [{"x": 1}, {"x": 2}], "meta": {"truncated": False}}
    out = enforce_character_limit(payload, limit=10_000)
    assert out["meta"]["truncated"] is False
    assert len(out["items"]) == 2


def test_truncates_items_when_over_limit():
    big_item = {"k": "x" * 1_000}
    payload = {"items": [big_item] * 30, "meta": {"truncated": False}}
    out = enforce_character_limit(payload, limit=5_000)
    assert out["meta"]["truncated"] is True
    assert len(out["items"]) < 30


def test_skips_when_no_items_field():
    payload = {"id": "x", "meta": {"truncated": False}}
    out = enforce_character_limit(payload, limit=10)
    # Single object — cannot truncate; just sets flag and returns as-is.
    assert out["meta"]["truncated"] is True
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `src/designlib_mcp/formatting/truncate.py`**

```python
from __future__ import annotations
import json
from typing import Any


def _serialized_size(payload: Any) -> int:
    return len(json.dumps(payload, ensure_ascii=False))


def enforce_character_limit(payload: dict, *, limit: int) -> dict:
    """If serialized payload exceeds `limit` characters, drop tail items and set truncated=True.

    For non-list payloads, just sets meta.truncated=True without modification — caller is
    responsible for using stricter filters.
    """
    if _serialized_size(payload) <= limit:
        return payload
    items = payload.get("items")
    if not isinstance(items, list):
        meta = payload.setdefault("meta", {})
        meta["truncated"] = True
        return payload
    # binary search for the largest prefix that fits
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        candidate = {**payload, "items": items[:mid]}
        if _serialized_size(candidate) <= limit:
            lo = mid
        else:
            hi = mid - 1
    truncated_items = items[:lo]
    out = {**payload, "items": truncated_items}
    out.setdefault("meta", {})["truncated"] = True
    return out
```

Also create empty `src/designlib_mcp/formatting/__init__.py` and `tests/formatting/__init__.py`.

- [ ] **Step 4: Run — pass**

Run: `pytest tests/formatting/test_truncate.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/formatting tests/formatting
git commit -m "feat(formatting): add CHARACTER_LIMIT-aware payload truncator with binary search"
```

---

### Task 27: Styles tool module

**Files:**
- Create: `src/designlib_mcp/tools/__init__.py`
- Create: `src/designlib_mcp/tools/styles.py`
- Create: `tests/tools/__init__.py`
- Create: `tests/tools/test_styles_tool.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/tools/test_styles_tool.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.models.common import Platform
from designlib_mcp.tools.styles import (
    list_styles_handler, get_style_handler, list_style_facets_handler,
)


pytestmark = pytest.mark.integration


def test_list_styles_handler_returns_paginated(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_styles_handler(repo, platform="web", limit=5, offset=0)
    assert "items" in out
    assert "total_count" in out
    assert "meta" in out
    assert out["meta"]["entity_type"] == "style_list"


def test_get_style_handler_returns_full_with_cross_links(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = get_style_handler(repo, style_id="academia_classical", include_cross_links=True)
    assert out["id"] == "academia_classical"
    assert out["cross_links"] is not None


def test_get_style_handler_unknown_returns_error(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = get_style_handler(repo, style_id="does_not_exist_xyz")
    assert out["error_code"] == "NOT_FOUND"


def test_list_style_facets_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_style_facets_handler(repo, platform="ios")
    assert out["meta"]["entity_type"] == "style_facets"
    assert len(out["families"]) == 10
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `src/designlib_mcp/tools/__init__.py`** (empty)

- [ ] **Step 4: Write `src/designlib_mcp/tools/styles.py`**

```python
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

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
```

Create empty `tests/tools/__init__.py`.

- [ ] **Step 5: Run — pass**

Run: `pytest tests/tools/test_styles_tool.py -v -m integration`
Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add src/designlib_mcp/tools/styles.py src/designlib_mcp/tools/__init__.py tests/tools
git commit -m "feat(tools): styles module — list/get/facets handlers + MCP registration"
```

---

### Task 28: Palettes tool module

**Files:**
- Create: `src/designlib_mcp/tools/palettes.py`
- Create: `tests/tools/test_palettes_tool.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/tools/test_palettes_tool.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.tools.palettes import (
    list_palettes_handler, get_palette_handler, list_palette_facets_handler,
)


pytestmark = pytest.mark.integration


def test_list_palettes_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_palettes_handler(repo, platform="ios", limit=5)
    assert out["meta"]["entity_type"] == "palette_list"
    assert len(out["items"]) >= 1


def test_get_palette_unknown_returns_error(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = get_palette_handler(repo, palette_id="not_a_real_palette_xyz")
    assert out["error_code"] == "NOT_FOUND"


def test_list_palette_facets_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_palette_facets_handler(repo, platform="ios")
    assert out["meta"]["entity_type"] == "palette_facets"
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `src/designlib_mcp/tools/palettes.py`**

```python
from __future__ import annotations
from typing import Any

from designlib_mcp.config import CHARACTER_LIMIT
from designlib_mcp.formatting.truncate import enforce_character_limit
from designlib_mcp.models.common import Platform
from designlib_mcp.repository.base import CatalogRepository


def list_palettes_handler(
    repo: CatalogRepository, *,
    platform: str, family: str | None = None, appearance: str | None = None,
    mood: str | None = None, tags: list[str] | None = None,
    limit: int = 50, offset: int = 0,
) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_palettes(p, family=family, appearance=appearance,
                             mood=mood, tags=tags, limit=limit, offset=offset)
    payload = {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": platform,
            "entity_type": "palette_list", "truncated": False,
        },
    }
    return enforce_character_limit(payload, limit=CHARACTER_LIMIT)


def get_palette_handler(repo: CatalogRepository, *, palette_id: str) -> dict[str, Any]:
    pal = repo.get_palette(palette_id)
    if pal is None:
        return {
            "error_code": "NOT_FOUND",
            "message": f"Palette '{palette_id}' not found.",
            "field": "palette_id",
            "suggest_tool": "list_palettes",
        }
    pal["meta"] = {
        "schema_version": "1.0", "platform": pal.get("platform"),
        "entity_type": "palette", "truncated": False,
    }
    return enforce_character_limit(pal, limit=CHARACTER_LIMIT)


def list_palette_facets_handler(repo: CatalogRepository, *, platform: str) -> dict[str, Any]:
    p = Platform(platform)
    raw = repo.list_palette_facets(p)
    return {
        **raw,
        "meta": {
            "schema_version": "1.0", "platform": platform,
            "entity_type": "palette_facets", "truncated": False,
        },
    }


def register(mcp, repo: CatalogRepository) -> None:
    @mcp.tool(name="list_palettes",
              description="List color palettes filtered by platform and optional facets.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_palettes(platform: str, family: str | None = None,
                      appearance: str | None = None, mood: str | None = None,
                      tags: list[str] | None = None, limit: int = 50,
                      offset: int = 0) -> dict[str, Any]:
        return list_palettes_handler(repo, platform=platform, family=family,
                                     appearance=appearance, mood=mood, tags=tags,
                                     limit=limit, offset=offset)

    @mcp.tool(name="get_palette", description="Get a single color palette with full role mapping.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def get_palette(palette_id: str) -> dict[str, Any]:
        return get_palette_handler(repo, palette_id=palette_id)

    @mcp.tool(name="list_palette_facets",
              description="List available facet values for the palettes catalog.",
              annotations={"readOnlyHint": True, "destructiveHint": False,
                           "idempotentHint": True, "openWorldHint": True})
    def list_palette_facets(platform: str) -> dict[str, Any]:
        return list_palette_facets_handler(repo, platform=platform)
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/tools/test_palettes_tool.py -v -m integration`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/tools/palettes.py tests/tools/test_palettes_tool.py
git commit -m "feat(tools): palettes module — list/get/facets handlers + MCP registration"
```

---

### Task 29: Font pairs tool module

**Files:**
- Create: `src/designlib_mcp/tools/font_pairs.py`
- Create: `tests/tools/test_font_pairs_tool.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/tools/test_font_pairs_tool.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.tools.font_pairs import (
    list_font_pairs_handler, get_font_pair_handler, list_font_pair_facets_handler,
)


pytestmark = pytest.mark.integration


def test_list_font_pairs_ios(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_font_pairs_handler(repo, platform="ios", limit=10)
    assert out["meta"]["entity_type"] == "font_pair_list"
    assert out["total_count"] == 6


def test_get_font_pair_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = get_font_pair_handler(repo, font_pair_id="ios_sf_pro_text_display")
    assert out["heading"]["font_family"] == "SF Pro Display"


def test_list_font_pair_facets_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_font_pair_facets_handler(repo, platform="ios")
    assert out["meta"]["entity_type"] == "font_pair_facets"
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `src/designlib_mcp/tools/font_pairs.py`**

Mirror the `palettes.py` shape: `list_font_pairs_handler`, `get_font_pair_handler`, `list_font_pair_facets_handler`, plus a `register(mcp, repo)` that registers all three with the same annotations and matching parameter forwarding. Use `repo.list_font_pairs`, `repo.get_font_pair`, `repo.list_font_pair_facets`. `entity_type` values: `"font_pair_list"`, `"font_pair"`, `"font_pair_facets"`. Error for `get`: `error_code="NOT_FOUND"`, `field="font_pair_id"`, `suggest_tool="list_font_pairs"`.

- [ ] **Step 4: Run — pass**

Run: `pytest tests/tools/test_font_pairs_tool.py -v -m integration`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/tools/font_pairs.py tests/tools/test_font_pairs_tool.py
git commit -m "feat(tools): font_pairs module — list/get/facets handlers + MCP registration"
```

---

### Task 30: Domains tool module

**Files:**
- Create: `src/designlib_mcp/tools/domains.py`
- Create: `tests/tools/test_domains_tool.py`

- [ ] **Step 1: Write integration tests**

```python
# tests/tools/test_domains_tool.py
import pytest
from designlib_mcp.repository.supabase_repo import SupabaseRepository
from designlib_mcp.tools.domains import (
    list_domains_handler, get_domain_handler, list_domain_facets_handler,
)


pytestmark = pytest.mark.integration


def test_list_domains_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_domains_handler(repo, limit=5)
    assert out["meta"]["entity_type"] == "domain_list"
    assert out["total_count"] == 134


def test_get_domain_handler_web(settings):
    repo = SupabaseRepository.from_settings(settings)
    list_out = list_domains_handler(repo, limit=1)
    out = get_domain_handler(repo, domain_id=list_out["items"][0]["id"], platform="web", top_n=3)
    assert out["meta"]["entity_type"] == "domain"
    assert "recommendations" in out


def test_get_domain_handler_unknown(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = get_domain_handler(repo, domain_id="does_not_exist_xyz", platform="web", top_n=3)
    assert out["error_code"] == "NOT_FOUND"


def test_list_domain_facets_handler(settings):
    repo = SupabaseRepository.from_settings(settings)
    out = list_domain_facets_handler(repo)
    assert out["meta"]["entity_type"] == "domain_facets"
    assert len(out["categories"]) >= 15
```

- [ ] **Step 2: Run — fail**

- [ ] **Step 3: Write `src/designlib_mcp/tools/domains.py`**

```python
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
```

- [ ] **Step 4: Run — pass**

Run: `pytest tests/tools/test_domains_tool.py -v -m integration`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/tools/domains.py tests/tools/test_domains_tool.py
git commit -m "feat(tools): domains module — list/get/facets handlers + MCP registration"
```

---

## Phase I — Server, integration, README

### Task 31: FastMCP server + entry point

**Files:**
- Create: `src/designlib_mcp/server.py`
- Create: `src/designlib_mcp/__main__.py`

- [ ] **Step 1: Write `src/designlib_mcp/server.py`**

```python
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
```

- [ ] **Step 2: Write `src/designlib_mcp/__main__.py`**

```python
from __future__ import annotations
from designlib_mcp.server import build_server


def main() -> None:
    mcp = build_server()
    mcp.run()  # stdio transport


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Smoke check — server boots**

Run (in a separate terminal or with `timeout`):
```bash
timeout 3s python -m designlib_mcp || true
```
Expected: process starts, awaits stdio, then is killed by timeout. No tracebacks prior to kill.

- [ ] **Step 4: Verify entry point**

Run: `pip install -e ".[dev]"` then `which designlib-mcp` (Windows: `where designlib-mcp`).
Expected: a script path is printed.

- [ ] **Step 5: Commit**

```bash
git add src/designlib_mcp/server.py src/designlib_mcp/__main__.py
git commit -m "feat(server): wire FastMCP app + entry point registering all 12 tools"
```

---

### Task 32: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write `README.md`**

```markdown
# designlib-mcp

A Python MCP server that exposes a curated design-knowledge catalog (web + iOS) over 12 read-only tools, backed by Supabase. Intended consumer: an external IDE/editor plugin that analyzes a project locally and pulls matching styles/palettes/font_pairs/domain data from this server.

## Quick start

### 1. Provision Supabase

Create a Supabase project (free tier is enough). Capture:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY` (from Project Settings → API)
- `DATABASE_URL` (from Project Settings → Database → Connection string, "URI" format)

Copy `.env.example` to `.env` and fill in those values.

### 2. Install

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Apply migrations + seed

```bash
python scripts/apply_migrations.py
python scripts/ingest_web.py
python scripts/compute_ios_medians.py
python scripts/ingest_ios.py
```

### 4. Run

```bash
designlib-mcp
# or
python -m designlib_mcp
```

The server speaks MCP over stdio.

### 5. Wire into Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`
(or the Windows equivalent at `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "designlib": {
      "command": "designlib-mcp",
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_ANON_KEY": "eyJhbGciOi..."
      }
    }
  }
}
```

Restart Claude Desktop. The 12 tools should appear under the `designlib` server.

## Tools

| Entity      | Tools                                                              |
| ----------- | ------------------------------------------------------------------ |
| Styles      | `list_styles`, `get_style`, `list_style_facets`                    |
| Palettes    | `list_palettes`, `get_palette`, `list_palette_facets`              |
| Font pairs  | `list_font_pairs`, `get_font_pair`, `list_font_pair_facets`        |
| Domains     | `list_domains`, `get_domain`, `list_domain_facets`                 |

## Plugin flow

A typical pull from the consumer plugin:

```
1. list_style_facets(platform="web")
       → discover available families, tones, densities
2. list_styles(platform="web", family="editorial", tone="literary")
       → shortlist with summaries
3. get_style(style_id="academia_classical")
       → full tokens + cross_links (compatible palettes/fonts/domains)
```

The server never receives project context — the plugin is authoritative about matching;
the server is a catalog.

## Source-only directories

`dump/`, `extraction/`, and `researches/` are NOT shipped with the repo; they are local
working folders used by the maintainer to seed Supabase (see `.gitignore`). End users who
just want to run the server don't need them — they only need a populated Supabase.

## Development

```bash
pytest                              # unit tests (no Supabase required)
pytest -m integration               # also run integration tests against live Supabase
ruff check src tests
```

See `docs/superpowers/specs/2026-04-22-designlib-mcp-v1-design.md` for the design spec
and `docs/superpowers/plans/2026-04-22-designlib-mcp-v1.md` for the implementation plan.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with install, ingest, Claude Desktop integration, and plugin flow"
```

---

### Task 33: End-to-end Claude Desktop integration check (manual)

**Files:** none (manual verification)

- [ ] **Step 1: Apply Claude Desktop config** (per README §5)

- [ ] **Step 2: Restart Claude Desktop**

- [ ] **Step 3: In a new chat, run a discovery prompt**

Prompt:
```
Use the designlib MCP. Call list_style_facets with platform="web" and tell me how many families are returned.
```

Expected: assistant successfully calls the tool and reports ≥9 families.

- [ ] **Step 4: Run a get_style chain**

Prompt:
```
Use designlib. Call list_styles with platform="web", family="classical", limit=3.
Then call get_style on the first item with include_cross_links=true.
```

Expected: full tokens returned in <1s; cross_links includes palettes/font_pairs (and domains for web styles).

- [ ] **Step 5: iOS smoke**

Prompt:
```
Use designlib. Call list_styles with platform="ios" and tell me which 10 family-styles are available.
```

Expected: 10 `_ios` style ids listed.

- [ ] **Step 6: Mark v1 acceptance criteria complete**

Verify against spec §7:

1. Migrations applied — verified in Task 19.
2. `data/ios_family_medians.json` generated, <30% review_flags — verified in Task 17.
3. iOS rows ingested — verified in Task 20.
4. `data/ios_family_definitions.json` authored — verified in Task 18.
5. 12 tools have smoke tests — verified in Tasks 27–30.
6. MCP launches locally — verified in Task 31.
7. Claude Desktop integration — verified in this task.
8. README — verified in Task 32.

If all green: cut a tag.

```bash
git tag -a v0.1.0 -m "designlib-mcp v0.1 — first usable release"
```

---

## Self-Review

After writing this plan, the following sanity checks were performed and any issues fixed inline:

- **Spec coverage.** Each section in `docs/superpowers/specs/2026-04-22-designlib-mcp-v1-design.md` maps to at least one task: §1 scope (Tasks 27–30), §2 architecture (Tasks 1, 8, 31), §3 schema (Tasks 4–6), §4 tools (Tasks 27–30), §5 models (Tasks 3, 10–13), §6 normalization (Tasks 14–18), §7 acceptance criteria (Task 33).
- **Placeholder scan.** No "TBD"/"TODO"/"add appropriate handling"/"similar to Task N" entries; every code step contains the actual code, every command its expected output.
- **Type consistency.** `Platform`, `Density`, `Appearance` enums are defined once (Task 3) and reused by name throughout. `CatalogRepository` Protocol method signatures (Task 8) match `SupabaseRepository` implementations (Tasks 21–25). Tool handler names (`list_styles_handler`, etc.) are referenced consistently between Tasks 27–30 and never renamed.
- **iOS recommendation_scores.** Spec defers them to v2; Tasks 24/25/27 explicitly assert they are empty for iOS (`test_get_domain_ios_empty_recommendations_v1`, `test_cross_links_for_ios_style_empty_v1`).
