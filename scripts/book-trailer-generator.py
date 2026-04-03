#!/usr/bin/env python3
"""
Book Trailer Generator for Mind Crimes - REFACTORED
ONE video prompt + THREE platform metadata sets
Saves 66% API costs (2 calls vs 6)
"""

import os
import sys
import json
import yaml
import re
import requests
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path("/root/.openclaw/workspace")

# Import refinement utilities
try:
    from refine_utils import refine_prompt
    REFINEMENT_AVAILABLE = True
except ImportError:
    REFINEMENT_AVAILABLE = False

DATA_DIR = WORKSPACE / "data"
STATE_FILE = WORKSPACE / ".state/trailers-generated.json"
BOOKS_DIR = Path("/opt/mind-crimes-automation/data/books")
OUTPUT_DIR = WORKSPACE / "output/mind-crimes-trailers"

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "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")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT_TOKEN", "8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "8116230130")

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATA LOADING (unchanged)
# ============================================================================

def load_formulas() -> Dict:
    with open(DATA_DIR / "formulas.yaml") as f:
        return yaml.safe_load(f)

def load_hashtags() -> Dict:
    with open(DATA_DIR / "hashtags.yaml") as f:
        return yaml.safe_load(f)

def load_compliance() -> Dict:
    with open(DATA_DIR / "compliance-filters.yaml") as f:
        return yaml.safe_load(f)

def load_mapping() -> Dict:
    with open(DATA_DIR / "book-formula-mapping.yaml") as f:
        return yaml.safe_load(f)

def load_state() -> List:
    if not STATE_FILE.exists():
        return []
    with open(STATE_FILE) as f:
        return json.load(f)

def save_state(book_name: str, formula: str):
    state = load_state()
    state.append({
        'book': book_name,
        'formula': formula,
        'platforms': ['tiktok', 'instagram', 'youtube'],  # All platforms from single prompt
        'generated_at': datetime.now().isoformat()
    })
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# ============================================================================
# BOOK DISCOVERY (unchanged)
# ============================================================================

def discover_books() -> List[Dict]:
    books = []
    for research_file in BOOKS_DIR.glob("*/research.md"):
        book_num = research_file.parent.name
        book_name = f"Book-{book_num}"
        books.append({
            'name': book_name,
            'slug': f"book-{book_num}",
            'research_file': research_file
        })
    return books

def select_book(books: List[Dict], force_book: Optional[str] = None) -> Optional[Dict]:
    if not books:
        return None
    
    if force_book:
        for book in books:
            if force_book.lower() in book['slug'].lower():
                return book
        print(f"⚠️  Book '{force_book}' not found")
        return None
    
    state = load_state()
    cooldown_date = datetime.now() - timedelta(days=7)
    used_recent = {
        entry['book'] for entry in state
        if datetime.fromisoformat(entry['generated_at']) > cooldown_date
    }
    
    available = [b for b in books if b['name'] not in used_recent]
    
    if available:
        return available[0]
    else:
        if state:
            oldest_book_name = sorted(state, key=lambda x: x['generated_at'])[0]['book']
            return next((b for b in books if b['name'] == oldest_book_name), books[0])
        return books[0]

# ============================================================================
# METADATA EXTRACTION (unchanged)
# ============================================================================

def extract_book_metadata(research_file: Path) -> Dict:
    with open(research_file) as f:
        content = f.read().lower()
    
    metadata = {
        'case_type': 'cold_case',
        'killer_relationship': 'unknown',
        'resolution_year': None,
        'forensic_method': '',
        'famous_comparison': '',
        'years_unsolved': 0,
        'victim_name': '',
        'location': '',
        'hook_detail': ''
    }
    
    relationship_patterns = [
        (r'affair|mistress|lover', 'affair'),
        (r'husband|wife|spouse|married', 'spouse'),
        (r'neighbor', 'neighbor'),
        (r'family|brother|sister|parent', 'family'),
        (r'friend|roommate', 'friend'),
        (r'stranger|unknown|random', 'stranger')
    ]
    
    for pattern, rel in relationship_patterns:
        if re.search(pattern, content):
            metadata['killer_relationship'] = rel
            break
    
    crime_year_match = re.search(r'(\d{4}).*?(?:murder|crime|death|killed)', content)
    solve_year_match = re.search(r'(?:arrest|solve|convict).*?(\d{4})', content)
    
    if solve_year_match:
        metadata['resolution_year'] = int(solve_year_match.group(1))
    
    if crime_year_match and solve_year_match:
        crime_year = int(crime_year_match.group(1))
        solve_year = int(solve_year_match.group(1))
        metadata['years_unsolved'] = solve_year - crime_year
    
    forensic_patterns = [
        'dna genealogy', 'familial dna', 'genetic genealogy',
        'dna', 'fingerprint', 'fiber', 'hair', 'wig',
        'surveillance', 'phone records', 'digital forensics'
    ]
    
    for pattern in forensic_patterns:
        if pattern in content:
            metadata['forensic_method'] = pattern
            break
    
    location_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s+([A-Z]{2})', content)
    if location_match:
        metadata['location'] = f"{location_match.group(1)}, {location_match.group(2)}"
    
    return metadata

