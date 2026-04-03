#!/usr/bin/env python3
"""
Viral Shorts Prompt Generator - REFACTORED
ONE video prompt + THREE platform metadata sets
Saves 66% API costs (2 calls vs 6)

Usage:
  python3 viral-prompt-generator-refactored.py               # Auto-select from keywords
  python3 viral-prompt-generator-refactored.py "stop dog jumping"
  python3 viral-prompt-generator-refactored.py "husky training" --formula myth_buster
  python3 viral-prompt-generator-refactored.py --random
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Import refinement utilities
try:
    from refine_utils import refine_prompt
    REFINEMENT_AVAILABLE = True
except ImportError:
    REFINEMENT_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path("/root/.openclaw/workspace")
KEYWORDS_FILE = WORKSPACE / "content/cleverdogmethod/KEYWORDS-V2-EXPANSION.md"
STATE_FILE = WORKSPACE / ".state/shorts-generated.json"
OPENROUTER_KEY = "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"
TELEGRAM_BOT = "8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU"
TELEGRAM_CHAT = "8116230130"
COOLDOWN_DAYS = 7

# ============================================================================
# FORMULAS (unchanged)
# ============================================================================

FORMULAS = {
    "problem_solution": {
        "name": "Problem → Solution",
        "retention": 85,
        "best_for": "Educational, quick wins",
        "structure": """
SCENE 1 (0-3s): Pattern interrupt
- Text: "[PROBLEM] that EVERYONE struggles with"
- Visual: Frustrated owner, chaotic scenario
- Hook: Dramatic + relatable

SCENE 2 (3-10s): The mistake
- Text: "Here's what you're doing WRONG"
- Visual: Common mistake shown
- Build tension

SCENE 3 (10-40s): The solution (step-by-step)
- Text: "Here's the fix:"
- Visual: Demonstrate correct method
- 3 clear steps with visual examples

SCENE 4 (40-55s): Result
- Text: "Before vs After"
- Visual: Split screen transformation
- Payoff moment

SCENE 5 (55-60s): CTA
- Text: "Follow for daily dog secrets 🐕"
- Visual: Channel branding
- Engagement hook: "Which tip next? 👇"
"""
    },
    
    "myth_buster": {
        "name": "Myth Buster",
        "retention": 82,
        "best_for": "Controversial, comment bait",
        "structure": """
SCENE 1 (0-3s): Controversial statement
- Text: "STOP doing this to your dog 🚫"
- Visual: Common mistake shown
- Red X animation

SCENE 2 (3-15s): Why it's wrong
- Text: "This actually makes it WORSE"
- Visual: Science/data showing harm
- Educational angle

SCENE 3 (15-40s): What actually works
- Text: "Here's what trainers ACTUALLY do"
- Visual: Correct method demonstrated
- Authority positioning

SCENE 4 (40-55s): Proof
- Text: "Results in 7 days"
- Visual: Before/after footage
- Credibility

SCENE 5 (55-60s): CTA
- Text: "Did you know this? 👇"
- Comment bait
- Follow CTA
"""
    },

    "transformation": {
        "name": "Transformation Story",
        "retention": 78,
        "best_for": "Emotional, shareable",
        "structure": """
SCENE 1 (0-5s): Sad beginning
- Text: "This [dog/situation] was [extreme problem]..."
- Visual: Dark, sad, problem state
- Emotional hook

SCENE 2 (5-15s): The turning point
- Text: "Then [owner/trainer] tried THIS"
- Visual: First step, hope appears
- Music shift (sad → uplifting)

SCENE 3 (15-40s): The journey
- Text: "Week 1... Week 2... Week 4..."
- Visual: Progress montage
- Show obstacles overcome

SCENE 4 (40-55s): The victory
- Text: "[Time] later: [Amazing outcome]"
- Visual: Happy ending
- Golden hour lighting, joy

