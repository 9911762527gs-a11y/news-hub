"""Character definitions for Bittu the blue cat and Chhotu the green bug."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Character:
    name: str
    species: str
    color: str
    personality: str
    voice_name: str  # edge-tts voice identifier
    voice_rate: str  # edge-tts rate adjustment
    image_prompt: str  # for image generation


OGGY = Character(
    name="Oggy",
    species="cat",
    color="bright blue",
    personality="lazy, chubby, easily angered, loves sleeping, naive but kind-hearted, always gets fooled by cockroaches",
    voice_name="hi-IN-MadhurNeural",  # male Hindi voice - deep and slightly lazy
    voice_rate="-10%",  # slower for Oggy's lazy personality
    image_prompt=(
        "A chubby bright blue cartoon cat, round body, sleepy half-closed eyes, "
        "small ears, short stubby legs, wearing white boxers with blue polka dots, "
        "simple cartoon style matching Oggy and the Cockroaches, "
        "solid color with minimal shading, 2D flat design, white outline, "
        "transparent background, PNG, high resolution"
    ),
)

JACK = Character(
    name="Jack",
    species="cockroach",
    color="bright green",
    personality="cunning, intelligent, mischievous leader, always planning trouble, sarcastic, loves causing chaos",
    voice_name="hi-IN-SwaraNeural",  # female Hindi voice (higher pitch for cockroach)
    voice_rate="+15%",  # faster for Jack's quick thinking
    image_prompt=(
        "A tall thin bright green cartoon cockroach, oval body, sharp clever eyes, "
        "long antennae, wearing red shirt and black pants, "
        "simple cartoon style matching Oggy and the Cockroaches, "
        "solid color with minimal shading, 2D flat design, white outline, "
        "transparent background, PNG, high resolution"
    ),
)

# Pose variations used for animation states
POSES = ("idle", "talking", "surprised", "laughing", "angry", "thinking", "scheming")

# Location backgrounds for slideshow — Indian landmarks + daily life
LOCATIONS = [
    "India Gate Delhi wide angle golden hour",
    "Gateway of India Mumbai with boats",
    "Marine Drive Mumbai sunset promenade",
    "Varanasi Ghats at sunrise with boats",
    "Jaipur Hawa Mahal pink city",
    "Kerala backwaters houseboat green",
    "Goa beach palm trees sunny",
    "Mysore Palace illuminated at night",
    "Chandni Chowk Old Delhi busy street",
    "Ladakh mountains Pangong Lake blue",
    "Kolkata Howrah Bridge at dusk",
    "Amritsar Golden Temple reflecting pool",
    "Jaisalmer Desert sand dunes sunset",
    "Bangalore MG Road lively evening",
    "Chennai Marina Beach morning crowd",
    "Taj Mahal Agra golden sunset",
    "Red Fort Delhi historic monument",
    "Mumbai local train crowded station",
]

# Location prompt template — ensures consistent style
LOCATION_PROMPT_TEMPLATE = (
    "{location_description}, vibrant colors, "
    "cartoon illustrated style matching Oggy and the Cockroaches, 9:16 vertical format, "
    "slightly blurred background bokeh effect, bright and cheerful, "
    "no text, no people close-up, wide establishing shot"
)

CHARACTERS = {"oggy": OGGY, "jack": JACK}