def extract_book_context(research_file: Path) -> Dict:
    with open(research_file) as f:
        content = f.read()
    
    metadata = extract_book_metadata(research_file)
    
    victim_match = re.search(r'victim[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)', content, re.IGNORECASE)
    if victim_match:
        metadata['victim_name'] = victim_match.group(1)
    
    if metadata['victim_name'] and metadata['years_unsolved']:
        metadata['one_sentence'] = (
            f"{metadata['victim_name']} was murdered {metadata['years_unsolved']} years ago. "
            f"Then {metadata['forensic_method']} revealed the shocking truth."
        )
    else:
        metadata['one_sentence'] = f"A cold case solved by {metadata['forensic_method']}."
    
    return metadata

# ============================================================================
# FORMULA MATCHING (unchanged)
# ============================================================================

def match_book_to_formula(metadata: Dict) -> str:
    betrayal_keywords = ['spouse', 'affair', 'husband', 'wife', 'partner', 'family', 'friend', 'neighbor']
    if any(kw in metadata['killer_relationship'] for kw in betrayal_keywords):
        return 'villain_reveal'
    
    if metadata['resolution_year'] and metadata['resolution_year'] >= 2015:
        if metadata['years_unsolved'] >= 10:
            return 'news_hook'
    
    dna_keywords = ['dna genealogy', 'familial dna', 'genetic', 'ancestry']
    if any(kw in metadata['forensic_method'] for kw in dna_keywords):
        return 'science_angle'
    
    evidence_keywords = ['wig', 'fiber', 'bite mark', 'surveillance', 'phone']
    if any(kw in metadata['forensic_method'] for kw in evidence_keywords):
        return 'evidence_reveal'
    
    return 'victim_story'

# ============================================================================
# REFACTORED: SINGLE VIDEO PROMPT + MULTI-PLATFORM METADATA
# ============================================================================

def build_universal_video_prompt(formula: Dict, context: Dict) -> str:
    """Build system prompt for universal 60s video (used on all platforms)"""
    
    formula_structure = "\n".join([
        f"SCENE {i+1} ({scene['timing']}): {scene.get('purpose', scene.get('hook_type', 'Scene'))} - {scene.get('text_template', '')}"
        for i, (scene_key, scene) in enumerate(formula['structure'].items())
    ])
    
    return f"""You are a viral true crime video expert creating ONE universal 60-second video prompt that works across ALL platforms (TikTok, Instagram, YouTube Shorts).

**FORMULA:** {formula['name']} (Target Retention: {formula['retention']}%)

**BOOK CONTEXT:**
- Victim: {context.get('victim_name', 'Unknown')}
- Location: {context.get('location', 'Unknown')}
- Years unsolved: {context.get('years_unsolved', 'Multiple')}
- Forensic method: {context.get('forensic_method', 'Investigation')}
- Relationship: {context.get('killer_relationship', 'Unknown')}

**FORMULA STRUCTURE:**
{formula_structure}

**UNIVERSAL REQUIREMENTS (all platforms):**
- 60 seconds MAX (scenes must total 60s exactly)
- 9:16 vertical format
- Hook in first 3 seconds (critical for retention)
- Fast cuts every 2-3 seconds
- NO graphic violence or gore
- Victim-respectful framing ALWAYS
- Family-approval test: Would victim's family object?
- Focus on justice, not sensationalism

**OUTPUT FORMAT:**
Generate a COMPACT, CapCut-ready video prompt with:

1. **HOOK** (0-3s): First line that appears in feed
2. **SCENE-BY-SCENE** (with exact timing, visual descriptions, text overlays)
3. **AUDIO/MUSIC** recommendations
4. **STYLE NOTES** (pacing, effects, transitions)

Keep it CONCISE and ACTIONABLE. Target <2000 characters for CapCut AI compatibility.

Generate the universal video prompt now."""

