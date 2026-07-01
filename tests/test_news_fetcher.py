"""Tests for news fetcher module."""

import unittest
from unittest.mock import patch, MagicMock

from news_hub.pipeline.news_fetcher import NewsStory, fetch_stories, get_top_stories, _guess_category


class TestNewsFetcher(unittest.TestCase):
    """Test cases for news fetcher."""

    def test_guess_category_politics(self) -> None:
        """Test category guessing for politics."""
        text = "Modi meets with BJP leaders in Parliament"
        category = _guess_category(text)
        self.assertEqual(category, "politics")

    def test_guess_category_tech(self) -> None:
        """Test category guessing for tech."""
        text = "New AI startup launches in India"
        category = _guess_category(text)
        self.assertEqual(category, "tech")

    def test_guess_category_sports(self) -> None:
        """Test category guessing for sports."""
        text = "India wins cricket match against Australia"
        category = _guess_category(text)
        self.assertEqual(category, "sports")

    def test_guess_category_entertainment(self) -> None:
        """Test category guessing for entertainment."""
        text = "Bollywood movie breaks box office records"
        category = _guess_category(text)
        self.assertEqual(category, "entertainment")

    def test_guess_category_business(self) -> None:
        """Test category guessing for business."""
        text = "Stock market reaches new high"
        category = _guess_category(text)
        self.assertEqual(category, "business")

    def test_guess_category_general(self) -> None:
        """Test category guessing returns general for unknown."""
        text = "Some random news story"
        category = _guess_category(text)
        self.assertEqual(category, "general")

    def test_news_story_uid(self) -> None:
        """Test NewsStory generates UID."""
        story = NewsStory(
            title="Test Story",
            summary="Test summary",
            source="test_source",
            url="http://test.com"
        )
        self.assertIsNotNone(story.uid)
        self.assertEqual(len(story.uid), 12)

    @patch("news_hub.pipeline.news_fetcher.requests.get")
    @patch("news_hub.pipeline.news_fetcher.feedparser.parse")
    def test_fetch_rss_success(self, mock_parse, mock_get) -> None:
        """Test successful RSS fetch."""
        # Mock response
        mock_resp = MagicMock()
        mock_resp.content = b"<rss><channel><item><title>Test</title></item></channel></rss>"
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp
        
        # Mock parsed feed
        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda key, default=None: {
            "title": "Test Title",
            "summary": "Test Summary",
            "link": "http://test.com"
        }.get(key, default)
        
        mock_parsed = MagicMock()
        mock_parsed.entries = [mock_entry]
        mock_parse.return_value = mock_parsed
        
        from news_hub.pipeline.news_fetcher import _fetch_rss
        stories = _fetch_rss("http://test.com", "test_source", max_items=1)
        
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].title, "Test Title")

    @patch("news_hub.pipeline.news_fetcher.requests.get")
    def test_fetch_rss_failure(self, mock_get) -> None:
        """Test RSS fetch failure handling."""
        mock_get.side_effect = Exception("Network error")
        
        from news_hub.pipeline.news_fetcher import _fetch_rss
        stories = _fetch_rss("http://test.com", "test_source")
        
        self.assertEqual(stories, [])


if __name__ == "__main__":
    unittest.main()
