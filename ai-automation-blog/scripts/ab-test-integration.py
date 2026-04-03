#!/usr/bin/env python3
"""
A/B Test Integration Module
Extends blog-auto-post-v2.py to support prompt A/B testing

This module should be imported by blog-auto-post-v2.py to:
1. Read active A/B test configuration
2. Randomly select prompt variant (50/50 split)
3. Track which variant was used for each post
4. Log results for evaluation
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple

WORKSPACE = Path(__file__).parent.parent
PROMPTS_DIR = WORKSPACE / "prompts"
CANDIDATES_DIR = PROMPTS_DIR / "candidates"
AB_TEST_FILE = PROMPTS_DIR / "ab-test.json"
CURRENT_PROMPT_FILE = PROMPTS_DIR / "blog-generation.txt"

def load_ab_test_config() -> Optional[Dict]:
    """Load active A/B test configuration"""
    if not AB_TEST_FILE.exists():
        return None
    
    try:
        with open(AB_TEST_FILE, 'r') as f:
            config = json.load(f)
        
        # Only return if test is active
        if config.get('status') == 'active':
            return config
        
        return None
    except Exception as e:
        print(f"⚠️  Error loading A/B test config: {e}")
        return None

def select_prompt_variant() -> Tuple[str, str]:
    """
    Select prompt variant for this post
    Returns: (variant_name, prompt_content)
    """
    config = load_ab_test_config()
    
    if not config:
        # No active test, use current prompt
        prompt = read_prompt_file(CURRENT_PROMPT_FILE)
        return ('current', prompt)
    
    # 50/50 random selection
    variant = random.choice(['A', 'B'])
    
    prompt_filename = config['variants'][variant]
    
    if variant == 'A':
        # Variant A is always the current prompt
        prompt_path = CURRENT_PROMPT_FILE
    else:
        # Variant B is a candidate
        prompt_path = CANDIDATES_DIR / prompt_filename
    
    prompt = read_prompt_file(prompt_path)
    
    print(f"🔬 A/B Test: Using variant {variant} ({prompt_filename})")
    
    return (variant, prompt)

def read_prompt_file(path: Path) -> str:
    """Read prompt from file, with fallback to default"""
    if not path.exists():
        print(f"⚠️  Prompt file not found: {path}")
        return get_default_prompt()
    
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"⚠️  Error reading prompt file: {e}")
        return get_default_prompt()

def get_default_prompt() -> str:
    """Fallback default prompt"""
    return """You are an expert tech blogger writing for solopreneurs interested in AI automation.

Write a comprehensive, engaging blog post that:
- Provides actionable insights and practical advice
- Uses clear examples and real-world scenarios
- Maintains a professional yet accessible tone
- Includes concrete steps or recommendations
- Structures content with clear sections and headers

Focus on helping solopreneurs save time and scale their businesses using AI."""

def log_ab_test_result(variant: str, post_slug: str, quality_score: float):
    """Log A/B test result for this post"""
    config = load_ab_test_config()
    
    if not config:
        return
    
    # Update results
    if variant in config['results']:
        config['results'][variant]['posts'] += 1
        config['results'][variant]['total_quality'] += quality_score
        config['results'][variant]['avg_quality'] = (
            config['results'][variant]['total_quality'] / config['results'][variant]['posts']
        )
    
    # Save updated config
    try:
        with open(AB_TEST_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"📊 A/B Test: Logged result for variant {variant} (quality: {quality_score:.2f})")
    except Exception as e:
        print(f"⚠️  Error logging A/B test result: {e}")

def get_ab_test_status() -> str:
    """Get human-readable A/B test status"""
    config = load_ab_test_config()
    
    if not config:
        return "No active A/B test"
    
    test_id = config.get('test_id', 'unknown')
    start_date = config.get('start_date', 'unknown')
    end_date = config.get('end_date', 'unknown')
    
    a_stats = config['results'].get('A', {})
    b_stats = config['results'].get('B', {})
    
    status = f"""
🔬 Active A/B Test: {test_id}
   Started: {start_date[:10]}
   Ends: {end_date[:10]}
   
   Variant A: {a_stats.get('posts', 0)} posts, avg quality {a_stats.get('avg_quality', 0):.2f}
   Variant B: {b_stats.get('posts', 0)} posts, avg quality {b_stats.get('avg_quality', 0):.2f}
"""
    
    return status.strip()

# Example usage for testing
if __name__ == "__main__":
    print("🔬 A/B Test Integration Module")
    print("=" * 60)
    
    # Check status
    print(get_ab_test_status())
    print("")
    
    # Test variant selection
    variant, prompt = select_prompt_variant()
    print(f"Selected variant: {variant}")
    print(f"Prompt preview: {prompt[:200]}...")
    print("")
    
    # Simulate logging result
    log_ab_test_result(variant, "test-post-slug", 75.5)
    print("✅ Test complete")