def build_metadata_prompt(context: Dict) -> str:
    """Build system prompt for 3 platform-specific metadata sets"""
    
    return f"""You are a social media optimization expert. Generate THREE platform-specific metadata sets for the same video.

**VIDEO CONTEXT:**
- Book: Mind Crimes - {context.get('victim_name', 'True Crime')} case
- Hook: {context.get('one_sentence', 'A cold case solved')}
- Genre: True crime, cold case, forensic investigation
- Target audience: True crime enthusiasts, documentary fans, ages 25-45

**YOUR TASK:** Create optimized metadata for each platform:

**1. TIKTOK METADATA**
- Title: 60 chars max, hook-driven, emoji-friendly
- Description: 150 chars max, conversational, intrigue
- Hashtags: 7 total (3 broad + 4 niche, trending-aware)
- Requirements: Casual tone, Gen Z friendly, comment bait

**2. INSTAGRAM METADATA**
- Title: 60 chars max, aesthetic, story-focused
- Caption: 200 chars max, emotional angle, story-driven
- Hashtags: 15 total (5 broad + 10 niche, community tags)
- Requirements: Visual emphasis, save-worthy, longer form OK

**3. YOUTUBE METADATA**
- Title: 70 chars max, SEO-optimized, keyword-rich, colon format
- Description: 300 chars max, informative, structured, CTA included
- Hashtags: 5 total (#Shorts mandatory + 4 relevant)
- Requirements: Search-optimized, professional, pinned comment CTA

**COMPLIANCE (all platforms):**
- Victim-respectful language
- No sensationalism or glorification
- Focus on justice/forensics, not gore
- CTA: Link in bio → Amazon book

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
Pinned Comment: [CTA for link in bio]
```

Generate metadata for all 3 platforms now. Keep character counts strict."""

