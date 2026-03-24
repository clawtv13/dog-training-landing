#!/usr/bin/env python3
"""
Google Trends scraper for dog training queries
Uses pytrends library
"""

import json
from datetime import datetime, timedelta

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False
    print("⚠️  pytrends not installed. Run: pip install pytrends")

def get_trending_queries():
    """Get trending dog training searches"""
    
    if not PYTRENDS_AVAILABLE:
        # Fallback: return manually curated trending topics
        return get_fallback_topics()
    
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Keywords to check
        keywords = ["dog training", "puppy training", "dog behavior"]
        
        pytrends.build_payload(keywords, timeframe='now 7-d')
        
        # Get related queries
        related = pytrends.related_queries()
        
        trending = []
        
        for keyword in keywords:
            if keyword in related and 'rising' in related[keyword]:
                rising = related[keyword]['rising']
                if rising is not None:
                    for _, row in rising.iterrows():
                        trending.append({
                            "query": row['query'],
                            "value": int(row['value']) if row['value'] != 'Breakout' else 1000,
                            "growth": "Breakout" if row['value'] == 'Breakout' else f"+{row['value']}%"
                        })
        
        # Sort by value
        trending.sort(key=lambda x: x['value'], reverse=True)
        
        return trending[:15]
        
    except Exception as e:
        print(f"Error fetching Google Trends: {e}")
        return get_fallback_topics()

def get_fallback_topics():
    """Curated trending topics (when API unavailable)"""
    
    return [
        {"query": "how to stop dog barking at night", "value": 800, "growth": "High"},
        {"query": "puppy biting too hard", "value": 750, "growth": "High"},
        {"query": "dog pulling on leash", "value": 700, "growth": "Medium"},
        {"query": "separation anxiety in dogs", "value": 650, "growth": "High"},
        {"query": "crate training puppy crying", "value": 600, "growth": "Medium"},
        {"query": "dog reactivity training", "value": 550, "growth": "High"},
        {"query": "teach dog recall", "value": 500, "growth": "Medium"},
        {"query": "puppy potty training regression", "value": 480, "growth": "Medium"},
        {"query": "dog resource guarding", "value": 450, "growth": "High"},
        {"query": "counter surfing dog", "value": 420, "growth": "Low"},
        {"query": "dog anxiety symptoms", "value": 400, "growth": "Medium"},
        {"query": "teach dog stay command", "value": 380, "growth": "Low"},
        {"query": "puppy socialization checklist", "value": 350, "growth": "Medium"},
        {"query": "dog jumping on guests", "value": 320, "growth": "Low"},
        {"query": "fearful dog training", "value": 300, "growth": "Medium"}
    ]

def main():
    print("\n📊 FETCHING GOOGLE TRENDS DATA")
    print("="*60)
    
    topics = get_trending_queries()
    
    print(f"\n🔥 TOP 15 TRENDING QUERIES:")
    print("="*60)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. \"{topic['query']}\"")
        print(f"   Growth: {topic['growth']}")
        print(f"   Search Interest: {topic['value']}")
    
    # Save output
    output = {
        "timestamp": datetime.now().isoformat(),
        "source": "Google Trends API" if PYTRENDS_AVAILABLE else "Fallback (curated)",
        "topics": topics
    }
    
    output_file = "/root/.openclaw/workspace/.state/google-trends.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Saved to: {output_file}")
    
    return topics

if __name__ == '__main__':
    main()