SCENE 5 (55-60s): CTA
- Text: "Every dog can change ❤️"
- Inspirational close
- Follow for more stories
"""
    },

    "quick_tip": {
        "name": "Quick Tip",
        "retention": 90,
        "best_for": "Loop-friendly, high saves",
        "structure": """
SCENE 1 (0-3s): Ultra-fast hook
- Text: "This 5-second trick [solves problem]"
- Visual: Problem in action
- Immediate value promise

SCENE 2 (3-30s): The trick (fast demo)
- Text: "Just do THIS:"
- Visual: Step-by-step (3-4 steps max)
- Clear, simple demo

SCENE 3 (30-40s): Why it works
- Text: "Why this works:"
- Visual: Simple diagram/explanation
- 1-sentence science

SCENE 4 (40-45s): CTA
- Text: "Save this for later 💾"
- Save CTA (algorithm boost)
- Follow for more hacks

STYLE: Fast-paced, trending sound, minimal text, repeatable
"""
    },

    "emotional": {
        "name": "Emotional Arc",
        "retention": 75,
        "best_for": "Shares, brand loyalty",
        "structure": """
SCENE 1 (0-8s): The problem (heart-breaking)
- Text: "[Sad situation] that broke my heart..."
- Visual: Emotional imagery
- Slow motion, sad music

SCENE 2 (8-25s): The journey
- Text: "But [person] didn't give up..."
- Visual: Effort, bonding moments
- Building hope

SCENE 3 (25-45s): The transformation
- Text: "Look at [dog/situation] now"
- Visual: Happy outcome
- Music peak, joy

SCENE 4 (45-60s): The lesson
- Text: "[Moral of story]"
- Universal message
- Follow CTA

STYLE: Cinematic, heartwarming, storytelling focus
"""
    },

    "controversial": {
        "name": "Controversial Take",
        "retention": 88,
        "best_for": "Comments, engagement",
        "structure": """
SCENE 1 (0-5s): Hot take
- Text: "Unpopular opinion: [controversial statement]"
- Visual: Bold text, attention-grabbing
- Pattern interrupt

SCENE 2 (5-25s): The argument
- Text: "Here's why [stance]"
- Visual: Evidence, data, expert clips
- Build case with facts

SCENE 3 (25-45s): Address objections
- Text: "But what about [common counter]?"
- Visual: Debunk with science
- Strengthen position

SCENE 4 (45-55s): The verdict
- Text: "The science is clear:"
- Visual: Conclusion statement
- Authority close

SCENE 5 (55-60s): CTA
- Text: "Agree or disagree? 👇"
- Comment bait
- Argument = algorithm boost

