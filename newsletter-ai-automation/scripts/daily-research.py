#!/usr/bin/env python3
"""
AI Automation Builder - Daily Research Script

Runs daily at 09:00 UTC to collect and curate content from:
- RSS feeds (TechCrunch, VentureBeat, etc)
- Reddit (r/automation, r/Entrepreneur, etc)
- Twitter (AI influencers)
- Product Hunt (AI tools)
- GitHub (trending AI repos)

Scores content with Claude and saves to database.
"""

import os
import sys
import json
import sqlite3
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"
STATE_PATH = Path(__file__).parent.parent / ".state"
LOG_PATH = Path(__file__).parent.parent / "logs"

# API Keys (will be set via env or config)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
PRODUCTHUNT_TOKEN = os.getenv("PRODUCTHUNT_TOKEN", "")

# RSS Feeds to monitor
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.producthunt.com/topics/artificial-intelligence.rss",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://blog.google/technology/ai/rss/",
]

# Subreddits to monitor
SUBREDDITS = [
    "artificial",
    "MachineLearning",
    "OpenAI",
    "ChatGPT",
    "AutomateYourself",
    "nocode",
    "Entrepreneur",
    "SideProject",
    "SaaS",
]

# Twitter accounts to monitor (if API available)
TWITTER_ACCOUNTS = [
    "sama",  # Sam Altman
    "gdb",  # Greg Brockman
    "AnthropicAI",
    "OpenAI",
    "GoogleAI",
    "LangChainAI",
    "n8n_io",
    "zapier",
]

# ============================================================================
# RSS MONITORING
# ============================================================================

def monitor_rss_feeds():
    """
    Fetch articles from RSS feeds
    Returns list of article dicts
    """
    articles = []
    
    print(f"\n📡 Monitoring {len(RSS_FEEDS)} RSS feeds...")
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            feed_name = feed.feed.title if hasattr(feed.feed, 'title') else feed_url
            
            for entry in feed.entries[:15]:  # Top 15 per feed
                # Only articles from last 3 days
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                    if pub_date < datetime.now() - timedelta(days=3):
                        continue
                
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:300],
                    'source': f"RSS: {feed_name}",
                    'type': 'article'
                })
            
            print(f"  ✓ {feed_name}: {len(feed.entries)} articles")
            
        except Exception as e:
            print(f"  ✗ Error fetching {feed_url}: {e}")
    
    print(f"✅ Collected {len(articles)} RSS articles\n")
    return articles

# ============================================================================
# REDDIT MONITORING
# ============================================================================

def monitor_reddit():
    """
    Fetch top posts from subreddits
    Requires Reddit API credentials
    """
    posts = []
    
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("⚠️  Reddit API credentials not configured, skipping...\n")
        return posts
    
    print(f"📱 Monitoring {len(SUBREDDITS)} subreddits...")
    
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent='ai-automation-builder-newsletter/1.0'
        )
        
        for sub_name in SUBREDDITS:
            try:
                subreddit = reddit.subreddit(sub_name)
                
                for post in subreddit.top('week', limit=10):
                    # Filter: high engagement only
                    if post.score > 50:
                        posts.append({
                            'title': post.title,
                            'url': post.url,
                            'published': datetime.fromtimestamp(post.created_utc).isoformat(),
                            'summary': post.selftext[:300] if post.selftext else '',
                            'source': f"Reddit: r/{sub_name}",
                            'type': 'reddit_post',
                            'score': post.score,
                            'comments': post.num_comments
                        })
                
                print(f"  ✓ r/{sub_name}: {len(list(subreddit.top('week', limit=10)))} posts")
                
            except Exception as e:
                print(f"  ✗ Error fetching r/{sub_name}: {e}")
        
        print(f"✅ Collected {len(posts)} Reddit posts\n")
        
    except ImportError:
        print("⚠️  PRAW not installed (pip install praw), skipping Reddit...\n")
    except Exception as e:
        print(f"✗ Reddit error: {e}\n")
    
    return posts

# ============================================================================
# PRODUCT HUNT MONITORING
# ============================================================================

def monitor_producthunt():
    """
    Fetch trending AI tools from Product Hunt
    """
    products = []
    
    print("🚀 Monitoring Product Hunt AI tools...")
    
    # For now, scrape RSS feed (GraphQL API requires auth)
    try:
        feed = feedparser.parse("https://www.producthunt.com/topics/artificial-intelligence.rss")
        
        for entry in feed.entries[:10]:
            products.append({
                'title': entry.title,
                'url': entry.link,
                'published': entry.get('published', ''),
                'summary': entry.get('summary', '')[:300],
                'source': 'Product Hunt',
                'type': 'tool'
            })
        
        print(f"✅ Collected {len(products)} Product Hunt tools\n")
        
    except Exception as e:
        print(f"✗ Product Hunt error: {e}\n")
    
    return products

