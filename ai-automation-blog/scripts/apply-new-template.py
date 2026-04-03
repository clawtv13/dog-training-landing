#!/usr/bin/env python3
"""
Apply New Template to Existing Posts

Regenerates all posts with updated templates/post.html
"""

import re
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.parent
TEMPLATE_FILE = WORKSPACE / "templates" / "post.html"
POSTS_DIR = WORKSPACE / "blog" / "posts"
INDEX_FILE = POSTS_DIR / "index.json"

def extract_content_from_post(html):
    """Extract key content from existing post"""
    
    # Extract title
    title_match = re.search(r'<title>([^|]+)', html)
    title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Extract article content (between <article> tags if exists)
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if article_match:
        content = article_match.group(1)
    else:
        # Fallback: content between main tags
        content_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        content = content_match.group(1) if content_match else html
    
    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    description = desc_match.group(1) if desc_match else ""
    
    # Extract date
    date_match = re.search(r'(\w+ \d+, \d{4})', html)
    date = date_match.group(1) if date_match else datetime.now().strftime("%B %d, %Y")
    
    # Extract read time
    read_match = re.search(r'(\d+) min read', html)
    read_time = read_match.group(1) if read_match else "5"
    
    return {
        'title': title,
        'content': content,
        'description': description,
        'date': date,
        'read_time': read_time
    }

def apply_template(post_data, template):
    """Apply template with extracted data"""
    
    html = template
    html = html.replace('{{TITLE}}', post_data['title'])
    html = html.replace('{{DATE}}', post_data['date'])
    html = html.replace('{{READ_TIME}}', post_data['read_time'])
    html = html.replace('{{DESCRIPTION}}', post_data['description'])
    html = html.replace('{{CONTENT}}', post_data['content'])
    html = html.replace('{{AUTHOR_NAME}}', 'Alex Chen')
    html = html.replace('{{AUTHOR_TITLE}}', 'AI Engineer & Automation Specialist')
    html = html.replace('{{AUTHOR_AVATAR}}', '👤')
    html = html.replace('{{HN_SCORE}}', '')  # Can be extracted if needed
    
    return html

def main():
    print("=" * 60)
    print("🎨 APPLYING NEW TEMPLATE TO ALL POSTS")
    print("=" * 60)
    print()
    
    # Read template
    if not TEMPLATE_FILE.exists():
        print(f"❌ Template not found: {TEMPLATE_FILE}")
        return
    
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()
    
    # Get all posts
    posts = list(POSTS_DIR.glob("2026-*.html"))
    
    if not posts:
        print("❌ No posts found")
        return
    
    print(f"Found {len(posts)} posts to regenerate\n")
    
    for post_file in posts:
        print(f"Processing: {post_file.name}")
        
        # Read existing post
        with open(post_file, 'r') as f:
            old_html = f.read()
        
        # Extract content
        post_data = extract_content_from_post(old_html)
        
        # Apply new template
        new_html = apply_template(post_data, template)
        
        # Write back
        with open(post_file, 'w') as f:
            f.write(new_html)
        
        print(f"  ✅ Regenerated: {post_data['title'][:50]}...")
    
    print()
    print("=" * 60)
    print(f"✅ Regenerated {len(posts)} posts with new template")
    print("=" * 60)

if __name__ == "__main__":
    main()