STYLE: Bold, confident, data-backed, debate-worthy
"""
    }
}

# Fallback topics if keywords file missing
DOG_TOPICS = [
    "stop dog jumping on people",
    "stop dog barking excessively", 
    "puppy biting and nipping",
    "dog pulling on leash",
    "dog not coming when called",
    "aggressive dog toward strangers",
    "dog separation anxiety",
    "potty training puppy fast",
    "stop dog chewing furniture",
    "fearful rescue dog training"
]

# ============================================================================
# STATE MANAGEMENT (unchanged)
# ============================================================================

def load_cleverdogmethod_keywords():
    if not KEYWORDS_FILE.exists():
        print("⚠️ Keywords V2 file not found, using fallback topics")
        return []
    
    with open(KEYWORDS_FILE) as f:
        content = f.read()
    
    keywords = []
    for line in content.split('\n'):
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and parts[1] and parts[1] != 'Keyword' and not parts[1].startswith('-'):
                keywords.append(parts[1])
    
    return keywords

def load_state():
    if not STATE_FILE.exists():
        return []
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return []

def save_state(topic, formula):
    state = load_state()
    state.append({
        "topic": topic,
        "formula": formula,
        "generated_at": datetime.now().isoformat()
    })
    
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def select_next_topic():
    keywords = load_cleverdogmethod_keywords()
    if not keywords:
        import random
        return random.choice(DOG_TOPICS)
    
    state = load_state()
    cooldown_date = datetime.now() - timedelta(days=COOLDOWN_DAYS)
    
    used_recent = {
        entry['topic'] for entry in state
        if datetime.fromisoformat(entry['generated_at']) > cooldown_date
    }
    
    available = [k for k in keywords if k not in used_recent]
    
    if not available:
        print(f"⚠️ All keywords used in last {COOLDOWN_DAYS} days, cycling back")
        available = keywords
    
    selected = available[0]
    print(f"✅ Auto-selected: {selected}")
    print(f"   Available pool: {len(available)} topics")
    print(f"   Used recently: {len(used_recent)} topics")
    
    return selected

def auto_select_formula(topic):
    topic_lower = topic.lower()
    
    if any(word in topic_lower for word in ['stop', 'fix', 'prevent', 'how to']):
        return 'quick_tip'
    
    if any(breed in topic_lower for breed in ['labrador', 'husky', 'german shepherd', 'chihuahua', 'poodle']):
        return 'problem_solution'
    
    if any(word in topic_lower for word in ['rescue', 'fearful', 'anxiety', 'aggressive']):
        return 'transformation'
    
    if any(word in topic_lower for word in ['training', 'method', 'technique', 'approach']):
        return 'myth_buster'
    
    return 'problem_solution'

# ============================================================================
# REFACTORED: SINGLE VIDEO PROMPT + MULTI-PLATFORM METADATA
# ============================================================================

def build_universal_video_prompt(topic: str, formula: dict) -> str:
    """Build system prompt for universal 60s video (used on all platforms)"""
    
    return f"""You are a viral dog training video expert creating ONE universal 60-second video prompt that works across ALL platforms (TikTok, Instagram Reels, YouTube Shorts).

**TOPIC:** {topic}
**FORMULA:** {formula['name']} (Retention: {formula['retention']}%)

**FORMULA STRUCTURE:**
{formula['structure']}

**UNIVERSAL REQUIREMENTS (all platforms):**
- 60 seconds MAX (scenes must total 60s exactly)
- 9:16 vertical format
- Hook in first 3 seconds (critical for retention)
- Fast cuts every 2-3 seconds
- Dog training educational content
- Family-friendly (all ages)
- Clear, actionable advice
- Focus on positive reinforcement

**TARGET AUDIENCE:** Dog owners struggling with {topic}, want quick wins

**OUTPUT FORMAT:**
Generate a COMPACT, CapCut-ready video prompt with:

1. **HOOK** (0-3s): First line that appears in feed
2. **SCENE-BY-SCENE** (with exact timing, visual descriptions, text overlays)
3. **AUDIO/MUSIC** recommendations
4. **STYLE NOTES** (pacing, effects, transitions)

Keep it CONCISE and ACTIONABLE. Target <2000 characters for CapCut AI compatibility.

Generate the universal video prompt now."""

def build_metadata_prompt(topic: str) -> str:
    """Build system prompt for 3 platform-specific metadata sets"""
    
    return f"""You are a social media optimization expert. Generate THREE platform-specific metadata sets for the same dog training video.

**VIDEO TOPIC:** {topic}
**NICHE:** Dog training, educational, problem-solving
**TARGET AUDIENCE:** Dog owners, pet parents, ages 25-55

**YOUR TASK:** Create optimized metadata for each platform:

**1. TIKTOK METADATA**
- Title: 60 chars max, hook-driven, emoji-friendly
- Description: 150 chars max, conversational, question or challenge
- Hashtags: 7 total (3 broad + 4 niche, trending-aware)
- Requirements: Casual tone, Gen Z friendly, comment bait

**2. INSTAGRAM METADATA**
- Title: 60 chars max, aesthetic, value-focused
- Caption: 200 chars max, storytelling angle, relatable
- Hashtags: 15 total (5 broad + 10 niche, community tags)
- Requirements: Visual emphasis, save-worthy, longer form OK

