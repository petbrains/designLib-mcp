import pytest
from pydantic import ValidationError
from designlib_mcp.models.animation import Animation, AnimationSummary


def _payload(**overrides):
    base = {
        "id": "animation_aurora_background",
        "title": "Aurora Background",
        "description": "Soft aurora gradient bands.",
        "use_when": ["dark_landing_page"],
        "category": "background",
        "framework": "react",
        "libraries": ["framer-motion"],
        "interactivity": "static",
        "complexity": "light",
        "style_tags": ["aurora", "gradient"],
        "placement": ["hero", "background"],
        "keyword": ["aurora", "gradient"],
        "component_filename": "aurora-background.tsx",
        "prompt_text": "# Aurora Background\n...",
        "meta": {"schema_version": "1.0", "platform": None,
                 "entity_type": "animation", "truncated": False},
    }
    base.update(overrides)
    return base


def test_animation_valid():
    a = Animation(**_payload())
    assert a.id == "animation_aurora_background"
    assert a.framework == "react"


def test_animation_rejects_unknown_category():
    with pytest.raises(ValidationError):
        Animation(**_payload(category="not_a_category"))


def test_animation_rejects_unknown_framework():
    with pytest.raises(ValidationError):
        Animation(**_payload(framework="vue"))


def test_animation_summary_minimal():
    s = AnimationSummary(
        id="animation_aurora_background",
        title="Aurora Background",
        description="x",
        category="background",
        framework="react",
        complexity="light",
        style_tags=["aurora"],
    )
    assert s.framework == "react"
