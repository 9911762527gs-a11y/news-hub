"""Central settings loaded from .env — single source of truth for all modules."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class Settings:
    """Immutable app-wide settings populated once at import time."""

    # ─── AI (FREE APIs only) ────────────────────────────────
    groq_api_key: str = field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    # Ollama runs locally - no API key needed, just install from https://ollama.ai
    use_ollama: bool = field(default_factory=lambda: os.getenv("USE_OLLAMA", "false").lower() == "true")

    # ─── News ──────────────────────────────────────────────
    news_sources: list[str] = field(
        default_factory=lambda: os.getenv("NEWS_SOURCES", "google_news,ndtv,the_hindu").split(",")
    )
    reels_per_day: int = field(default_factory=lambda: int(os.getenv("REELS_PER_DAY", "3")))
    reel_schedule_times: list[str] = field(
        default_factory=lambda: os.getenv("REEL_SCHEDULE_TIMES", "08:00,14:00,19:00").split(",")
    )

    # ─── Paths ─────────────────────────────────────────────
    output_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("OUTPUT_DIR", "output")
    )
    assets_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "assets")
    backgrounds_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "assets" / "backgrounds"
    )
    characters_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / "assets" / "characters"
    )

    # ─── YouTube ───────────────────────────────────────────
    youtube_client_id: str = field(default_factory=lambda: os.getenv("YOUTUBE_CLIENT_ID", ""))
    youtube_client_secret: str = field(
        default_factory=lambda: os.getenv("YOUTUBE_CLIENT_SECRET", "")
    )
    youtube_access_token: str = field(
        default_factory=lambda: os.getenv("YOUTUBE_ACCESS_TOKEN", "")
    )
    youtube_refresh_token: str = field(
        default_factory=lambda: os.getenv("YOUTUBE_REFRESH_TOKEN", "")
    )

    # ─── X / Twitter (OAuth 1.0a - FREE) ──────────────────
    x_api_key: str = field(default_factory=lambda: os.getenv("X_API_KEY", ""))
    x_api_secret: str = field(default_factory=lambda: os.getenv("X_API_SECRET", ""))
    x_access_token: str = field(default_factory=lambda: os.getenv("X_ACCESS_TOKEN", ""))
    x_access_token_secret: str = field(
        default_factory=lambda: os.getenv("X_ACCESS_TOKEN_SECRET", "")
    )

    # ─── Instagram (FREE via Instaloader) ──────────────────
    ig_username: str = field(default_factory=lambda: os.getenv("IG_USERNAME", ""))
    ig_password: str = field(default_factory=lambda: os.getenv("IG_PASSWORD", ""))

    # ─── Facebook (Graph API - FREE) ────────────────────────
    fb_page_id: str = field(default_factory=lambda: os.getenv("FB_PAGE_ID", ""))
    fb_access_token: str = field(default_factory=lambda: os.getenv("FB_ACCESS_TOKEN", ""))

    # ─── Misc ──────────────────────────────────────────────
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # ─── Derived ──────────────────────────────────────────
    @property
    def is_configured(self) -> bool:
        """True when the minimum required keys are set (AI + at least one social platform)."""
        # AI is configured if we have Groq key OR using Ollama
        ai_configured = bool(self.groq_api_key) or self.use_ollama
        return ai_configured

    @property
    def youtube_configured(self) -> bool:
        return bool(self.youtube_client_id and self.youtube_client_secret and self.youtube_refresh_token)

    @property
    def x_configured(self) -> bool:
        # OAuth 1.0a (free) requires all 4 keys
        return bool(self.x_api_key and self.x_api_secret and self.x_access_token and self.x_access_token_secret)

    @property
    def instagram_configured(self) -> bool:
        # Using Instaloader (free) - requires username and password
        return bool(self.ig_username and self.ig_password)

    @property
    def facebook_configured(self) -> bool:
        return bool(self.fb_page_id and self.fb_access_token)

    def __post_init__(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
