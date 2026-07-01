"""Generate funny Hindi scripts for Oggy & Jack news discussions using FREE AI APIs."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests

from news_hub.config.settings import settings

if TYPE_CHECKING:
    from news_hub.pipeline.news_fetcher import NewsStory

logger = logging.getLogger(__name__)

# ─── FREE AI API Configuration ────────────────────────────────────────

# Groq API - FREE tier (30,000 tokens/day)
# Alternative: Use Ollama (local) - completely free
# Alternative: Use Hugging Face Inference - free but slower

# Groq models that support Hindi well
GROQ_MODELS = {
    "fast": "llama-3.1-8b-instant",
    "smart": "mixtral-8x7b-instruct",
}

# Hugging Face free inference (slower, but works)
HF_MODELS = {
    "default": "mistralai/Mistral-7B-Instruct-v0.2",
    "hindi": "ai4bharat/Hin-7B-Instruct",  # Hindi-specific model
}


class ScriptGenerator:
    """Generates scripts for Oggy & Jack news discussions using FREE AI."""

    def __init__(self, use_groq: bool | None = None) -> None:
        """Initialize script generator.
        
        Args:
            use_groq: If True, uses Groq API. If False, uses Ollama. If None, auto-detect from settings.
        """
        # Auto-detect from settings if not specified
        if use_groq is None:
            use_groq = not settings.use_ollama
        
        self.use_groq = use_groq
        
        # Check which free API is configured
        self.groq_configured = bool(settings.groq_api_key) if use_groq else False
        self.ollama_configured = use_groq is False or settings.use_ollama
        
        if use_groq and not self.groq_configured:
            logger.warning("GROQ_API_KEY not configured, falling back to local Ollama")
            self.use_groq = False
            self.ollama_configured = True
        
        if not (self.groq_configured or self.ollama_configured):
            raise ValueError(
                "No free AI API configured. "
                "Either set GROQ_API_KEY in .env OR install Ollama locally (https://ollama.ai) "
                "and set USE_OLLAMA=true in .env"
            )

    def _generate_with_groq(self, prompt: str, system_prompt: str = "") -> str:
        """Generate script using Groq's FREE API."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": GROQ_MODELS["fast"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 2000,
            "stream": False,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            script = result["choices"][0]["message"]["content"]
            
            logger.info("Generated script via Groq API")
            return script
            
        except Exception as e:
            logger.error("Groq API failed: %s", e)
            raise

    def _generate_with_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Generate script using local Ollama (completely free)."""
        import subprocess
        
        # Use Llama 3 or Mixtral via Ollama
        model = "llama3:8b-instruct"  # or "mixtral:8x7b-instruct"
        
        full_prompt = f"""<|im_start|>system
{system_prompt}
<|im_end|>
<|im_start|>user
{prompt}
<|im_end|>
<|im_start|>assistant
"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", model, full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                raise Exception(f"Ollama failed: {result.stderr}")
            
            script = result.stdout.strip()
            logger.info("Generated script via local Ollama")
            return script
            
        except FileNotFoundError:
            raise ValueError("Ollama not installed. Install from https://ollama.ai")
        except Exception as e:
            logger.error("Ollama generation failed: %s", e)
            raise

    def _generate_script_text(self, story_text: str, location: str) -> str:
        """Generate script using configured free AI method."""
        system_prompt = """Tu ek comedian script writer hai. Teri task hai ki Oggy aur Jack ke liye Hindi mein news par funny dialogue script generate karna hai.

Character Details:
- Oggy: Mota aalasu blue cat, har waqt sohne ko taiyaar, asaani se gusse ho jaata hai, naive, cockroaches se har baar dhoka khata hai. Voice: deep, slow, lazy.
- Jack: Chatur green cockroach, har waqt shararat sochta hai, sarcastic, Oggy ko tang karne mein maza aata hai. Voice: fast, clever, mischievous.

Script Requirements:
1. PURE HINDI language only - no English
2. Based on the news story provided
3. 8-12 dialogue lines total (45-60 seconds duration)
4. Entertaining, viral-worthy, funny
5. Reflect Oggy and Jack's personalities accurately
6. End with a punchline or twist
7. Format EXACTLY as shown below:

---SCRIPT START---
[SCENE: LOCATION_NAME]
Oggy: [dialogue line 1]
Jack: [dialogue line 2]
Oggy: [dialogue line 3]
Jack: [dialogue line 4]
...
---SCRIPT END---

IMPORTANT: Use the location name in the SCENE marker. Only output the script, nothing else."""

        user_prompt = f"""News Story:
{story_text}

Location for scene: {location}

Generate the script now following all requirements above."""
        
        if self.groq_configured:
            return self._generate_with_groq(user_prompt, system_prompt)
        else:
            return self._generate_with_ollama(user_prompt, system_prompt)

    def _format_story_for_prompt(self, story: NewsStory) -> str:
        """Format a news story for the AI prompt."""
        return (
            f"Title: {story.title}\n"
            f"Summary: {story.summary}\n"
            f"Category: {story.category}\n"
            f"Source: {story.source}\n"
            "---"
        )

    def generate_script(self, story: NewsStory, location: str) -> str:
        """Generate a script for a single news story.
        
        Args:
            story: News story to base the script on
            location: Background location name for scene setting
            
        Returns:
            Formatted script with Oggy and Jack dialogue
        """
        # Build the prompt with the story
        story_text = self._format_story_for_prompt(story)
        
        try:
            # Generate using free AI
            script = self._generate_script_text(story_text, location)
            
            # Clean up the response to extract just the script
            script = self._clean_script(script, location)
            
            logger.info("Generated script for story: %s", story.title[:50])
            return script
            
        except Exception as e:
            logger.error("Failed to generate script for %s: %s", story.title, e)
            # Return a fallback script
            return self._generate_fallback_script(story, location)

    def _clean_script(self, script: str, location: str) -> str:
        """Clean the AI response to extract just the script."""
        # Look for the script markers
        start_marker = "---SCRIPT START---"
        end_marker = "---SCRIPT END---"
        
        start_idx = script.find(start_marker)
        end_idx = script.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            # Extract between markers
            script = script[start_idx:end_idx + len(end_marker)]
        else:
            # Try to find any script-like content
            lines = script.split('\n')
            cleaned_lines = []
            in_script = False
            for line in lines:
                line = line.strip()
                if line.startswith("Oggy:") or line.startswith("Jack:"):
                    in_script = True
                    cleaned_lines.append(line)
                elif line.startswith("[SCENE:") or line.startswith("---SCRIPT"):
                    cleaned_lines.append(line)
                elif in_script and line and not line.startswith("```"):
                    # Check if it's a character line
                    if ":" in line and ("Oggy" in line or "Jack" in line):
                        cleaned_lines.append(line)
            
            if cleaned_lines:
                script = "\n".join(cleaned_lines)
            else:
                # If all else fails, return as-is
                pass
        
        return script

    def _generate_fallback_script(self, story: NewsStory, location: str) -> str:
        """Generate a fallback script if AI fails."""
        logger.warning("Using fallback script for: %s", story.title)
        
        # Simple fallback based on category
        category_greetings = {
            "politics": {
                "oggy": "Arre yaar, yeh politics wale phir se kya kar rahe hain?",
                "jack": "Oggy, tu toh ab bhi soh raha hai! Desh ka kya hoga?"
            },
            "tech": {
                "oggy": "Sun Jack, AI ne phir se koi new gadget nikal diya hai!",
                "jack": "Haan Oggy, lekin tu use kar bhi nahin payega!"
            },
            "sports": {
                "oggy": "Jack, dekh India ne phir se jeet liya!",
                "jack": "Arre Oggy, tu toh match dekhne ki jagah soh raha tha!"
            },
            "entertainment": {
                "oggy": "Yaar Jack, Bollywood mein phir naya drama hai!",
                "jack": "Oggy, tu toh movie dekhne ki jagah samosa khane mein busy rehta hai!"
            },
            "business": {
                "oggy": "Jack, share market mein phir utar chadhao hai!",
                "jack": "Oggy, tu toh paise kamane ki jagah paise kharch karne mein expert hai!"
            }
        }
        
        category = story.category if story.category in category_greetings else "general"
        greetings = category_greetings.get(category, category_greetings["politics"])
        
        return f"""---SCRIPT START---
[SCENE: {location}]
Oggy: {greetings['oggy']}
Jack: {greetings['jack']}
Oggy: "{story.title[:40]}..." Ye toh bilkul unexpected hai!
Jack: Haan Oggy, par tu toh ab bhi samajh nahin paya hoga!
Oggy: Arre mat chhed, main toh bas itna jaanta hoon ki India great hai!
Jack: *haha* Achha Oggy, ab soh le, main toh chalta hoon shararat karne!
---SCRIPT END---"""


def generate_scripts_for_stories(stories: list[NewsStory]) -> list[str]:
    """Generate scripts for multiple news stories.
    
    Args:
        stories: List of news stories
        
    Returns:
        List of generated scripts
    """
    from news_hub.config.characters import LOCATIONS
    import random
    
    generator = ScriptGenerator()
    scripts = []
    
    # Select random locations for each story
    locations = random.sample(LOCATIONS, len(stories))
    
    for story, location in zip(stories, locations):
        script = generator.generate_script(story, location)
        scripts.append(script)
    
    return scripts
