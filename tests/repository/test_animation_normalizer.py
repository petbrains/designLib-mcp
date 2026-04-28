from designlib_mcp.repository.normalizer import (
    _to_animation_summary, _to_animation_full,
)


ROW = {
    "id": "animation_aurora_background",
    "title": "Aurora Background",
    "description": "Soft aurora.",
    "use_when": ["dark_landing_page"],
    "category": "background",
    "framework": "react",
    "libraries": ["framer-motion"],
    "interactivity": "static",
    "complexity": "light",
    "style_tags": ["aurora"],
    "placement": ["hero"],
    "keyword": ["aurora"],
    "component_filename": "aurora-background.tsx",
    "prompt_text": "# Aurora Background\n",
    "source_file": "animations2.md",
    "source_index": 9,
}


def test_summary_keeps_summary_fields():
    s = _to_animation_summary(ROW)
    assert s == {
        "id": "animation_aurora_background",
        "title": "Aurora Background",
        "description": "Soft aurora.",
        "category": "background",
        "framework": "react",
        "complexity": "light",
        "style_tags": ["aurora"],
    }


def test_full_returns_all_searchable_fields():
    f = _to_animation_full(ROW)
    assert f["use_when"] == ["dark_landing_page"]
    assert f["libraries"] == ["framer-motion"]
    assert f["prompt_text"].startswith("# Aurora Background")
    assert f["component_filename"] == "aurora-background.tsx"


def test_full_handles_missing_arrays():
    bare = {"id": "x", "title": "X", "description": "x", "category": "background",
            "framework": "react", "interactivity": "static", "complexity": "light",
            "component_filename": "x.tsx", "prompt_text": "# X"}
    f = _to_animation_full(bare)
    assert f["use_when"] == []
    assert f["libraries"] == []
    assert f["style_tags"] == []
