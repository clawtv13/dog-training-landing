#!/usr/bin/env python3
"""
AI Automation Builder - Real-Time Research (Enhanced)

Multi-source monitoring for FIRST MOVER advantage:
- Twitter streaming (AI founders, companies)
- Hacker News top stories
- GitHub trending (hourly updates)
- Product Hunt daily launches
- Discord webhooks (if configured)
- Reddit live threads

Runs every 30 minutes to catch breaking news.
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import deduplication module
from deduplication import deduplicate_items

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"
STATE_PATH = Path(__file__).parent.parent / ".state"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# High-priority Twitter accounts (breaking news)
PRIORITY_TWITTER = [
    "sama",           # Sam Altman (OpenAI CEO)
    "gdb",            # Greg Brockman (OpenAI)
    "AnthropicAI",    # Anthropic official
    "OpenAI",         # OpenAI official
    "GoogleAI",       # Google AI
    "demishassabis",  # DeepMind CEO
    "ylecun",         # Yann LeCun (Meta AI)
    "karpathy",       # Andrej Karpathy
    "tszzl",          # Aravind Srinivas (Perplexity)
    "emollick",       # Ethan Mollick (AI educator)
    "levelsio",       # Pieter Levels (indie hacker)
    "marc_louvion",   # AI automation expert
]

# ============================================================================
# HACKER NEWS MONITORING
# ============================================================================

def monitor_hackernews():
    """
    Fetch top AI-related stories from Hacker News
    HN is usually 10-60 min ahead of RSS feeds
    """
    items = []
    
    print("📰 Monitoring Hacker News...")
    
    try:
        # Get top 30 stories
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        
        if response.status_code == 200:
            story_ids = response.json()[:30]
            
            for story_id in story_ids:
                try:
                    story_response = requests.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                        timeout=5
                    )
                    
                    if story_response.status_code == 200:
                        story = story_response.json()
                        title = story.get('title', '').lower()
                        
                        # Filter AI-related stories
                        ai_keywords = ['ai', 'gpt', 'llm', 'claude', 'gemini', 
                                     'automation', 'machine learning', 'openai',
                                     'anthropic', 'agent', 'chatbot']
                        
                        if any(kw in title for kw in ai_keywords):
                            items.append({
                                'title': story.get('title', ''),
                                'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                                'published': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                                'summary': f"HN Score: {story.get('score', 0)} points, {story.get('descendants', 0)} comments",
                                'source': 'Hacker News',
                                'type': 'news',
                                'hn_score': story.get('score', 0)
                            })
                
                except Exception as e:
                    continue
            
            print(f"✅ Found {len(items)} AI stories on HN\n")
        
    except Exception as e:
        print(f"✗ HN error: {e}\n")
    
    return items

# ============================================================================
# GITHUB TRENDING (Real-time)
# ============================================================================

def monitor_github_trending():
    """
    Check GitHub trending repos (updates hourly)
    No API key needed for trending page scraping
    """
    items = []
    
    print("⭐ Monitoring GitHub Trending...")
    
    # Trending repositories for AI topics
    trending_urls = [
        "https://api.github.com/search/repositories?q=topic:artificial-intelligence+stars:>100&sort=updated&order=desc&per_page=10",
        "https://api.github.com/search/repositories?q=topic:llm+stars:>50&sort=updated&order=desc&per_page=10",
        "https://api.github.com/search/repositories?q=topic:ai-agents+stars:>20&sort=updated&order=desc&per_page=10",
    ]
    
    for url in trending_urls:
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', [])[:5]:
                    # Only repos updated in last 24 hours
                    updated = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
                    if updated > datetime.now().astimezone() - timedelta(days=1):
                        items.append({
                            'title': f"{repo['full_name']} - {repo.get('description', 'No description')[:100]}",
                            'url': repo['html_url'],
                            'published': repo['created_at'],
                            'summary': f"⭐ {repo['stargazers_count']} stars, {repo.get('language', 'Unknown')} | {repo.get('description', '')}",
                            'source': 'GitHub Trending',
                            'type': 'repo',
                            'stars': repo['stargazers_count']
                        })
            
        except Exception as e:
            print(f"  ✗ Error with {url}: {e}")
            continue
    
    print(f"✅ Found {len(items)} trending AI repos\n")
    return items

# ============================================================================
# PRODUCT HUNT (Daily Launches)
# ============================================================================

def monitor_producthunt_today():
    """
    Get today's AI tool launches from Product Hunt
    Launches go live at 00:01 PST daily
    """
    items = []
    
    print("🚀 Monitoring Product Hunt today's launches...")
    
    try:
        # Product Hunt RSS feed
        import feedparser
        
        feed = feedparser.parse("https://www.producthunt.com/topics/artificial-intelligence.rss")
        
        today = datetime.now().date()
        
        for entry in feed.entries[:20]:
            # Parse publish date
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime(*entry.published_parsed[:6]).date()
                
                # Only today's launches
                if pub_date == today:
                    items.append({
                        'title': entry.title,
                        'url': entry.link,
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', '')[:300],
                        'source': 'Product Hunt (Today)',
                        'type': 'tool'
                    })
        
        print(f"✅ Found {len(items)} AI tools launched today\n")
        
    except Exception as e:
        print(f"✗ Product Hunt error: {e}\n")
    
    return items

# ============================================================================
# REDDIT LIVE MONITORING
# ============================================================================

def monitor_reddit_live():
    """
    Check Reddit for breaking AI news
    Focus on 'new' instead of 'top' for speed
    """
    items = []
    
    print("🔴 Monitoring Reddit live threads...")
    
    subreddits = [
        'artificial',
        'MachineLearning',
        'OpenAI',
        'ChatGPT',
        'singularity',
        'Futurology'
    ]
    
    for sub in subreddits:
        try:
            # Use Reddit JSON API (no auth needed for public posts)
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=25"
            headers = {'User-Agent': 'AI-Automation-Builder/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data['data']['children']:
                    post_data = post['data']
                    
                    # Only posts from last 6 hours
                    created = datetime.fromtimestamp(post_data['created_utc'])
                    if created > datetime.now() - timedelta(hours=6):
                        # High engagement filter
                        if post_data['score'] > 10 or post_data['num_comments'] > 5:
                            items.append({
                                'title': post_data['title'],
                                'url': post_data['url'],
                                'published': created.isoformat(),
                                'summary': post_data.get('selftext', '')[:300],
                                'source': f"Reddit: r/{sub} (Live)",
                                'type': 'discussion',
                                'score': post_data['score']
                            })
        
        except Exception as e:
            print(f"  ✗ Error r/{sub}: {e}")
            continue
    
    print(f"✅ Found {len(items)} live Reddit discussions\n")
    return items

# ============================================================================
# AI-POWERED BREAKING NEWS DETECTION
# ============================================================================

def detect_breaking_news(items):
    """
    Use Claude to identify genuinely breaking/important news
    Send instant Telegram alert for critical stories
    """
    if not OPENROUTER_API_KEY:
        print("⚠️  OpenRouter key not set, skipping breaking news detection\n")
        return items
    
    print(f"🔥 Analyzing {len(items)} items for breaking news...")
    
    try:
        # Prepare items for Claude
        items_summary = []
        for i, item in enumerate(items[:30]):
            items_summary.append({
                'id': i,
                'title': item['title'],
                'source': item['source'],
                'url': item['url']
            })
        
        prompt = f"""# Research Breaking News Detection

