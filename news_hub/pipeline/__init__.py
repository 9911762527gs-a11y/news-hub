"""Pipeline modules for News Hub."""

from news_hub.pipeline.news_fetcher import fetch_stories, get_top_stories, NewsStory
from news_hub.pipeline.script_generator import ScriptGenerator, generate_scripts_for_stories
from news_hub.pipeline.video_generator import VideoGenerator, generate_reels_from_scripts
from news_hub.pipeline.social_uploader import SocialUploader, upload_reels, UploadResult

__all__ = [
    "fetch_stories",
    "get_top_stories",
    "NewsStory",
    "ScriptGenerator",
    "generate_scripts_for_stories",
    "VideoGenerator",
    "generate_reels_from_scripts",
    "SocialUploader",
    "upload_reels",
    "UploadResult",
]
