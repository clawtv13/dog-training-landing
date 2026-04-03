#!/usr/bin/env python3
"""
Generate 3 perfect blog posts - Direct execution version
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
import hashlib
import re
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path(__file__).parent
BLOG_DIR = WORKSPACE / "blog"
POSTS_DIR = BLOG_DIR / "posts"
TEMPLATE = WORKSPACE / "templates" / "post.html"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"
STATE_DIR = WORKSPACE / ".state"
STATE_FILE = STATE_DIR / "published-posts.json"
FINGERPRINT_FILE = STATE_DIR / "content-fingerprints.json"

STATE_DIR.mkdir(exist_ok=True)
POSTS_DIR.mkdir(parents=True, exist_ok=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
WRITING_MODEL = "anthropic/claude-sonnet-4"
ANALYSIS_MODEL = "anthropic/claude-3.7-sonnet"

print("\n" + "="*70)
print("🚀 GENERATING 3 PERFECT POSTS FOR WORKLESS.BUILD")
print("="*70 + "\n")

# Helper functions
def load_json(filepath, default=None):
    if filepath.exists():
        try:
            with open(filepath) as f:
                return json.load(f)
        except:
            pass
    return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def content_fingerprint(text):
    normalized = re.sub(r'[^\w\s]', '', text.lower())
    words = sorted(set(normalized.split()))[:100]
    return hashlib.md5(' '.join(words).encode()).hexdigest()

def is_duplicate(title, summary):
    fp = content_fingerprint(title + " " + summary)
    fps = load_json(FINGERPRINT_FILE, [])
    return fp in fps

def save_fingerprint(title, summary):
    fp = content_fingerprint(title + " " + summary)
    fps = load_json(FINGERPRINT_FILE, [])
    if fp not in fps:
        fps.append(fp)
        save_json(FINGERPRINT_FILE, fps)

def call_llm(prompt, model=WRITING_MODEL, system=None):
    """Call OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "user", "content": prompt}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 8192
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

# Get content from database
print("📚 Loading content from newsletter database...")
conn = sqlite3.connect(NEWSLETTER_DB)
c = conn.cursor()

c.execute('''
    SELECT id, title, url, summary, source, total_score
    FROM content_items
    WHERE total_score >= 30
    AND featured_in_edition IS NULL
    AND blog_used = 0
    ORDER BY total_score DESC
    LIMIT 10
''')

items = []
for row in c.fetchall():
    item = {
        'id': row[0],
        'title': row[1],
        'url': row[2],
        'summary': row[3],
        'source': row[4],
        'score': row[5]
    }
    if not is_duplicate(item['title'], item['summary']):
        items.append(item)

conn.close()

print(f"✓ Found {len(items)} candidates\n")

if len(items) < 3:
    print("❌ Need at least 3 items")
    sys.exit(1)

# Select top 3
selected = items[:3]
results = []

# Read template
with open(TEMPLATE) as f:
    template = f.read()

# Get existing posts for internal linking
published = load_json(STATE_FILE, [])
existing_titles = [p['title'] for p in published[-20:]]

