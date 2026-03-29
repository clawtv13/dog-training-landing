#!/usr/bin/env python3
"""
AI Automation Builder - Auto Distribution

Automatically posts newsletter to social platforms after publishing:
- Reddit (2-3 relevant subreddits)
- Twitter (thread)
- LinkedIn (post)
- Hacker News (if applicable)

Run after newsletter is published.
"""

import os
import sys
import json
import sqlite3
import requests
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

NEWSLETTER_BASE_URL = "https://aiautomationbuilder.beehiiv.com"

# ============================================================================
# GET NEWSLETTER SUMMARY
# ============================================================================

def get_latest_edition():
    """
    Get latest published edition from database
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT edition_number, subject_line, publish_date
        FROM editions
        WHERE status = 'published'
        ORDER BY edition_number DESC
        LIMIT 1
    ''')
    
    row = c.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        'number': row[0],
        'subject': row[1],
        'date': row[2]
    }

def get_edition_highlights(edition_number):
    """
    Get top content items from edition for summary
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT title, url, newsletter_section
        FROM content_items
        WHERE featured_in_edition = ?
        ORDER BY total_score DESC
        LIMIT 5
    ''', (edition_number,))
    
    items = []
    for row in c.fetchall():
        items.append({
            'title': row[0],
            'url': row[1],
            'section': row[2]
        })
    
    conn.close()
    return items

def generate_social_summary(edition, highlights):
    """
    Use Claude to generate platform-specific summaries
    """
    if not OPENROUTER_API_KEY:
        print("⚠️  OpenRouter key not set, using basic summary")
        return generate_basic_summary(edition, highlights)
    
    print("✍️  Generating social summaries with Claude...")
    
    prompt = f"""Generate social media posts for newsletter edition #{edition['number']}.

Subject: {edition['subject']}

Top content this week:
{json.dumps([h['title'] for h in highlights], indent=2)}

Create 3 versions:

1. REDDIT POST (200-300 words)
   - Casual, helpful tone
   - Specific value points
   - Not too salesy
   - Ends with "Full newsletter: [link]"

2. TWITTER THREAD (8-10 tweets, 250 chars each)
   - Tweet 1: Hook (curiosity gap)
   - Tweets 2-7: Key tools/insights (one per tweet)
   - Tweet 8: CTA (subscribe link)
   - Each standalone but flows together

3. LINKEDIN POST (150-200 words)
   - Professional tone
   - Business value focus
   - Ends with newsletter link

Return as JSON:
{{
  "reddit": "...",
  "twitter": ["tweet1", "tweet2", ...],
  "linkedin": "..."
}}"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Try parsing JSON
            try:
                summaries = json.loads(content)
            except:
                # Fallback: extract from markdown
                import re
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    summaries = json.loads(match.group(1))
                else:
                    print("✗ Could not parse summaries, using basic")
                    return generate_basic_summary(edition, highlights)
            
            print("✅ Summaries generated\n")
            return summaries
        
    except Exception as e:
        print(f"✗ Error generating summaries: {e}\n")
    
    return generate_basic_summary(edition, highlights)

def generate_basic_summary(edition, highlights):
    """
    Fallback basic summary when Claude unavailable
    """
    reddit = f"""AI Automation Builder #{edition['number']}

This week's edition covers:
"""
    for h in highlights[:4]:
        reddit += f"• {h['title']}\n"
    
    reddit += f"\nFull newsletter: {NEWSLETTER_BASE_URL}\n\nFree weekly AI tools & automation workflows for solopreneurs."
    
    twitter = [
        f"AI Automation Builder #{edition['number']} just dropped 👇",
        f"This week: {highlights[0]['title']}",
    ]
    
    for h in highlights[1:4]:
        twitter.append(f"• {h['title'][:100]}")
    
    twitter.append(f"Get it weekly: {NEWSLETTER_BASE_URL}")
    
    linkedin = f"""New edition of AI Automation Builder is live.

This week's highlights:
{chr(10).join(['• ' + h['title'] for h in highlights[:3]])}

Subscribe: {NEWSLETTER_BASE_URL}"""

    return {
        'reddit': reddit,
        'twitter': twitter,
        'linkedin': linkedin
    }

# ============================================================================
# REDDIT POSTING
# ============================================================================

def post_to_reddit(edition, summary):
    """
    Post to relevant subreddits
    """
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("⚠️  Reddit credentials not set, skipping...\n")
        return False
    
    print("📱 Posting to Reddit...")
    
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            user_agent='AI-Automation-Builder-Bot/1.0'
        )
        
        # Subreddits to post to (rotate to avoid spam)
        subreddits = [
            'AutomateYourself',
            'Entrepreneur', 
            'SideProject',
            'Newsletters'
        ]
        
        # Post to 2 subreddits per edition (rotate)
        selected = subreddits[edition['number'] % len(subreddits):edition['number'] % len(subreddits) + 2]
        
        for sub_name in selected[:2]:
            try:
                subreddit = reddit.subreddit(sub_name)
                
                title = f"AI Automation Builder #{edition['number']} - {edition['subject'][:50]}"
                
                submission = subreddit.submit(
                    title=title,
                    selftext=summary['reddit']
                )
                
                print(f"  ✓ Posted to r/{sub_name}: {submission.url}")
                
                # Wait between posts
                time.sleep(600)  # 10 minutes
                
            except Exception as e:
                print(f"  ✗ Error posting to r/{sub_name}: {e}")
        
        print("✅ Reddit posting complete\n")
        return True
        
    except ImportError:
        print("⚠️  PRAW not installed, skipping Reddit\n")
        return False
    except Exception as e:
        print(f"✗ Reddit error: {e}\n")
        return False

# ============================================================================
# TWITTER POSTING
# ============================================================================

def post_twitter_thread(edition, summary):
    """
    Post thread to Twitter
    """
    if not TWITTER_BEARER_TOKEN:
        print("⚠️  Twitter token not set, skipping...\n")
        print("📝 Thread preview (copy/paste manually):\n")
        for i, tweet in enumerate(summary['twitter'], 1):
            print(f"{i}. {tweet}\n")
        return False
    
    print("🐦 Posting Twitter thread...")
    
    try:
        # Twitter API v2 (would need OAuth 2.0 setup)
        # For now, just print thread for manual posting
        print("📝 Copy this thread:\n")
        for i, tweet in enumerate(summary['twitter'], 1):
            print(f"{i}. {tweet}")
            print()
        
        print("⚠️  Auto-posting requires Twitter API v2 OAuth setup")
        print("For now, copy/paste manually\n")
        
        return False
        
    except Exception as e:
        print(f"✗ Twitter error: {e}\n")
        return False

# ============================================================================
# LINKEDIN POSTING
# ============================================================================

def post_to_linkedin(edition, summary):
    """
    Post to LinkedIn
    """
    if not LINKEDIN_ACCESS_TOKEN:
        print("⚠️  LinkedIn token not set, skipping...\n")
        print("📝 Post preview (copy/paste manually):\n")
        print(summary['linkedin'])
        print()
        return False
    
    print("💼 Posting to LinkedIn...")
    
    try:
        # LinkedIn API (would need OAuth setup)
        # For now, print for manual posting
        print("📝 Copy this post:\n")
        print(summary['linkedin'])
        print()
        
        print("⚠️  Auto-posting requires LinkedIn OAuth setup")
        print("For now, copy/paste manually\n")
        
        return False
        
    except Exception as e:
        print(f"✗ LinkedIn error: {e}\n")
        return False

# ============================================================================
# HACKER NEWS
# ============================================================================

def post_to_hackernews(edition):
    """
    Post to Hacker News (if edition has tech depth)
    Show HN posts
    """
    print("📰 Hacker News posting...")
    print("⚠️  HN posting requires manual submission")
    print(f"   Title: AI Automation Builder #{edition['number']}")
    print(f"   URL: {NEWSLETTER_BASE_URL}")
    print(f"   Submit at: https://news.ycombinator.com/submit\n")
    
    return False

# ============================================================================
# TRACKING
# ============================================================================

def track_distribution(edition_number, platform, success, url=None):
    """
    Track distribution results
    """
    log_path = Path(__file__).parent.parent / "logs" / "distribution.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing log
    if log_path.exists():
        with open(log_path, 'r') as f:
            log = json.load(f)
    else:
        log = []
    
    # Add entry
    entry = {
        'edition': edition_number,
        'platform': platform,
        'success': success,
        'url': url,
        'timestamp': datetime.now().isoformat()
    }
    
    log.append(entry)
    
    # Save
    with open(log_path, 'w') as f:
        json.dump(log, f, indent=2)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main distribution workflow
    """
    print("=" * 60)
    print("AI AUTOMATION BUILDER - AUTO DISTRIBUTION")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    # Get latest edition
    edition = get_latest_edition()
    
    if not edition:
        print("⚠️  No published edition found")
        print("Publish a newsletter first, then run this script\n")
        return
    
    print(f"\n📰 Edition #{edition['number']}: {edition['subject']}\n")
    
    # Get content highlights
    highlights = get_edition_highlights(edition['number'])
    
    if not highlights:
        print("⚠️  No content found for edition")
        return
    
    print(f"📊 Found {len(highlights)} highlights\n")
    
    # Generate summaries for each platform
    summaries = generate_social_summary(edition, highlights)
    
    # Distribute to platforms
    results = {}
    
    # Reddit
    results['reddit'] = post_to_reddit(edition, summaries)
    track_distribution(edition['number'], 'reddit', results['reddit'])
    
    # Twitter
    results['twitter'] = post_twitter_thread(edition, summaries)
    track_distribution(edition['number'], 'twitter', results['twitter'])
    
    # LinkedIn
    results['linkedin'] = post_to_linkedin(edition, summaries)
    track_distribution(edition['number'], 'linkedin', results['linkedin'])
    
    # Hacker News (manual)
    results['hackernews'] = post_to_hackernews(edition)
    
    # Summary
    print("=" * 60)
    print("✅ DISTRIBUTION COMPLETE")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    print(f"\nAutomated: {success_count}/4 platforms")
    print(f"Manual: {4 - success_count}/4 platforms\n")
    
    if success_count < 4:
        print("💡 Tip: Set up OAuth for full automation")
        print("   For now, copy/paste the previews above\n")

if __name__ == "__main__":
    main()
