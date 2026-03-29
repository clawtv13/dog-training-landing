#!/usr/bin/env python3
"""
AI Automation Builder - Blog Auto-Posting

Generates blog posts from newsletter research database.
Creates authentic, credible content that doesn't feel AI-generated.

Runs daily, creates 1-2 high-quality posts per day.
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_DIR = WORKSPACE / "blog"
POSTS_DIR = BLOG_DIR / "posts"
TEMPLATE = WORKSPACE / "templates" / "post.html"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"
STATE_FILE = WORKSPACE / ".state" / "published-posts.json"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

POSTS_PER_DAY = 2
MIN_QUALITY_SCORE = 30

# Author persona for credibility
AUTHOR = {
    'name': 'Alex Chen',
    'title': 'AI Engineer & Indie Maker',
    'bio': 'Building automation tools after 8 years in ML. Previously at a fintech startup, now shipping products solo.',
    'avatar': '👤'
}

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_published_posts():
    """Load list of already published post URLs"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_published_post(post_data):
    """Save published post to state"""
    published = load_published_posts()
    published.append({
        'url': post_data['url'],
        'title': post_data['title'],
        'published_at': datetime.now().isoformat(),
        'source_item_id': post_data.get('source_id')
    })
    
    with open(STATE_FILE, 'w') as f:
        json.dump(published, f, indent=2)

# ============================================================================
# CONTENT SELECTION
# ============================================================================

def get_unpublished_content():
    """
    Get high-quality items from newsletter database that haven't been published to blog yet
    """
    if not NEWSLETTER_DB.exists():
        print("⚠️  Newsletter database not found")
        return []
    
    conn = sqlite3.connect(NEWSLETTER_DB)
    c = conn.cursor()
    
    # Get items not yet featured in newsletter and high quality
    c.execute('''
        SELECT id, title, url, summary, source, total_score, created_at
        FROM content_items
        WHERE total_score >= ?
        AND featured_in_edition IS NULL
        ORDER BY total_score DESC, created_at DESC
        LIMIT 20
    ''', (MIN_QUALITY_SCORE,))
    
    items = []
    for row in c.fetchall():
        items.append({
            'id': row[0],
            'title': row[1],
            'url': row[2],
            'summary': row[3],
            'source': row[4],
            'score': row[5],
            'created_at': row[6]
        })
    
    conn.close()
    
    # Filter out already published
    published = load_published_posts()
    published_urls = [p['url'] for p in published]
    
    unpublished = [item for item in items if item['url'] not in published_urls]
    
    return unpublished

# ============================================================================
# BLOG POST GENERATION
# ============================================================================

