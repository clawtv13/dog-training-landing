"""LLM module for parsing scripts into scenes"""
import json
import httpx
from config import OPENROUTER_API_KEY, LLM_MODEL

SCENE_PROMPT = """You are a video editor AI. Given a script, break it into scenes for a short-form video.

For each scene, provide:
1. The text/narration for that scene
2. A search query to find relevant stock video footage
3. Duration in seconds (based on reading speed ~150 words/min)

Return JSON array with this exact format:
[
  {{"text": "The narration text for this scene", "search_query": "search terms for stock video", "duration": 3.5}}
]

Rules:
- Keep scenes 2-5 seconds each
- Search queries should be visual and specific (e.g., "dog barking at night indoors")
- Total duration should match natural reading pace
- Max 3-4 words per search query for better results

Script to parse:
{script}

Return ONLY valid JSON, no markdown or explanation."""


async def parse_script_to_scenes(script: str) -> list[dict]:
    """Use LLM to parse script into scenes with video search queries"""
    
    if not OPENROUTER_API_KEY:
        # Fallback: simple sentence splitting
        return _simple_parse(script)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "user", "content": SCENE_PROMPT.format(script=script)}
                ],
                "temperature": 0.3,
            },
            timeout=30.0,
        )
        
        if response.status_code != 200:
            print(f"LLM API error: {response.status_code}")
            return _simple_parse(script)
        
        data = response.json()
        
        # Handle different response structures
        try:
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
            else:
                print(f"Unexpected API response structure: {data}")
                return _simple_parse(script)
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error extracting content from response: {e}")
            return _simple_parse(script)
        
        # Clean up response (remove markdown if present)
        content = content.strip()
        
        # Handle various markdown code block formats
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            parts = content.split("```")
            if len(parts) >= 2:
                content = parts[1]
                if content.startswith("json"):
                    content = content[4:]
        
        content = content.strip()
        
        try:
            scenes = json.loads(content)
            if isinstance(scenes, list) and len(scenes) > 0:
                return scenes
            else:
                print("LLM returned empty or invalid scenes")
                return _simple_parse(script)
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Content was: {content[:200]}...")
            return _simple_parse(script)


def _simple_parse(script: str) -> list[dict]:
    """Fallback: simple sentence-based parsing"""
    import re
    
    # Split by sentence
    sentences = re.split(r'(?<=[.!?])\s+', script.strip())
    
    scenes = []
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Estimate duration (150 words per minute = 2.5 words per second)
        word_count = len(sentence.split())
        duration = max(2.0, word_count / 2.5)
        
        # Generate simple search query (first 3-4 meaningful words)
        words = [w for w in sentence.split() if len(w) > 3][:3]
        search_query = " ".join(words).lower()
        
        scenes.append({
            "text": sentence.strip(),
            "search_query": search_query or "person talking",
            "duration": round(duration, 1)
        })
    
    return scenes


# Sync wrapper for non-async usage
def parse_script_sync(script: str) -> list[dict]:
    """Synchronous wrapper for parse_script_to_scenes"""
    import asyncio
    return asyncio.run(parse_script_to_scenes(script))
