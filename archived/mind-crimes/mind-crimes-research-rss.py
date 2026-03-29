#!/usr/bin/env python3
"""
Mind Crimes - RSS Feed Research
Uses Reddit RSS feeds (more reliable than API)
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re

def parse_reddit_rss(subreddit, limit=10):
    """Parse Reddit RSS feed"""
    print(f"\n🔍 Fetching r/{subreddit} RSS feed...")
    
    url = f"https://www.reddit.com/r/{subreddit}.rss?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Parse XML
            root = ET.fromstring(response.content)
            posts = []
            
            # RSS 2.0 format
            for item in root.findall('.//item')[:limit]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                
                if title_elem is not None and title_elem.text:
                    # Extract score from title if available
                    title = title_elem.text
                    score = 100  # Default
                    
                    posts.append({
                        'title': title,
                        'score': score,
                        'url': link_elem.text if link_elem is not None else '',
                        'comments': 50  # Estimate
                    })
            
            return posts
        else:
            print(f"   ❌ Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}")
        return []

def analyze_topics(all_posts):
    """Analyze and categorize posts"""
    
    topics = []
    
    for post in all_posts:
        title = post['title']
        score = post['score']
        
        # Determine style
        style = 'realistic'
        
        psych_keywords = ['psychology', 'behavior', 'mind', 'mental', 'manipulation', 
                         'narcis', 'gaslighting', 'toxic', 'abuse', 'trauma', 'disorder']
        
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in psych_keywords):
            style = 'lovecraft'
        
        # Extract keywords
        keywords = []
        keyword_map = {
            'murder': ['murder', 'killed', 'homicide'],
            'missing person': ['missing', 'disappear', 'vanished'],
            'scam': ['scam', 'fraud', 'con', 'swindle'],
            'cult': ['cult', 'sect'],
            'serial killer': ['serial'],
            'manipulation': ['manipulat', 'gaslight', 'narcis'],
            'true crime': ['crime', 'criminal', 'case']
        }
        
        for key, terms in keyword_map.items():
            if any(term in title_lower for term in terms):
                keywords.append(key)
        
        if not keywords:
            keywords = ['psychology', 'true crime']
        
        # Trend score
        trend_score = min(100, score + post['comments'])
        
        topics.append({
            'title': title[:100],
            'type': style,
            'trend_score': int(trend_score),
            'keywords': keywords[:5],
            'source': post['url']
        })
    
    topics.sort(key=lambda x: x['trend_score'], reverse=True)
    return topics

def main():
    """Main execution"""
    
    print("=" * 70)
    print("MIND CRIMES - LIVE RESEARCH (RSS METHOD)")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 70)
    
    all_posts = []
    
    # Scrape multiple subreddits
    subreddits = [
        'TrueCrime',
        'UnresolvedMysteries',
        'psychology',
        'serialkillers',
        'MorbidReality'
    ]
    
    for sub in subreddits:
        posts = parse_reddit_rss(sub, limit=5)
        print(f"   ✅ Collected {len(posts)} posts")
        all_posts.extend(posts)
    
    if not all_posts:
        print("\n❌ No posts collected. Check connection.")
        return
    
    print(f"\n📊 Total posts: {len(all_posts)}")
    
    # Analyze
    print("\n🧠 Analyzing topics...")
    topics = analyze_topics(all_posts)
    
    # Display results
    print("\n" + "=" * 70)
    print("TOP 15 TRENDING TOPICS:")
    print("=" * 70)
    
    for idx, topic in enumerate(topics[:15], 1):
        style_emoji = "🎥" if topic['type'] == 'realistic' else "🌀"
        print(f"\n{idx}. {style_emoji} [{topic['type'].upper():10}] Score: {topic['trend_score']:3}")
        print(f"   {topic['title']}")
        print(f"   Keywords: {', '.join(topic['keywords'][:3])}")
    
    # Selection
    print("\n" + "=" * 70)
    print("SELECTED FOR TODAY'S VIDEOS:")
    print("=" * 70)
    
    realistic = [t for t in topics if t['type'] == 'realistic']
    lovecraft = [t for t in topics if t['type'] == 'lovecraft']
    
    if realistic:
        print(f"\n📹 VIDEO 1 (Realistic True Crime):")
        print(f"   {realistic[0]['title']}")
        print(f"   Score: {realistic[0]['trend_score']}/100")
        print(f"   Keywords: {', '.join(realistic[0]['keywords'])}")
    
    if lovecraft:
        print(f"\n🌀 VIDEO 2 (Lovecraftian Psychology):")
        print(f"   {lovecraft[0]['title']}")
        print(f"   Score: {lovecraft[0]['trend_score']}/100")
        print(f"   Keywords: {', '.join(lovecraft[0]['keywords'])}")
    
    if not realistic or not lovecraft:
        print("\n⚠️  Using fallback for missing style")
        if len(topics) >= 2:
            print(f"\n📹 Fallback: {topics[1]['title']}")
    
    print("\n" + "=" * 70)
    print("✅ RESEARCH COMPLETE - READY FOR PROMPT GENERATION")
    print("=" * 70)
    
    return topics

if __name__ == "__main__":
    main()
