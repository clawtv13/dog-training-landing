#!/usr/bin/env python3
"""
CLEVERDOGMETHOD DAILY AUTOMATION
Generates 3 unique, SEO-optimized blog posts every day at 9:00 AM Spain time

Process:
1. Research trending topics (Reddit + Google Trends)
2. Select 3 unique topics (no duplicates)
3. Generate high-quality content with AI
4. Check uniqueness
5. Deploy to Netlify
6. Notify via Telegram
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.append(str(Path(__file__).parent))

from research.reddit_scraper import main as scrape_reddit
from research.google_trends import main as scrape_trends
from content.content_generator import generate_post
from deploy.uniqueness_checker import check_posts, load_published_posts, save_published_posts
from deploy.deploy_posts import deploy
import requests
import os

def send_telegram_notification(posts, batch_type="morning"):
    """Send Telegram notification about published posts"""
    
    # Prepare message
    emoji = "☀️" if batch_type == "morning" else "🌙"
    time = "9:00 AM" if batch_type == "morning" else "9:00 PM"
    
    message = f"{emoji} *CleverDogMethod — {time} Batch*\n\n"
    message += f"✅ {len(posts)} new posts published:\n\n"
    
    for i, post in enumerate(posts, 1):
        title = post['metadata']['title']
        url = f"https://cleverdogmethod.com/blog/{post['metadata']['slug']}.html"
        message += f"{i}. _{title}_\n   🔗 {url}\n\n"
    
    message += f"📊 Live at: https://cleverdogmethod.com/blog/"
    
    try:
        print(f"\n📱 Sending Telegram notification...")
        
        # Write message to file that will be picked up
        notif_file = f"/root/.openclaw/workspace/.notifications/cleverdogmethod-{datetime.now().strftime('%Y%m%d-%H%M')}.txt"
        os.makedirs(os.path.dirname(notif_file), exist_ok=True)
        
        with open(notif_file, 'w') as f:
            f.write(message)
        
        print(f"✅ Notification saved: {notif_file}")
        print(message)
        
        return True
        
    except Exception as e:
        print(f"⚠️  Notification failed: {e}")
        return False

def combine_research(reddit_topics, trends_topics):
    """Combine and rank topics from both sources"""
    
    print("\n🎯 COMBINING RESEARCH DATA")
    print("="*60)
    
    # Create unified topic list
    all_topics = []
    
    # Add Reddit topics
    for topic in reddit_topics[:10]:
        all_topics.append({
            "title": f"How to Handle {topic['topic'].title()} in Dogs",
            "keywords": topic['topic'] + ", dog behavior, dog training",
            "score": topic['popularity'],
            "source": "Reddit"
        })
    
    # Add Google Trends topics
    for topic in trends_topics[:10]:
        all_topics.append({
            "title": topic['query'].title(),
            "keywords": topic['query'] + ", dog training",
            "score": topic['value'],
            "source": "Google Trends"
        })
    
    # Sort by score
    all_topics.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n📊 Found {len(all_topics)} potential topics")
    
    return all_topics

def select_unique_topics(candidates, published_posts, count=3):
    """Select N unique topics that haven't been published"""
    
    print(f"\n🔍 SELECTING {count} UNIQUE TOPICS")
    print("="*60)
    
    selected = []
    
    for candidate in candidates:
        # Check if topic already published
        is_duplicate = False
        
        for existing in published_posts:
            # Simple keyword overlap check
            candidate_words = set(candidate['title'].lower().split())
            existing_words = set(existing['title'].lower().split())
            overlap = len(candidate_words & existing_words)
            
            if overlap > 3:  # More than 3 words in common
                is_duplicate = True
                break
        
        if not is_duplicate:
            selected.append(candidate)
            print(f"✅ Selected: {candidate['title']}")
        else:
            print(f"⏭️  Skipped (duplicate): {candidate['title'][:50]}...")
        
        if len(selected) >= count:
            break
    
    if len(selected) < count:
        print(f"\n⚠️  Only found {len(selected)} unique topics (needed {count})")
    
    return selected

def generate_posts(topics):
    """Generate content for selected topics"""
    
    print("\n✍️  GENERATING CONTENT")
    print("="*60)
    
    posts = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Generating: {topic['title']}")
        
        post = generate_post(
            topic=topic['title'],
            keywords=topic['keywords'],
            category="Training"
        )
        
        if post:
            posts.append(post)
        else:
            print(f"   ❌ Failed to generate post for: {topic['title']}")
    
    return posts

def main():
    print("\n" + "="*70)
    print("🐕 CLEVERDOGMETHOD — DAILY CONTENT AUTOMATION".center(70))
    print("="*70)
    print(f"\n📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"🕐 {datetime.now().strftime('%H:%M UTC')}\n")
    
    # STEP 1: Research
    print("\n" + "="*70)
    print("STEP 1: RESEARCH TRENDING TOPICS".center(70))
    print("="*70)
    
    reddit_topics = scrape_reddit()
    trends_topics = scrape_trends()
    
    # STEP 2: Combine & Rank
    all_candidates = combine_research(reddit_topics, trends_topics)
    
    # STEP 3: Load published history
    published_posts = load_published_posts()
    print(f"\n📚 {len(published_posts)} posts already published")
    
    # STEP 4: Select 3 unique topics
    selected_topics = select_unique_topics(all_candidates, published_posts, count=3)
    
    if len(selected_topics) < 3:
        print(f"\n❌ ERROR: Could only find {len(selected_topics)} unique topics")
        print("   Try again tomorrow or expand topic sources")
        return False
    
    # STEP 5: Generate content
    print("\n" + "="*70)
    print("STEP 2: GENERATE CONTENT".center(70))
    print("="*70)
    
    new_posts = generate_posts(selected_topics)
    
    if len(new_posts) < 3:
        print(f"\n⚠️  Only generated {len(new_posts)} posts (wanted 3)")
    
    # STEP 6: Final uniqueness check
    print("\n" + "="*70)
    print("STEP 3: UNIQUENESS CHECK".center(70))
    print("="*70)
    
    approved, rejected = check_posts(new_posts)
    
    if len(approved) == 0:
        print("\n❌ No posts passed uniqueness check")
        return False
    
    # STEP 7: Deploy
    print("\n" + "="*70)
    print("STEP 4: DEPLOY TO NETLIFY".center(70))
    print("="*70)
    
    deployed = deploy(approved)
    
    if deployed:
        print("\n" + "="*70)
        print(f"✅ SUCCESS — {len(approved)} POSTS LIVE".center(70))
        print("="*70)
        print(f"\n🌐 Visit: https://cleverdogmethod.com/blog/")
        print(f"📊 Total published: {len(published_posts) + len(approved)}")
        
        # Determine batch type based on hour
        current_hour = datetime.now().hour
        batch_type = "morning" if 6 <= current_hour < 14 else "evening"
        
        # Send Telegram notification
        send_telegram_notification(approved, batch_type)
    else:
        print("\n❌ Deployment failed")
    
    return deployed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
