"""
Shared prompt refinement utilities for all generators
"""

import requests

OPENROUTER_KEY = "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"

def refine_prompt(raw_prompt: str, platform: str = "shorts", compact_mode: bool = False) -> str:
    """
    Enhance prompt for CapCut AI clarity
    
    Args:
        raw_prompt: Original generated prompt
        platform: tiktok, instagram, youtube, or shorts
        compact_mode: If True, generate ultra-compact output (<3K chars) for CapCut limits
    
    Returns:
        Enhanced prompt (detailed or ultra-compact based on mode)
    """
    
    if compact_mode:
        # Ultra-compact mode for CapCut character limits (2-3KB)
        system_prompt = f"""You are a CapCut prompt compressor. Make this {platform.upper()} prompt ULTRA-COMPACT.

**TARGET:** 2000-3000 characters TOTAL (current is too long for CapCut).

**KEEP ONLY:**
- Scene timing (0-4s, 4-15s, etc.)
- Core visual (1 sentence max per scene)
- Audio cue (short, 3-5 words)
- Text overlay (exact words)

**REMOVE:**
- Verbose descriptions
- Multiple visual options
- Explanations
- Compliance notes (separate doc)
- Hashtag strategies (put in separate section)
- Marketing copy
- Long instructions

**FORMAT (strict):**
```
0-4s: Funeral chairs, man crying | Audio: piano | Text: "Killer at funeral"
4-15s: Suburban house, family photo | Audio: acoustic | Text: "Perfect life"
15-30s: Detective with evidence folder | Audio: suspense | Text: "One clue changed everything"
```

**AFTER SCENES, ADD:**
```
HASHTAGS: #truecrime #coldcase #solved
TITLE: [10 words max]
DESC: [20 words max]
CTA: [5 words max]
```

**CRITICAL:** 
- Maximum 2000-3000 chars TOTAL
- Still actionable for CapCut AI
- No fluff, only essentials
- Each scene = 1 line

OUTPUT: Ultra-compact prompt ready for CapCut paste."""
    else:
        # Standard detailed mode
        system_prompt = f"""You are a CapCut AI prompt optimizer.

TASK: Enhance this {platform.upper()} prompt for maximum CapCut AI understanding.

FOCUS ON:
1. VISUAL SPECIFICITY (+30% detail)
   - Not "happy dog" → "golden retriever puppy with floppy ears jumping excitedly in green backyard, tail wagging, tongue out, sunny afternoon lighting"
   - Not "crime scene" → "yellow police tape across suburban driveway, two patrol cars, evidence markers 1-5, detective in dark suit"

2. AUDIO PRECISION
   - Specify exact timing: "low bass rumble (0-2s), violin crescendo (3-10s), silence at 11s"
   - Name sound effects: "handcuff click at 15s, heartbeat starting 20s"

3. TEXT OVERLAY PUNCH
   - Shorter, impactful
   - Not "Then something happened" → "Then DNA revealed truth"
   - {platform.upper()} limit: {"8 words max" if platform == "tiktok" else "10 words max"}

4. CAPCUT AI CLARITY
   - Be literal (CapCut AI understands concrete, not metaphor)
   - Specify camera angles: "close-up", "wide shot", "overhead view"
   - Name objects: "red evidence bag", "silver handcuffs", "manila folder"

MAINTAIN:
- Same scene structure
- Exact timing
- Same formula
- Compliance rules

OUTPUT: Enhanced prompt, 30% more specific, same structure."""

    user_prompt = f"Enhance this {platform} prompt:\n\n{raw_prompt}"

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4.5",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"⚠️  Refinement failed ({response.status_code}), using original")
            return raw_prompt
            
    except Exception as e:
        print(f"⚠️  Refinement error: {e}, using original")
        return raw_prompt

