"""Tests for video generator module."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from news_hub.pipeline.video_generator import VideoGenerator, DialogueLine


class TestVideoGenerator(unittest.TestCase):
    """Test cases for video generator."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a temporary directory for test assets
        self.temp_dir = Path(tempfile.mkdtemp())
        self.assets_dir = self.temp_dir / "assets"
        self.assets_dir.mkdir()
        
        # Patch settings
        self.patcher = patch("news_hub.pipeline.video_generator.settings")
        self.mock_settings = MagicMock()
        self.mock_settings.assets_dir = self.assets_dir
        self.mock_settings.backgrounds_dir = self.assets_dir / "backgrounds"
        self.mock_settings.characters_dir = self.assets_dir / "characters"
        self.mock_settings.output_dir = self.assets_dir / "output"
        self.patcher.start()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        self.patcher.stop()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_script(self) -> None:
        """Test script parsing."""
        generator = VideoGenerator()
        
        script = """---SCRIPT START---
[SCENE: India Gate Delhi]
Oggy: Hello Jack!
Jack: Hi Oggy, what's up?
Oggy: Just discussing the news
Jack: Interesting!
---SCRIPT END---"""
        
        location, lines = generator.parse_script(script)
        
        self.assertEqual(location, "India Gate Delhi")
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0].character, "oggy")
        self.assertEqual(lines[0].text, "Hello Jack!")
        self.assertEqual(lines[1].character, "jack")
        self.assertEqual(lines[1].text, "Hi Oggy, what's up?")

    def test_parse_script_no_scene(self) -> None:
        """Test script parsing without scene marker."""
        generator = VideoGenerator()
        
        script = "Oggy: Hello\nJack: Hi"
        
        location, lines = generator.parse_script(script)
        
        self.assertEqual(location, "Delhi")  # Default
        self.assertEqual(len(lines), 2)

    def test_placeholder_character_creation(self) -> None:
        """Test placeholder character image creation."""
        generator = VideoGenerator()
        
        char_dir = self.assets_dir / "characters" / "oggy"
        char_dir.mkdir(parents=True)
        
        image_path = generator._create_placeholder_character("oggy", char_dir)
        
        self.assertTrue(image_path.exists())
        self.assertTrue(image_path.name == "talking.png")

    def test_placeholder_background_creation(self) -> None:
        """Test placeholder background creation."""
        generator = VideoGenerator()
        
        bg_dir = self.assets_dir / "backgrounds"
        bg_dir.mkdir(parents=True)
        
        bg_path = bg_dir / "test_location.jpg"
        image_path = generator._create_placeholder_background("Test Location", bg_path)
        
        self.assertTrue(image_path.exists())

    def test_dialogue_line_creation(self) -> None:
        """Test DialogueLine dataclass."""
        line = DialogueLine(
            character="oggy",
            text="Test dialogue",
            duration=5.0
        )
        
        self.assertEqual(line.character, "oggy")
        self.assertEqual(line.text, "Test dialogue")
        self.assertEqual(line.duration, 5.0)


if __name__ == "__main__":
    unittest.main()
