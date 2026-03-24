"""Configuration for Video Generator"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Keys
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")  # For videos AND music
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
ASSETS_DIR = BASE_DIR / "assets"

# Create directories
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# Video Settings
VIDEO_SETTINGS = {
    "9:16": {"width": 1080, "height": 1920},  # TikTok/Reels/Shorts
    "16:9": {"width": 1920, "height": 1080},  # YouTube
    "1:1": {"width": 1080, "height": 1080},   # Instagram Feed
}

# Music Settings
MUSIC_SETTINGS = {
    "default_volume": 0.8,   # Music volume during silence (0.0-1.0)
    "duck_level": 0.2,       # Music volume when voice is present (0.0-1.0)
    "voice_volume": 1.0,     # Voice/narration volume (0.0-1.0)
    "fade_duration": 0.3,    # Fade in/out duration in seconds
    "default_mood": "calm",  # Default mood if not specified
}

# TTS Voices (Edge TTS)
VOICES = {
    "male_us": "en-US-GuyNeural",
    "female_us": "en-US-JennyNeural",
    "male_uk": "en-GB-RyanNeural", 
    "female_uk": "en-GB-SoniaNeural",
    "male_au": "en-AU-WilliamNeural",
    "female_au": "en-AU-NatashaNeural",
}

# Subtitle Styles
SUBTITLE_STYLES = {
    "bold": {
        "fontsize": 60,
        "color": "white",
        "stroke_color": "black",
        "stroke_width": 3,
        "font": "Arial-Bold",
        "position": ("center", 0.75),  # 75% from top
    },
    "minimal": {
        "fontsize": 45,
        "color": "white",
        "stroke_color": None,
        "stroke_width": 0,
        "font": "Arial",
        "position": ("center", 0.85),
    },
    "highlight": {
        "fontsize": 55,
        "color": "yellow",
        "stroke_color": "black",
        "stroke_width": 2,
        "font": "Arial-Bold",
        "position": ("center", 0.75),
    }
}

# LLM Settings
LLM_MODEL = "google/gemini-2.0-flash-001"  # Working model

# Stock Video Settings
STOCK_SETTINGS = {
    "cache_enabled": True,      # Cache search results to reduce API calls
    "use_placeholder": True,    # Create placeholder when no video found
    "max_concurrent": 3,        # Max concurrent downloads
    "fallback_queries": [       # Fallback queries when search fails
        "abstract background",
        "nature scenery", 
        "city lights",
        "bokeh lights",
    ],
}
