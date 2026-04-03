#!/usr/bin/env python3
"""
Demo: Analytics flow simulation
Shows what happens when blog-auto-post-v2.py publishes a new post
"""

import sqlite3
from pathlib import Path
from datetime import datetime

ANALYTICS_DB = Path(__file__).parent.parent / "data" / "analytics.db"

def simulate_new_post():
    """Simulate publishing a new post with v1 prompt"""
    
    print("🔄 Simulating new post publication...\n")
    
    # This is what blog-auto-post-v2.py will call
    post_data = {
        'slug': '2026-04-03-demo-analytics-integration-test',
        'published_date': '2026-04-03',
        'word_count': 1500,
        'prompt_version': 'v1'  # New posts use v1
    }
    
    print(f"📝 Post: {post_data['slug']}")
    print(f"📅 Date: {post_data['published_date']}")
    print(f"📊 Words: {post_data['word_count']}")
    print(f"🏷️  Version: {post_data['prompt_version']}\n")
    
    # Save to analytics (this is the function we added)
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO posts (slug, published_date, word_count, prompt_version)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(slug) DO NOTHING
    """, (
        post_data['slug'],
        post_data['published_date'],
        post_data['word_count'],
        post_data['prompt_version']
    ))
    
    conn.commit()
    
    # Show database state
    cursor.execute("""
        SELECT prompt_version, COUNT(*) as count
        FROM posts
        GROUP BY prompt_version
    """)
    
    results = cursor.fetchall()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 Analytics Database State:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for version, count in results:
        print(f"   {version:10} → {count:3} posts")
    
    # Get total
    cursor.execute("SELECT COUNT(*) FROM posts")
    total = cursor.fetchone()[0]
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total: {total} posts tracked")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Clean up demo data
    cursor.execute("DELETE FROM posts WHERE slug = ?", (post_data['slug'],))
    conn.commit()
    conn.close()
    
    print("✅ Analytics integration ready!")
    print("   Next real post will be tracked automatically.\n")

if __name__ == "__main__":
    simulate_new_post()
