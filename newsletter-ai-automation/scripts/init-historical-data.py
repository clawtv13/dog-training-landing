#!/usr/bin/env python3
"""
Initialize database with historical data (8 editions)
Simulates 2 months of newsletter operation
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"

def init_database_with_history():
    """
    Create database and populate with 8 editions of historical data
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS content_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            source TEXT,
            type TEXT,
            total_score INTEGER,
            relevance_score INTEGER,
            novelty_score INTEGER,
            usefulness_score INTEGER,
            impact_score INTEGER,
            summary TEXT,
            newsletter_section TEXT,
            published_date TEXT,
            featured_in_edition INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS editions (
            edition_number INTEGER PRIMARY KEY,
            publish_date TEXT,
            subject_line TEXT,
            open_rate REAL,
            click_rate REAL,
            subscriber_count INTEGER,
            status TEXT DEFAULT 'published'
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriber_stats (
            date TEXT PRIMARY KEY,
            total_subscribers INTEGER,
            new_subscribers INTEGER,
            unsubscribes INTEGER,
            source TEXT
        )
    ''')
    
    # Historical editions data
    editions = [
        (1, "2026-01-28", "Launch: AI tools for solopreneurs who ship", 0.524, 0.081, 143),
        (2, "2026-02-04", "The $29/mo stack replacing my VA", 0.472, 0.078, 287),
        (3, "2026-02-11", "3 workflows that saved me 10 hrs this week", 0.443, 0.069, 512),
        (4, "2026-02-18", "AI agents are eating customer support", 0.417, 0.064, 789),
        (5, "2026-02-25", "Building a micro-SaaS with $0 code", 0.398, 0.061, 1124),
        (6, "2026-03-04", "The AI automation stack everyone's copying", 0.389, 0.063, 1456),
        (7, "2026-03-11", "I automated my entire sales funnel (here's how)", 0.372, 0.060, 1683),
        (8, "2026-03-18", "New AI coding agents are insane (tested 5)", 0.384, 0.062, 1847),
    ]
    
    for edition in editions:
        c.execute('''
            INSERT OR IGNORE INTO editions 
            (edition_number, publish_date, subject_line, open_rate, click_rate, subscriber_count, status)
            VALUES (?, ?, ?, ?, ?, ?, 'published')
        ''', edition)
    
    print(f"✅ Created {len(editions)} historical editions")
    
    # Sample content items (featured in past editions)
    sample_content = [
        # Edition 1 content
        ("https://n8n.io/blog/automate-customer-support", "Automate Customer Support with n8n and GPT", 
         "RSS: n8n Blog", "article", 38, 9, 10, 10, 9, "Tutorial on building AI customer support workflow", "Tool Review", "2026-01-25", 1),
        
        # Edition 2 content
        ("https://make.com/en/integrations/claude", "Make.com Claude Integration Guide",
         "Product Hunt", "tool", 37, 9, 9, 10, 9, "Connect Claude API to any app with Make.com", "Tutorial", "2026-02-01", 2),
        
        # Edition 3 content
        ("https://github.com/openai/whisper", "Whisper: Speech Recognition by OpenAI",
         "GitHub", "repo", 39, 10, 9, 10, 10, "State-of-the-art speech recognition", "Tool Review", "2026-02-08", 3),
        
        # Edition 4 content
        ("https://intercom.com/blog/ai-customer-support", "AI is Transforming Customer Support",
         "RSS: Intercom Blog", "article", 36, 9, 8, 10, 9, "Industry analysis of AI support agents", "News", "2026-02-15", 4),
        
        # Edition 5 content
        ("https://bubble.io/plugin/openai-gpt-4", "Bubble OpenAI Plugin",
         "Product Hunt", "tool", 38, 10, 9, 10, 9, "Build AI-powered apps in Bubble no-code", "Tool Review", "2026-02-22", 5),
        
        # Edition 6 content
        ("https://supabase.com/blog/ai-sql-queries", "AI SQL Query Generation in Supabase",
         "RSS: Supabase Blog", "article", 37, 9, 9, 9, 10, "Natural language to SQL with AI", "Tool Review", "2026-03-01", 6),
        
        # Edition 7 content
        ("https://clay.com/automations", "Clay: AI-Powered Sales Automation",
         "Product Hunt", "tool", 39, 10, 10, 9, 10, "Automate lead qualification and outreach", "Tool Review", "2026-03-08", 7),
        
        # Edition 8 content
        ("https://cursor.sh/blog/cursor-vs-copilot", "Cursor vs GitHub Copilot: Deep Comparison",
         "Reddit: r/programming", "article", 40, 10, 10, 10, 10, "Comprehensive AI coding assistant comparison", "Tool Review", "2026-03-15", 8),
    ]
    
    for item in sample_content:
        c.execute('''
            INSERT OR IGNORE INTO content_items 
            (url, title, source, type, total_score, relevance_score, novelty_score, 
             usefulness_score, impact_score, summary, newsletter_section, published_date, featured_in_edition)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)
    
    print(f"✅ Added {len(sample_content)} sample content items")
    
    # Subscriber growth data (daily)
    start_date = datetime(2026, 1, 28)
    current_subs = 143
    
    for day in range(60):  # 60 days of history
        date = start_date + timedelta(days=day)
        
        # Growth varies by day (higher on publish days - Tuesday/Friday)
        is_publish_day = date.weekday() in [1, 4]  # Tuesday, Friday
        new_subs = 25 if is_publish_day else 8
        unsubs = 1 if is_publish_day else 0
        
        current_subs += new_subs - unsubs
        
        c.execute('''
            INSERT OR IGNORE INTO subscriber_stats
            (date, total_subscribers, new_subscribers, unsubscribes, source)
            VALUES (?, ?, ?, ?, 'organic')
        ''', (date.strftime('%Y-%m-%d'), current_subs, new_subs, unsubs))
    
    print(f"✅ Added 60 days of subscriber growth data")
    
    conn.commit()
    conn.close()
    
    print("\n✅ DATABASE INITIALIZED WITH HISTORICAL DATA")
    print(f"   Location: {DB_PATH}")
    print(f"   Editions: 8 published")
    print(f"   Content items: {len(sample_content)}")
    print(f"   Current subscribers: 1,847")

if __name__ == "__main__":
    init_database_with_history()
