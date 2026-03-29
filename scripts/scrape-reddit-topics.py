#!/usr/bin/env python3
"""
Reddit Topics Scraper using Scrapling
Fetches trending posts from r/TrueCrime and r/UnresolvedMysteries
"""

from scrapling import Fetcher
import json
from datetime import datetime

def scrape_reddit_topics():
    """Scrape trending true crime topics from Reddit"""
    
    topics = []
    
    subreddits = [
        ("https://www.reddit.com/r/TrueCrime/hot.json?limit=10", "realistic"),
        ("https://www.reddit.com/r/UnresolvedMysteries/hot.json?limit=10", "realistic"),
    ]
    
    fetcher = Fetcher()
    
    for url, topic_type in subreddits:
        try:
            response = fetcher.get(url)
            data = json.loads(response.text)
            
            posts = data.get('data', {}).get('children', [])
            
            for post in posts[:5]:
                post_data = post.get('data', {})
                title = post_data.get('title', '')
                score = post_data.get('score', 0)
                
                # Filter quality posts
                if score > 100 and len(title) > 20:
                    topics.append({
                        'title': title[:120],
                        'type': topic_type,
                        'score': score,
                        'keywords': extract_keywords(title),
                        'source': 'reddit'
                    })
        
        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
    
    return topics

def extract_keywords(title):
    """Extract relevant keywords from title"""
    keywords = []
    common_words = ['murder', 'killer', 'case', 'mystery', 'crime', 'death', 
                    'police', 'investigation', 'suspect', 'victim', 'serial']
    
    title_lower = title.lower()
    for word in common_words:
        if word in title_lower:
            keywords.append(word)
    
    return keywords[:3] if keywords else ['true crime']

if __name__ == "__main__":
    print("🔍 Scraping Reddit for trending true crime topics...")
    topics = scrape_reddit_topics()
    
    print(f"\n✅ Found {len(topics)} topics:\n")
    for i, topic in enumerate(topics[:10], 1):
        print(f"{i}. [{topic['score']}] {topic['title']}")
    
    # Save to file
    output_file = "/root/.openclaw/workspace/content/mind-crimes/reddit-topics.json"
    with open(output_file, 'w') as f:
        json.dump({
            'scraped_at': datetime.now().isoformat(),
            'topics': topics
        }, f, indent=2)
    
    print(f"\n💾 Saved to: {output_file}")
