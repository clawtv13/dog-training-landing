#!/usr/bin/env python3
"""Generate remaining 5 CleverDogMethod posts"""
import json, requests, re
from pathlib import Path
import time

API_KEY = "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"

# Load topics
with open("/root/.openclaw/workspace/.state/cleverdogmethod-topics-selected.json") as f:
    topics = json.load(f)['topics']

# Skip first (already generated)
remaining = topics[1:6]

print(f"📝 GENERATING POSTS 2-6")
print("="*60)

for i, topic in enumerate(remaining, 2):
    print(f"\n{i}/6: {topic['title']}")
    
    prompt = f"""SEO blog post for CleverDogMethod.com

Title: {topic['title']}
Keywords: {topic['keywords']}

Requirements:
- 1500 words minimum
- SEO optimized (keyword in H1, first paragraph, H2 headings)
- Practical step-by-step advice
- Include 5-question FAQ section
- Add CTA link: https://258e5df6f75r1pezy8tb13r53z.hop.clickbank.net
- Conversational, helpful tone

Output: HTML only (no markdown, no doctype)"""

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4.5",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=180
        )
        
        if r.status_code == 200:
            content = r.json()['choices'][0]['message']['content']
            
            # Extract HTML
            if '```html' in content:
                html = content.split('```html')[1].split('```')[0].strip()
            elif '<article' in content or '<div' in content:
                html = content.strip()
            else:
                html = f"<article>{content}</article>"
            
            # Create slug
            slug = re.sub(r'[^a-z0-9]+', '-', topic['title'].lower()).strip('-')
            
            # Save
            output = Path(f"/root/.openclaw/workspace/content/cleverdogmethod/batch-2026-03-27/{slug}.html")
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            
            words = len(html.split())
            print(f"✅ {slug}.html ({words:,} words)")
        else:
            print(f"❌ API error: {r.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Rate limiting
    if i < 6:
        time.sleep(3)

print("\n✅ Batch generation complete!")