## ROLE
AI news analyst specializing in actionable intelligence for AI builders, solopreneurs, and technical implementers.

## INPUT
{json.dumps(items_summary, indent=2)} - timestamped news items from last 24h

## TASK
Identify 1-3 breaking news stories that require immediate attention from AI practitioners building products or businesses.

## REQUIREMENTS

### MUST:
- Return valid JSON matching exact schema below
- Flag only stories published <6 hours ago
- Select max 3 items (prefer 1-2 high-impact over 3 marginal)
- Include specific business/technical impact in reason

### SHOULD:
- Prioritize stories affecting product development, API changes, new capabilities
- Focus on actionable intelligence over industry commentary
- Consider urgency 7+ only for stories requiring action within 48h
- Weight toward cost changes, feature launches, policy updates

### AVOID:
- Funding announcements without product implications
- Vague "AI advancement" stories without specifics
- Repackaged existing news with new headlines
- Pure research papers without implementation path
- Marketing announcements disguised as news

## BREAKING NEWS CRITERIA
Score stories on:
- **Recency**: <2h = high priority, 2-6h = medium priority
- **Impact**: API breaking changes, pricing shifts, new model releases
- **Actionability**: Can readers act on this within 1 week?
- **Relevance**: Affects AI builders, not just enterprise/research