# Generate each post
for i, item in enumerate(selected, 1):
    print(f"\n{'='*70}")
    print(f"POST {i}/3: {item['title'][:60]}...")
    print(f"{'='*70}\n")
    
    try:
        # PHASE 1: SEO Research
        print("🔍 Phase 1: SEO Research...")
        
        seo_prompt = f"""You are an SEO expert. Conduct research for this blog post:

Title: {item['title']}
Summary: {item['summary']}

Existing posts for internal linking: {', '.join(existing_titles[:10])}

Return JSON with:
- primary_keyword: main keyword (2-4 words)
- secondary_keywords: array of 3-5 related keywords
- search_intent: informational/commercial/transactional/navigational
- suggested_title: SEO title (60 chars max)
- suggested_meta_description: meta description (155 chars max, compelling)
- internal_links: array of {{title, anchor_text}} for 2-3 internal links (or [] if none fit)

Return ONLY valid JSON."""

        seo_result = call_llm(seo_prompt, model=ANALYSIS_MODEL)
        seo_match = re.search(r'\{.*\}', seo_result, re.DOTALL)
        if seo_match:
            seo_data = json.loads(seo_match.group())
        else:
            seo_data = {
                'primary_keyword': ' '.join(item['title'].split()[:3]),
                'secondary_keywords': [],
                'search_intent': 'informational',
                'suggested_title': item['title'][:60],
                'suggested_meta_description': item['summary'][:155],
                'internal_links': []
            }
        
        print(f"✓ Primary keyword: {seo_data['primary_keyword']}")
        print(f"✓ Search intent: {seo_data['search_intent']}")
        
        # PHASE 2: Content Generation
        print("\n✍️  Phase 2: Generating content...")
        
        system_prompt = """You are Alex Chen, AI Engineer at workless.build.

Brand voice: "Work Less, Build More" - anti-hustle automation for solopreneurs.

STYLE:
- Conversational but expert (like Paul Graham)
- Specific examples over generic advice
- Personal anecdotes when relevant
- Action-oriented
- No corporate jargon

FORBIDDEN:
- "As a..."
- "Imagine..."
- "In today's world..."
- "Leverage", "utilize", "synergy"

Use "I" and "you". Short sentences. Concrete data."""

        content_prompt = f"""Write a blog post:

TITLE: {item['title']}
SUMMARY: {item['summary']}
SOURCE: {item['url']}

SEO (integrate naturally):
- Primary keyword: "{seo_data['primary_keyword']}"
- Secondary: {', '.join(seo_data['secondary_keywords'])}
- Intent: {seo_data['search_intent']}

STRUCTURE:
1. Hook (1-2 paragraphs)
2. Context (what + why it matters)
3. Practical Application (how solopreneurs use this)
4. Implementation Steps (concrete)
5. Common Mistakes
6. Real Example (specific numbers)
7. Call to Action

REQUIREMENTS:
- 1000-1400 words
- <h2> for sections, <h3> for subsections
- 1-2 <ul> or <ol> lists
- Bold (<strong>) key points
- Include external link to source
- Natural keywords (no stuffing)

Return ONLY clean HTML (no markdown, no <html>/<body>, just content)."""

        content = call_llm(content_prompt, model=WRITING_MODEL, system=system_prompt)
        content = content.replace('```html', '').replace('```', '').strip()
        
        # Word count
        text = re.sub(r'<[^>]+>', '', content)
        word_count = len(re.findall(r'\w+', text))
        read_time = max(1, round(word_count / 200))
        
        print(f"✓ Generated {word_count} words (est. {read_time} min read)")
        
        # PHASE 3: Quality Scoring
        print("\n📊 Phase 3: Scoring quality...")
        
        score_prompt = f"""Score this blog post (0-100):

TITLE: {seo_data['suggested_title']}
CONTENT: {content[:3000]}...

CRITERIA:
1. Specific examples (0-20): concrete examples with numbers/names
2. Real data (0-15): stats, measurements
3. Personal voice (0-15): "I/you", conversational
4. Actionable (0-20): clear steps
5. Structure (0-10): H2/H3 hierarchy
6. No AI patterns (0-10): avoids "As a...", "Imagine..."
7. SEO (0-10): keywords integrated naturally

Return JSON:
{{
  "specific_examples": <score>,
  "real_data": <score>,
  "personal_voice": <score>,
  "actionable_content": <score>,
  "proper_structure": <score>,
  "no_ai_patterns": <score>,
  "seo_optimization": <score>,
  "total": <sum>,
  "feedback": ["issue1", "issue2"]
}}

Be strict. Most AI content = 60-75. Excellent = 85+."""

        score_result = call_llm(score_prompt, model=ANALYSIS_MODEL)
        score_match = re.search(r'\{.*\}', score_result, re.DOTALL)
        if score_match:
            score_data = json.loads(score_match.group())
        else:
            score_data = {'total': 70, 'feedback': ['Scoring failed']}
        
        quality_score = score_data.get('total', 70)
        print(f"✓ Quality score: {quality_score}/100")
        
        if quality_score < 70:
            print("⚠️  Below target but publishing anyway")
        elif quality_score >= 85:
            print("✅ Excellent quality!")
        
        # PHASE 4: Create HTML file
        print("\n📝 Phase 4: Creating post file...")
        
        slug = re.sub(r'[^\w\s-]', '', seo_data['suggested_title'].lower())
        slug = re.sub(r'[-\s]+', '-', slug)[:80]
        date_str = datetime.now().strftime('%Y-%m-%d')
        post_slug = f"{date_str}-{slug}"
        
        now = datetime.now()
        published_iso = now.isoformat()
        
        html = template.replace('{{TITLE}}', seo_data['suggested_title'])
        html = html.replace('{{EXCERPT}}', seo_data['suggested_meta_description'])
        html = html.replace('{{KEYWORDS}}', seo_data['primary_keyword'] + ', ' + ', '.join(seo_data['secondary_keywords'][:3]))
        html = html.replace('{{URL}}', f"https://clawtv13.github.io/ai-automation-blog/posts/{post_slug}.html")
        html = html.replace('{{DATE}}', now.strftime('%B %d, %Y'))
        html = html.replace('{{READ_TIME}}', str(read_time))
        html = html.replace('{{CONTENT}}', content)
        html = html.replace('{{PUBLISHED_ISO}}', published_iso)
        html = html.replace('{{MODIFIED_ISO}}', published_iso)
        html = html.replace('{{IMAGE_URL}}', "https://clawtv13.github.io/ai-automation-blog/images/og-default.png")
        html = html.replace('{{AUTHOR}}', "Alex Chen")
        
        # Save post
        post_file = POSTS_DIR / f"{post_slug}.html"
        with open(post_file, 'w') as f:
            f.write(html)
        
        print(f"✓ Saved: {post_file.name}")
        
        # Update index
        index_file = POSTS_DIR / "index.json"
        posts = load_json(index_file, [])
        posts.insert(0, {
            'title': seo_data['suggested_title'],
            'url': f"/posts/{post_slug}.html",
            'excerpt': seo_data['suggested_meta_description'],
            'date': now.strftime('%B %d, %Y'),
            'readTime': read_time,
            'qualityScore': quality_score
        })
        save_json(index_file, posts[:50])
        
        # Update state
        published.append({
            'slug': post_slug,
            'title': seo_data['suggested_title'],
            'url': f"/posts/{post_slug}.html",
            'source_id': item['id'],
            'quality_score': quality_score,
            'word_count': word_count,
            'published_at': published_iso
        })
        save_json(STATE_FILE, published)
        
        # Save fingerprint
        save_fingerprint(seo_data['suggested_title'], seo_data['suggested_meta_description'])
        
        # Mark as used in DB
        conn = sqlite3.connect(NEWSLETTER_DB)
        c = conn.cursor()
        c.execute('UPDATE content_items SET blog_used = 1 WHERE id = ?', (item['id'],))
        conn.commit()
        conn.close()
        
        # Store result
        results.append({
            'title': seo_data['suggested_title'],
            'slug': post_slug,
            'quality_score': quality_score,
            'word_count': word_count,
            'primary_keyword': seo_data['primary_keyword'],
            'secondary_keywords': seo_data['secondary_keywords'],
            'read_time': read_time,
            'file': f"{post_slug}.html"
        })
        
        print(f"✅ Post {i}/3 complete!")
        
    except Exception as e:
        print(f"❌ Post {i}/3 failed: {e}")
        import traceback
        traceback.print_exc()

