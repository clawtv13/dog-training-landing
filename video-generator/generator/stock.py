"""Stock video fetcher with multi-provider fallback (Pexels → Pixabay → placeholder)"""
import httpx
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Optional
from config import PEXELS_API_KEY, PIXABAY_API_KEY, TEMP_DIR

# API URLs
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
PIXABAY_VIDEO_URL = "https://pixabay.com/api/videos/"

# Fallback queries when original search fails
FALLBACK_QUERIES = ["abstract background", "nature scenery", "city lights", "bokeh lights"]

# Simple in-memory cache for search results
_search_cache: dict[str, dict] = {}
CACHE_FILE = TEMP_DIR / "video_cache.json"


def _load_cache() -> dict:
    """Load cache from disk"""
    global _search_cache
    if CACHE_FILE.exists():
        try:
            _search_cache = json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            _search_cache = {}
    return _search_cache


def _save_cache():
    """Save cache to disk"""
    try:
        CACHE_FILE.write_text(json.dumps(_search_cache, indent=2))
    except IOError:
        pass


def _cache_key(query: str, orientation: str, provider: str) -> str:
    """Generate cache key"""
    return hashlib.md5(f"{provider}:{query}:{orientation}".encode()).hexdigest()


async def search_pexels(query: str, orientation: str = "portrait") -> Optional[dict]:
    """Search for a video on Pexels"""
    
    if not PEXELS_API_KEY:
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                PEXELS_VIDEO_URL,
                headers={"Authorization": PEXELS_API_KEY},
                params={
                    "query": query,
                    "orientation": orientation,
                    "size": "medium",
                    "per_page": 5,
                },
                timeout=15.0,
            )
            
            if response.status_code != 200:
                print(f"Pexels API error: {response.status_code}")
                return None
            
            data = response.json()
            videos = data.get("videos", [])
            
            if not videos:
                return None
            
            video = videos[0]
            video_files = video.get("video_files", [])
            
            # Find best quality file (prefer HD)
            best_file = None
            for vf in video_files:
                if vf.get("quality") == "hd":
                    if orientation == "portrait" and vf.get("height", 0) >= 1080:
                        best_file = vf
                        break
                    elif orientation != "portrait":
                        best_file = vf
                        break
            
            if not best_file and video_files:
                best_file = video_files[0]
            
            if best_file:
                return {
                    "id": video["id"],
                    "url": best_file["link"],
                    "width": best_file.get("width", 1080),
                    "height": best_file.get("height", 1920),
                    "duration": video.get("duration", 10),
                    "provider": "pexels",
                }
    
    except httpx.HTTPError as e:
        print(f"Pexels request error: {e}")
    
    return None


async def search_pixabay(query: str, orientation: str = "portrait") -> Optional[dict]:
    """Search for a video on Pixabay"""
    
    if not PIXABAY_API_KEY:
        return None
    
    # Map orientation to Pixabay format
    pixabay_orientation = {
        "portrait": "vertical",
        "landscape": "horizontal",
        "square": "all",  # Pixabay doesn't have square filter
    }.get(orientation, "all")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                PIXABAY_VIDEO_URL,
                params={
                    "key": PIXABAY_API_KEY,
                    "q": query,
                    "video_type": "film",  # film, animation, all
                    "orientation": pixabay_orientation,
                    "safesearch": "true",
                    "per_page": 5,
                },
                timeout=15.0,
            )
            
            if response.status_code != 200:
                print(f"Pixabay API error: {response.status_code}")
                return None
            
            data = response.json()
            videos = data.get("hits", [])
            
            if not videos:
                return None
            
            video = videos[0]
            
            # Pixabay provides multiple sizes: large, medium, small, tiny
            # Prefer large (1920x1080) or medium (1280x720)
            video_data = video.get("videos", {})
            
            # Priority: large > medium > small
            for size in ["large", "medium", "small"]:
                if size in video_data:
                    vf = video_data[size]
                    return {
                        "id": video["id"],
                        "url": vf["url"],
                        "width": vf.get("width", 1080),
                        "height": vf.get("height", 1920),
                        "duration": video.get("duration", 10),
                        "provider": "pixabay",
                    }
    
    except httpx.HTTPError as e:
        print(f"Pixabay request error: {e}")
    
    return None


