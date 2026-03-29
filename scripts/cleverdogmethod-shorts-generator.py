#!/usr/bin/env python3
"""
CleverDogMethod - Shorts Script Generator

Generates ready-to-use scripts and CapCut AI prompts for dog training shorts.
Pulls content from CleverDogMethod blog posts.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OUTPUT_DIR = Path("/root/.openclaw/workspace/output/cleverdogmethod-shorts")
STATE_FILE = Path("/root/.openclaw/workspace/.state/shorts-generated.json")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# ============================================================================
# SCRIPT GENERATION
# ============================================================================

def generate_short_script(topic):
    """
    Generate 30-45 second script for dog training short
    """
    print(f"📝 Generating script for: {topic}...")
    
    prompt = f"""Create a viral YouTube Short script for dog training content.

Topic: {topic}

Requirements:
- 30-45 seconds when read (150-200 words max)
- Hook in first 3 seconds (problem-based)
- 1 specific, actionable tip
- Before/after implicit
- Conversational tone (not lecture-y)
- End with clear CTA

Structure:
[0-3s] HOOK - State the problem (relatable)
[3-8s] WHY - Quick explanation
[8-35s] SOLUTION - Specific step-by-step (3 simple steps max)
[35-45s] RESULT + CTA - What happens when you do this + follow for more

Format as:
HOOK: "..."
WHY: "..."
STEP 1: "..."
STEP 2: "..."
STEP 3: "..."
RESULT: "..."
CTA: "..."

Make it feel like a friend sharing a hack, not a textbook. Use "you" and "your dog" throughout.

Return ONLY the script in the format above, no explanations."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            script = data['choices'][0]['message']['content'].strip()
            return script
        else:
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

# ============================================================================
# CAPCUT AI PROMPT GENERATION
# ============================================================================

def generate_capcut_prompt(script, topic):
    """
    Generate detailed CapCut AI prompt for video generation
    """
    print(f"🎬 Generating CapCut prompt...")
    
    prompt = f"""Create a detailed CapCut AI video generation prompt.

Topic: {topic}

Script:
{script}

Generate a prompt for CapCut AI that will create a professional dog training short video.

Requirements:
- Describe visual scenes for each section
- Specify camera angles and movements
- Describe text overlay style
- Mention pacing and transitions
- Include mood/tone direction

Format as a single cohesive prompt that CapCut AI can understand.

Example format:
"Create a 45-second vertical video (9:16) for dog training. Open with close-up of frustrated dog owner being pulled on leash, text overlay 'Your Dog Pulls? Try This ⬇️' in bold white font with dark outline. Cut to medium shot of professional trainer demonstrating proper technique, showing 3 clear steps with numbered text overlays. Include quick cuts between demonstration angles. End with side-by-side before/after comparison, dog walking calmly. Upbeat background music. Professional but friendly tone. End screen: 'CleverDogMethod.com' logo."

Return ONLY the CapCut prompt, ready to copy/paste."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            capcut_prompt = data['choices'][0]['message']['content'].strip()
            # Remove any markdown artifacts
            capcut_prompt = capcut_prompt.replace('```', '').replace('"', '').strip()
            return capcut_prompt
        else:
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def save_short_package(topic, script, capcut_prompt):
    """
    Save script and CapCut prompt as ready-to-use package
    """
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    slug = topic.lower().replace(' ', '-')[:50]
    
    output_file = OUTPUT_DIR / f"{timestamp}-{slug}.txt"
    
    content = f"""# CleverDogMethod Short - {topic}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

{'='*60}
SCRIPT (Copy to CapCut script input)
{'='*60}

{script}

{'='*60}
CAPCUT AI PROMPT (Copy to CapCut AI generator)
{'='*60}

{capcut_prompt}

{'='*60}
PRODUCTION NOTES
{'='*60}

Video Specs:
- Duration: 30-45 seconds
- Format: 9:16 (vertical)
- Resolution: 1080x1920
- FPS: 30
- Music: Upbeat, subtle (royalty-free from CapCut library)

Text Overlay Style:
- Font: Bold, sans-serif (Montserrat or similar)
- Color: White with dark outline
- Size: Large (readable on mobile)
- Position: Center or lower third
- Animation: Pop-in or slide-in

Pacing:
- Quick cuts (3-5 seconds per scene)
- Match voiceover timing
- Sync text with key words

CTA:
- End screen: "CleverDogMethod.com"
- Duration: 3-5 seconds
- Logo + website URL

{'='*60}

Ready to create in CapCut:
1. Open CapCut
2. New Project → Vertical (9:16)
3. Paste script (if using text-to-video)
4. OR paste CapCut AI prompt
5. Generate
6. Review & tweak
7. Export 1080p
8. Upload to YouTube Shorts

"""
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Saved: {output_file.name}\n")
    
    # Update state
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = []
    
    state.append({
        'topic': topic,
        'file': str(output_file),
        'generated_at': datetime.now().isoformat()
    })
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    return output_file

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Generate shorts scripts and CapCut prompts
    """
    print("=" * 60)
    print("CLEVERDOGMETHOD - SHORTS GENERATOR")
    print("=" * 60)
    print()
    
    # Top viral topics for dog training shorts
    topics = [
        "How to Stop Leash Pulling in 30 Seconds",
        "The 3 Commands Every Puppy Needs by 6 Months",
        "Why Your Dog Jumps on Guests (And How to Fix It)",
        "Puppy Biting? Try This Immediate Solution",
        "The Recall Training Trick That Actually Works",
        "Stop Your Dog From Barking at the Doorbell",
        "The Body Language Sign Your Dog is Stressed",
        "How to Teach Your Dog to Stay (5 Minute Method)",
        "Why Your Dog Pulls You to Every Dog They See",
        "The Crate Training Mistake 90% of Owners Make"
    ]
    
    print(f"📊 Will generate {len(topics)} short scripts + CapCut prompts\n")
    
    generated = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] {topic}")
        print("-" * 60)
        
        # Generate script
        script = generate_short_script(topic)
        
        if not script:
            print("✗ Script generation failed, skipping\n")
            continue
        
        # Generate CapCut prompt
        capcut_prompt = generate_capcut_prompt(script, topic)
        
        if not capcut_prompt:
            print("✗ CapCut prompt generation failed, skipping\n")
            continue
        
        # Save package
        output_file = save_short_package(topic, script, capcut_prompt)
        
        generated.append({
            'topic': topic,
            'file': str(output_file)
        })
    
    print("\n" + "=" * 60)
    print(f"✅ GENERATION COMPLETE")
    print("=" * 60)
    print(f"\nGenerated {len(generated)} short packages")
    print(f"\nLocation: {OUTPUT_DIR}/")
    print("\nEach file contains:")
    print("  - Ready-to-use script")
    print("  - CapCut AI prompt")
    print("  - Production notes")
    print("\nCopy/paste into CapCut and generate! 🎬\n")

if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY not set")
        sys.exit(1)
    
    main()
