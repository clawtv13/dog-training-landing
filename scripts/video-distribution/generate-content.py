#!/usr/bin/env python3
"""
Generate platform-specific titles/descriptions
Usage: python generate-content.py <channel> <transcript> <duration>
"""
import sys
import os
import json
import requests

CHANNEL_CONTEXTS = {
    "HEALTH_HACKS": {
        "niche": "Pain relief, energy, sleep, stress, gut health, mental clarity",
        "audience": "Office workers, health-conscious adults 25-45",
        "tone": "Science-backed, practical, empathetic, no BS",
        "products": ["calmorarelief.com"],
        "handles": {
            "youtube": "@HealthHacks",
            "tiktok": "@healthhacks",
            "instagram": "@healthhacks"
        }
    },
    "MONEYSTACK": {
        "niche": "Money psychology, savings, financial mental health",
        "audience": "Young professionals, students 18-35",
        "tone": "Real talk, relatable, anti-hustle, honest",
        "products": [],
        "handles": {
            "youtube": "@MONEYSTACK_YT",
            "tiktok": "@moneystack",
            "instagram": "@moneystack"
        }
    }
}

def generate_content(channel, transcript, duration):
    """Generate platform-specific content using Claude"""
    
    context = CHANNEL_CONTEXTS.get(channel)
    if not context:
        raise ValueError(f"Unknown channel: {channel}")
    
    # Build prompt
    prompt = f"""You're writing social media content for {channel}.

**Channel context:**
- Niche: {context['niche']}
- Audience: {context['audience']}
- Tone: {context['tone']}

**Video transcript:**
"{transcript}"

**Duration:** {duration} seconds

Generate 3 UNIQUE titles and descriptions for each platform. Each platform needs a DIFFERENT ANGLE (not just rewording).

## TikTok (Viral/Hook)
- Title: 8-12 words max, emotional hook, 1 emoji
- Caption: 1-2 sentences, relatable pain point, 4-6 hashtags
- Hook formula: "POV:", "If you...", "When you..."
- Goal: Stop scroll, high engagement

## Instagram Reels (Aspirational)
- Title: Brand-aligned, lifestyle angle
- Caption: Mini-story (2-3 sentences), emojis, 5-8 hashtags
- Style: Personal experience, transformation
- Goal: Save/share, community

## YouTube Shorts (Educational/SEO)
- Title: Keyword-rich, clear value, under 60 chars
- Description: What/why/how (3-4 sentences), add "#Shorts" at end{"," if context["products"] else ""} {f'link: {context["products"][0]}' if context["products"] else ''}
- Tags: 5-8 search keywords
- Goal: Search ranking, watch time

**CRITICAL RULES:**
1. Each platform = DIFFERENT angle (POV vs story vs education)
2. Write like a human YouTuber/TikToker (casual, direct)
3. NO corporate speak: "innovative", "transformative", "serves as", "delve", "tapestry"
4. NO clickbait that misrepresents content
5. Match transcript tone and energy
6. Keep it REAL and SIMPLE

Output ONLY valid JSON (no markdown, no explanation):
{{
  "tiktok": {{"title": "...", "caption": "...", "hashtags": ["tag1", "tag2"]}},
  "instagram": {{"title": "...", "caption": "...", "hashtags": ["tag1", "tag2"]}},
  "youtube": {{"title": "...", "description": "...", "tags": ["tag1", "tag2"]}}
}}"""
    
    # Get API key (OpenRouter)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        cred_file = "/root/.openclaw/workspace/.credentials/openrouter-key.txt"
        if os.path.exists(cred_file):
            with open(cred_file) as f:
                api_key = f.read().strip()
    
    if not api_key:
        raise ValueError("OpenRouter API key not found")
    
    # Call Claude via OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    
    result = response.json()
    content_text = result["choices"][0]["message"]["content"]
    
    # Parse JSON (handle markdown wrappers)
    try:
        content = json.loads(content_text)
    except:
        # Remove markdown code blocks if present
        cleaned = content_text.replace("```json\n", "").replace("```\n", "").replace("```", "").strip()
        content = json.loads(cleaned)
    
    return content

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate-content.py <channel> <transcript> <duration>")
        sys.exit(1)
    
    channel = sys.argv[1]
    transcript = sys.argv[2]
    duration = float(sys.argv[3])
    
    try:
        content = generate_content(channel, transcript, duration)
        print(json.dumps(content, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
