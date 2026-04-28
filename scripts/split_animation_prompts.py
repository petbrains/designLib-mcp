"""Split prompts/animations*.md into per-prompt raw files.

Usage:
    python scripts/split_animation_prompts.py [--source-dir prompts] [--out-dir mcp-migration/animations/raw]

Also populates the status table in mcp-migration/animations/PROGRESS.md.
"""
from __future__ import annotations
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "prompts"
DEFAULT_OUT = REPO_ROOT / "mcp-migration" / "animations" / "raw"
PROGRESS_PATH = REPO_ROOT / "mcp-migration" / "animations" / "PROGRESS.md"

REACT_DELIM = re.compile(
    r"^You are given a task to integrate an existing React component",
    re.MULTILINE,
)
HTML_DELIM = re.compile(r"^Create a complete", re.MULTILINE)


@dataclass
class Block:
    source_file: str
    source_index: int
    raw_path: Path
    component_filename: str | None


def _detect_delim(text: str) -> re.Pattern[str]:
    react_hits = len(REACT_DELIM.findall(text))
    html_hits = len(HTML_DELIM.findall(text))
    return REACT_DELIM if react_hits >= html_hits else HTML_DELIM


def _extract_filename(block_text: str) -> str | None:
    m = re.search(r"```tsx\s*\n([a-zA-Z0-9_\-]+\.tsx)\b", block_text)
    if m:
        return m.group(1)
    m = re.search(r"```html\s*\n([a-zA-Z0-9_\-]+\.html)\b", block_text)
    return m.group(1) if m else None


def split_file(src: Path, out_dir: Path, source_stem: str) -> list[Block]:
    text = src.read_text(encoding="utf-8")
    delim = _detect_delim(text)
    starts = [m.start() for m in delim.finditer(text)]
    if not starts:
        return []
    starts.append(len(text))
    blocks: list[Block] = []
    for idx in range(len(starts) - 1):
        chunk = text[starts[idx]:starts[idx + 1]].rstrip() + "\n"
        out_path = out_dir / f"{source_stem}_{idx:03d}.md"
        out_path.write_text(chunk, encoding="utf-8")
        blocks.append(Block(
            source_file=src.name,
            source_index=idx,
            raw_path=out_path,
            component_filename=_extract_filename(chunk),
        ))
    return blocks


def write_progress(blocks: list[Block]) -> None:
    header = (
        "# Animations Standardization — Progress Tracker\n\n"
        "**Read PROTOCOL.md before processing any prompt.**\n\n"
        "Status flow: `todo` → `in_progress` → `done` | `needs_review` | `skipped`.\n\n"
        "| # | source_file | source_index | raw_filename | staging_id | status | owner | notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )
    rows: list[str] = []
    for i, b in enumerate(blocks, start=1):
        if b.component_filename:
            stem = b.component_filename.rsplit(".", 1)[0].replace("-", "_").lower()
            staging_id = f"animation_{stem}"
        else:
            staging_id = f"animation_{b.source_file.replace('.md','')}_{b.source_index:03d}"
        rows.append(
            f"| {i} | {b.source_file} | {b.source_index} | {b.raw_path.name} | {staging_id} | todo |  |  |"
        )
    PROGRESS_PATH.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    p.add_argument("--out-dir", default=str(DEFAULT_OUT))
    args = p.parse_args()
    src_dir = Path(args.source_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    all_blocks: list[Block] = []
    for src in sorted(src_dir.glob("animations*.md")):
        stem = src.stem
        blocks = split_file(src, out_dir, source_stem=stem)
        print(f"  {src.name}: {len(blocks)} prompts")
        all_blocks.extend(blocks)
    write_progress(all_blocks)
    print(f"Total: {len(all_blocks)} prompts -> {out_dir}")
    print(f"Tracker: {PROGRESS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
