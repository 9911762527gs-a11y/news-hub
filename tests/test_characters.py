"""Tests for characters configuration."""

import unittest

from news_hub.config.characters import OGGY, JACK, CHARACTERS, LOCATIONS, POSES


class TestCharacters(unittest.TestCase):
    """Test cases for character definitions."""

    def test_oggy_character(self) -> None:
        """Test Oggy character definition."""
        self.assertEqual(OGGY.name, "Oggy")
        self.assertEqual(OGGY.species, "cat")
        self.assertEqual(OGGY.color, "bright blue")
        self.assertIn("lazy", OGGY.personality)
        self.assertIn("chubby", OGGY.personality)
        self.assertEqual(OGGY.voice_name, "hi-IN-MadhurNeural")
        self.assertEqual(OGGY.voice_rate, "-10%")
        self.assertIn("blue", OGGY.image_prompt)

    def test_jack_character(self) -> None:
        """Test Jack character definition."""
        self.assertEqual(JACK.name, "Jack")
        self.assertEqual(JACK.species, "cockroach")
        self.assertEqual(JACK.color, "bright green")
        self.assertIn("cunning", JACK.personality)
        self.assertIn("mischievous", JACK.personality)
        self.assertEqual(JACK.voice_name, "hi-IN-SwaraNeural")
        self.assertEqual(JACK.voice_rate, "+15%")
        self.assertIn("green", JACK.image_prompt)

    def test_characters_dict(self) -> None:
        """Test CHARACTERS dictionary."""
        self.assertIn("oggy", CHARACTERS)
        self.assertIn("jack", CHARACTERS)
        self.assertEqual(CHARACTERS["oggy"], OGGY)
        self.assertEqual(CHARACTERS["jack"], JACK)

    def test_poses(self) -> None:
        """Test pose variations."""
        self.assertIn("idle", POSES)
        self.assertIn("talking", POSES)
        self.assertIn("surprised", POSES)
        self.assertIn("laughing", POSES)
        self.assertIn("angry", POSES)
        self.assertIn("thinking", POSES)
        self.assertIn("scheming", POSES)

    def test_locations(self) -> None:
        """Test Indian locations list."""
        self.assertGreater(len(LOCATIONS), 15)
        self.assertIn("India Gate Delhi", LOCATIONS)
        self.assertIn("Taj Mahal Agra", LOCATIONS)
        self.assertIn("Marine Drive Mumbai", LOCATIONS)
        self.assertIn("Varanasi Ghats", LOCATIONS)

    def test_location_prompt_template(self) -> None:
        """Test location prompt template includes required elements."""
        from news_hub.config.characters import LOCATION_PROMPT_TEMPLATE
        
        template = LOCATION_PROMPT_TEMPLATE
        self.assertIn("{location_description}", template)
        self.assertIn("9:16", template)
        self.assertIn("vertical", template)
        self.assertIn("cartoon", template)


if __name__ == "__main__":
    unittest.main()
