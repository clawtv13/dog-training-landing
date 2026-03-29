#!/usr/bin/env python3
"""
CleverDogMethod - Fully Autonomous Worker
- Self-healing: Handles errors automatically
- Smart retry: Backoff on failures
- Auto-recovery: Falls back to alternatives
- Zero manual intervention needed

Runs: 08:00 + 20:00 UTC daily (6 posts/day)
"""

import requests
import json
import subprocess
import time
import random
from pathlib import Path
from datetime import datetime
import sys
import re

# Config
WORKSPACE = Path("/root/.openclaw/workspace")
REPO_PATH = WORKSPACE / "dog-training-landing-clean"
STATE_FILE = WORKSPACE / ".state/cleverdogmethod-published.json"
KEYWORDS_FILE = WORKSPACE / "content/cleverdogmethod/KEYWORDS-EXPANSION.md"
LOG_FILE = WORKSPACE / "logs/cleverdogmethod-autonomous.log"

TELEGRAM_BOT = "8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU"
TELEGRAM_CHAT = "8116230130"
OPENROUTER_KEY = "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"

MAX_RETRIES = 3
POSTS_PER_RUN = 3

def log(msg, level="INFO"):
    """Log with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [{level}] {msg}"
    print(log_line)
    
    # Write to log file
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def notify_telegram(message, silent=True):
    """Send Telegram notification (only for critical issues)"""
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": message, "disable_notification": silent},
            timeout=10
        )
    except:
        pass

def load_published_posts():
    """Load list of published posts"""
    if not STATE_FILE.exists():
        return []
    
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        log("⚠️ Corrupted state file, resetting", "WARN")
        return []

def save_published_post(post_data):
    """Save published post to state"""
    published = load_published_posts()
    published.append(post_data)
    
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(published, f, indent=2)

def load_keywords_expansion():
    """Load keywords from expansion database"""
    
    if not KEYWORDS_FILE.exists():
        log("❌ Keywords expansion file not found", "ERROR")
        return []
    
    with open(KEYWORDS_FILE) as f:
        content = f.read()
    
    keywords = []
    for line in content.split('\n'):
        if '|' in line and '⭐' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5 and parts[1] and parts[1] != 'Keyword':
                keywords.append({
                    'keyword': parts[1],
                    'volume': parts[2],
                    'priority': parts[4].count('⭐')
                })
    
    # Sort by priority
    keywords.sort(key=lambda x: x['priority'], reverse=True)
    return keywords

def select_unused_keywords(count=10):
    """Select keywords not yet published"""
    
    keywords = load_keywords_expansion()
    published = load_published_posts()
    published_slugs = {p['slug'] for p in published}
    published_titles = {p['title'].lower() for p in published}
    
    unused = []
    for kw in keywords:
        slug = kw['keyword'].lower().replace(' ', '-')
        title_base = kw['keyword'].lower()
        
        # Check if not published (slug or similar title)
        if slug not in published_slugs:
            # Also check for title similarity
            is_similar = any(
                title_base in pub_title or pub_title in title_base
                for pub_title in published_titles
            )
            if not is_similar:
                unused.append(kw)
        
        if len(unused) >= count:
            break
    
    if len(unused) == 0:
        log("⚠️ All keywords exhausted, cycling back", "WARN")
        # Fallback: use all keywords again
        unused = keywords[:count]
    
    return unused

def generate_content(keyword, retry=0):
    """Generate blog post content with AI"""
    
    if retry > MAX_RETRIES:
        log(f"❌ Max retries exceeded for: {keyword}", "ERROR")
        return None
    
    # V3 Optimized Prompt - Concise & High-Impact
    prompt = f"""Expert dog training blog: {keyword}

1000 words. 4-5 H2 sections. 3+ specific scenarios (breed/age/timing). 4-question FAQ. HTML only: h2,p,ul,li,strong,em.

Voice:
❌ "Teaching sit is important"
✅ "Sit is impulse-control foundation—I use it to stop jumping, begging, door-rushing in 90% of cases"

❌ "Reward when they do well"
✅ "Mark exact moment bottom touches ground with 'YES!' then treat within 2sec"

❌ "Practice makes perfect"
✅ "5min sessions 2x daily first week. Most dogs nail this in 3-7 days"

Scenarios must include:
- Dog: "8mo Golden Retriever Max"
- Counts: "5 reps/session, 3 sessions daily"
- Setup: "indoors, 6ft leash"
- Success: "day 3, Max held sit 15sec"

Structure:
1. Understanding [Behavior] in Dogs
2. Step-by-Step Training Method
3. Common Challenges & Solutions
4. Troubleshooting: When Progress Stalls
5. FAQ (4 questions)

Forbidden: "every dog different", "be patient", "consistency key", "practice regularly"

Edge cases:
- Aggression → management + pro referral
- Puppy → age expectations (8-16wk vs 4-6mo)
- Off-leash → safety + enclosed area