# ============================================================================
# GITHUB TRENDING
# ============================================================================

def monitor_github_trending():
    """
    Fetch trending AI repositories
    """
    repos = []
    
    if not GITHUB_TOKEN:
        print("⚠️  GitHub token not configured, skipping...\n")
        return repos
    
    print("💻 Monitoring GitHub trending AI repos...")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    ai_topics = ['artificial-intelligence', 'machine-learning', 'gpt', 'llm', 'ai-agents', 'automation']
    
    for topic in ai_topics:
        try:
            # Search repos by topic, sorted by stars, created in last 30 days
            url = f"https://api.github.com/search/repositories?q=topic:{topic}+created:>{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')}&sort=stars&order=desc&per_page=5"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', []):
                    repos.append({
                        'title': repo['full_name'],
                        'url': repo['html_url'],
                        'published': repo['created_at'],
                        'summary': repo.get('description', '')[:300],
                        'source': 'GitHub',
                        'type': 'repo',
                        'stars': repo['stargazers_count']
                    })
            
        except Exception as e:
            print(f"  ✗ Error fetching topic {topic}: {e}")
    
    print(f"✅ Collected {len(repos)} GitHub repos\n")
    return repos

# ============================================================================
# CLAUDE CURATION
# ============================================================================

def curate_with_claude(items):
    """
    Use Claude to score and curate content
    """
    if not OPENROUTER_API_KEY:
        print("⚠️  OpenRouter API key not configured, using simple scoring...\n")
        return simple_score(items)
    
    print(f"🤖 Curating {len(items)} items with Claude...")
    
    try:
        # Prepare items for Claude (truncate for token efficiency)
        items_summary = []
        for i, item in enumerate(items[:50]):  # Limit to 50 items per batch
            items_summary.append({
                'id': i,
                'title': item['title'],
                'source': item['source'],
                'type': item['type'],
                'summary': item['summary'][:200]
            })
        
        prompt = f"""You are curating content for "AI Automation Builder", a newsletter for solopreneurs building automated businesses with AI.

Target audience:
- One-person businesses
- Indie hackers  
- Automation enthusiasts
- Technical but not researchers

Analyze these {len(items_summary)} items and score each on:
1. **Relevance** (1-10): How relevant to automation/solopreneurs?
2. **Novelty** (1-10): How new/fresh is this?
3. **Usefulness** (1-10): Can readers actually use this?
4. **Impact** (1-10): How significant is this development?

Items:
{json.dumps(items_summary, indent=2)}

Return JSON array with:
- id (from input)
- relevance_score
- novelty_score  
- usefulness_score
- impact_score
- total_score (sum of 4 scores)
- one_sentence_summary
- newsletter_section (pick: "Tool Review" / "News" / "Tutorial" / "Case Study" / "Quick Hit")

Only return the JSON array, nothing else."""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aiautomationbuilder.beehiiv.com"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8192
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
            
            # Parse JSON from response
            scored_items = json.loads(content)
            
            # Merge scores back into original items
            for scored in scored_items:
                item_id = scored['id']
                if item_id < len(items):
                    items[item_id].update(scored)
            
            print(f"✅ Curated {len(scored_items)} items\n")
            return [item for item in items if 'total_score' in item]
            
        else:
            print(f"✗ Claude API error: {response.status_code}")
            return simple_score(items)
            
    except Exception as e:
        print(f"✗ Curation error: {e}")
        return simple_score(items)

