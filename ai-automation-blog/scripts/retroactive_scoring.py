#!/usr/bin/env python3
"""
Retroactive Analytics Scoring
Scans all existing blog posts in blog/md/ and populates analytics.db
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import re

WORKSPACE = Path(__file__).parent.parent
MD_DIR = WORKSPACE / "blog" / "md"
ANALYTICS_DB = WORKSPACE / "data" / "analytics.db"

def extract_date_from_slug(filename: str) -> str:
    """Extract date from filename like 2026-03-29-title.md"""
    match = re.match(r'^(\d{4}-\d{2}-\d{2})-', filename)
    if match:
        return match.group(1)
    return datetime.now().strftime('%Y-%m-%d')

def calculate_word_count(filepath: Path) -> int:
    """Count words in markdown file (excluding frontmatter)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove frontmatter
        content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
        
        # Count words
        words = content.split()
        return len(words)
    except Exception as e:
        print(f"⚠️  Error reading {filepath.name}: {e}")
        return 0

def scan_and_import():
    """Scan all .md files and import to analytics.db"""
    
    if not MD_DIR.exists():
        print(f"❌ Directory not found: {MD_DIR}")
        return
    
    md_files = list(MD_DIR.glob("*.md"))
    
    if not md_files:
        print(f"❌ No .md files found in {MD_DIR}")
        return
    
    print(f"📂 Found {len(md_files)} markdown files")
    
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for md_file in sorted(md_files):
        slug = md_file.stem  # filename without .md
        published_date = extract_date_from_slug(md_file.name)
        word_count = calculate_word_count(md_file)
        
        try:
            cursor.execute("""
                INSERT INTO posts (slug, published_date, word_count, prompt_version)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(slug) DO NOTHING
            """, (slug, published_date, word_count, "baseline"))
            
            if cursor.rowcount > 0:
                imported += 1
                print(f"✅ {slug[:60]} ({word_count} words)")
            else:
                skipped += 1
                print(f"⏭️  {slug[:60]} (already exists)")
                
        except Exception as e:
            print(f"❌ Failed to import {slug}: {e}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Retroactive Import Complete:")
    print(f"   ✅ Imported: {imported}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   📁 Total files: {len(md_files)}")
    
    # Verify
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM posts")
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n🗄️  Total rows in analytics.db: {total}")

if __name__ == "__main__":
    print("🔄 Starting retroactive analytics import...\n")
    scan_and_import()