**3. YOUTUBE METADATA**
- Title: 70 chars max, SEO-optimized, keyword-rich, colon format
- Description: 300 chars max, informative, structured, CTA included
- Hashtags: 5 total (#Shorts mandatory + 4 relevant)
- Requirements: Search-optimized, professional, pinned comment CTA

**CONTENT GUIDELINES:**
- Educational, helpful tone
- Avoid clickbait or misleading claims
- Focus on practical value
- CTA: Follow for daily tips / link in bio for training guide

**OUTPUT FORMAT:**
```
# TIKTOK METADATA
Title: [60 chars]
Description: [150 chars]
Hashtags: [7 tags]

# INSTAGRAM METADATA
Title: [60 chars]
Caption: [200 chars]
Hashtags: [15 tags]

# YOUTUBE METADATA
Title: [70 chars]
Description: [300 chars]
Hashtags: [5 tags]
Pinned Comment: [CTA for engagement]
```

Generate metadata for all 3 platforms now. Keep character counts strict."""

def generate_universal_video_prompt(topic: str, formula: dict) -> str:
    """Generate ONE video prompt for all platforms (API call #1)"""
    
    system_prompt = build_universal_video_prompt(topic, formula)
    
    print(f"   🎬 Generating universal 60s video prompt...")
    
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
                    {"role": "user", "content": system_prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 2048
            },
            timeout=90
        )
        
        if response.status_code == 200:
            generated = response.json()['choices'][0]['message']['content']
            
            # Refine for CapCut AI clarity (compact mode)
            if REFINEMENT_AVAILABLE:
                print(f"   🔄 Compacting video prompt...")
                generated = refine_prompt(generated, "universal", compact_mode=True)
                char_count = len(generated)
                print(f"   ✨ Video prompt: {char_count} chars")
            
            return generated
        else:
            return f"❌ Error: {response.status_code}"
            
    except Exception as e:
        return f"❌ Exception: {e}"

def generate_platform_metadata(topic: str) -> str:
    """Generate 3 platform metadata sets in ONE call (API call #2)"""
    
    system_prompt = build_metadata_prompt(topic)
    
    print(f"   📊 Generating 3 platform metadata sets...")
    
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
                    {"role": "user", "content": system_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=120
        )
        
        if response.status_code == 200:
            generated = response.json()['choices'][0]['message']['content']
            char_count = len(generated)
            print(f"   ✨ Metadata: {char_count} chars (all 3 platforms)")
            return generated
        else:
            return f"❌ Error: {response.status_code}"
            
    except Exception as e:
        return f"❌ Exception: {e}"

def generate_complete_package(topic: str, formula_key: str) -> dict:
    """Generate 1 video + 3 metadata sets (2 API calls total)"""
    
    formula = FORMULAS[formula_key]
    
    print(f"\n🎬 Generating shorts package")
    print(f"📌 Topic: {topic}")
    print(f"🎯 Formula: {formula['name']}")
    print(f"📱 Output: 1 video prompt + 3 platform metadata sets\n")
    
    # API CALL #1: Universal video prompt
    video_prompt = generate_universal_video_prompt(topic, formula)
    if video_prompt.startswith("❌"):
        print(f"   ✗ Video generation failed: {video_prompt}")
        return None
    
    # API CALL #2: All platform metadata
    metadata = generate_platform_metadata(topic)
    if metadata.startswith("❌"):
        print(f"   ✗ Metadata generation failed: {metadata}")
        return None
    
    # Calculate total size
    total_chars = len(video_prompt) + len(metadata)
    print(f"\n✅ Package complete: {total_chars} total chars")
    
    # Check size constraint
    if total_chars > 3000:
        print(f"   ⚠️  WARNING: Total size {total_chars} chars exceeds 3K target")
    
    return {
        'video_prompt': video_prompt,
        'metadata': metadata,
        'formula': formula,
        'topic': topic,
        'total_chars': total_chars
    }

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_output(package: dict) -> str:
    """Format final output with clear sections"""
    
    video_prompt = package['video_prompt']
    metadata = package['metadata']
    formula = package['formula']
    topic = package['topic']
    total_chars = package['total_chars']
    
    output = f"""🎬 **VIRAL SHORT PACKAGE**

📌 **Topic:** {topic}
🎯 **Formula:** {formula['name']} ({formula['retention']}% retention)
📊 **API Calls:** 2 (saved 66% vs old method)

{'='*70}

# VIDEO PROMPT (USE ON ALL PLATFORMS)
**Copy this to CapCut AI / Runway / Luma:**

{video_prompt}

{'='*70}

# PLATFORM-SPECIFIC METADATA

{metadata}

{'='*70}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Total Size:** {total_chars} characters {'✅' if total_chars <= 3000 else '⚠️'}
**Ready for:** CapCut AI, Runway, Luma, manual production
**Deploy:** Use same video on all 3 platforms, customize metadata only
"""
    
    return output

# ============================================================================
# TELEGRAM DELIVERY
# ============================================================================

def send_telegram(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT,
                "text": message,
                "parse_mode": "Markdown",
                "disable_notification": False
            },
            timeout=10
        )
        print("✅ Sent to Telegram")
    except Exception as e:
        print(f"⚠️ Telegram failed: {e}")

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate viral shorts prompts - REFACTORED VERSION",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
REFACTORED: 1 video prompt + 3 platform metadata (2 API calls vs 6)

