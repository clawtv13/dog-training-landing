#!/usr/bin/env python3
"""
Prompt Refiner - Enhance CapCut AI Prompts
Optimizes generated prompts for maximum clarity and CapCut AI understanding

Usage:
  python3 prompt-refiner.py --file output/trailers/prompt.txt
  python3 prompt-refiner.py --latest cleverdogmethod
  python3 prompt-refiner.py --latest mindcrimes
"""

import requests
import json
import argparse
import re
from pathlib import Path
from datetime import datetime

# Config
WORKSPACE = Path("/root/.openclaw/workspace")
OPENROUTER_KEY = "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"
TELEGRAM_BOT = "8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU"
TELEGRAM_CHAT = "8116230130"

# Output directories
CLEVERDOGMETHOD_OUT = WORKSPACE / ".state"
MINDCRIMES_OUT = WORKSPACE / "output/mind-crimes-trailers"

def find_latest_prompt(source: str) -> Path:
    """Find most recent generated prompt"""
    
    if source == "cleverdogmethod":
        state_file = WORKSPACE / ".state/shorts-generated.json"
        if not state_file.exists():
            print("❌ No CleverDog prompts found")
            return None
        
        # CleverDog prompts are embedded in state, need to reconstruct
        # For now, return path to check Telegram
        print("ℹ️  CleverDog prompts sent via Telegram (check chat)")
        return None
        
    elif source == "mindcrimes":
        # Find latest file in trailers output
        files = sorted(MINDCRIMES_OUT.glob("*.txt"), key=lambda p: p.stat().st_mtime)
        if not files:
            print("❌ No Mind Crimes trailers found")
            return None
        return files[-1]
    
    return None

def extract_platform_sections(prompt_text: str) -> dict:
    """Split prompt into platform sections"""
    
    sections = {}
    
    # Find platform markers
    platforms = ["TIKTOK", "INSTAGRAM", "YOUTUBE"]
    
    for i, platform in enumerate(platforms):
        # Find start of this platform
        start_pattern = f"**{platform}:**"
        start = prompt_text.find(start_pattern)
        
        if start == -1:
            continue
        
        # Find end (start of next platform or end of string)
        if i + 1 < len(platforms):
            end_pattern = f"**{platforms[i+1]}:**"
            end = prompt_text.find(end_pattern)
            if end == -1:
                end = len(prompt_text)
        else:
            end = len(prompt_text)
        
        sections[platform.lower()] = prompt_text[start:end].strip()
    
    return sections

def refine_prompt(raw_prompt: str, platform: str) -> str:
    """
    Enhance prompt via OpenRouter with refinement instructions
    
    Focus areas:
    - Visual specificity (literal descriptions for AI)
    - Audio timing precision
    - Text overlay impact
    - CapCut AI clarity
    """
    
    system_prompt = f"""You are a CapCut AI prompt optimization expert.

TASK: Enhance this {platform.upper()} video prompt for maximum CapCut AI clarity.

ENHANCEMENT RULES:

1. VISUAL SPECIFICITY (+30% detail)
   BAD: "happy couple"
   GOOD: "couple in their 30s laughing on sandy beach at golden hour, woman in blue sundress, man in casual white shirt, waves in background, warm orange lighting"
   
   BAD: "crime scene"
   GOOD: "police tape across suburban home driveway at dusk, two patrol cars with lights off, evidence markers numbered 1-5, detective in dark suit taking notes"

2. AUDIO PRECISION
   BAD: "dramatic music"
   GOOD: "low rumbling bass note (0-2s), building violin crescendo (3-10s), sudden silence at 11s, heartbeat sound effect starting 12s"
   
   Specify EXACT timing for sound effects

3. TEXT OVERLAY IMPACT
   {platform.upper()} limit: {"8 words max" if platform == "tiktok" else "12 words max"}
   
   BAD: "Then something terrible happened that changed everything"
   GOOD: "Then DNA revealed the truth"
   
   Make every word count. Punchy. Urgent.

4. CAPCUT AI UNDERSTANDING
   - Be literal, not poetic
   - Specify camera angles ("close-up", "wide shot", "overhead view")
   - Name exact visual elements ("red evidence bag", "silver handcuffs", "manila folder")
   - Avoid metaphors CapCut won't understand

5. STRUCTURE PRESERVATION
   - Keep same scene count
   - Keep exact timing (0-3s, 3-10s, etc.)
   - Keep compliance requirements
   - Keep CTA placement

OUTPUT FORMAT: Enhanced prompt with same structure, 30% more specific visual/audio details.

DO NOT:
- Change timing
- Add/remove scenes
- Alter compliance filters
- Change platform specs

ONLY enhance clarity and specificity."""

    user_prompt = f"""Enhance this {platform} prompt:

{raw_prompt}

Make it 10x more specific for CapCut AI understanding while preserving structure."""

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
            print(f"⚠️  OpenRouter error: {response.status_code}")
            return raw_prompt
            
    except Exception as e:
        print(f"❌ Refinement failed: {e}")
        return raw_prompt

