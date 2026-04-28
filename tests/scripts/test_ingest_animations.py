import json
from pathlib import Path

import pytest

from scripts.ingest_animations import load_staging, validate_record


def test_load_staging_reads_all_json(tmp_path: Path):
    fixture = Path(__file__).parent / "fixtures" / "animation_staging_sample.json"
    (tmp_path / "a.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "b.json").write_text(
        fixture.read_text(encoding="utf-8").replace("test_sample", "test_sample_b"),
        encoding="utf-8",
    )
    rows = load_staging(tmp_path)
    assert len(rows) == 2
    ids = {r["id"] for r in rows}
    assert ids == {"animation_test_sample", "animation_test_sample_b"}


def test_validate_record_accepts_valid():
    fixture = Path(__file__).parent / "fixtures" / "animation_staging_sample.json"
    rec = json.loads(fixture.read_text(encoding="utf-8"))
    validate_record(rec)


def test_validate_record_rejects_missing_required():
    fixture = Path(__file__).parent / "fixtures" / "animation_staging_sample.json"
    rec = json.loads(fixture.read_text(encoding="utf-8"))
    rec.pop("category")
    with pytest.raises(ValueError, match="category"):
        validate_record(rec)


def test_validate_record_rejects_bad_enum():
    fixture = Path(__file__).parent / "fixtures" / "animation_staging_sample.json"
    rec = json.loads(fixture.read_text(encoding="utf-8"))
    rec["category"] = "not_a_category"
    with pytest.raises(ValueError, match="category"):
        validate_record(rec)