Examples:
  %(prog)s                                    # Auto-select from keywords
  %(prog)s "stop dog jumping"                 # Manual topic
  %(prog)s "husky training" --formula myth_buster  # Force formula
  %(prog)s --random                           # Random fallback topic
  %(prog)s --list-formulas                    # Show available formulas
        """
    )
    
    parser.add_argument("topic", nargs="?", help="Dog training topic (optional - auto-selects if not provided)")
    parser.add_argument("--formula", choices=list(FORMULAS.keys()), help="Force specific formula (default: auto-match)")
    parser.add_argument("--random", action="store_true", help="Pick random fallback topic")
    parser.add_argument("--list-formulas", action="store_true", help="List available formulas")
    
    args = parser.parse_args()
    
    # List formulas
    if args.list_formulas:
        print("\n🎬 AVAILABLE FORMULAS:\n")
        for key, formula in FORMULAS.items():
            print(f"  {key}")
            print(f"    Name: {formula['name']}")
            print(f"    Retention: {formula['retention']}%")
            print(f"    Best for: {formula['best_for']}\n")
        return
    
    # Header
    print("\n" + "="*70)
    print("🎬 VIRAL SHORTS GENERATOR - REFACTORED")
    print("="*70)
    
    # Pick topic
    if args.random:
        import random
        topic = random.choice(DOG_TOPICS)
        print(f"🎲 Random fallback topic: {topic}")
    elif args.topic:
        topic = args.topic
        print(f"📌 Manual topic: {topic}")
    else:
        topic = select_next_topic()
    
    # Auto-select formula if not specified
    if args.formula:
        formula_key = args.formula
        print(f"🎯 Manual formula: {FORMULAS[formula_key]['name']}")
    else:
        formula_key = auto_select_formula(topic)
        print(f"🎯 Auto-matched formula: {FORMULAS[formula_key]['name']}")
    
    # Generate complete package (2 API calls)
    package = generate_complete_package(topic, formula_key)
    
    if not package:
        print("\n✗ Generation failed")
        sys.exit(1)
    
    # Save to state
    save_state(topic, formula_key)
    
    # Format output
    output_text = format_output(package)
    
    # Display
    print("\n" + "="*70)
    print(output_text)
    print("="*70)
    
    # Send to Telegram
    send_telegram(output_text)
    
    print("\n✅ Complete! 2 API calls (saved 66% cost)")

if __name__ == "__main__":
    main()
