"""Text-to-Speech module using Edge TTS (free, unlimited)"""
import edge_tts
import asyncio
from pathlib import Path
from config import TEMP_DIR, VOICES


async def generate_speech(
    text: str,
    voice: str = "en-US-GuyNeural",
    output_path: Path = None
) -> tuple[Path, list[dict]]:
    """
    Generate speech from text using Edge TTS.
    
    Returns:
        tuple: (audio_path, word_timings)
        word_timings: list of {"text": str, "start": float, "end": float}
    """
    
    if output_path is None:
        output_path = TEMP_DIR / "narration.mp3"
    
    # Create communicator
    communicate = edge_tts.Communicate(text, voice)
    
    # Collect word timings for subtitles
    word_timings = []
    
    # Save audio and collect timing data
    submaker = edge_tts.SubMaker()
    
    with open(output_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_timings.append({
                    "text": chunk["text"],
                    "start": chunk["offset"] / 10_000_000,  # Convert to seconds
                    "duration": chunk["duration"] / 10_000_000,
                })
    
    return output_path, word_timings


async def generate_speech_for_scenes(
    scenes: list[dict],
    voice: str = "en-US-GuyNeural"
) -> tuple[Path, list[dict]]:
    """
    Generate speech for all scenes combined.
    
    Returns full audio path and timing info per scene.
    """
    
    # Combine all text
    full_text = " ".join(scene["text"] for scene in scenes)
    
    audio_path, word_timings = await generate_speech(full_text, voice)
    
    return audio_path, word_timings


def list_voices() -> list[str]:
    """List available Edge TTS voices"""
    # Return curated list of good English voices
    return [
        # US English
        "en-US-GuyNeural",      # Male, casual
        "en-US-JennyNeural",    # Female, casual  
        "en-US-AriaNeural",     # Female, professional
        "en-US-DavisNeural",    # Male, professional
        "en-US-TonyNeural",     # Male, friendly
        "en-US-SaraNeural",     # Female, friendly
        # UK English
        "en-GB-RyanNeural",     # Male
        "en-GB-SoniaNeural",    # Female
        # Australian
        "en-AU-WilliamNeural",  # Male
        "en-AU-NatashaNeural",  # Female
    ]


async def get_all_voices() -> list[dict]:
    """Get all available voices from Edge TTS"""
    voices = await edge_tts.list_voices()
    # Filter English voices
    return [v for v in voices if v["Locale"].startswith("en-")]


# Sync wrappers
def generate_speech_sync(text: str, voice: str = "en-US-GuyNeural", output_path: Path = None) -> tuple[Path, list[dict]]:
    """Synchronous wrapper for generate_speech"""
    return asyncio.run(generate_speech(text, voice, output_path))


def generate_scenes_speech_sync(scenes: list[dict], voice: str = "en-US-GuyNeural") -> tuple[Path, list[dict]]:
    """Synchronous wrapper for generate_speech_for_scenes"""
    return asyncio.run(generate_speech_for_scenes(scenes, voice))
