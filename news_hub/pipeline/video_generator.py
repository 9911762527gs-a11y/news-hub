"""Generate video reels from scripts with Oggy & Jack characters and Indian location backgrounds."""

from __future__ import annotations

import logging
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import edge_tts
import numpy as np
from moviepy import (
    AudioClip,
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_audioclips,
    concatenate_videoclips,
)


from news_hub.config.characters import CHARACTERS, LOCATION_PROMPT_TEMPLATE
from news_hub.config.settings import settings

if TYPE_CHECKING:
    from news_hub.pipeline.script_generator import ScriptGenerator

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────

# Video settings for reels (9:16 vertical)
REEL_WIDTH = 1080
REEL_HEIGHT = 1920
REEL_FPS = 30
REEL_DURATION_PER_LINE = 4.5  # seconds per dialogue line

# Character positions (left and right for conversation)
# Convert percentages to actual pixel positions for moviepy 2.x compatibility
OGGY_POSITION = (int(REEL_WIDTH * 0.20), int(REEL_HEIGHT * 0.60))  # Left side
JACK_POSITION = (int(REEL_WIDTH * 0.70), int(REEL_HEIGHT * 0.60))  # Right side

# Font settings
FONT_PATH = settings.assets_dir / "fonts" / "Hindi-Font.ttf"
TEXT_FONT_SIZE = 70
TEXT_COLOR = "white"
TEXT_BG_COLOR = (0, 0, 0, 179)  # RGBA: black with 70% opacity
TEXT_POSITION = ("center", int(REEL_HEIGHT * 0.85))


@dataclass
class DialogueLine:
    """A single line of dialogue with character and text."""

    character: str
    text: str
    duration: float


@dataclass
class Scene:
    """A video scene with background, characters, and dialogue."""

    background_path: Path
    lines: list[DialogueLine]
    location_name: str


