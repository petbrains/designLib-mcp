"""Ingest mcp-migration/animations/staging/*.json into Supabase.

Usage:
    python scripts/ingest_animations.py [--staging-dir mcp-migration/animations/staging] [--dry-run]

Idempotent: upserts on `id`. Requires SUPABASE_SERVICE_ROLE_KEY in .env (or falls back
to SUPABASE_ANON_KEY when RLS allows writes; service role recommended).
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STAGING = REPO_ROOT / "mcp-migration" / "animations" / "staging"

REQUIRED_FIELDS = (
    "id", "title", "description", "use_when", "category", "framework",
    "libraries", "interactivity", "complexity", "style_tags", "placement",
    "keyword", "component_filename", "prompt_text", "source_file", "source_index",
)
VALID_CATEGORIES = {"background", "hero", "loader", "text_effect",
                    "element", "cursor_effect", "overlay", "decoration"}
VALID_FRAMEWORKS = {"react", "vanilla_html"}
VALID_INTERACTIVITY = {"static", "hover", "click", "cursor_track", "scroll", "mount_only"}
VALID_COMPLEXITY = {"light", "medium", "heavy"}


def load_staging(staging_dir: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(staging_dir.glob("*.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def validate_record(rec: dict) -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in rec]
    if missing:
        raise ValueError(f"missing fields: {missing}")
    if rec["category"] not in VALID_CATEGORIES:
        raise ValueError(f"invalid category: {rec['category']}")
    if rec["framework"] not in VALID_FRAMEWORKS:
        raise ValueError(f"invalid framework: {rec['framework']}")
    if rec["interactivity"] not in VALID_INTERACTIVITY:
        raise ValueError(f"invalid interactivity: {rec['interactivity']}")
    if rec["complexity"] not in VALID_COMPLEXITY:
        raise ValueError(f"invalid complexity: {rec['complexity']}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--staging-dir", default=str(DEFAULT_STAGING))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    load_dotenv()
    rows = load_staging(Path(args.staging_dir))
    print(f"Loaded {len(rows)} records from {args.staging_dir}")

    for rec in rows:
        validate_record(rec)
    print("All records validated.")

    if args.dry_run:
        print("Dry run -- not writing to Supabase.")
        return 0

    url = os.environ["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ["SUPABASE_ANON_KEY"]
    client = create_client(url, key)

    for i, rec in enumerate(rows):
        rec.setdefault("sort_order", i)
        client.table("animations").upsert(rec, on_conflict="id").execute()
    print(f"Upserted {len(rows)} animations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