Output: HTML only. No wrapper."""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4.5",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=120
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            
            # Clean up
            content = content.replace('```html', '').replace('```', '').strip()
            
            word_count = len(content.split())
            log(f"✅ Generated {word_count} words for: {keyword}")
            
            return content
        
        elif response.status_code == 429:
            wait_time = 30 * (retry + 1)
            log(f"⏳ Rate limited, waiting {wait_time}s...", "WARN")
            time.sleep(wait_time)
            return generate_content(keyword, retry + 1)
        
        else:
            log(f"❌ API error {response.status_code}: {response.text[:100]}", "ERROR")
            return None
            
    except Exception as e:
        log(f"❌ Generation exception: {e}", "ERROR")
        if retry < MAX_RETRIES:
            time.sleep(10)
            return generate_content(keyword, retry + 1)
        return None

def create_html_post(keyword, content):
    """Create full HTML blog post"""
    
    slug = keyword.lower().replace(' ', '-')
    title = f"Complete Guide to {keyword.title()}"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | CleverDogMethod</title>
    <meta name="description" content="Expert guide on {keyword}. Proven strategies and actionable tips for dog training success.">
    <link rel="stylesheet" href="../style.css">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-QR48M1K012"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-QR48M1K012');
    </script>
</head>
<body>
    <header>
        <nav>
            <a href="../index.html" class="logo">🐕 CleverDogMethod</a>
            <a href="../blog.html">Blog</a>
        </nav>
    </header>
    
    <main class="blog-post">
        <article>
            <h1>{title}</h1>
            <div class="meta">
                <span>Published: {datetime.now().strftime('%B %d, %Y')}</span>
                <span>Reading time: 5 min</span>
            </div>
            
            {content}
            
            <div class="cta-box">
                <h3>Ready to Transform Your Dog's Behavior?</h3>
                <p>Get instant access to proven training techniques that work.</p>
                <a href="https://258e5d6f75r1pezy8tb13r53z.hop.clickbank.net" class="cta-button">Start Training Now →</a>
            </div>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2026 CleverDogMethod. All rights reserved.</p>
    </footer>
</body>
</html>"""
    
    return html, slug, title

def deploy_to_vercel(post_file, slug):
    """Deploy post to Vercel via git"""
    
    try:
        # Git operations
        subprocess.run(['git', 'add', post_file], cwd=REPO_PATH, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', f'Add blog post: {slug}'],
            cwd=REPO_PATH,
            check=True,
            capture_output=True
        )
        result = subprocess.run(
            ['git', 'push', 'origin', 'master'],
            cwd=REPO_PATH,
            check=True,
            capture_output=True,
            timeout=60
        )
        
        log(f"✅ Deployed: {slug}")
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"❌ Git error: {e.stderr.decode()[:200]}", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Deploy exception: {e}", "ERROR")
        return False

def generate_and_publish_post(keyword):
    """Full pipeline: generate + publish single post"""
    
    log(f"📝 Processing: {keyword['keyword']}")
    
    # Generate content
    content = generate_content(keyword['keyword'])
    if not content:
        log(f"❌ Failed to generate content for: {keyword['keyword']}", "ERROR")
        return False
    
    # Create HTML
    html, slug, title = create_html_post(keyword['keyword'], content)
    
    # Save file
    post_file = REPO_PATH / f"blog/{slug}.html"
    post_file.parent.mkdir(exist_ok=True)
    
    with open(post_file, 'w') as f:
        f.write(html)
    
    log(f"💾 Saved: {post_file.name}")
    
    # Deploy
    if deploy_to_vercel(post_file, slug):
        # Save to state
        save_published_post({
            'slug': slug,
            'title': title,
            'keyword': keyword['keyword'],
            'published': datetime.now().isoformat(),
            'url': f'https://cleverdogmethod.com/blog/{slug}.html'
        })
        
        log(f"✅ Published: {title}")
        return True
    else:
        log(f"❌ Deploy failed: {slug}", "ERROR")
        return False

def main():
    """Main autonomous worker"""
    
    log("="*60)
    log("🚀 CLEVERDOG AUTONOMOUS WORKER STARTING")
    log("="*60)
    
    try:
        # Select unused keywords
        log(f"🔍 Selecting {POSTS_PER_RUN} keywords...")
        keywords = select_unused_keywords(POSTS_PER_RUN * 2)  # Get extra as buffer
        
        if len(keywords) == 0:
            log("❌ No keywords available", "ERROR")
            notify_telegram("⚠️ CleverDog: No keywords available", silent=False)
            return False
        
        log(f"✅ Selected {len(keywords)} candidate keywords")
        
        # Try to publish POSTS_PER_RUN posts
        published_count = 0
        attempts = 0
        max_attempts = POSTS_PER_RUN * 3  # Try up to 3x the target
        
        for keyword in keywords:
            if published_count >= POSTS_PER_RUN:
                break
            
            if attempts >= max_attempts:
                log(f"⚠️ Max attempts reached, stopping", "WARN")
                break
            
            attempts += 1
            
            success = generate_and_publish_post(keyword)
            if success:
                published_count += 1
                # Small delay between posts
                if published_count < POSTS_PER_RUN:
                    time.sleep(10)
        
        # Summary
        log("="*60)
        log(f"📊 SUMMARY: {published_count}/{POSTS_PER_RUN} posts published")
        log("="*60)
        
        if published_count == 0:
            notify_telegram(f"❌ CleverDog: 0/{POSTS_PER_RUN} posts published", silent=False)
            return False
        elif published_count < POSTS_PER_RUN:
            log(f"⚠️ Only {published_count}/{POSTS_PER_RUN} published", "WARN")
            # Don't notify unless completely failed
        
        return True
        
    except Exception as e:
        log(f"❌ Critical error: {e}", "ERROR")
        notify_telegram(f"🚨 CleverDog critical error: {e}", silent=False)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
