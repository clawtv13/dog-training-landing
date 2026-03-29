#!/usr/bin/env python3
"""
Mind Crimes - Live Research Test
Tests real-time research from Reddit and Google Trends
"""

import requests
import json
from datetime import datetime
import re

def scrape_reddit_truecrime():
    """Scrape r/TrueCrime for trending posts"""
    print("\n🔍 Scraping r/TrueCrime...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MindCrimesBot/1.0)'}
    
    try:
        # Get top posts from r/TrueCrime
        url = "https://www.reddit.com/r/TrueCrime/hot.json?limit=10"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                posts.append({
                    'title': post_data['title'],
                    'score': post_data['score'],
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'comments': post_data['num_comments']
                })
            
            return posts
        else:
            print(f"❌ Reddit returned status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error scraping Reddit: {e}")
        return []

def scrape_reddit_unresolved():
    """Scrape r/UnresolvedMysteries for cases"""
    print("🔍 Scraping r/UnresolvedMysteries...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MindCrimesBot/1.0)'}
    
    try:
        url = "https://www.reddit.com/r/UnresolvedMysteries/hot.json?limit=10"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                # Filter for actual cases (not meta posts)
                if '[' in post_data['title']:
                    posts.append({
                        'title': post_data['title'],
                        'score': post_data['score'],
                        'url': f"https://reddit.com{post_data['permalink']}",
                        'comments': post_data['num_comments']
                    })
            
            return posts
        else:
            print(f"❌ Reddit returned status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error scraping Reddit: {e}")
        return []

def scrape_reddit_psychology():
    """Scrape r/psychology for trending concepts"""
    print("🔍 Scraping r/psychology...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MindCrimesBot/1.0)'}
    
    try:
        url = "https://www.reddit.com/r/psychology/hot.json?limit=10"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                posts.append({
                    'title': post_data['title'],
                    'score': post_data['score'],
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'comments': post_data['num_comments']
                })
            
            return posts
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error scraping Reddit: {e}")
        return []

def analyze_topics(all_posts):
    """Analyze posts and categorize by type"""
    
    topics = []
    
    for post in all_posts:
        title = post['title']
        score = post['score']
        
        # Determine if realistic or lovecraft style
        style = 'realistic'
        
        # Keywords indicating educational/psychological content
        psych_keywords = ['psychology', 'behavior', 'mind', 'mental', 'manipulation', 
                         'narcis', 'gaslighting', 'toxic', 'abuse', 'trauma']
        
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in psych_keywords):
            style = 'lovecraft'
        
        # Extract potential keywords
        keywords = []
        if 'murder' in title_lower or 'killed' in title_lower:
            keywords.append('murder')
        if 'missing' in title_lower or 'disappear' in title_lower:
            keywords.append('missing person')
        if 'scam' in title_lower or 'fraud' in title_lower:
            keywords.extend(['scam', 'fraud'])
        if 'cult' in title_lower:
            keywords.append('cult')
        if 'serial' in title_lower:
            keywords.append('serial killer')
        
        # Calculate trend score based on engagement
        trend_score = min(100, (score + post['comments']) / 50)
        
        topics.append({
            'title': title[:80],  # Truncate long titles
            'type': style,
            'trend_score': int(trend_score),
            'keywords': keywords if keywords else ['true crime', 'psychology'],
            'source': post['url']
        })
    
    # Sort by trend score
    topics.sort(key=lambda x: x['trend_score'], reverse=True)
    
    return topics

def main():
    """Main research execution"""
    
    print("=" * 60)
    print("MIND CRIMES - LIVE RESEARCH TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    
    all_posts = []
    
    # Collect from multiple subreddits
    truecrime_posts = scrape_reddit_truecrime()
    print(f"✅ Found {len(truecrime_posts)} posts in r/TrueCrime")
    all_posts.extend(truecrime_posts)
    
    unresolved_posts = scrape_reddit_unresolved()
    print(f"✅ Found {len(unresolved_posts)} posts in r/UnresolvedMysteries")
    all_posts.extend(unresolved_posts)
    
    psych_posts = scrape_reddit_psychology()
    print(f"✅ Found {len(psych_posts)} posts in r/psychology")
    all_posts.extend(psych_posts)
    
    if not all_posts:
        print("\n❌ No posts found. Using fallback topics.")
        return
    
    print(f"\n📊 Total posts collected: {len(all_posts)}")
    
    # Analyze and categorize
    print("\n🧠 Analyzing topics...")
    topics = analyze_topics(all_posts)
    
    # Display top 10
    print("\n" + "=" * 60)
    print("TOP 10 TRENDING TOPICS:")
    print("=" * 60)
    
    for idx, topic in enumerate(topics[:10], 1):
        style_emoji = "🎥" if topic['type'] == 'realistic' else "🌀"
        print(f"\n{idx}. {style_emoji} [{topic['type'].upper()}] Score: {topic['trend_score']}")
        print(f"   Title: {topic['title']}")
        print(f"   Keywords: {', '.join(topic['keywords'])}")
        print(f"   Source: {topic['source'][:60]}...")
    
    # Show what would be selected
    print("\n" + "=" * 60)
    print("SELECTED FOR TODAY'S VIDEOS:")
    print("=" * 60)
    
    realistic = [t for t in topics if t['type'] == 'realistic']
    lovecraft = [t for t in topics if t['type'] == 'lovecraft']
    
    if realistic and lovecraft:
        print(f"\n📹 VIDEO 1 (Realistic): {realistic[0]['title']}")
        print(f"   Score: {realistic[0]['trend_score']}/100")
        
        print(f"\n🌀 VIDEO 2 (Lovecraft): {lovecraft[0]['title']}")
        print(f"   Score: {lovecraft[0]['trend_score']}/100")
    else:
        print("\n⚠️  Not enough diversity in topics. Would use fallback mix.")
        if topics:
            print(f"\n📹 VIDEO 1: {topics[0]['title']}")
            print(f"📹 VIDEO 2: {topics[1]['title'] if len(topics) > 1 else 'Fallback topic'}")
    
    print("\n" + "=" * 60)
    print("✅ RESEARCH TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
