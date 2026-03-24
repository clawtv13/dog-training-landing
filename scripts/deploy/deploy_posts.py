#!/usr/bin/env python3
"""
Deploy new blog posts to cleverdogmethod
- Saves HTML files
- Updates sitemap
- Git commit + push
- Telegram notification
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path("/root/.openclaw/workspace/dog-training-landing/blog")
SITE_DIR = Path("/root/.openclaw/workspace/dog-training-landing")
SITEMAP = SITE_DIR / "sitemap.xml"
STATE_FILE = Path("/root/.openclaw/workspace/.state/cleverdogmethod-published.json")

def save_posts(posts):
    """Save HTML files to blog directory"""
    
    print("\n💾 SAVING POSTS")
    print("="*60)
    
    saved = []
    
    for post in posts:
        filename = f"{post['slug']}.html"
        filepath = BLOG_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(post['html'])
        
        print(f"✅ Saved: {filename}")
        
        saved.append({
            "title": post['title'],
            "slug": post['slug'],
            "keywords": post['keywords'],
            "date": datetime.now().isoformat(),
            "url": f"https://cleverdogmethod.com/blog/{post['slug']}.html"
        })
    
    return saved

def update_sitemap(posts):
    """Add new posts to sitemap.xml"""
    
    print("\n📄 UPDATING SITEMAP")
    print("="*60)
    
    with open(SITEMAP, 'r') as f:
        sitemap = f.read()
    
    new_urls = ""
    for post in posts:
        new_urls += f"""
    <url>
        <loc>https://cleverdogmethod.com/blog/{post['slug']}.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>"""
    
    sitemap = sitemap.replace('</urlset>', f'{new_urls}\n</urlset>')
    
    with open(SITEMAP, 'w') as f:
        f.write(sitemap)
    
    print(f"✅ Added {len(posts)} URLs to sitemap")

def update_state(posts):
    """Track published posts"""
    
    STATE_FILE.parent.mkdir(exist_ok=True)
    
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            published = json.load(f)
    else:
        published = []
    
    published.extend(posts)
    
    with open(STATE_FILE, 'w') as f:
        json.dump(published, f, indent=2)
    
    print(f"\n📊 State updated: {len(published)} total posts published")

def git_deploy():
    """Commit and push to trigger Netlify deploy"""
    
    print("\n🚀 DEPLOYING TO NETLIFY")
    print("="*60)
    
    os.chdir(SITE_DIR)
    
    try:
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        commit_msg = f"Daily posts: {datetime.now().strftime('%Y-%m-%d')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        
        subprocess.run(["git", "push"], check=True, capture_output=True)
        
        print("✅ Pushed to Git")
        print("⏳ Netlify deploy triggered (live in ~2 min)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def send_telegram_notification(posts):
    """Send notification via Telegram"""
    
    message = f"🐕 **CleverDogMethod — 3 New Posts Live**\n\n"
    
    for i, post in enumerate(posts, 1):
        message += f"{i}. \"{post['title']}\"\n"
        message += f"   🔗 {post['url']}\n"
        message += f"   🔑 Keywords: {post['keywords']}\n\n"
    
    message += f"✅ Published at {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
    message += f"📊 Total posts: {len(load_all_posts())}"
    
    print("\n📱 TELEGRAM NOTIFICATION")
    print("="*60)
    print(message)
    
    # TODO: Implement actual Telegram API call
    # For now just print
    
    return message

def load_all_posts():
    """Load all published posts from state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return []

def deploy(posts):
    """Full deployment pipeline"""
    
    print("\n" + "="*60)
    print("🚀 CLEVERDOGMETHOD DEPLOYMENT".center(60))
    print("="*60)
    
    # Save HTML files
    saved_posts = save_posts(posts)
    
    # Update sitemap
    update_sitemap(saved_posts)
    
    # Update state tracking
    update_state(saved_posts)
    
    # Git deploy
    deployed = git_deploy()
    
    if deployed:
        # Send notification
        send_telegram_notification(saved_posts)
    
    print("\n" + "="*60)
    print("✅ DEPLOYMENT COMPLETE".center(60))
    print("="*60 + "\n")
    
    return deployed

def main():
    # Test with dummy post
    test_posts = [
        {
            "title": "Test Post: Why Dogs Bark at Night",
            "slug": "test-why-dogs-bark-night",
            "keywords": "barking, night barking, sleep",
            "html": "<html><body><h1>Test Post</h1><p>Content here...</p></body></html>"
        }
    ]
    
    deploy(test_posts)

if __name__ == '__main__':
    main()
