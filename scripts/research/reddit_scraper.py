#!/usr/bin/env python3
"""
Reddit scraper for dog training trending topics
No API key needed - scrapes via requests
"""

import requests
import json
from datetime import datetime

SUBREDDITS = ["Dogtraining", "dogs", "puppy101"]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CleverDog/1.0)"}

def scrape_subreddit(subreddit):
    """Get hot posts from subreddit"""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            p = post['data']
            
            # Extract problem keywords from title
            title_lower = p['title'].lower()
            keywords = []
            
            # Common dog behavior keywords
            problem_keywords = [
                "barking", "biting", "jumping", "pulling", "chewing",
                "anxiety", "aggressive", "reactive", "fearful", "scared",
                "potty", "pee", "poop", "house training", "crate",
                "leash", "walk", "command", "sit", "stay", "come",
                "puppy", "rescue", "separation", "destructive"
            ]
            
            for keyword in problem_keywords:
                if keyword in title_lower:
                    keywords.append(keyword)
            
            if keywords:  # Only include posts with relevant keywords
                posts.append({
                    "title": p['title'],
                    "score": p['score'],
                    "num_comments": p['num_comments'],
                    "keywords": keywords,
                    "url": f"https://reddit.com{p['permalink']}"
                })
        
        return posts
        
    except Exception as e:
        print(f"Error scraping r/{subreddit}: {e}")
        return []

def extract_topics(posts):
    """Convert posts to topic ideas"""
    
    # Group by keyword
    keyword_counts = {}
    for post in posts:
        for keyword in post['keywords']:
            if keyword not in keyword_counts:
                keyword_counts[keyword] = {
                    "count": 0,
                    "total_score": 0,
                    "examples": []
                }
            keyword_counts[keyword]["count"] += 1
            keyword_counts[keyword]["total_score"] += post['score']
            if len(keyword_counts[keyword]["examples"]) < 3:
                keyword_counts[keyword]["examples"].append(post['title'])
    
    # Rank topics
    topics = []
    for keyword, data in keyword_counts.items():
        topics.append({
            "topic": keyword,
            "mentions": data["count"],
            "popularity": data["total_score"],
            "examples": data["examples"]
        })
    
    # Sort by popularity
    topics.sort(key=lambda x: x["popularity"], reverse=True)
    
    return topics[:15]  # Top 15

def main():
    print("\n🔍 SCRAPING REDDIT FOR DOG TRAINING TOPICS")
    print("="*60)
    
    all_posts = []
    
    for subreddit in SUBREDDITS:
        print(f"\n📡 Fetching r/{subreddit}...")
        posts = scrape_subreddit(subreddit)
        all_posts.extend(posts)
        print(f"   Found {len(posts)} relevant posts")
    
    print(f"\n📊 EXTRACTING TRENDING TOPICS")
    print("="*60)
    
    topics = extract_topics(all_posts)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic['topic'].upper()}")
        print(f"   Mentions: {topic['mentions']}")
        print(f"   Popularity: {topic['popularity']}")
        print(f"   Example: \"{topic['examples'][0][:60]}...\"")
    
    # Save output
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_posts": len(all_posts),
        "topics": topics
    }
    
    output_file = "/root/.openclaw/workspace/.state/reddit-topics.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Saved to: {output_file}")
    
    return topics

if __name__ == '__main__':
    main()
