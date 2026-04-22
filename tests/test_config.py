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
    # Monkeypatch load_dotenv to prevent it from reloading .env file
    monkeypatch.setattr("designlib_mcp.config.load_dotenv", lambda: None)
    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        Settings.from_env()
