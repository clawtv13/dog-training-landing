#!/usr/bin/env python3
"""
Smart Reddit Distribution Strategy
- 10+ relevant subreddits
- Rotation to avoid spam detection
- Timing optimization
- Value-first approach (not just links)
- Track what works
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# SUBREDDIT DATABASE
# ============================================================================

SUBREDDITS = {
    # High-value, automation-focused
    'AutomateYourself': {
        'size': 'small',
        'vibe': 'casual_helpful',
        'best_time': '14:00',  # UTC
        'frequency': 'weekly',
        'rules': 'Self-promotion OK if valuable'
    },
    'Entrepreneur': {
        'size': 'large',
        'vibe': 'professional',
        'best_time': '13:00',
        'frequency': 'biweekly',
        'rules': 'Must add value, not just links'
    },
    'SideProject': {
        'size': 'medium',
        'vibe': 'community_show_and_tell',
        'best_time': '15:00',
        'frequency': 'weekly',
        'rules': 'Show your work, ask feedback'
    },
    'Newsletters': {
        'size': 'small',
        'vibe': 'newsletter_focused',
        'best_time': '12:00',
        'frequency': 'biweekly',
        'rules': 'Newsletter promotion welcomed'
    },
    'SaaS': {
        'size': 'medium',
        'vibe': 'professional',
        'best_time': '14:00',
        'frequency': 'biweekly',
        'rules': 'Focus on tools/products'
    },
    'startups': {
        'size': 'large',
        'vibe': 'professional',
        'best_time': '13:00',
        'frequency': 'monthly',
        'rules': 'High-quality only'
    },
    'artificial': {
        'size': 'large',
        'vibe': 'technical',
        'best_time': '15:00',
        'frequency': 'monthly',
        'rules': 'Technical depth required'
    },
    'ChatGPT': {
        'size': 'huge',
        'vibe': 'casual',
        'best_time': '16:00',
        'frequency': 'weekly',
        'rules': 'Practical use cases'
    },
    'OpenAI': {
        'size': 'large',
        'vibe': 'technical',
        'best_time': '15:00',
        'frequency': 'biweekly',
        'rules': 'OpenAI-specific content'
    },
    'ArtificialIntelligence': {
        'size': 'huge',
        'vibe': 'technical',
        'best_time': '14:00',
        'frequency': 'monthly',
        'rules': 'High signal-to-noise ratio'
    },
    'ProductManagement': {
        'size': 'medium',
        'vibe': 'professional',
        'best_time': '13:00',
        'frequency': 'biweekly',
        'rules': 'Product-focused insights'
    },
    'marketing': {
        'size': 'large',
        'vibe': 'professional',
        'best_time': '12:00',
        'frequency': 'monthly',
        'rules': 'Marketing strategy'
    },
    'GrowthHacking': {
        'size': 'medium',
        'vibe': 'tactical',
        'best_time': '14:00',
        'frequency': 'biweekly',
        'rules': 'Tactics & experiments'
    },
    'buildinpublic': {
        'size': 'small',
        'vibe': 'transparent',
        'best_time': '15:00',
        'frequency': 'weekly',
        'rules': 'Share your journey'
    },
    'IndieHackers': {
        'size': 'medium',
        'vibe': 'community',
        'best_time': '14:00',
        'frequency': 'weekly',
        'rules': 'Indie maker content'
    }
}

STATE_FILE = Path(__file__).parent.parent / ".state" / "reddit-posts.json"

# ============================================================================
# POSTING STRATEGY
# ============================================================================

def load_posting_history():
    """Load history of Reddit posts"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_post_record(subreddit, post_data):
    """Save post record"""
    history = load_posting_history()
    
    if subreddit not in history:
        history[subreddit] = []
    
    history[subreddit].append({
        'title': post_data['title'],
        'url': post_data.get('reddit_url'),
        'posted_at': datetime.now().isoformat(),
        'post_slug': post_data.get('post_slug')
    })
    
    with open(STATE_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def can_post_to_subreddit(subreddit):
    """Check if we can post to this subreddit based on frequency rules"""
    history = load_posting_history()
    
    if subreddit not in history or not history[subreddit]:
        return True
    
    last_post = history[subreddit][-1]
    last_post_time = datetime.fromisoformat(last_post['posted_at'])
    
    frequency = SUBREDDITS[subreddit]['frequency']
    
    thresholds = {
        'daily': timedelta(days=1),
        'weekly': timedelta(days=7),
        'biweekly': timedelta(days=14),
        'monthly': timedelta(days=30)
    }
    
    return datetime.now() - last_post_time > thresholds[frequency]

def select_subreddits_for_today(max_posts=3):
    """Select best subreddits to post to today"""
    available = []
    
    for subreddit, info in SUBREDDITS.items():
        if can_post_to_subreddit(subreddit):
            # Calculate priority score
            size_score = {'small': 1, 'medium': 2, 'large': 3, 'huge': 4}[info['size']]
            
            # Prefer subreddits we haven't posted to recently
            history = load_posting_history()
            recency_score = 1 if subreddit not in history else 1 / (len(history[subreddit]) + 1)
            
            priority = size_score * recency_score
            
            available.append((subreddit, priority))
    
    # Sort by priority and return top N
    available.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in available[:max_posts]]