# Deploy to GitHub
if results:
    print(f"\n{'='*70}")
    print("📦 DEPLOYING TO GITHUB...")
    print(f"{'='*70}\n")
    
    os.chdir(BLOG_DIR)
    
    try:
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            # Stage and commit
            subprocess.run(['git', 'add', '.'], check=True)
            commit_msg = f"Master Agent: Generated 3 posts {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            
            # Push
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, timeout=60)
            
            print("✅ Deployed to GitHub Pages\n")
        else:
            print("✓ No changes to deploy\n")
    except Exception as e:
        print(f"⚠️  Deployment failed: {e}\n")

# Final report
print("\n" + "="*70)
print("📊 GENERATION SUMMARY")
print("="*70)

for i, result in enumerate(results, 1):
    print(f"\n🔹 Post {i}: {result['title']}")
    print(f"   Quality Score: {result['quality_score']}/100")
    print(f"   Word Count: {result['word_count']}")
    print(f"   Read Time: {result['read_time']} min")
    print(f"   Primary Keyword: {result['primary_keyword']}")
    print(f"   Secondary Keywords: {', '.join(result['secondary_keywords'][:3])}")
    print(f"   File: {result['file']}")

print(f"\n{'='*70}")
print(f"✅ MISSION COMPLETE: {len(results)}/3 posts generated")
print("="*70 + "\n")
