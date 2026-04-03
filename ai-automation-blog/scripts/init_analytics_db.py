#!/usr/bin/env python3
"""
Initialize analytics.db for AI Automation Builder blog
Creates schema for tracking post performance and prompt evolution
"""

import sqlite3
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
DATA_DIR = WORKSPACE / "data"
DB_PATH = DATA_DIR / "analytics.db"

def init_database():
    """Create analytics database with schema"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Posts table - tracks individual post metrics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            published_date TEXT NOT NULL,
            word_count INTEGER,
            readability_score REAL,
            seo_score REAL,
            quality_score REAL,
            topic_cluster TEXT,
            prompt_version TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(slug)
        )
    """)
    
    # Prompt versions table - tracks prompt iterations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompt_versions (
            version TEXT PRIMARY KEY,
            prompt_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            avg_quality REAL,
            posts_count INTEGER DEFAULT 0
        )
    """)
    
    # Weekly reports table - aggregated analytics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_reports (
            week_start TEXT PRIMARY KEY,
            avg_quality REAL,
            top_topics TEXT,
            best_post_id INTEGER,
            prompt_winner TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(best_post_id) REFERENCES posts(id)
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_date ON posts(published_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_prompt ON posts(prompt_version)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_quality ON posts(quality_score)")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Analytics database created: {DB_PATH}")
    print(f"📊 Schema ready for tracking {3} tables")

if __name__ == "__main__":
    init_database()