## OUTPUT FORMAT

VALID:
{{
  "breaking_news": [
    {{
      "id": 2,
      "reason": "OpenAI GPT-4 API price dropped 60% - immediate cost savings for production apps",
      "urgency": 8
    }}
  ]
}}

INVALID:
```json
{{
  "breaking_news": [...]
}}
```
(Reason: markdown formatting)

{{
  "stories": [...]
}}
(Reason: wrong key name)

VALIDATION:
- JSON parses without errors
- "breaking_news" array with 0-3 objects
- Each object has: id (number), reason (string), urgency (1-10)
- Reason explains specific impact, not generic importance

## EDGE CASES
IF no stories <6h old: THEN return empty array
IF >3 high-impact stories: THEN select 3 highest urgency scores
IF uncertain about timing: THEN exclude (prefer false negative)
ELSE: Return empty array

## RETURN
Return ONLY valid JSON. No markdown blocks, explanations, or additional text."""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            try:
                # Try direct JSON parse first
                analysis = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: Extract JSON from markdown code blocks
                import re
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    try:
                        analysis = json.loads(match.group(1))
                    except:
                        print("✗ Could not parse breaking news (even from markdown)\n")
                        return items
                else:
                    print("✗ No valid JSON found in response\n")
                    return items
            
            # Process breaking news
            breaking_news = analysis.get('breaking_news', [])
            
            # Send Telegram alerts for breaking news
            for news_item in breaking_news:
                item_id = news_item.get('id', -1)
                if 0 <= item_id < len(items):
                    item = items[item_id]
                    urgency = news_item.get('urgency', 5)
                    reason = news_item.get('reason', 'Breaking AI news')
                    
                    if urgency >= 8:
                        send_breaking_news_alert(item, reason, urgency)
            
            print(f"🔥 Detected {len(breaking_news)} breaking stories\n")
        
    except Exception as e:
        print(f"✗ Breaking news detection error: {e}\n")
    
    return items

def send_breaking_news_alert(item, reason, urgency):
    """
    Send immediate Telegram alert for breaking news
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    message = f"""🚨 **BREAKING AI NEWS** (Urgency: {urgency}/10)

**{item['title']}**

{reason}

🔗 {item['url']}

Source: {item['source']}

_Add to next newsletter immediately_"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
        print(f"  📲 Sent breaking news alert: {item['title'][:50]}...\n")
    except:
        pass

# ============================================================================
# ENHANCED SCORING WITH RECENCY BOOST
# ============================================================================

def score_with_recency(items):
    """
    Score items with bonus for recency
    Newer = higher priority
    """
    print(f"📊 Scoring {len(items)} items with recency boost...")
    
    now = datetime.now()
    
    for item in items:
        # Base score
        score = 24
        
        # Source bonus
        if 'Hacker News' in item['source']:
            score += 8  # HN is high quality
        elif 'GitHub' in item['source']:
            score += 6
        elif 'Product Hunt (Today)' in item['source']:
            score += 10  # Today's launches are priority
        elif 'Live' in item['source']:
            score += 7  # Live threads are fresh
        elif 'RSS' in item['source']:
            score += 4
        
        # Recency bonus (published in last 6 hours = +8 points)
        try:
            if item.get('published'):
                pub_date = None
                if isinstance(item['published'], str):
                    # Try parsing ISO format
                    try:
                        pub_date = datetime.fromisoformat(item['published'].replace('Z', '+00:00'))
                    except:
                        pass
                
                if pub_date:
                    hours_old = (now.astimezone() - pub_date).total_seconds() / 3600
                    
                    if hours_old < 1:
                        score += 10  # Less than 1 hour old = BREAKING
                    elif hours_old < 6:
                        score += 8   # Last 6 hours
                    elif hours_old < 24:
                        score += 4   # Last 24 hours
        except:
            pass
        
        # Engagement bonus
        if item.get('hn_score', 0) > 100:
            score += 5
        elif item.get('hn_score', 0) > 50:
            score += 3
        
        if item.get('score', 0) > 100:  # Reddit
            score += 4
        
        # Keyword matching
        keywords = ['automation', 'api', 'no-code', 'workflow', 'agent', 'gpt',
                   'claude', 'ai', 'launch', 'release', 'announce', 'tool']
        title_lower = item['title'].lower()
        summary_lower = item.get('summary', '').lower()
        
        keyword_matches = sum(1 for kw in keywords if kw in title_lower or kw in summary_lower)
        score += min(keyword_matches * 2, 10)
        
        item['total_score'] = min(score, 50)  # Cap at 50
        item['relevance_score'] = score // 5
        item['novelty_score'] = score // 5
        item['usefulness_score'] = score // 5
        item['impact_score'] = score // 5
        item['one_sentence_summary'] = item.get('summary', '')[:150]
        
        # Categorize
        if 'launch' in title_lower or 'product hunt' in item['source'].lower():
            item['newsletter_section'] = 'Tool Review'
        elif 'github' in item['source'].lower():
            item['newsletter_section'] = 'Tool Review'
        elif 'tutorial' in title_lower or 'how to' in title_lower:
            item['newsletter_section'] = 'Tutorial'
        else:
            item['newsletter_section'] = 'News'
    
    print(f"✅ Scored {len(items)} items\n")
    return items

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def save_to_database(items):
    """
    Save items to database, avoiding duplicates
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
                item.get('newsletter_section', 'News'),
                item.get('published', datetime.now().isoformat())
            ))
            saved_count += 1
            
        except sqlite3.IntegrityError:
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
    Real-time monitoring workflow
    Run every 30 minutes for first-mover advantage
    """
    print("=" * 60)
    print("AI AUTOMATION BUILDER - REAL-TIME RESEARCH")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    STATE_PATH.mkdir(parents=True, exist_ok=True)
    
    # Collect from all sources
    all_items = []
    
    all_items.extend(monitor_hackernews())
    all_items.extend(monitor_github_trending())
    all_items.extend(monitor_producthunt_today())
    all_items.extend(monitor_reddit_live())
    
    print(f"📊 Total items collected: {len(all_items)}\n")
    
    if not all_items:
        print("⚠️  No new content found. Exiting.")
        return
    
    # Deduplicate before processing (50% similarity threshold)
    all_items = deduplicate_items(all_items, similarity_threshold=0.50)
    
    # Detect breaking news (sends alerts)
    all_items = detect_breaking_news(all_items)
    
    # Score with recency boost
    scored_items = score_with_recency(all_items)
    
    # Filter high-quality (threshold: 32 for breaking news)
    high_quality = [item for item in scored_items if item.get('total_score', 0) >= 32]
    
    print(f"⭐ High-priority items (score >= 32): {len(high_quality)}\n")
    
    # Save to database
    if high_quality:
        saved = save_to_database(high_quality)
        
        # Update state
        state = {
            'last_run': datetime.now().isoformat(),
            'items_collected': len(all_items),
            'items_saved': saved,
            'breaking_news': len([i for i in scored_items if i.get('total_score', 0) >= 45])
        }
        
        with open(STATE_PATH / 'realtime-research-state.json', 'w') as f:
            json.dump(state, f, indent=2)
    
    print("=" * 60)
    print("✅ REAL-TIME RESEARCH COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
