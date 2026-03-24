"""Background music fetcher with auto-ducking for narration"""
import httpx
import asyncio
import json
from pathlib import Path
from typing import Optional, Literal
from config import PIXABAY_API_KEY, TEMP_DIR, MUSIC_SETTINGS

# Pixabay Audio API
PIXABAY_AUDIO_URL = "https://pixabay.com/api/"

# Mood categories mapped to Pixabay search terms
MOOD_QUERIES = {
    "energetic": ["upbeat electronic", "energetic pop", "action music", "workout beats"],
    "calm": ["ambient calm", "peaceful piano", "relaxing nature", "meditation music"],
    "dramatic": ["cinematic epic", "dramatic orchestra", "tension suspense", "trailer music"],
    "happy": ["happy uplifting", "cheerful acoustic", "fun positive", "joyful"],
    "sad": ["melancholy piano", "sad emotional", "somber strings"],
    "mysterious": ["mystery suspense", "dark ambient", "eerie atmosphere"],
    "romantic": ["romantic piano", "love ballad", "soft emotional"],
    "neutral": ["background music", "corporate neutral", "ambient"],
}

MoodType = Literal["energetic", "calm", "dramatic", "happy", "sad", "mysterious", "romantic", "neutral"]


async def search_music(
    query: str = None,
    mood: MoodType = None,
    min_duration: int = 30,
    max_duration: int = 300,
) -> Optional[dict]:
    """
    Search for music on Pixabay.
    
    Args:
        query: Search query (optional if mood is provided)
        mood: Mood category for auto-selecting query
        min_duration: Minimum track duration in seconds
        max_duration: Maximum track duration in seconds
    
    Returns:
        Dict with track info or None
    """
    
    if not PIXABAY_API_KEY:
        print("Warning: No Pixabay API key. Get one free at pixabay.com")
        return None
    
    # Build search query from mood if not provided
    if not query and mood:
        queries = MOOD_QUERIES.get(mood, MOOD_QUERIES["neutral"])
        query = queries[0]  # Use first option
    elif not query:
        query = "background music"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                PIXABAY_AUDIO_URL,
                params={
                    "key": PIXABAY_API_KEY,
                    "q": query,
                    "audio_type": "music",  # music, sfx, all
                    "safesearch": "true",
                    "per_page": 10,
                },
                timeout=15.0,
            )
            
            if response.status_code != 200:
                print(f"Pixabay Audio API error: {response.status_code}")
                return None
            
            data = response.json()
            tracks = data.get("hits", [])
            
            # Filter by duration
            suitable = [
                t for t in tracks 
                if min_duration <= t.get("duration", 0) <= max_duration
            ]
            
            if not suitable:
                # Fall back to any track if none match duration
                suitable = tracks[:3] if tracks else []
            
            if not suitable:
                return None
            
            track = suitable[0]
            
            return {
                "id": track["id"],
                "title": track.get("tags", "Unknown"),
                "url": track["audio"],
                "duration": track.get("duration", 60),
                "downloads": track.get("downloads", 0),
                "provider": "pixabay",
            }
    
    except httpx.HTTPError as e:
        print(f"Pixabay Audio request error: {e}")
    
    return None


async def search_music_by_mood(
    mood: MoodType, 
    min_duration: int = 30,
    max_duration: int = 300,
) -> Optional[dict]:
    """
    Search for music by mood category.
    Tries multiple queries until one returns results.
    """
    
    queries = MOOD_QUERIES.get(mood, MOOD_QUERIES["neutral"])
    
    for query in queries:
        result = await search_music(query=query, min_duration=min_duration, max_duration=max_duration)
        if result:
            print(f"Found music for mood '{mood}': {result['title']}")
            return result
    
    # Fallback to neutral
    if mood != "neutral":
        print(f"No music for mood '{mood}', trying neutral...")
        return await search_music_by_mood("neutral", min_duration, max_duration)
    
    return None


async def download_music(url: str, output_path: Path) -> Path:
    """Download music track from URL"""
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0, follow_redirects=True)
            
            if response.status_code == 200:
                output_path.write_bytes(response.content)
                return output_path
            else:
                raise Exception(f"Failed to download music: {response.status_code}")
    
    except httpx.HTTPError as e:
        raise Exception(f"Music download error: {e}")


