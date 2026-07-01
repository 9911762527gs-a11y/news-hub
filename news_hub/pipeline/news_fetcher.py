"""Fetch top Indian news stories from free RSS / API sources."""

from __future__ import annotations

import dataclasses
import hashlib
import logging
import random
import time
from typing import Any

import feedparser
import requests

from news_hub.config.settings import settings

logger = logging.getLogger(__name__)

# ─── RSS Feed URLs for Indian news ───────────────────────────────────
RSS_FEEDS: dict[str, str] = {
    "google_news": "https://news.google.com/rss/search?q=india+news&hl=en-IN&gl=IN&ceid=IN:en",
    "google_news_hindi": "https://news.google.com/rss/search?q=india+news&hl=hi&gl=IN&ceid=IN:hi",
    "ndtv": "https://feeds.feedburner.com/ndtvnews-topstories",
    "the_hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "indian_express": "https://indianexpress.com/feed/",
    "times_of_india": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "bbc_india": "https://feeds.bbci.co.uk/news/world/south_asia/rss.xml",
}

# Categories we track (used for hashtag generation)
CATEGORIES = ("politics", "tech", "sports", "entertainment", "business", "crime", "weather", "viral")


@dataclasses.dataclass(frozen=True)
class NewsStory:
    """A single news story ready for script generation."""

    title: str
    summary: str
    source: str
    url: str
    category: str = "general"
    uid: str = ""

    def __post_init__(self) -> None:
        if not self.uid:
            uid = hashlib.sha256(f"{self.source}:{self.title}".encode()).hexdigest()[:12]
            object.__setattr__(self, "uid", uid)


def _fetch_rss(feed_url: str, source_name: str, max_items: int = 10) -> list[NewsStory]:
    """Parse an RSS feed and return NewsStory objects."""
    try:
        resp = requests.get(feed_url, timeout=15, headers={"User-Agent": "NewsHub/1.0"})
        resp.raise_for_status()
    except requests.RequestException:
        logger.warning("Failed to fetch %s from %s", source_name, feed_url)
        return []

    parsed = feedparser.parse(resp.content)
    stories: list[NewsStory] = []
    for entry in parsed.entries[:max_items]:
        title = entry.get("title", "").strip()
        summary = entry.get("summary", entry.get("description", "")).strip()
        # Strip HTML tags from summary
        summary = _strip_html(summary)
        if not title:
            continue
        stories.append(
            NewsStory(
                title=title,
                summary=summary[:500],  # cap length
                source=source_name,
                url=entry.get("link", ""),
                category=_guess_category(title + " " + summary),
            )
        )
    return stories


def _strip_html(text: str) -> str:
    """Remove basic HTML tags from feed content."""
    import re

    return re.sub(r"<[^>]+>", "", text).strip()


def _guess_category(text: str) -> str:
    """Simple keyword-based category guesser."""
    text_lower = text.lower()
    keywords: dict[str, list[str]] = {
        "politics": ["modi", "bjp", "congress", "parliament", "election", "lok sabha", "rajya sabha", "minister", "government", "policy", "bill"],
        "tech": ["ai", "startup", "tech", "software", "app", "phone", "chip", "digital", "cyber", "computer", "internet"],
        "sports": ["cricket", "ipl", "football", "olympics", "hockey", "match", "win", "tournament", "world cup", "test match", "virat", "dhoni"],
        "entertainment": ["bollywood", "film", "movie", "actor", "actress", "song", "release", "ott", "series", "box office"],
        "business": ["market", "stock", "economy", "gdp", "rupee", "inflation", "budget", "tax", "richest", "billionaire", "ipo"],
        "crime": ["murder", "arrest", "fire", "accident", "scam", "fraud", "police", "court", "probe", "justice"],
        "weather": ["rain", "flood", "heatwave", "cyclone", "monsoon", "temperature", "weather", "storm"],
        "viral": ["viral", "trending", "meme", "video", "twitter", "social media", "reddit"],
    }
    for category, words in keywords.items():
        if any(w in text_lower for w in words):
            return category
    return "general"


def fetch_stories(max_per_source: int = 5, max_total: int = 15) -> list[NewsStory]:
    """Fetch stories from all configured sources, deduplicate, and return top stories."""
    all_stories: list[NewsStory] = []
    seen_titles: set[str] = set()

    sources = settings.news_sources
    for source_key in sources:
        feed_url = RSS_FEEDS.get(source_key)
        if not feed_url:
            logger.debug("Unknown source: %s, skipping", source_key)
            continue
        stories = _fetch_rss(feed_url, source_key, max_items=max_per_source)
        for s in stories:
            normalized = s.title.lower().strip()
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                all_stories.append(s)
        time.sleep(0.5)  # be polite between requests

    # Shuffle then sort by recency proxy (just shuffle for variety)
    random.shuffle(all_stories)
    return all_stories[:max_total]


def get_top_stories(count: int = 3) -> list[NewsStory]:
    """Get exactly `count` diverse top stories for today's reels.

    Tries to pick from different categories so we don't get 3 political stories.
    """
    stories = fetch_stories(max_total=30)
    if not stories:
        logger.error("No stories fetched from any source!")
        return []

    # Pick diverse categories
    picked: list[NewsStory] = []
    used_categories: set[str] = set()

    for story in stories:
        if len(picked) >= count:
            break
        # Prefer stories from new categories, but fill remaining slots from any
        if story.category not in used_categories or len(picked) >= len(used_categories):
            picked.append(story)
            used_categories.add(story.category)

    return picked[:count]
