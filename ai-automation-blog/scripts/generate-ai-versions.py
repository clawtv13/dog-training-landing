#!/usr/bin/env python3
"""
Generate AI-optimized text and markdown versions of blog posts
For Perplexity, ChatGPT, Claude, Gemini crawlers
"""

import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
import html2text

def strip_html_to_text(html_content):
    """Extract clean text from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script, style, nav, footer
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    
    # Find article content
    article = soup.find('article') or soup.find('main') or soup.body
    
    if not article:
        return None
    
    # Get text
    text = article.get_text(separator='\n', strip=True)
    
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def html_to_markdown(html_content):
    """Convert HTML to clean markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    
    # Find article
    article = soup.find('article') or soup.find('main') or soup.body
    
    if not article:
        return None
    
    # Convert to markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # No wrapping
    h.skip_internal_links = False
    
    markdown = h.handle(str(article))
    
    return markdown

def extract_metadata(html_content):
    """Extract title, date, author from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    metadata = {
        'title': '',
        'date': '',
        'author': 'Alex Chen',
        'description': '',
        'tags': []
    }
    
    # Title
    title_tag = soup.find('h1')
    if title_tag:
        metadata['title'] = title_tag.get_text(strip=True)
    
    # Meta description
    desc_meta = soup.find('meta', {'name': 'description'})
    if desc_meta:
        metadata['description'] = desc_meta.get('content', '')
    
    # Date from meta or filename
    date_meta = soup.find('meta', {'property': 'article:published_time'})
    if date_meta:
        metadata['date'] = date_meta.get('content', '')[:10]
    
    # Keywords
    kw_meta = soup.find('meta', {'name': 'keywords'})
    if kw_meta:
        metadata['tags'] = [t.strip() for t in kw_meta.get('content', '').split(',')]
    
    return metadata

def generate_txt_version(html_path, output_dir):
    """Generate plain text version for AI crawlers"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extract metadata
    meta = extract_metadata(html)
    
    # Extract clean text
    content = strip_html_to_text(html)
    
    if not content:
        return None
    
    # Build text version
    txt_content = f"""# {meta['title']}

Author: {meta['author']}
Published: {meta['date']}
URL: https://workless.build/posts/{Path(html_path).stem}.html

---

{meta['description']}

---

{content}

---

Topics: {', '.join(meta['tags']) if meta['tags'] else 'AI Automation'}

© 2026 Work Less, Build. All rights reserved.
"""
    
    # Save
    slug = Path(html_path).stem
    txt_path = output_dir / f"{slug}.txt"
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content.strip())
    
    print(f"  ✅ Generated: {txt_path.name}")
    return str(txt_path)

def generate_md_version(html_path, output_dir):
    """Generate markdown version for LLM training/indexing"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extract metadata
    meta = extract_metadata(html)
    
    # Convert to markdown
    markdown = html_to_markdown(html)
    
    if not markdown:
        return None
    
    # Build markdown with frontmatter
    md_content = f"""---
title: {meta['title']}
author: {meta['author']}
date: {meta['date']}
url: https://workless.build/posts/{Path(html_path).stem}.html
description: {meta['description']}
tags: {', '.join(meta['tags']) if meta['tags'] else 'ai-automation'}
---

{markdown}

---

*Published on Work Less, Build - AI automation for solo builders*  
*Subscribe: https://workless.build/#newsletter*
"""
    
    # Save
    slug = Path(html_path).stem
    md_path = output_dir / f"{slug}.md"
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content.strip())
    
    print(f"  ✅ Generated: {md_path.name}")
    return str(md_path)

def main():
    blog_dir = Path('/root/.openclaw/workspace/ai-automation-blog/blog')
    posts_dir = blog_dir / 'posts'
    md_dir = blog_dir / 'md'
    
    # Create md directory
    md_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🤖 GENERATING AI-OPTIMIZED VERSIONS")
    print("=" * 60)
    print()
    
    # Get all HTML posts (exclude EXAMPLE)
    html_posts = [p for p in posts_dir.glob('*.html') if 'EXAMPLE' not in p.name]
    
    print(f"Found {len(html_posts)} posts to process\n")
    
    txt_count = 0
    md_count = 0
    
    for html_path in sorted(html_posts):
        print(f"Processing: {html_path.name}")
        
        # Generate .txt version (in posts/ directory)
        txt_path = generate_txt_version(html_path, posts_dir)
        if txt_path:
            txt_count += 1
        
        # Generate .md version (in md/ directory)
        md_path = generate_md_version(html_path, md_dir)
        if md_path:
            md_count += 1
        
        print()
    
    print("=" * 60)
    print(f"✅ COMPLETE")
    print(f"  - {txt_count} .txt versions created (posts/*.txt)")
    print(f"  - {md_count} .md versions created (md/*.md)")
    print("=" * 60)
    print()
    print("Next: Update sitemap.xml to include new formats")

if __name__ == '__main__':
    main()
