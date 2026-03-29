#!/usr/bin/env python3
"""
Smart Deduplication for Newsletter Content

Detects duplicate stories from multiple sources and keeps the best version.
"""

from difflib import SequenceMatcher
import re

def normalize_title(title):
    """
    Normalize title for better matching
    """
    # Lowercase
    title = title.lower()
    
    # Remove common prefixes
    prefixes = ['show hn:', 'ask hn:', 'launch:', 'new:', 'breaking:']
    for prefix in prefixes:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
    
    # Remove extra whitespace
    title = ' '.join(title.split())
    
    # Remove special characters (keep alphanumeric and spaces)
    title = re.sub(r'[^a-z0-9\s]', '', title)
    
    return title

def calculate_similarity(title1, title2):
    """
    Calculate similarity between two titles (0.0 to 1.0)
    Uses key term matching + sequence similarity
    """
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)
    
    # Sequence similarity
    seq_sim = SequenceMatcher(None, norm1, norm2).ratio()
    
    # Key term overlap (important words in both titles)
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    
    # Remove stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                  'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are'}
    
    words1 = words1 - stop_words
    words2 = words2 - stop_words
    
    if not words1 or not words2:
        return seq_sim
    
    # Jaccard similarity for key terms
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    key_term_sim = intersection / union if union > 0 else 0
    
    # Weighted average (60% key terms, 40% sequence)
    return (key_term_sim * 0.6) + (seq_sim * 0.4)

def are_duplicates(item1, item2, threshold=0.50):
    """
    Check if two items are duplicates
    
    Criteria:
    - Title similarity > threshold (default 55%)
    - OR same URL
    """
    # Exact URL match
    if item1.get('url') == item2.get('url'):
        return True
    
    # Title similarity
    similarity = calculate_similarity(item1['title'], item2['title'])
    
    return similarity >= threshold

def deduplicate_items(items, similarity_threshold=0.50):
    """
    Group duplicate items and keep the best version from each group
    
    Returns: List of deduplicated items with merged sources
    
    Lower threshold (55%) catches more duplicates
    """
    
    print(f"🔍 Deduplicating {len(items)} items (threshold: {similarity_threshold:.0%})...")
    
    # Group similar items
    groups = []
    
    for item in items:
        matched = False
        
        # Check if item matches any existing group
        # Compare against ALL items in group, not just first
        for group in groups:
            for group_item in group:
                if are_duplicates(item, group_item, similarity_threshold):
                    group.append(item)
                    matched = True
                    break
            if matched:
                break
        
        # Create new group if no match
        if not matched:
            groups.append([item])
    
    # Select best item from each group
    deduplicated = []
    
    for group in groups:
        if len(group) == 1:
            # No duplicates, keep as-is
            deduplicated.append(group[0])
        else:
            # Multiple versions - select best
            best = select_best_item(group)
            
            # Merge sources
            best['sources'] = [item['source'] for item in group]
            best['duplicate_count'] = len(group)
            
            deduplicated.append(best)
    
    duplicates_removed = len(items) - len(deduplicated)
    
    print(f"✅ Removed {duplicates_removed} duplicates")
    print(f"   {len(deduplicated)} unique items remaining\n")
    
    return deduplicated

def select_best_item(group):
    """
    Select the best version from a group of duplicates
    
    Priority:
    1. Highest score
    2. Most recent
    3. Best source (HN > GitHub > Reddit > RSS)
    """
    
    # Score by source quality
    source_priority = {
        'Hacker News': 10,
        'GitHub Trending': 9,
        'Product Hunt': 8,
        'Reddit': 7,
        'RSS': 5
    }
    
    for item in group:
        # Add source priority bonus
        source_bonus = 0
        for source_type, priority in source_priority.items():
            if source_type in item.get('source', ''):
                source_bonus = priority
                break
        
        item['selection_score'] = item.get('total_score', 0) + source_bonus
    
    # Select highest scoring
    best = max(group, key=lambda x: x.get('selection_score', 0))
    
    # Remove temporary selection score
    if 'selection_score' in best:
        del best['selection_score']
    
    return best

def merge_duplicate_summaries(group):
    """
    Merge summaries from duplicate items for richer context
    """
    summaries = []
    
    for item in group:
        summary = item.get('summary', '').strip()
        if summary and summary not in summaries:
            summaries.append(summary)
    
    # Combine unique summaries
    merged = ' | '.join(summaries[:3])  # Max 3 summaries
    
    return merged[:500]  # Truncate to 500 chars

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Test cases
    test_items = [
        {
            'title': 'OpenAI launches GPT-5',
            'url': 'https://techcrunch.com/gpt5',
            'source': 'TechCrunch',
            'total_score': 35,
            'summary': 'OpenAI announced GPT-5 today'
        },
        {
            'title': 'OpenAI Launches GPT-5 with New Features',  # Very similar to above
            'url': 'https://hackernews.com/gpt5',
            'source': 'Hacker News',
            'total_score': 38,
            'summary': 'Major model upgrade from OpenAI'
        },
        {
            'title': 'OpenAI Announces GPT-5 Launch',  # Also very similar
            'url': 'https://reddit.com/gpt5',
            'source': 'Reddit',
            'total_score': 32,
            'summary': 'Discussion about new GPT-5'
        },
        {
            'title': 'Google releases Gemini 2.0',  # Different story
            'url': 'https://google.com/gemini2',
            'source': 'Google Blog',
            'total_score': 40,
            'summary': 'New Gemini model'
        }
    ]
    
    print("Testing deduplication...\n")
    print(f"Input: {len(test_items)} items")
    print(f"  - 3 about GPT-5 launch (should merge)")
    print(f"  - 1 about Gemini (unique)\n")
    
    result = deduplicate_items(test_items)
    
    print(f"Output: {len(result)} unique items\n")
    
    for item in result:
        print(f"✓ {item['title']}")
        print(f"  Source: {item['source']}")
        print(f"  Score: {item['total_score']}")
        if 'sources' in item:
            print(f"  Merged from: {', '.join(item['sources'])}")
        print()
    
    assert len(result) == 2, f"Should have 2 unique items but got {len(result)}"
    assert result[0]['total_score'] == 38, "Should keep highest-scored GPT-5 version (HN)"
    
    print("✅ All tests passed!")