# ============================================================================
# POST FORMATTING
# ============================================================================

def format_post_for_subreddit(subreddit, post_data):
    """
    Format post based on subreddit culture
    """
    vibe = SUBREDDITS[subreddit]['vibe']
    
    # Base format
    if vibe == 'casual_helpful':
        # AutomateYourself, ChatGPT style
        title = f"🤖 {post_data['title'][:90]}"
        body = f"""Hey everyone!

Found this really helpful: {post_data['title']}

{post_data['summary'][:200]}...

**Why it's useful:**
{post_data['takeaway']}

Full article: {post_data['url']}

Also running a free weekly newsletter on AI automation if anyone's interested: {post_data['newsletter_url']}

Happy to answer questions!"""
    
    elif vibe == 'professional':
        # Entrepreneur, SaaS, ProductManagement style
        title = f"{post_data['title'][:100]}"
        body = f"""Wanted to share something I found valuable:

{post_data['summary'][:300]}

**Key takeaway:** {post_data['takeaway']}

This is particularly relevant for [audience benefit].

Read more: {post_data['url']}

*(I write about AI automation for solopreneurs at {post_data['newsletter_url']})*"""
    
    elif vibe == 'community_show_and_tell':
        # SideProject, buildinpublic style
        title = f"Built: {post_data['title'][:80]}"
        body = f"""Working on a project to help solopreneurs automate with AI.

Latest article: {post_data['title']}

{post_data['summary'][:250]}

Would love your feedback!

Link: {post_data['url']}

Newsletter: {post_data['newsletter_url']}"""
    
    elif vibe == 'technical':
        # artificial, ArtificialIntelligence, OpenAI style
        title = f"[Research] {post_data['title'][:90]}"
        body = f"""Deep dive into {post_data['topic']}:

{post_data['summary'][:400]}

Technical details: {post_data['url']}

Background: I'm researching AI automation workflows and sharing findings weekly at {post_data['newsletter_url']}

Thoughts?"""
    
    elif vibe == 'newsletter_focused':
        # Newsletters subreddit
        title = f"AI Automation Builder - {post_data['title'][:70]}"
        body = f"""Running a newsletter on AI automation for solopreneurs.

This week's highlight: {post_data['title']}

{post_data['summary'][:300]}

Subscribe: {post_data['newsletter_url']}

Latest article: {post_data['url']}

Free, weekly, actionable tips. No fluff."""
    
    else:
        # Default format
        title = post_data['title'][:100]
        body = f"""{post_data['summary'][:300]}

{post_data['url']}"""
    
    return {
        'title': title,
        'body': body
    }

