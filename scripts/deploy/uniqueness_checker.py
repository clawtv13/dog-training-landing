#!/usr/bin/env python3
"""
Check if new posts are unique vs existing blog content
Prevents duplicates and keyword cannibalization
"""

import os
import json
from pathlib import Path
from difflib import SequenceMatcher

BLOG_DIR = Path("/root/.openclaw/workspace/dog-training-landing/blog")
STATE_FILE = Path("/root/.openclaw/workspace/.state/cleverdogmethod-published.json")

def load_published_posts():
    """Load list of all published posts"""
    
    if not STATE_FILE.exists():
        return []
    
    with open(STATE_FILE) as f:
        return json.load(f)

def save_published_posts(posts):
    """Save updated published posts list"""
    
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

def title_similarity(title1, title2):
    """Calculate similarity between two titles (0-1)"""
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

def keyword_overlap(keywords1, keywords2):
    """Check if keyword sets overlap significantly"""
    set1 = set(k.strip().lower() for k in keywords1.split(','))
    set2 = set(k.strip().lower() for k in keywords2.split(','))
    
    overlap = set1 & set2
    total = set1 | set2
    
    return len(overlap) / len(total) if total else 0

def is_unique(new_post, published_posts):
    """Check if new post is unique enough"""
    
    for existing in published_posts:
        # Check title similarity
        title_sim = title_similarity(new_post['title'], existing['title'])
        if title_sim > 0.7:
            return False, f"Title too similar to: {existing['title']}"
        
        # Check keyword overlap
        keyword_sim = keyword_overlap(new_post['keywords'], existing['keywords'])
        if keyword_sim > 0.6:
            return False, f"Keyword cannibalization with: {existing['title']}"
        
        # Check slug collision
        if new_post['slug'] == existing['slug']:
            return False, f"Slug collision with: {existing['title']}"
    
    return True, "Unique"

def check_posts(new_posts):
    """Check all new posts for uniqueness"""
    
    print("\n🔍 CHECKING POST UNIQUENESS")
    print("="*60)
    
    published = load_published_posts()
    
    print(f"\n📚 {len(published)} posts already published")
    print(f"🆕 Checking {len(new_posts)} new posts\n")
    
    approved = []
    rejected = []
    
    for post in new_posts:
        unique, reason = is_unique(post, published)
        
        if unique:
            print(f"✅ \"{post['title'][:60]}...\"")
            print(f"   {reason}")
            approved.append(post)
        else:
            print(f"❌ \"{post['title'][:60]}...\"")
            print(f"   {reason}")
            rejected.append(post)
    
    print(f"\n📊 RESULTS: {len(approved)} approved, {len(rejected)} rejected")
    
    return approved, rejected

def main():
    # Test with dummy data
    published = load_published_posts()
    
    test_posts = [
        {
            "title": "Why Smart Dogs Get Separation Anxiety",
            "slug": "smart-dogs-separation-anxiety",
            "keywords": "separation anxiety, smart dogs, anxiety training"
        },
        {
            "title": "How to Stop Dog Barking at Night",
            "slug": "stop-dog-barking-night",
            "keywords": "barking, night barking, excessive barking"
        }
    ]
    
    approved, rejected = check_posts(test_posts)
    
    print(f"\n✅ {len(approved)} posts ready to publish")
    print(f"❌ {len(rejected)} posts need regeneration")

if __name__ == '__main__':
    main()