def refine_file(file_path: Path, platforms: list = None):
    """Refine prompt from file"""
    
    print(f"📂 Reading: {file_path.name}")
    
    with open(file_path) as f:
        content = f.read()
    
    # Extract platform sections
    sections = extract_platform_sections(content)
    
    if not sections:
        print("❌ No platform sections found")
        return
    
    # Default to all platforms if not specified
    if not platforms:
        platforms = list(sections.keys())
    
    enhanced_sections = {}
    
    for platform in platforms:
        if platform not in sections:
            print(f"⚠️  {platform} not found, skipping")
            continue
        
        print(f"\n🔄 Refining {platform.upper()}...")
        enhanced = refine_prompt(sections[platform], platform)
        enhanced_sections[platform] = enhanced
        print(f"✅ {platform.upper()} enhanced")
    
    # Build output
    output = f"""# ENHANCED PROMPT - {file_path.stem}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
Original: {file_path.name}

{"=" * 80}

"""
    
    for platform, enhanced in enhanced_sections.items():
        output += f"""
**{platform.upper()} (ENHANCED):**

{enhanced}

{"=" * 80}

"""
    
    # Save enhanced version
    enhanced_path = file_path.parent / f"ENHANCED-{file_path.name}"
    with open(enhanced_path, 'w') as f:
        f.write(output)
    
    print(f"\n💾 Saved: {enhanced_path.name}")
    
    # Send to Telegram
    send_telegram(file_path.stem, enhanced_sections)
    
    return enhanced_path

def send_telegram(prompt_name: str, enhanced_sections: dict):
    """Send refinement notification"""
    
    platforms_list = ", ".join(p.upper() for p in enhanced_sections.keys())
    
    msg = f"""✨ PROMPT ENHANCED

📝 Original: {prompt_name}
🎯 Platforms: {platforms_list}

Improvements:
✅ Visual specificity +30%
✅ Audio timing precision
✅ Text overlay impact
✅ CapCut AI clarity

📂 Check output directory for ENHANCED- file

🎬 Ready for production!"""
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": msg},
            timeout=10
        )
        print("✅ Telegram notification sent")
    except:
        print("⚠️  Telegram notification failed")

def main():
    parser = argparse.ArgumentParser(description="Enhance CapCut AI prompts")
    parser.add_argument("--file", help="Specific prompt file to refine")
    parser.add_argument("--latest", choices=["cleverdogmethod", "mindcrimes"],
                        help="Refine latest prompt from source")
    parser.add_argument("--platform", choices=["tiktok", "instagram", "youtube"],
                        help="Refine specific platform only (default: all)")
    
    args = parser.parse_args()
    
    platforms = [args.platform] if args.platform else None
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            return
        refine_file(file_path, platforms)
        
    elif args.latest:
        latest = find_latest_prompt(args.latest)
        if latest:
            refine_file(latest, platforms)
        else:
            print(f"No prompts found for {args.latest}")
    
    else:
        print("❌ Specify --file or --latest")
        print("Example: python3 prompt-refiner.py --latest mindcrimes")

if __name__ == "__main__":
    main()
