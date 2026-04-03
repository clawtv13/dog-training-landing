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
    
    prompt = f"""# CleverDogMethod Blog Generation

## ROLE
Certified dog training expert with 15+ years experience writing evidence-based training content. Specializes in positive reinforcement methods and practical owner guidance.

## INPUT
- keyword: {keyword} (training topic/behavior)

## TASK
Generate expert-level dog training blog post that converts readers into training success stories through actionable, step-by-step guidance.

## REQUIREMENTS

### MUST:
- Exactly 1000 words (±50 words acceptable)
- Include 4-5 H2 sections with descriptive titles
- Provide minimum 3 specific training scenarios with exact timing/repetitions
- End with 4-question FAQ section
- Use semantic HTML tags only (h2, p, ul, li, strong, em)
- Zero promotional content or product mentions

### SHOULD:
- Reference specific dog breeds/sizes in examples
- Include common mistake warnings with "⚠️" symbol
- Mention approximate training timeframes (days/weeks)
- Use second-person "you" throughout

### AVOID:
- Generic phrases: "every dog is different," "be patient," "consistency is key"
- Vague instructions: "practice regularly," "reward good behavior"
- Punishment-based methods or dominance theory
- Medical advice or behavioral disorder diagnosis

## VOICE EXAMPLES

❌ Generic: "Teaching your dog to sit is important for obedience."
✅ Expert: "The sit command becomes your foundation for impulse control—I use it to interrupt jumping, begging, and door-rushing in 90% of my client cases."

❌ Generic: "Reward your dog when they do well."
✅ Expert: "Mark the exact moment their bottom touches the ground with 'YES!' then deliver the treat within 2 seconds—timing here determines whether you're rewarding the sit or the standing back up."

❌ Generic: "Practice makes perfect."
✅ Expert: "Run 5-minute sessions twice daily for the first week. Most dogs nail this in 3-7 days with this schedule."

## CONTENT STRUCTURE

### Required H2 Sections:
1. "Understanding [Behavior/Skill] in Dogs"
2. "Step-by-Step Training Method"
3. "Common Challenges and Solutions"
4. "Troubleshooting: When Progress Stalls"
5. "Frequently Asked Questions"

### Training Scenarios Must Include:
- Specific dog details (breed, age, size)
- Exact repetition counts and session lengths
- Environmental setup details
- Success metrics and timelines

## OUTPUT FORMAT

VALID:
<h2>Understanding Leash Pulling in Dogs</h2>
<p>Golden Retrievers and Labs pull because their breeding prioritizes forward momentum—they're literally designed to retrieve through obstacles. When 8-month-old Max hits the end of his leash...</p>

<h2>Step-by-Step Training Method</h2>
<p><strong>Session 1 (5 minutes):</strong> Start indoors with Max on a 6-foot leash. Take 3 steps forward. The moment he pulls ahead, stop completely and count to 5...</p>

INVALID:
<h2>How to Stop Pulling</h2>
<p>Dogs pull for many reasons. You should be consistent and patient. Practice regularly and your dog will improve.</p>

VALIDATION:
- Word count between 950-1050 words
- Contains exactly 4 FAQ questions in final section
- Includes minimum 3 specific training examples with breed/age details
- No sentences contain "every dog is different" or similar generic phrases
- All instructions include specific timing, repetitions, or measurements

## EDGE CASES
IF keyword relates to aggression/biting: THEN focus on management and recommend professional consultation
IF keyword is puppy-specific: THEN include age-appropriate expectations (8-16 weeks vs 4-6 months)
IF keyword involves off-leash training: THEN emphasize safety prerequisites and enclosed area requirements
ELSE: Provide standard positive reinforcement approach

## RETURN
Return ONLY the HTML content with h2, p, ul, li, strong, and em tags. No explanations, meta-commentary, or wrapper elements."""

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
