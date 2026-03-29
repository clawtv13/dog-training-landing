#!/usr/bin/env python3
"""
Newsletter-Blog Sync
Ensures content coordination between newsletter and blog

Features:
- Marks blog-used items in newsletter DB
- Prevents duplicate content across both channels
- Cross-reference tracking
- Content repurposing suggestions
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_STATE_DIR = WORKSPACE / ".state"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"
NEWSLETTER_STATE = WORKSPACE.parent / "newsletter-ai-automation" / ".state"

PUBLISHED_POSTS_FILE = BLOG_STATE_DIR / "published-posts.json"
SYNC_STATE_FILE = BLOG_STATE_DIR / "newsletter-sync.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# SYNC LOGIC
# ============================================================================

def load_json(file_path: Path, default=None):
    """Load JSON with fallback"""
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            pass
    return default if default is not None else []

def save_json(file_path: Path, data):
    """Save JSON atomically"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp = file_path.with_suffix('.tmp')
    with open(temp, 'w') as f:
        json.dump(data, f, indent=2)
    temp.replace(file_path)

def mark_items_as_blog_used():
    """Mark items in newsletter DB as used by blog"""
    
    if not NEWSLETTER_DB.exists():
        logger.warning("Newsletter database not found")
        return
    
    published_posts = load_json(PUBLISHED_POSTS_FILE, [])
    
    if not published_posts:
        logger.info("No published posts to sync")
        return
    
    # Get source item IDs from published posts
    blog_item_ids = [p['source_item_id'] for p in published_posts if 'source_item_id' in p]
    
    if not blog_item_ids:
        logger.info("No source IDs to sync")
        return
    
    conn = sqlite3.connect(NEWSLETTER_DB)
    c = conn.cursor()
    
    # Check if blog_used column exists
    c.execute("PRAGMA table_info(content_items)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'blog_used' not in columns:
        logger.info("Adding blog_used column to newsletter DB")
        c.execute("ALTER TABLE content_items ADD COLUMN blog_used INTEGER DEFAULT 0")
    
    # Mark items as blog used
    marked_count = 0
    for item_id in blog_item_ids:
        c.execute("""
            UPDATE content_items 
            SET blog_used = 1 
            WHERE id = ? AND blog_used = 0
        """, (item_id,))
        
        if c.rowcount > 0:
            marked_count += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Marked {marked_count} items as blog-used in newsletter DB")
    
    # Update sync state
    sync_state = load_json(SYNC_STATE_FILE, {})
    sync_state['last_sync'] = datetime.now().isoformat()
    sync_state['items_synced'] = len(blog_item_ids)
    sync_state['new_items_marked'] = marked_count
    save_json(SYNC_STATE_FILE, sync_state)

def get_content_distribution():
    """Analyze content distribution across blog and newsletter"""
    
    if not NEWSLETTER_DB.exists():
        return None
    
    conn = sqlite3.connect(NEWSLETTER_DB)
    c = conn.cursor()
    
    # Check if blog_used column exists
    c.execute("PRAGMA table_info(content_items)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'blog_used' not in columns:
        return None
    
    # Get distribution stats
    c.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN featured_in_edition IS NOT NULL THEN 1 ELSE 0 END) as newsletter_used,
            SUM(CASE WHEN blog_used = 1 THEN 1 ELSE 0 END) as blog_used,
            SUM(CASE WHEN featured_in_edition IS NOT NULL AND blog_used = 1 THEN 1 ELSE 0 END) as both_used,
            SUM(CASE WHEN featured_in_edition IS NULL AND blog_used = 0 AND total_score >= 30 THEN 1 ELSE 0 END) as available
        FROM content_items
    """)
    
    row = c.fetchone()
    conn.close()
    
    stats = {
        'total_items': row[0],
        'newsletter_used': row[1],
        'blog_used': row[2],
        'both_used': row[3],
        'available': row[4],
        'newsletter_only': row[1] - row[3],
        'blog_only': row[2] - row[3]
    }
    
    return stats

def suggest_repurposing_opportunities():
    """Find items from newsletter that could be expanded for blog"""
    
    if not NEWSLETTER_DB.exists():
        return []
    
    conn = sqlite3.connect(NEWSLETTER_DB)
    c = conn.cursor()
    
    # Check if blog_used column exists
    c.execute("PRAGMA table_info(content_items)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'blog_used' not in columns:
        conn.close()
        return []
    
    # Get high-scoring newsletter items not yet on blog
    c.execute("""
        SELECT id, title, url, total_score, featured_in_edition
        FROM content_items
        WHERE featured_in_edition IS NOT NULL
        AND blog_used = 0
        AND total_score >= 35
        ORDER BY total_score DESC
        LIMIT 10
    """)
    
    opportunities = []
    for row in c.fetchall():
        opportunities.append({
            'id': row[0],
            'title': row[1],
            'url': row[2],
            'score': row[3],
            'featured_in': row[4],
            'suggestion': 'High-performing newsletter item - could make great blog post'
        })
    
    conn.close()
    return opportunities

def print_sync_report():
    """Print comprehensive sync report"""
    
    logger.info("=" * 60)
    logger.info("NEWSLETTER-BLOG SYNC REPORT")
    logger.info("=" * 60)
    
    # Sync state
    sync_state = load_json(SYNC_STATE_FILE, {})
    if sync_state:
        logger.info(f"\n📊 Sync Status:")
        logger.info(f"   Last sync: {sync_state.get('last_sync', 'Never')}")
        logger.info(f"   Items synced: {sync_state.get('items_synced', 0)}")
        logger.info(f"   New items marked: {sync_state.get('new_items_marked', 0)}")
    
    # Distribution
    stats = get_content_distribution()
    if stats:
        logger.info(f"\n📈 Content Distribution:")
        logger.info(f"   Total items: {stats['total_items']}")
        logger.info(f"   Newsletter only: {stats['newsletter_only']}")
        logger.info(f"   Blog only: {stats['blog_only']}")
        logger.info(f"   Both channels: {stats['both_used']}")
        logger.info(f"   Available: {stats['available']}")
    
    # Repurposing opportunities
    opportunities = suggest_repurposing_opportunities()
    if opportunities:
        logger.info(f"\n💡 Repurposing Opportunities ({len(opportunities)}):")
        for opp in opportunities[:5]:
            logger.info(f"   • {opp['title'][:60]} (score: {opp['score']})")
    
    logger.info("\n" + "=" * 60)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run sync process"""
    logger.info("🔄 Starting newsletter-blog sync...")
    
    # Mark blog-used items
    mark_items_as_blog_used()
    
    # Print report
    print_sync_report()
    
    logger.info("✅ Sync complete")

if __name__ == "__main__":
    main()
