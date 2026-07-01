"""Upload reels to social media platforms using FREE methods.

This module uses:
- YouTube Data API (free tier: 10,000 units/day)
- Twitter/X via Tweepy OAuth 1.0a (legacy free access)
- Instagram via Instaloader (unofficial, free)
- Facebook via Graph API (free with business verification)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import instaloader
import requests
import tweepy
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from news_hub.config.settings import settings

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# Platform names
PLATFORM_YOUTUBE = "youtube"
PLATFORM_X = "x"
PLATFORM_INSTAGRAM = "instagram"
PLATFORM_FACEBOOK = "facebook"

# Hashtags for Indian news
INDIAN_NEWS_HASHTAGS = [
    "#IndiaNews", "#NewsHub", "#OggyAndJack", "#DailyNews",
    "#BreakingNews", "#IndianNews", "#ViralNews", "#NewsUpdate",
    "#Trending", "#India",
]


@dataclass
class UploadResult:
    """Result of a social media upload."""
    platform: str
    success: bool
    video_path: Path
    url: str | None = None
    error: str | None = None
    post_id: str | None = None


class SocialUploader:
    """Handles uploading videos to all configured social platforms using FREE methods."""

    def __init__(self) -> None:
        self.youtube_configured = settings.youtube_configured
        self.x_configured = settings.x_configured
        self.instagram_configured = self._check_instagram_configured()
        self.facebook_configured = settings.facebook_configured

    def _check_instagram_configured(self) -> bool:
        """Check if Instagram upload is possible."""
        return bool(settings.ig_username and settings.ig_password)

    def generate_caption(self, news_story_title: str, category: str = "general") -> str:
        """Generate caption with hashtags."""
        base_caption = (
            f"Oggy & Jack Discuss: {news_story_title[:100]}\n\n"
            f"Latest Indian News | Daily Updates | News Hub\n\n"
        )
        hashtags = " ".join(INDIAN_NEWS_HASHTAGS[:8])
        category_hashtags = {
            "politics": "#Politics #Modi #BJP #Congress",
            "tech": "#Technology #AI #Startup #IndiaTech",
            "sports": "#Sports #Cricket #IPL #IndiaSports",
            "entertainment": "#Bollywood #Movies #OTT #Entertainment",
            "business": "#Business #StockMarket #Economy #IndiaBiz",
        }
        extra = category_hashtags.get(category, "#India")
        return f"{base_caption}{hashtags} {extra}"

    def upload_to_youtube(self, video_path: Path, title: str, description: str) -> UploadResult:
        """Upload to YouTube using FREE API tier (10,000 units/day)."""
        if not self.youtube_configured:
            return UploadResult(PLATFORM_YOUTUBE, False, video_path, error="YouTube not configured")
        
        try:
            credentials = Credentials(
                token=settings.youtube_access_token,
                refresh_token=settings.youtube_refresh_token,
                client_id=settings.youtube_client_id,
                client_secret=settings.youtube_client_secret,
                token_uri="https://oauth2.googleapis.com/token",
            )
            youtube = build("youtube", "v3", credentials=credentials)
            request_body = {
                "snippet": {"title": title[:100], "description": description[:5000],
                           "tags": ["India News", "Oggy and Jack", "News Hub"], "categoryId": "22"},
                "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
            }
            media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
            response = youtube.videos().insert(
                part=",".join(request_body.keys()), body=request_body, media_body=media
            ).execute()
            video_url = f"https://www.youtube.com/watch?v={response['id']}"
            logger.info("Uploaded to YouTube: %s", video_url)
            return UploadResult(PLATFORM_YOUTUBE, True, video_path, url=video_url, post_id=response["id"])
        except Exception as e:
            return UploadResult(PLATFORM_YOUTUBE, False, video_path, error=str(e))

    def upload_to_x(self, video_path: Path, caption: str) -> UploadResult:
        """Upload to X/Twitter using FREE OAuth 1.0a."""
        if not self.x_configured:
            return UploadResult(PLATFORM_X, False, video_path, error="X/Twitter not configured")
        
        try:
            auth = tweepy.OAuth1UserHandler(
                settings.x_api_key, settings.x_api_secret,
                settings.x_access_token, settings.x_access_token_secret
            )
            api = tweepy.API(auth)
            media = api.media_upload(str(video_path))
            tweet = api.update_status(status=caption[:280], media_ids=[media.media_id])
            tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            logger.info("Uploaded to X/Twitter: %s", tweet_url)
            return UploadResult(PLATFORM_X, True, video_path, url=tweet_url, post_id=str(tweet.id))
        except Exception as e:
            return UploadResult(PLATFORM_X, False, video_path, error=str(e))

    def upload_to_instagram(self, video_path: Path, caption: str) -> UploadResult:
        """Upload to Instagram using FREE Instaloader."""
        if not self.instagram_configured:
            return UploadResult(PLATFORM_INSTAGRAM, False, video_path,
                                 error="Instagram not configured. Add IG_USERNAME and IG_PASSWORD")
        
        try:
            L = instaloader.Instaloader(user=settings.ig_username, passwd=settings.ig_password)
            L.login(L.context.username)
            L.upload_video(str(video_path), caption)
            logger.info("Uploaded to Instagram via Instaloader")
            return UploadResult(PLATFORM_INSTAGRAM, True, video_path)
        except Exception as e:
            return UploadResult(PLATFORM_INSTAGRAM, False, video_path, error=str(e))

    def upload_to_facebook(self, video_path: Path, caption: str) -> UploadResult:
        """Upload to Facebook using FREE Graph API."""
        if not self.facebook_configured:
            return UploadResult(PLATFORM_FACEBOOK, False, video_path,
                                 error="Facebook not configured. Add FB_PAGE_ID and FB_ACCESS_TOKEN")
        
        try:
            url = f"https://graph-video.facebook.com/v19.0/{settings.fb_page_id}/videos"
            with open(video_path, "rb") as f:
                files = {"video_file_chunk": f}
                data = {"description": caption[:63206], "access_token": settings.fb_access_token,
                       "title": caption[:100], "published": "true"}
                response = requests.post(url, files=files, data=data, timeout=120)
                response.raise_for_status()
            video_id = response.json().get("id")
            video_url = f"https://www.facebook.com/{settings.fb_page_id}/videos/{video_id}"
            logger.info("Uploaded to Facebook: %s", video_url)
            return UploadResult(PLATFORM_FACEBOOK, True, video_path, url=video_url, post_id=video_id)
        except Exception as e:
            return UploadResult(PLATFORM_FACEBOOK, False, video_path, error=str(e))

    def upload_to_all(self, video_path: Path, news_title: str, category: str = "general") -> list[UploadResult]:
        """Upload to all configured platforms."""
        caption = self.generate_caption(news_title, category)
        title = f"Oggy & Jack News: {news_title[:60]}"
        description = f"Oggy & Jack discuss: {news_title}\n\nWatch daily news updates!\n"
        
        results = []
        if self.youtube_configured:
            results.append(self.upload_to_youtube(video_path, title, description))
        if self.x_configured:
            results.append(self.upload_to_x(video_path, caption))
        if self.instagram_configured:
            results.append(self.upload_to_instagram(video_path, caption))
        if self.facebook_configured:
            results.append(self.upload_to_facebook(video_path, caption))
        return results


def upload_reels(reels: list[Path], news_titles: list[str], categories: list[str]) -> list[list[UploadResult]]:
    """Upload multiple reels."""
    uploader = SocialUploader()
    return [uploader.upload_to_all(reel, title, cat) for reel, title, cat in zip(reels, news_titles, categories)]