def generate_universal_video_prompt(book: Dict, formula_key: str) -> Optional[str]:
    """Generate ONE video prompt for all platforms (API call #1)"""
    
    formulas = load_formulas()
    formula = formulas[formula_key]
    book_context = extract_book_context(book['research_file'])
    
    system_prompt = build_universal_video_prompt(formula, book_context)
    
    print(f"   🎬 Generating universal 60s video prompt...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [
                    {"role": "user", "content": system_prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 2048
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            generated = result["choices"][0]["message"]["content"]
            
            # Refine for CapCut AI clarity (compact mode)
            if REFINEMENT_AVAILABLE:
                print(f"   🔄 Compacting video prompt...")
                generated = refine_prompt(generated, "universal", compact_mode=True)
                char_count = len(generated)
                print(f"   ✨ Video prompt: {char_count} chars")
            
            return generated
        else:
            print(f"   ✗ OpenRouter error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return None

def generate_platform_metadata(book: Dict) -> Optional[str]:
    """Generate 3 platform metadata sets in ONE call (API call #2)"""
    
    book_context = extract_book_context(book['research_file'])
    system_prompt = build_metadata_prompt(book_context)
    
    print(f"   📊 Generating 3 platform metadata sets...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [
                    {"role": "user", "content": system_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            generated = result["choices"][0]["message"]["content"]
            char_count = len(generated)
            print(f"   ✨ Metadata: {char_count} chars (all 3 platforms)")
            return generated
        else:
            print(f"   ✗ OpenRouter error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return None

def generate_complete_package(book: Dict, formula_key: str) -> Optional[Dict]:
    """Generate 1 video + 3 metadata sets (2 API calls total)"""
    
    formulas = load_formulas()
    formula = formulas[formula_key]
    
    print(f"\n📹 Generating trailer package for: {book['name']}")
    print(f"🎯 Formula: {formula_key}")
    print(f"📱 Output: 1 video prompt + 3 platform metadata sets\n")
    
    # API CALL #1: Universal video prompt
    video_prompt = generate_universal_video_prompt(book, formula_key)
    if not video_prompt:
        print("   ✗ Video generation failed")
        return None
    
    # API CALL #2: All platform metadata
    metadata = generate_platform_metadata(book)
    if not metadata:
        print("   ✗ Metadata generation failed")
        return None
    
    # Calculate total size
    total_chars = len(video_prompt) + len(metadata)
    print(f"\n✅ Package complete: {total_chars} total chars")
    
    return {
        'video_prompt': video_prompt,
        'metadata': metadata,
        'formula': formula,
        'book': book
    }

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_output(package: Dict) -> str:
    """Format final output with clear sections"""
    
    video_prompt = package['video_prompt']
    metadata = package['metadata']
    formula = package['formula']
    book = package['book']
    
    output = f"""📹 **BOOK TRAILER PACKAGE**

📚 **Book:** {book['name']}
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
**Total Size:** {len(video_prompt) + len(metadata)} characters
**Ready for:** CapCut AI, Runway, Luma, manual production
**Deploy:** Use same video on all 3 platforms, customize metadata only
"""
    
    return output

def save_output(package: Dict):
    """Save results to file"""
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    slug = package['book']['slug']
    formula_key = list(load_formulas().keys())[list(load_formulas().values()).index(package['formula'])]
    
    output_file = OUTPUT_DIR / f"{timestamp}-{slug}-{formula_key}-REFACTORED.txt"
    
    content = format_output(package)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"\n💾 Saved to: {output_file}")
    return output_file

# ============================================================================
# COMPLIANCE VALIDATION
# ============================================================================

def validate_compliance(prompt: str) -> Tuple[bool, List[str]]:
    compliance = load_compliance()
    issues = []
    
    prompt_lower = prompt.lower()
    
    for category, rules in compliance['prohibited_content'].items():
        if 'keywords' in rules:
            for keyword in rules['keywords']:
                if keyword in prompt_lower:
                    issues.append(f"Prohibited: {keyword} ({category})")
    
    required = ['victim', 'justice']
    for term in required:
        if term not in prompt_lower:
            issues.append(f"Missing required element: {term}")
    
    return (len(issues) == 0, issues)

# ============================================================================
# TELEGRAM DELIVERY
# ============================================================================

def send_telegram(message: str):
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print("⚠️  Telegram not configured")
        return False
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT,
                "text": message,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
                json={
                    "chat_id": TELEGRAM_CHAT,
                    "text": message
                },
                timeout=10
            )
        
        if response.status_code == 200:
            print("✅ Sent to Telegram")
            return True
        else:
            print(f"⚠️  Telegram error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Telegram failed: {e}")
        return False

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate viral book trailer prompts - REFACTORED VERSION",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
REFACTORED: 1 video prompt + 3 platform metadata (2 API calls vs 6)

Examples:
  %(prog)s                                    # Auto-select book and formula
  %(prog)s --book "killer-clown"              # Specific book
  %(prog)s --book "8" --formula villain_reveal  # Force formula
  %(prog)s --list-books                       # Show available books
  %(prog)s --list-formulas                    # Show available formulas
  %(prog)s --dry-run                          # Preview without saving state
        """
    )
    
    parser.add_argument("--book", help="Force specific book (partial match)")
    parser.add_argument("--formula", 
                        choices=['news_hook', 'evidence_reveal', 'villain_reveal',
                                'victim_story', 'science_angle', 'comparison_hook'],
                        help="Force specific formula (default: auto-match)")
    parser.add_argument("--list-books", action="store_true",
                        help="List available books and exit")
    parser.add_argument("--list-formulas", action="store_true",
                        help="List available formulas and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate but don't save state")
    parser.add_argument("--no-telegram", action="store_true",
                        help="Skip Telegram notification")
    
    args = parser.parse_args()
    
    # List commands
    if args.list_formulas:
        formulas = load_formulas()
        print("\n📋 Available Formulas:\n")
        for key, formula in formulas.items():
            print(f"  {key:20} - {formula['name']:20} ({formula['retention']}% retention)")
            print(f"  {'':20}   Best for: {formula['best_for']}\n")
        return
    
    if args.list_books:
        books = discover_books()
        print(f"\n📚 Available Books ({len(books)}):\n")
        for book in books:
            print(f"  - {book['name']} ({book['slug']})")
        print()
        return
    
    # Main generation flow
    print("\n" + "="*70)
    print("📹 BOOK TRAILER GENERATOR - REFACTORED")
    print("="*70)
    
    if not OPENROUTER_KEY:
        print("\n✗ Error: OPENROUTER_API_KEY not set")
        sys.exit(1)
    
    books = discover_books()
    if not books:
        print("\n✗ No books found in", BOOKS_DIR)
        sys.exit(1)
    
    book = select_book(books, args.book)
    if not book:
        print("\n✗ No suitable book found")
        sys.exit(1)
    
    metadata = extract_book_metadata(book['research_file'])
    formula_key = args.formula or match_book_to_formula(metadata)
    
    print(f"\n📖 Selected: {book['name']}")
    print(f"🎯 Formula: {formula_key} {'(auto-matched)' if not args.formula else '(forced)'}")
    
    # Generate complete package (2 API calls)
    package = generate_complete_package(book, formula_key)
    
    if not package:
        print("\n✗ Generation failed")
        sys.exit(1)
    
    # Validate compliance
    print("\n🔒 Checking compliance...")
    full_content = package['video_prompt'] + package['metadata']
    is_valid, issues = validate_compliance(full_content)
    if not is_valid:
        print(f"   ⚠️  {len(issues)} compliance issues:")
        for issue in issues:
            print(f"      - {issue}")
    else:
        print(f"   ✓ Compliant")
    
    # Save output
    output_file = save_output(package)
    
    # Format message
    output_text = format_output(package)
    
    # Print to console
    print("\n" + "="*70)
    print(output_text)
    print("="*70)
    
    # Send to Telegram
    if not args.no_telegram:
        send_telegram(output_text)
    
    # Save state
    if not args.dry_run:
        save_state(book['name'], formula_key)
        print(f"\n✅ State saved (7-day cooldown active)")
    else:
        print(f"\n⚠️  Dry run - state not saved")
    
    print(f"\n✅ Complete! 2 API calls (saved 66% cost)")

if __name__ == "__main__":
    main()