def generate_blog_post(item):
    """
    Generate authentic blog post that doesn't feel AI-generated
    """
    if not OPENROUTER_API_KEY:
        print("⚠️  OpenRouter API key not found")
        return None
    
    print(f"📝 Generating blog post for: {item['title'][:60]}...")
    
    prompt = f"""You are {AUTHOR['name']}, {AUTHOR['title']}, writing for your blog "AI Automation Builder".

Write a blog post analyzing this piece:

Title: {item['title']}
URL: {item['url']}
Summary: {item['summary']}
HN Score: {item['score']} points

CRITICAL - AVOID THESE "AI TELLS":
❌ Never start with "As a..."
❌ No generic "imagine if..." hypotheticals  
❌ Don't force "solopreneur" framing into every topic
❌ Never use corporate phrases like "game-changing" or "unlock potential"
❌ No tutorial structure for news analysis
❌ Don't explain basic terms (assume technical audience)

WRITE LIKE A REAL HUMAN BLOG:
✅ Personal perspective - "I tried this", "I've seen", "reminds me of"
✅ Specific examples from YOUR experience (make them believable)
✅ Admit when you don't know something
✅ Link to 2-3 related sources (GitHub repos, papers, tools)
✅ Include skepticism or caveats when appropriate
✅ Natural tangents (like real writing)

STRUCTURE:
- Opening: Your immediate reaction or observation (2-3 sentences)
- Main analysis: Why this matters, technical details, your take
- Practical angle: Who can actually use this and how
- Sources section: Link to 2-3 related resources
- Closing: Your honest conclusion

TONE: Technical blog, not marketing copy. Write like you're explaining to a peer developer over coffee.

LENGTH: 600-900 words (don't pad it)

FORMAT: Clean HTML (no <html> or <body> tags):
- <h2> for main sections
- <h3> for subsections  
- <p> for paragraphs
- <ul>/<ol> for lists
- <strong> and <em> for emphasis
- <code> for technical terms
- <a href="..."> for links

Add a "Sources & Related" section at the end with 2-3 links to:
- Original source
- Related tools/repos
- Further reading

Return ONLY the HTML content (no markdown, no code blocks, no meta-commentary)."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.8  # Higher temp for more natural voice
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Clean up any markdown artifacts
            content = content.replace('```html', '').replace('```', '').strip()
            
            return content
        else:
            print(f"✗ API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ Generation error: {e}")
        return None

# ============================================================================
# POST PUBLISHING
# ============================================================================

def create_blog_post(item, content):
    """
    Create blog post HTML file and update index
    """
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate slug
    slug = item['title'].lower()
    slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
    slug = '-'.join(slug.split())[:80]
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    post_slug = f"{date_str}-{slug}"
    post_file = POSTS_DIR / f"{post_slug}.html"
    
    # Read template
    with open(TEMPLATE, 'r') as f:
        template = f.read()
    
    # Calculate read time
    word_count = len(content.split())
    read_time = max(1, round(word_count / 200))
    
    # Generate excerpt from content (first paragraph)
    import re
    first_p = re.search(r'<p>(.*?)</p>', content)
    if first_p:
        excerpt = first_p.group(1)[:200] + "..."
    else:
        excerpt = item['summary'][:200] + "..."
    
    # Generate keywords (from title, less spammy)
    title_words = [w for w in item['title'].split() if len(w) > 3][:5]
    keywords = f"AI automation, {', '.join(title_words)}"
    
    # Fill template
    html = template.replace('{{TITLE}}', item['title'])
    html = html.replace('{{EXCERPT}}', excerpt)
    html = html.replace('{{KEYWORDS}}', keywords)
    html = html.replace('{{URL}}', f"https://aiautomationbuilder.com/posts/{post_slug}.html")
    html = html.replace('{{DATE}}', datetime.now().strftime('%B %d, %Y'))
    html = html.replace('{{READ_TIME}}', str(read_time))
    html = html.replace('{{CONTENT}}', content)
    html = html.replace('{{AUTHOR_NAME}}', AUTHOR['name'])
    html = html.replace('{{AUTHOR_TITLE}}', AUTHOR['title'])
    html = html.replace('{{AUTHOR_BIO}}', AUTHOR['bio'])
    html = html.replace('{{AUTHOR_AVATAR}}', AUTHOR['avatar'])
    html = html.replace('{{HN_SCORE}}', str(item['score']))
    
    # Save post
    with open(post_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Created: {post_file.name}")
    
    # Update index
    update_posts_index(post_slug, item, excerpt, read_time)
    
    # Mark as published
    post_data = {
        'url': f"/posts/{post_slug}.html",
        'title': item['title'],
        'source_id': item['id']
    }
    save_published_post(post_data)
    
    return post_slug

def update_posts_index(post_slug, item, excerpt, read_time):
    """
    Update posts/index.json with new post
    """
    index_file = BLOG_DIR / "posts" / "index.json"
    
    if index_file.exists():
        with open(index_file, 'r') as f:
            posts = json.load(f)
    else:
        posts = []
    
    # Add new post at beginning
    posts.insert(0, {
        'title': item['title'],
        'url': f"/posts/{post_slug}.html",
        'excerpt': excerpt,
        'date': datetime.now().strftime('%B %d, %Y'),
        'readTime': read_time,
        'author': AUTHOR['name']
    })
    
    # Keep last 50 posts in index
    posts = posts[:50]
    
    with open(index_file, 'w') as f:
        json.dump(posts, f, indent=2)

# ============================================================================
# GIT DEPLOYMENT
# ============================================================================

def deploy_to_github():
    """
    Commit and push to GitHub (triggers GitHub Pages deploy)
    """
    os.chdir(BLOG_DIR)
    
    try:
        # Check if git repo exists
        if not (BLOG_DIR / ".git").exists():
            print("🔧 Initializing git repo...")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            print("⚠️  Add GitHub remote manually:")
            print(f"   cd {BLOG_DIR}")
            print("   git remote add origin https://github.com/yourusername/ai-automation-blog.git")
            return False
        
        # Stage changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        commit_msg = f"Auto-post: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                              capture_output=True, text=True)
        
        if "nothing to commit" in result.stdout:
            print("✓ No changes to deploy")
            return True
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ Deployed to GitHub Pages")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")
        return False

# ============================================================================
# NOTIFICATIONS
# ============================================================================

def send_telegram_notification(posts_created):
    """
    Notify via Telegram when posts are published
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    message = f"""🤖 **AI Automation Blog - Auto-Post**

✅ Published {len(posts_created)} new post(s):

"""
    
    for post in posts_created:
        message += f"• {post['title']}\n"
    
    message += f"\n🌐 Live: https://aiautomationbuilder.com\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main blog automation workflow
    """
    print("=" * 60)
    print("AI AUTOMATION BUILDER - BLOG AUTO-POSTING")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    print()
    
    # Get unpublished content
    print("🔍 Fetching unpublished content from newsletter database...")
    items = get_unpublished_content()
    
    if not items:
        print("✓ No new content to publish (all items already used)")
        return
    
    print(f"📊 Found {len(items)} unpublished high-quality items")
    print(f"🎯 Publishing top {POSTS_PER_DAY} today\n")
    
    # Select best items
    selected = items[:POSTS_PER_DAY]
    
    posts_created = []
    
    for item in selected:
        print(f"\n📝 Processing: {item['title'][:60]}...")
        print(f"   Score: {item['score']} | Source: {item['source']}")
        
        # Generate full blog post
        content = generate_blog_post(item)
        
        if not content:
            print("✗ Generation failed, skipping")
            continue
        
        # Create HTML file
        post_slug = create_blog_post(item, content)
        
        posts_created.append({
            'title': item['title'],
            'slug': post_slug,
            'score': item['score']
        })
        
        print(f"✅ Published: {post_slug}\n")
    
    if posts_created:
        print(f"\n✅ Created {len(posts_created)} new blog posts")
        
        # Deploy to GitHub Pages
        print("\n🚀 Deploying to GitHub...")
        deployed = deploy_to_github()
        
        if deployed:
            # Notify success
            send_telegram_notification(posts_created)
            print("\n✅ BLOG AUTOMATION COMPLETE\n")
        else:
            print("\n⚠️  Posts created but deployment failed")
    else:
        print("\n✓ No posts created this run")

if __name__ == "__main__":
    main()