def simple_score(items):
    """
    Fallback simple scoring when Claude unavailable
    """
    print("📊 Using simple scoring algorithm...")
    
    for item in items:
        # Basic scoring based on source type and keywords
        score = 24  # Base score (higher to pass threshold)
        
        # Source bonus
        if 'Product Hunt' in item['source']:
            score += 8
        elif 'GitHub' in item['source']:
            score += 6
        elif 'Reddit' in item['source']:
            score += item.get('score', 0) // 20  # Reddit karma
        elif 'RSS' in item['source']:
            score += 4  # RSS articles are usually good
        
        # Keyword bonuses (AI automation related)
        keywords = ['automation', 'api', 'no-code', 'workflow', 'agent', 'gpt', 'claude', 
                   'ai', 'machine learning', 'llm', 'chatgpt', 'openai', 'zapier', 'n8n',
                   'make.com', 'airtable', 'notion', 'tool', 'integration']
        title_lower = item['title'].lower()
        summary_lower = item.get('summary', '').lower()
        
        keyword_matches = 0
        for keyword in keywords:
            if keyword in title_lower or keyword in summary_lower:
                keyword_matches += 1
        
        score += min(keyword_matches * 2, 10)  # Up to +10 for keywords
        
        item['total_score'] = min(score, 40)  # Cap at 40
        item['relevance_score'] = score // 4
        item['novelty_score'] = score // 4
        item['usefulness_score'] = score // 4  
        item['impact_score'] = score // 4
        item['one_sentence_summary'] = item.get('summary', '')[:150]
        
        # Categorize by keywords in title
        if any(kw in title_lower for kw in ['tutorial', 'how to', 'guide']):
            item['newsletter_section'] = 'Tutorial'
        elif any(kw in title_lower for kw in ['tool', 'product', 'app', 'platform']):
            item['newsletter_section'] = 'Tool Review'
        elif any(kw in title_lower for kw in ['launch', 'release', 'announce']):
            item['newsletter_section'] = 'News'
        else:
            item['newsletter_section'] = 'Quick Hit'
    
    print(f"✅ Scored {len(items)} items\n")
    return items

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def init_database():
    """
    Initialize SQLite database with required tables
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Content items table
    c.execute('''
        CREATE TABLE IF NOT EXISTS content_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            source TEXT,
            type TEXT,
            total_score INTEGER,
            relevance_score INTEGER,
            novelty_score INTEGER,
            usefulness_score INTEGER,
            impact_score INTEGER,
            summary TEXT,
            newsletter_section TEXT,
            published_date TEXT,
            featured_in_edition INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Editions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS editions (
            edition_number INTEGER PRIMARY KEY,
            publish_date TEXT,
            subject_line TEXT,
            open_rate REAL,
            click_rate REAL,
            subscriber_count INTEGER,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    # Subscriber stats table
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriber_stats (
            date TEXT PRIMARY KEY,
            total_subscribers INTEGER,
            new_subscribers INTEGER,
            unsubscribes INTEGER,
            source TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized\n")

def save_content_to_db(items):
    """
    Save curated content items to database
    Avoid duplicates based on URL
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    saved_count = 0
    duplicate_count = 0
    
    for item in items:
        try:
            c.execute('''
                INSERT INTO content_items 
                (url, title, source, type, total_score, relevance_score, 
                 novelty_score, usefulness_score, impact_score, summary, 
                 newsletter_section, published_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['url'],
                item['title'],
                item['source'],
                item['type'],
                item.get('total_score', 0),
                item.get('relevance_score', 0),
                item.get('novelty_score', 0),
                item.get('usefulness_score', 0),
                item.get('impact_score', 0),
                item.get('one_sentence_summary', item.get('summary', '')),
                item.get('newsletter_section', 'Quick Hit'),
                item.get('published', datetime.now().isoformat())
            ))
            saved_count += 1
            
        except sqlite3.IntegrityError:
            # URL already exists
            duplicate_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"💾 Saved {saved_count} new items, skipped {duplicate_count} duplicates\n")
    return saved_count

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main research workflow
    """
    print("=" * 60)
    print("AI AUTOMATION BUILDER - DAILY RESEARCH")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    # Ensure directories exist
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    STATE_PATH.mkdir(parents=True, exist_ok=True)
    
    # Initialize database
    init_database()
    
    # Collect content from all sources
    all_items = []
    
    all_items.extend(monitor_rss_feeds())
    all_items.extend(monitor_reddit())
    all_items.extend(monitor_producthunt())
    all_items.extend(monitor_github_trending())
    
    print(f"📊 Total items collected: {len(all_items)}\n")
    
    if not all_items:
        print("⚠️  No new content collected. Exiting.")
        return
    
    # Curate with Claude (or simple scoring)
    scored_items = curate_with_claude(all_items)
    
    # Filter high-quality items (score >= 28 out of 40)
    high_quality = [item for item in scored_items if item.get('total_score', 0) >= 28]
    
    print(f"⭐ High-quality items (score >= 28): {len(high_quality)}\n")
    
    # Save to database
    saved = save_content_to_db(high_quality)
    
    # Update state file
    state = {
        'last_run': datetime.now().isoformat(),
        'items_collected': len(all_items),
        'items_scored': len(scored_items),
        'items_saved': saved
    }
    
    with open(STATE_PATH / 'daily-research-state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print("=" * 60)
    print("✅ DAILY RESEARCH COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