class VideoGenerator:
    """Generates video reels from Oggy & Jack scripts."""

    def __init__(self) -> None:
        self.characters = CHARACTERS
        self.assets_dir = settings.assets_dir
        self.backgrounds_dir = settings.backgrounds_dir
        self.characters_dir = settings.characters_dir
        
        # Ensure directories exist
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.backgrounds_dir.mkdir(parents=True, exist_ok=True)
        self.characters_dir.mkdir(parents=True, exist_ok=True)

    def parse_script(self, script: str) -> tuple[str, list[DialogueLine]]:
        """Parse a script into location and dialogue lines.
        
        Args:
            script: Raw script text
            
        Returns:
            Tuple of (location, list of DialogueLine)
        """
        location = "Delhi"
        lines: list[DialogueLine] = []
        
        # Extract location from scene marker
        scene_match = re.search(r"\[SCENE:\s*([^\]]+)\]", script)
        if scene_match:
            location = scene_match.group(1)
        
        # Parse dialogue lines
        dialogue_pattern = r"(Oggy|Jack):\s*(\[.*?\]\s*)?(.+)"
        
        for match in re.finditer(dialogue_pattern, script):
            character = match.group(1).lower()
            text = match.group(3).strip()
            
            # Clean up the text
            text = re.sub(r'[""\']', '', text)
            text = text.replace("*", "").strip()
            
            if text:
                lines.append(DialogueLine(
                    character=character,
                    text=text,
                    duration=REEL_DURATION_PER_LINE
                ))
        
        return location, lines

    def get_character_image_path(self, character_name: str, pose: str = "talking") -> Path:
        """Get or create character image path."""
        char_dir = self.characters_dir / character_name
        char_dir.mkdir(parents=True, exist_ok=True)
        
        # For now, we'll use placeholder paths
        # In production, you'd generate or download actual images
        image_path = char_dir / f"{pose}.png"
        
        if not image_path.exists():
            # Create a placeholder image
            logger.warning("Character image not found: %s, using placeholder", image_path)
            # We'll create a colored circle as placeholder
            return self._create_placeholder_character(character_name, char_dir)
        
        return image_path

    def _create_placeholder_character(self, character_name: str, char_dir: Path) -> Path:
        """Create a simple placeholder image for a character."""
        from PIL import Image, ImageDraw
        
        char = self.characters[character_name]
        color = char.color
        
        # Map color names to RGB
        color_map = {
            "bright blue": (0, 150, 255),
            "bright green": (0, 255, 0),
            "blue": (0, 150, 255),
            "green": (0, 255, 0),
        }
        
        rgb = color_map.get(color, (200, 200, 200))
        
        # Create a circular character image
        image_path = char_dir / "talking.png"
        img = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw circle
        draw.ellipse((50, 50, 462, 462), fill=rgb + (255,))
        
        # Draw eyes
        draw.ellipse((150, 150, 200, 200), fill=(255, 255, 255, 255))
        draw.ellipse((312, 150, 362, 200), fill=(255, 255, 255, 255))
        draw.ellipse((170, 170, 190, 190), fill=(0, 0, 0, 255))
        draw.ellipse((332, 170, 352, 190), fill=(0, 0, 0, 255))
        
        # Draw mouth (smile)
        draw.arc((180, 250, 332, 300), start=0, end=180, fill=(0, 0, 0, 255), width=5)
        
        img.save(image_path)
        return image_path

    def get_background_image_path(self, location: str) -> Path:
        """Get or create background image for a location."""
        # Create a safe filename from location
        safe_name = re.sub(r'[^\w\s-]', '', location).strip().replace(' ', '_')
        background_path = self.backgrounds_dir / f"{safe_name}.jpg"
        
        if not background_path.exists():
            # Create a placeholder background
            logger.warning("Background not found: %s, using placeholder", background_path)
            return self._create_placeholder_background(location, background_path)
        
        return background_path

    def _create_placeholder_background(self, location: str, path: Path) -> Path:
        """Create a simple gradient placeholder background."""
        from PIL import Image, ImageDraw
        
        # Create gradient background
        width, height = REEL_WIDTH, REEL_HEIGHT
        img = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create a simple gradient
        for y in range(height):
            color = tuple(int(c * (y / height)) for c in (135, 206, 235))  # Sky blue gradient
            draw.line((0, y, width, y), fill=color)
        
        # Add some text
        draw.text((width // 2 - 100, height // 2), location, fill=(255, 255, 255))
        
        img.save(path)
        return path

    def generate_tts_audio(self, text: str, character: str) -> str:
        """Generate TTS audio for a character's dialogue.
        
        Args:
            text: Text to speak
            character: Character name (oggy or jack)
            
        Returns:
            Path to generated audio file
        """
        char = self.characters[character]
        voice_name = char.voice_name
        voice_rate = char.voice_rate
        
        # Create a temp file for audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio_path = tmp.name
        
        try:
            # Use edge-tts to generate speech
            voice = voice_name
            
            # Handle rate adjustment
            rate = voice_rate.replace("%", "").replace("+", "").replace("-", "")
            if "-" in voice_rate:
                rate_adjustment = f"-{rate}%"
            elif "+" in voice_rate:
                rate_adjustment = f"+{rate}%"
            else:
                rate_adjustment = "0%"
            
            # Generate audio and save directly
            communicate = edge_tts.Communicate(text, voice, rate=rate_adjustment)
            communicate.save_sync(audio_path)
            
            logger.info("Generated TTS audio for %s: %s", character, text[:50])
            return audio_path
            
        except Exception as e:
            logger.error("Failed to generate TTS for %s: %s", text[:50], e)
            # Create silent audio as fallback
            return self._create_silent_audio(audio_path)

    def _create_silent_audio(self, path: str, duration: float = 1.0) -> str:
        """Create a silent audio file as fallback."""
        from moviepy import AudioClip
        
        silent = AudioClip(lambda t: np.zeros(int(duration * 44100)), 
                          fps=44100, duration=duration)
        silent.write_audiofile(path, codec="pcm_s16le")
        silent.close()
        return path

    def create_scene_video(
        self, 
        background_path: Path, 
        lines: list[DialogueLine],
        output_path: Path
    ) -> Path:
        """Create a video for a single scene with dialogue.
        
        Args:
            background_path: Path to background image
            lines: List of dialogue lines
            output_path: Where to save the video
            
        Returns:
            Path to generated video
        """
        # Load background
        background = ImageClip(str(background_path), duration=sum(l.duration for l in lines))
        background = background.resized((REEL_WIDTH, REEL_HEIGHT))
        
        # Create character clips
        oggy_img = ImageClip(str(self.get_character_image_path("oggy", "talking")))
        jack_img = ImageClip(str(self.get_character_image_path("jack", "talking")))
        
        # Resize characters
        char_size = (REEL_WIDTH // 3, REEL_WIDTH // 3)
        oggy_img = oggy_img.resized(char_size)
        jack_img = jack_img.resized(char_size)
        
        # Position characters
        oggy_img = oggy_img.with_position(OGGY_POSITION)
        jack_img = jack_img.with_position(JACK_POSITION)
        
        # Generate audio for all lines
        audio_clips = []
        text_clips = []
        
        current_time = 0.0
        
        for line in lines:
            # Generate TTS audio
            audio_path = self.generate_tts_audio(line.text, line.character)
            audio_clip = AudioFileClip(audio_path)
            
            # Set audio position
            audio_clip = audio_clip.with_start(current_time)
            audio_clips.append(audio_clip)
            
            # Create text clip
            text_kwargs = {
                "text": line.text,
                "font_size": TEXT_FONT_SIZE,
                "color": TEXT_COLOR,
                "bg_color": TEXT_BG_COLOR,
                "size": (int(REEL_WIDTH * 0.9), None),
                "method": "caption"
            }
            if FONT_PATH.exists():
                text_kwargs["font"] = str(FONT_PATH)
            
            text_clip = TextClip(**text_kwargs)
            text_clip = text_clip.with_position(TEXT_POSITION)
            text_clip = text_clip.with_start(current_time)
            text_clip = text_clip.with_duration(line.duration)
            text_clips.append(text_clip)
            
            current_time += line.duration
            
            # Clean up temp audio
            try:
                os.unlink(audio_path)
            except:
                pass
        
        # Combine all audio
        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips)
        else:
            final_audio = AudioClip(lambda t: np.zeros(int(current_time * 44100)), 
                                   fps=44100, duration=current_time)
        
        # Combine all video elements
        video_clips = [background, oggy_img.with_duration(current_time), 
                      jack_img.with_duration(current_time)] + text_clips
        
        final_video = CompositeVideoClip(video_clips, size=(REEL_WIDTH, REEL_HEIGHT))
        final_video = final_video.with_audio(final_audio)
        final_video = final_video.with_duration(current_time)
        
        # Write to file
        final_video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=REEL_FPS,
            threads=4,
            preset="ultrafast"
        )
        
        # Close clips
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass
        for clip in audio_clips:
            try:
                clip.close()
            except:
                pass
        
        logger.info("Created scene video: %s", output_path)
        return output_path

    def generate_reel(self, script: str, output_path: Path | None = None) -> Path:
        """Generate a complete reel from a script.
        
        Args:
            script: Full script text
            output_path: Optional output path (auto-generated if None)
            
        Returns:
            Path to generated reel video
        """
        # Parse script
        location, lines = self.parse_script(script)
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = settings.output_dir / f"reel_{timestamp}.mp4"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get background
        background_path = self.get_background_image_path(location)
        
        # Create scene video
        video_path = self.create_scene_video(background_path, lines, output_path)
        
        return video_path


def generate_reels_from_scripts(scripts: list[str]) -> list[Path]:
    """Generate reels from multiple scripts.
    
    Args:
        scripts: List of script texts
        
    Returns:
        List of generated video paths
    """
    generator = VideoGenerator()
    videos = []
    
    for i, script in enumerate(scripts):
        output_path = settings.output_dir / f"reel_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        video_path = generator.generate_reel(script, output_path)
        videos.append(video_path)
    
    return videos