async def get_music_for_video(
    mood: MoodType = "neutral",
    target_duration: int = 60,
    output_name: str = "background_music.mp3",
) -> Optional[Path]:
    """
    Fetch and download background music for a video.
    
    Args:
        mood: Mood category
        target_duration: Approximate video duration to match
        output_name: Output filename
    
    Returns:
        Path to downloaded music file or None
    """
    
    output_path = TEMP_DIR / output_name
    
    # Search with duration tolerance
    min_dur = max(20, target_duration - 30)
    max_dur = target_duration + 120  # Allow longer tracks (we'll trim)
    
    result = await search_music_by_mood(mood, min_dur, max_dur)
    
    if not result:
        print(f"No music found for mood: {mood}")
        return None
    
    print(f"Downloading music: {result['title']} ({result['duration']}s)")
    await download_music(result["url"], output_path)
    
    return output_path


def detect_voice_segments(audio_path: Path, threshold_db: float = -40) -> list[tuple[float, float]]:
    """
    Detect segments where voice/speech is present.
    Returns list of (start_time, end_time) tuples.
    
    Requires pydub.
    """
    try:
        from pydub import AudioSegment
        from pydub.silence import detect_nonsilent
        
        audio = AudioSegment.from_file(str(audio_path))
        
        # Detect non-silent segments (likely voice)
        # min_silence_len: minimum silence to consider as gap
        # silence_thresh: dB threshold for silence
        nonsilent = detect_nonsilent(
            audio,
            min_silence_len=300,  # 300ms silence = gap
            silence_thresh=threshold_db,
            seek_step=50,  # Check every 50ms
        )
        
        # Convert to seconds
        segments = [(start / 1000.0, end / 1000.0) for start, end in nonsilent]
        
        return segments
    
    except ImportError:
        print("Warning: pydub not available for voice detection")
        return []


