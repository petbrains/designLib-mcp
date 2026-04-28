from pathlib import Path
from scripts.split_animation_prompts import split_file


def test_split_file_react_format(tmp_path: Path):
    src = Path(__file__).parent / "fixtures" / "animation_sample.md"
    out_dir = tmp_path / "raw"
    out_dir.mkdir()
    blocks = split_file(src, out_dir, source_stem="animation_sample")
    assert len(blocks) == 2
    assert blocks[0].source_index == 0
    assert blocks[0].raw_path.name == "animation_sample_000.md"
    assert "foo-bar.tsx" in blocks[0].raw_path.read_text()
    assert "baz-qux.tsx" in blocks[1].raw_path.read_text()


def test_split_file_html_format(tmp_path: Path):
    src = tmp_path / "html_sample.md"
    src.write_text(
        "Create a complete loading animation UI featuring spinner A.\n"
        "~~~html\n<html>A</html>\n~~~\n"
        "Create a complete loading animation UI featuring spinner B.\n"
        "~~~html\n<html>B</html>\n~~~\n"
    )
    out_dir = tmp_path / "raw"
    out_dir.mkdir()
    blocks = split_file(src, out_dir, source_stem="html_sample")
    assert len(blocks) == 2
