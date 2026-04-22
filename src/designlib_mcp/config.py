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
