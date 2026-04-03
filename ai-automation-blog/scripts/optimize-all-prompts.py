#!/usr/bin/env python3
"""
Optimize all 15 system prompts using advanced framework
Applies: specificity, constraints, examples, validation, persona, efficiency
"""

import os
import json
import requests
import time
from pathlib import Path

API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
MODEL = "anthropic/claude-sonnet-4"

def optimize_with_claude(name, current_prompt, context):
    """Apply optimization framework via Claude"""
    
    optimization_meta_prompt = f"""You are an expert prompt engineer optimizing AI system prompts.

PROMPT TO OPTIMIZE:
═══════════════════════════════════════════════════════════
Name: {name}
Context: {context}

CURRENT PROMPT:
{current_prompt}
═══════════════════════════════════════════════════════════

APPLY ADVANCED OPTIMIZATION FRAMEWORK:

1. SPECIFICITY UPGRADE:
   - Change ranges to exact targets (800-1200 → 1000 ±100)
   - Break sections into word count targets
   - Replace "include examples" with "include: [specific type] example with [specific data]"
   - Add "what good looks like" concrete examples

2. CONSTRAINT HIERARCHY:
   Structure as:
   
   MUST (critical, will regenerate if violated):
   - [non-negotiable requirement 1]
   - [non-negotiable requirement 2]
   
   SHOULD (important, reduces quality if violated):
   - [strong guideline 1]
   - [strong guideline 2]
   
   AVOID (anti-patterns that hurt quality):
   - [specific phrase/pattern to avoid]
   - [behavior that reduces effectiveness]
   
   MAY (optional enhancements):
   - [nice-to-have 1]

3. OUTPUT VALIDATION:
   Add validation section:
   
   VALID OUTPUT:
   [concrete example of correct format]
   
   INVALID OUTPUT:
   [example of wrong format + why]
   
   VALIDATION RULES:
   - [rule 1: what to check]
   - [rule 2: constraint to verify]

4. PERSONA STRENGTHENING (if content generation):
   Replace "professional tone" with:
   
   VOICE EXAMPLES:
   ❌ Generic: "Consider using automation"
   ✅ Alex Chen: "I cut email time 2h → 15min with this setup"
   
   ❌ Generic: "This could help businesses"
   ✅ Alex Chen: "Tested on 3 businesses, saved $4K/month each"

5. ERROR HANDLING:
   Add explicit edge cases:
   
   HANDLE EDGE CASES:
   IF [condition]: THEN [action]
   IF [condition]: THEN [action]
   ELSE: [fallback]

6. TOKEN EFFICIENCY:
   - Remove filler ("please", "I would like", "in order to")
   - Use bullets instead of prose for lists
   - Abbreviate where clear (e.g., i.e., etc.)
   - Keep "Return ONLY [format]" pattern

DELIVERABLE:

Return the optimized prompt following this structure:

# [PROMPT NAME]

## ROLE
[Who/what this is - specific expertise]

## INPUT
[What data/context is provided - use variable names]

## TASK
[What to generate/analyze - specific outcome]

## REQUIREMENTS

### MUST:
- [critical 1]
- [critical 2]

### SHOULD:
- [important 1]
- [important 2]

### AVOID:
- [anti-pattern 1]
- [anti-pattern 2]

## [CONTENT-SPECIFIC SECTIONS]
[Structure, word counts, etc.]

## OUTPUT FORMAT

VALID:
[example]

INVALID:
[counter-example]

VALIDATION:
- [rule 1]
- [rule 2]

## RETURN
Return ONLY [specific format]. No explanations.

═══════════════════════════════════════════════════════════

CRITICAL: Return ONLY the optimized prompt. No meta-commentary. No explanations. Just the improved prompt text ready to use in production.

Make it 30-50% longer if needed (specificity worth the tokens).
Target: 2x effectiveness, +20% quality, -10% regenerations.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": optimization_meta_prompt}],
        "max_tokens": 6000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

# Define all 15 prompts to optimize
PROMPTS_TO_OPTIMIZE = [
    {
        "name": "Blog Post Generation",
        "context": "Generates 1,000-word blog posts 2x/day. Must score 70+ quality. $0.075/post. Success rate 95% but need more consistency.",
        "current": """You are writing for "AI Automation Builder" - a blog for solopreneurs learning AI automation.

Write a detailed, practical blog post based on this source:

Title: {item['title']}
URL: {item['url']}
Summary: {item['summary']}
Source: {item['source']}