def apply_auto_ducking(
    music_path: Path,
    narration_path: Path,
    output_path: Path,
    voice_volume: float = None,  # Use config default
    duck_volume: float = None,   # Volume during voice
    normal_volume: float = None, # Volume during silence
    fade_duration: float = 0.3,  # Fade in/out duration
) -> Path:
    """
    Mix background music with narration, applying auto-ducking.
    Music volume reduces when voice is detected.
    
    Args:
        music_path: Path to background music file
        narration_path: Path to narration/voice file  
        output_path: Path for output mixed audio
        voice_volume: Voice track volume (0.0-1.0)
        duck_volume: Music volume when voice present (0.0-1.0)
        normal_volume: Music volume during silence (0.0-1.0)
        fade_duration: Fade in/out duration in seconds
    
    Returns:
        Path to mixed audio file
    """
    
    # Use config defaults
    voice_volume = voice_volume or MUSIC_SETTINGS.get("voice_volume", 1.0)
    duck_volume = duck_volume or MUSIC_SETTINGS.get("duck_level", 0.2)
    normal_volume = normal_volume or MUSIC_SETTINGS.get("default_volume", 0.8)
    
    try:
        from pydub import AudioSegment
        
        # Load audio files
        music = AudioSegment.from_file(str(music_path))
        narration = AudioSegment.from_file(str(narration_path))
        
        # Match music length to narration (loop or trim)
        narration_len = len(narration)
        
        if len(music) < narration_len:
            # Loop music to match narration length
            loops_needed = (narration_len // len(music)) + 1
            music = music * loops_needed
        
        music = music[:narration_len]  # Trim to exact length
        
        # Detect voice segments
        voice_segments = detect_voice_segments(narration_path)
        
        if voice_segments:
            # Create ducked music track
            ducked_music = AudioSegment.silent(duration=len(music))
            
            # Convert volumes to dB adjustments
            duck_db = 20 * (duck_volume / normal_volume if normal_volume > 0 else 0.25).__log10__() if duck_volume > 0 else -60
            normal_db = 0  # No change for normal volume
            
            # Apply volume based on voice presence
            current_pos = 0
            fade_ms = int(fade_duration * 1000)
            
            for start, end in voice_segments:
                start_ms = int(start * 1000)
                end_ms = int(end * 1000)
                
                # Before voice: normal volume
                if start_ms > current_pos:
                    segment = music[current_pos:start_ms]
                    # Fade out at the end approaching voice
                    if start_ms - current_pos > fade_ms:
                        segment = segment.fade_out(fade_ms)
                    ducked_music = ducked_music.overlay(segment, position=current_pos)
                
                # During voice: ducked volume
                voice_segment = music[start_ms:end_ms] + duck_db
                # Fade in/out for smooth transition
                if end_ms - start_ms > fade_ms * 2:
                    voice_segment = voice_segment.fade_in(fade_ms).fade_out(fade_ms)
                ducked_music = ducked_music.overlay(voice_segment, position=start_ms)
                
                current_pos = end_ms
            
            # After last voice segment: normal volume
            if current_pos < len(music):
                segment = music[current_pos:]
                segment = segment.fade_in(fade_ms)
                ducked_music = ducked_music.overlay(segment, position=current_pos)
            
            music = ducked_music
        else:
            # No voice detected - just apply normal volume
            music = music + (20 * normal_volume.__log10__() if normal_volume > 0 else -60)
        
        # Adjust voice volume
        if voice_volume != 1.0:
            narration = narration + (20 * voice_volume.__log10__() if voice_volume > 0 else -60)
        
        # Mix music and narration
        mixed = music.overlay(narration)
        
        # Export
        mixed.export(str(output_path), format="mp3")
        
        print(f"Mixed audio saved to: {output_path}")
        return output_path
    
    except ImportError:
        print("Error: pydub is required for auto-ducking. Install with: pip install pydub")
        raise
    except Exception as e:
        print(f"Error applying auto-ducking: {e}")
        raise


def mix_audio_simple(
    music_path: Path,
    narration_path: Path,
    output_path: Path,
    music_volume: float = None,
) -> Path:
    """
    Simple audio mixing without auto-ducking.
    Just overlays music at reduced volume under narration.
    
    Useful as fallback when voice detection fails.
    """
    
    music_volume = music_volume or MUSIC_SETTINGS.get("duck_level", 0.2)
    
    try:
        from pydub import AudioSegment
        
        music = AudioSegment.from_file(str(music_path))
        narration = AudioSegment.from_file(str(narration_path))
        
        # Match lengths
        if len(music) < len(narration):
            loops_needed = (len(narration) // len(music)) + 1
            music = music * loops_needed
        music = music[:len(narration)]
        
        # Reduce music volume
        music_db = 20 * music_volume.__log10__() if music_volume > 0 else -60
        music = music + music_db
        
        # Fade in/out music
        music = music.fade_in(1000).fade_out(2000)
        
        # Mix
        mixed = music.overlay(narration)
        mixed.export(str(output_path), format="mp3")
        
        return output_path
    
    except ImportError:
        print("Error: pydub is required for audio mixing")
        raise


# Sync wrappers
def get_music_sync(mood: MoodType = "neutral", target_duration: int = 60) -> Optional[Path]:
    """Synchronous wrapper for get_music_for_video"""
    return asyncio.run(get_music_for_video(mood, target_duration))


def mix_with_music_sync(
    narration_path: Path,
    mood: MoodType = "neutral",
    output_path: Path = None,
    use_ducking: bool = True,
) -> Optional[Path]:
    """
    Complete workflow: fetch music and mix with narration.
    
    Args:
        narration_path: Path to narration audio
        mood: Music mood category
        output_path: Output path (default: temp/mixed_audio.mp3)
        use_ducking: Whether to use auto-ducking
    
    Returns:
        Path to mixed audio or None
    """
    
    output_path = output_path or TEMP_DIR / "mixed_audio.mp3"
    
    # Estimate duration from narration
    try:
        from pydub import AudioSegment
        narration = AudioSegment.from_file(str(narration_path))
        duration = len(narration) // 1000
    except Exception:
        duration = 60
    
    # Fetch music
    music_path = asyncio.run(get_music_for_video(mood, duration))
    
    if not music_path:
        print("Could not fetch background music")
        return None
    
    # Mix audio
    if use_ducking:
        return apply_auto_ducking(music_path, narration_path, output_path)
    else:
        return mix_audio_simple(music_path, narration_path, output_path)
