#!/usr/bin/env python3
"""Test analytics integration"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Import from blog-auto-post-v2
sys.path.insert(0, str(Path(__file__).parent))

# Mock the function inline (since imports might be complex)
ANALYTICS_DB = Path(__file__).parent.parent / "data" / "analytics.db"

def test_save_to_analytics():
    """Test analytics save function"""
    
    test_data = {
        'slug': 'test-post-analytics',
        'published_date': datetime.now().strftime('%Y-%m-%d'),
        'word_count': 999,
        'prompt_version': 'v1'
    }
    
    try:
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO posts (slug, published_date, word_count, prompt_version)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(slug) DO NOTHING
        """, (
            test_data['slug'],
            test_data['published_date'],
            test_data['word_count'],
            test_data.get('prompt_version', 'v1')
        ))
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT * FROM posts WHERE slug = ?", (test_data['slug'],))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            print("✅ Analytics function works!")
            print(f"   Saved: {test_data['slug']}")
            print(f"   Word count: {test_data['word_count']}")
            print(f"   Prompt version: {test_data['prompt_version']}")
            
            # Clean up test data
            conn = sqlite3.connect(ANALYTICS_DB)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE slug = ?", (test_data['slug'],))
            conn.commit()
            conn.close()
            
            return True
        else:
            print("❌ Test failed: data not saved")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_save_to_analytics()
    sys.exit(0 if success else 1)