async def search_video(query: str, orientation: str = "portrait", use_cache: bool = True) -> Optional[dict]:
    """
    Search for a video with multi-provider fallback.
    Order: Pexels → Pixabay → None
    """
    
    # Check cache first
    if use_cache:
        _load_cache()
        for provider in ["pexels", "pixabay"]:
            key = _cache_key(query, orientation, provider)
            if key in _search_cache:
                print(f"Cache hit for '{query}' ({provider})")
                return _search_cache[key]
    
    # Try Pexels first
    result = await search_pexels(query, orientation)
    if result:
        if use_cache:
            _search_cache[_cache_key(query, orientation, "pexels")] = result
            _save_cache()
        return result
    
    # Fallback to Pixabay
    result = await search_pixabay(query, orientation)
    if result:
        if use_cache:
            _search_cache[_cache_key(query, orientation, "pixabay")] = result
            _save_cache()
        return result
    
    return None


async def download_video(url: str, output_path: Path) -> Path:
    """Download video from URL with retry logic"""
    
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=60.0, follow_redirects=True)
                
                if response.status_code == 200:
                    output_path.write_bytes(response.content)
                    return output_path
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = 2 ** attempt
                    print(f"Rate limited, waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception(f"Failed to download video: {response.status_code}")
        
        except httpx.HTTPError as e:
            if attempt < max_retries - 1:
                print(f"Download error (attempt {attempt + 1}): {e}")
                await asyncio.sleep(1)
            else:
                raise Exception(f"Failed to download after {max_retries} attempts: {e}")
    
    raise Exception("Download failed")


def create_placeholder_video(output_path: Path, duration: float = 5.0, 
                              width: int = 1080, height: int = 1920) -> Path:
    """
    Create a simple placeholder video (black screen with text).
    Requires moviepy to be installed.
    """
    try:
        from moviepy import ColorClip, TextClip, CompositeVideoClip
        
        # Black background
        bg = ColorClip(size=(width, height), color=(20, 20, 30), duration=duration)
        
        # Try to add text (may fail if no font available)
        try:
            txt = TextClip(
                text="Stock footage\nunavailable",
                font_size=50,
                color="gray",
                font="Arial",
            )
            txt = txt.with_position("center").with_duration(duration)
            video = CompositeVideoClip([bg, txt])
        except Exception:
            video = bg
        
        video.write_videofile(
            str(output_path),
            fps=30,
            codec="libx264",
            audio=False,
            logger=None,
        )
        video.close()
        
        return output_path
    
    except ImportError:
        print("Warning: moviepy not available for placeholder creation")
        return None


async def get_video_for_scene(
    query: str, 
    scene_index: int, 
    orientation: str = "portrait",
    use_placeholder: bool = True
) -> Optional[Path]:
    """Search and download video for a scene with full fallback chain"""
    
    output_path = TEMP_DIR / f"clip_{scene_index}.mp4"
    
    # Try original query
    result = await search_video(query, orientation)
    
    # Try fallback queries if original fails
    if not result:
        for fallback in FALLBACK_QUERIES:
            result = await search_video(fallback, orientation)
            if result:
                print(f"Using fallback query '{fallback}' for scene {scene_index}")
                break
    
    if result:
        print(f"Downloading from {result['provider']} for scene {scene_index}: {query}")
        await download_video(result["url"], output_path)
        return output_path
    
    # Last resort: create placeholder
    if use_placeholder:
        print(f"Creating placeholder for scene {scene_index} (no video found for: {query})")
        placeholder = create_placeholder_video(output_path)
        if placeholder:
            return placeholder
    
    print(f"No video found for: {query}")
    return None


async def get_videos_for_scenes(
    scenes: list[dict], 
    orientation: str = "portrait",
    use_placeholder: bool = True
) -> list[Path]:
    """Get videos for all scenes (parallel download with rate limiting)"""
    
    # Use semaphore to limit concurrent downloads (avoid rate limiting)
    semaphore = asyncio.Semaphore(3)
    
    async def limited_get(scene: dict, index: int):
        async with semaphore:
            return await get_video_for_scene(
                scene["search_query"], 
                index, 
                orientation,
                use_placeholder
            )
    
    tasks = [
        limited_get(scene, i)
        for i, scene in enumerate(scenes)
    ]
    
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


def get_videos_sync(scenes: list[dict], orientation: str = "portrait") -> list[Path]:
    """Synchronous wrapper"""
    return asyncio.run(get_videos_for_scenes(scenes, orientation))


def clear_cache():
    """Clear the video search cache"""
    global _search_cache
    _search_cache = {}
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
    print("Video cache cleared")