Requirements:
- 800-1200 words
- Practical and actionable (not just news reporting)
- Include specific use cases for solopreneurs
- Add "How to use this" section if it's a tool
- Add "Why this matters" section for news
- Conversational but professional tone
- Include external link to source
- SEO optimized (keywords naturally integrated)

Format as clean HTML (no <html> or <body> tags, just content):
- Use <h2> for main sections
- Use <h3> for subsections
- Use <p> for paragraphs
- Use <ul> and <ol> for lists
- Use <strong> and <em> for emphasis
- Use <code> for technical terms
- Use <a href="..."> for links

Start with a compelling intro paragraph, then break into sections.

Return ONLY the HTML content (no markdown, no code blocks, no explanations)."""
    },
    {
        "name": "Research Breaking News Detection",
        "context": "Runs every 6h, identifies 1-3 breaking stories from 10-15 items. Must return valid JSON. $0.023/run.",
        "current": """You are monitoring AI news for a newsletter.

Identify BREAKING NEWS - stories that:
1. Just happened (last few hours)
2. Are significant for AI builders/solopreneurs
3. Actionable or impactful
4. NOT just announcements or hype

Items to analyze:
{json.dumps(items_summary, indent=2)}

CRITICAL: Respond ONLY with valid JSON. No markdown, no explanation, just JSON.

Format:
{
  "breaking_news": [
    {
      "id": 0,
      "reason": "Why this is breaking",
      "urgency": 9
    }
  ]
}

Only flag 1-3 truly breaking stories max. If none are breaking, return empty array."""
    },
    {
        "name": "Newsletter Weekly Generation",
        "context": "Creates weekly 1,000-word newsletter from 10-15 curated items. Must be coherent and valuable. $0.30/edition.",
        "current": """You are the editor of "AI Automation Insights" - a weekly newsletter for solo founders.

Create this week's newsletter from these curated items:

{top_items}

Newsletter structure:
1. Opening (2-3 sentences - what's the theme this week?)
2. Featured Story (1 main item - deep analysis)
3. Quick Hits (3-5 items - 2 sentences each)
4. Tools Worth Checking (1-2 tools)
5. One Thing to Try This Week (actionable)

Voice:
- Direct, no corporate speak
- Personal but professional
- "We" not "I" (community feeling)
- Opinionated where warranted

Format as clean markdown.
Length: 800-1200 words total.

Return ONLY the newsletter content (no subject line, no metadata)."""
    }
]

def main():
    output_file = Path('/root/.openclaw/workspace/ai-automation-blog/PROMPTS-OPTIMIZED-V3.txt')
    
    print("=" * 60)
    print("🧠 OPTIMIZING FIRST 3 CRITICAL PROMPTS")
    print("=" * 60)
    print()
    
    optimized_prompts = []
    
    for i, prompt_data in enumerate(PROMPTS_TO_OPTIMIZE, 1):
        print(f"{i}. {prompt_data['name']}")
        print(f"   Context: {prompt_data['context']}")
        print(f"   Optimizing...", end=" ", flush=True)
        
        optimized = optimize_with_claude(
            prompt_data['name'],
            prompt_data['current'],
            prompt_data['context']
        )
        
        if optimized:
            print(f"✅ ({len(optimized)} chars)")
            optimized_prompts.append({
                'name': prompt_data['name'],
                'original_length': len(prompt_data['current']),
                'optimized_length': len(optimized),
                'optimized': optimized
            })
            time.sleep(2)  # Rate limiting
        else:
            print("❌ Failed")
        
        print()
    
    # Save results
    with open(output_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("📝 OPTIMIZED PROMPTS V3 - FIRST 3 CRITICAL\n")
        f.write("=" * 60 + "\n\n")
        
        for item in optimized_prompts:
            improvement = ((item['optimized_length'] - item['original_length']) / item['original_length']) * 100
            
            f.write(f"\n{'=' * 60}\n")
            f.write(f"{item['name'].upper()}\n")
            f.write(f"Original: {item['original_length']} chars\n")
            f.write(f"Optimized: {item['optimized_length']} chars ({improvement:+.0f}%)\n")
            f.write(f"{'=' * 60}\n\n")
            f.write(item['optimized'])
            f.write("\n\n")
    
    print("=" * 60)
    print(f"✅ SAVED: {output_file}")
    print(f"   Optimized: {len(optimized_prompts)} prompts")
    print("=" * 60)

if __name__ == '__main__':
    main()
PROMPT_EOF

python3 /tmp/optimize-prompts.py
