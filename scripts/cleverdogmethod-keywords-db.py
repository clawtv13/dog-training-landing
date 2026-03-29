#!/usr/bin/env python3
"""
CleverDogMethod Keywords Database
High-value, high-intent keywords for content generation
"""

KEYWORDS_DB = [
    # TIER 1: HIGH VOLUME (>10K searches/month)
    {"keyword": "dog training for aggression", "volume": 12100, "priority": 5, "type": "problem"},
    {"keyword": "clicker training for dogs", "volume": 9900, "priority": 4, "type": "method"},
    {"keyword": "german shepherd training", "volume": 5400, "priority": 4, "type": "breed"},
    {"keyword": "dog leash training", "volume": 5400, "priority": 4, "type": "basic"},
    
    # TIER 2: MEDIUM VOLUME (2K-5K)
    {"keyword": "dog training for separation anxiety", "volume": 3600, "priority": 5, "type": "problem"},
    {"keyword": "e-collar training", "volume": 3600, "priority": 3, "type": "equipment"},
    {"keyword": "pitbull training", "volume": 2900, "priority": 4, "type": "breed"},
    {"keyword": "off-leash dog training", "volume": 2400, "priority": 4, "type": "advanced"},
    {"keyword": "emotional support dog training", "volume": 2400, "priority": 3, "type": "specialized"},
    
    # TIER 3: LONG-TAIL HIGH-INTENT (1K-2K)
    {"keyword": "puppy socialization", "volume": 1900, "priority": 5, "type": "puppy"},
    {"keyword": "positive reinforcement dog training", "volume": 1900, "priority": 4, "type": "method"},
    {"keyword": "online dog training", "volume": 1900, "priority": 3, "type": "format"},
    {"keyword": "dog training for anxiety", "volume": 1600, "priority": 5, "type": "problem"},
    {"keyword": "belgian malinois training", "volume": 1600, "priority": 3, "type": "breed"},
    {"keyword": "puppy biting training", "volume": 1300, "priority": 4, "type": "puppy"},
    {"keyword": "rottweiler training", "volume": 1000, "priority": 3, "type": "breed"},
    {"keyword": "dog training for barking", "volume": 1000, "priority": 4, "type": "problem"},
    
    # TIER 4: NICHE SPECIFIC (500-1K)
    {"keyword": "dog socialization training", "volume": 720, "priority": 4, "type": "behavior"},
    {"keyword": "beagle training", "volume": 720, "priority": 3, "type": "breed"},
    {"keyword": "rescue dog training", "volume": 720, "priority": 4, "type": "specialized"},
    {"keyword": "great dane training", "volume": 590, "priority": 2, "type": "breed"},
    {"keyword": "dog trick training", "volume": 590, "priority": 3, "type": "advanced"},
    
    # ADDITIONAL HIGH-POTENTIAL
    {"keyword": "dog training collars", "volume": 33100, "priority": 3, "type": "equipment"},
    {"keyword": "crate training for puppies", "volume": 27100, "priority": 4, "type": "puppy"},
    {"keyword": "protection dog training", "volume": 4400, "priority": 3, "type": "specialized"},
    {"keyword": "therapy dog training", "volume": 8100, "priority": 3, "type": "specialized"},
    {"keyword": "dog agility training", "volume": 6600, "priority": 3, "type": "advanced"},
    {"keyword": "reactive dog training", "volume": 5400, "priority": 5, "type": "problem"},
    {"keyword": "fearful dog training", "volume": 320, "priority": 4, "type": "problem"},
    {"keyword": "dog confidence training", "volume": 140, "priority": 3, "type": "behavior"},
]

def get_keywords_by_priority(min_priority=3):
    """Get keywords filtered by priority"""
    return [k for k in KEYWORDS_DB if k['priority'] >= min_priority]

def get_keywords_by_type(keyword_type):
    """Get keywords by type (problem, breed, method, etc.)"""
    return [k for k in KEYWORDS_DB if k['type'] == keyword_type]

def get_high_volume_keywords(min_volume=2000):
    """Get keywords above certain search volume"""
    return [k for k in KEYWORDS_DB if k['volume'] >= min_volume]

def format_as_post_topic(keyword_data):
    """Convert keyword to post-friendly title"""
    keyword = keyword_data['keyword']
    kw_type = keyword_data['type']
    
    # Generate compelling title based on type
    if kw_type == "problem":
        return f"How to Stop {keyword.replace('dog training for ', '').title()}"
    elif kw_type == "breed":
        breed = keyword.replace(' training', '')
        return f"{breed.title()} Training: Complete Guide"
    elif kw_type == "method":
        method = keyword.replace(' for dogs', '')
        return f"{method.title()}: Beginner's Guide"
    elif kw_type == "puppy":
        return f"{keyword.title()}: 7-Day Plan"
    elif kw_type == "advanced":
        return f"{keyword.title()}: Step-by-Step Guide"
    elif kw_type == "equipment":
        return f"Best {keyword.title()} (2024 Review)"
    else:
        return keyword.title().replace(' Training', '') + " Training Guide"

if __name__ == "__main__":
    # Test
    print("📊 CleverDogMethod Keywords Database")
    print(f"Total keywords: {len(KEYWORDS_DB)}")
    print(f"\nTop 10 by volume:")
    
    sorted_kw = sorted(KEYWORDS_DB, key=lambda x: x['volume'], reverse=True)
    for i, kw in enumerate(sorted_kw[:10], 1):
        title = format_as_post_topic(kw)
        print(f"{i}. {title} ({kw['volume']:,} searches/mo)")