# ============================================================================
# SMART POSTING
# ============================================================================

def smart_reddit_post(post_data, dry_run=True):
    """
    Intelligently post to Reddit with:
    - Subreddit selection
    - Timing optimization
    - Format customization
    - Rate limiting
    """
    print("=" * 60)
    print("SMART REDDIT DISTRIBUTION")
    print("=" * 60)
    print()
    
    # Select best subreddits for today
    selected_subs = select_subreddits_for_today(max_posts=3)
    
    if not selected_subs:
        print("⚠️  No subreddits available today (frequency limits)")
        print("Next available posting slots:")
        for sub in list(SUBREDDITS.keys())[:5]:
            if not can_post_to_subreddit(sub):
                history = load_posting_history()
                last_post = history[sub][-1]
                print(f"  • r/{sub}: {last_post['posted_at'][:10]}")
        return
    
    print(f"📊 Selected {len(selected_subs)} subreddits for today:\n")
    
    for subreddit in selected_subs:
        info = SUBREDDITS[subreddit]
        
        print(f"r/{subreddit}")
        print(f"  Size: {info['size']} | Vibe: {info['vibe']}")
        print(f"  Best time: {info['best_time']} UTC")
        print(f"  Rules: {info['rules']}")
        
        # Format post
        formatted = format_post_for_subreddit(subreddit, post_data)
        
        print(f"\n  📝 Post preview:")
        print(f"  Title: {formatted['title']}")
        print(f"  Body: {formatted['body'][:150]}...\n")
        
        if dry_run:
            print(f"  [DRY RUN] Would post to r/{subreddit}\n")
        else:
            # Actually post (requires PRAW setup)
            try:
                import praw
                
                reddit = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                    username=os.getenv('REDDIT_USERNAME'),
                    password=os.getenv('REDDIT_PASSWORD'),
                    user_agent='AI-Automation-Builder/1.0'
                )
                
                subreddit_obj = reddit.subreddit(subreddit)
                submission = subreddit_obj.submit(
                    title=formatted['title'],
                    selftext=formatted['body']
                )
                
                print(f"  ✅ Posted: {submission.url}\n")
                
                save_post_record(subreddit, {
                    'title': formatted['title'],
                    'reddit_url': submission.url,
                    'post_slug': post_data.get('slug')
                })
                
                # Wait between posts (be respectful)
                time.sleep(random.randint(300, 600))  # 5-10 minutes
                
            except ImportError:
                print(f"  ⚠️  PRAW not installed (pip install praw)\n")
            except Exception as e:
                print(f"  ✗ Error posting: {e}\n")
        
        print("-" * 60)
        print()
    
    if dry_run:
        print("🔧 To enable real posting:")
        print("  1. pip install praw")
        print("  2. Set environment variables:")
        print("     export REDDIT_CLIENT_ID='...'")
        print("     export REDDIT_CLIENT_SECRET='...'")
        print("     export REDDIT_USERNAME='...'")
        print("     export REDDIT_PASSWORD='...'")
        print("  3. Run again with dry_run=False")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Test with sample post data"""
    
    sample_post = {
        'title': 'How I Automated My Entire Content Pipeline with AI (Saves 10h/week)',
        'summary': 'Built a system that researches, writes, and distributes content automatically using ChatGPT, Zapier, and custom scripts. Goes from research to published in minutes.',
        'takeaway': 'You can automate 80% of content work while maintaining quality. The key is breaking it into small, repeatable steps.',
        'topic': 'content automation',
        'url': 'https://aiautomationbuilder.com/posts/content-automation',
        'newsletter_url': 'https://aiautomationbuilder.beehiiv.com',
        'slug': '2026-03-29-content-automation'
    }
    
    smart_reddit_post(sample_post, dry_run=True)

if __name__ == "__main__":
    main()
