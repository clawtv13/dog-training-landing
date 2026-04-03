#!/usr/bin/env python3
"""Generate HTML from MD files for AI Automation Blog"""

import os
import re
import markdown
from pathlib import Path
from datetime import datetime

# Paths
MD_DIR = Path("blog/md")
HTML_DIR = Path("blog")
TEMPLATE_PATH = Path("templates/post.html")

def extract_frontmatter(md_content):
    """Extract YAML frontmatter from MD file"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', md_content, re.DOTALL)
    if not match:
        return {}, md_content
    
    frontmatter_text = match.group(1)
    body = match.group(2)
    
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter, body

def extract_excerpt(body):
    """Extract first paragraph as excerpt"""
    # Remove headers
    lines = [l for l in body.split('\n') if not l.startswith('#')]
    # Get first non-empty paragraph
    for para in '\n'.join(lines).split('\n\n'):
        para = para.strip()
        if para and len(para) > 50:
            # Clean markdown
            para = re.sub(r'\*\*(.*?)\*\*', r'\1', para)  # Bold
            para = re.sub(r'\*(.*?)\*', r'\1', para)      # Italic
            para = re.sub(r'`(.*?)`', r'\1', para)        # Code
            para = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', para)  # Links
            return para[:200] + ('...' if len(para) > 200 else '')
    return "Practical automation insights for smart builders."

def estimate_read_time(body):
    """Estimate reading time (250 words per minute)"""
    word_count = len(body.split())
    minutes = max(1, round(word_count / 250))
    return minutes

def generate_html(md_file):
    """Generate HTML from MD file"""
    print(f"Processing: {md_file.name}")
    
    # Read MD
    md_content = md_file.read_text(encoding='utf-8')
    frontmatter, body = extract_frontmatter(md_content)
    
    # Parse with markdown
    html_body = markdown.markdown(body, extensions=['extra', 'codehilite'])
    
    # Extract metadata
    title = frontmatter.get('title', 'Untitled')
    date_str = frontmatter.get('date', '').strip()
    
    # Parse date from filename if not in frontmatter
    if not date_str:
        # Extract from filename: 2026-03-29-title.md
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', md_file.stem)
        if date_match:
            date_str = date_match.group(1)
    
    # Format date
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            display_date = date_obj.strftime('%B %d, %Y')
            iso_date = date_obj.isoformat()
        except:
            display_date = date_str
            iso_date = date_str
    else:
        display_date = 'Recently'
        iso_date = datetime.now().isoformat()
    
    excerpt = frontmatter.get('description', '').replace('{{EXCERPT}}...', '').strip()
    if not excerpt:
        excerpt = extract_excerpt(body)
    
    read_time = estimate_read_time(body)
    word_count = len(body.split())
    
    # Generate slug from filename
    slug = md_file.stem
    
    # Build URL
    url = f"https://workless.build/blog/{slug}.html"
    
    # Keywords
    keywords = frontmatter.get('tags', 'AI automation, productivity, solopreneurs')
    
    # Short title for breadcrumb
    title_short = title[:50] + '...' if len(title) > 50 else title
    
    # Load template
    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    
    # Replace placeholders
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{TITLE_SHORT}}', title_short)
    html = html.replace('{{CONTENT}}', html_body)
    html = html.replace('{{EXCERPT}}', excerpt)
    html = html.replace('{{URL}}', url)
    html = html.replace('{{DATE}}', display_date)
    html = html.replace('{{PUBLISHED_ISO}}', iso_date)
    html = html.replace('{{MODIFIED_ISO}}', iso_date)
    html = html.replace('{{READ_TIME}}', str(read_time))
    html = html.replace('{{WORD_COUNT}}', str(word_count))
    html = html.replace('{{KEYWORDS}}', keywords)
    html = html.replace('{{IMAGE_URL}}', 'https://workless.build/og-default.png')
    
    # Save HTML
    output_path = HTML_DIR / f"{slug}.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"  ✅ Generated: {output_path}")
    
    return {
        'slug': slug,
        'title': title,
        'url': url,
        'date': display_date,
        'excerpt': excerpt,
        'readTime': read_time
    }

def main():
    print("🚀 Starting HTML generation for AI Automation Blog\n")
    
    # Check paths
    if not MD_DIR.exists():
        print(f"❌ MD directory not found: {MD_DIR}")
        return
    
    if not TEMPLATE_PATH.exists():
        print(f"❌ Template not found: {TEMPLATE_PATH}")
        return
    
    # Ensure output dir exists
    HTML_DIR.mkdir(exist_ok=True)
    
    # Get all MD files
    md_files = sorted(MD_DIR.glob("*.md"), reverse=True)
    print(f"Found {len(md_files)} MD files\n")
    
    if len(md_files) == 0:
        print("❌ No MD files found!")
        return
    
    # Generate HTML for each
    posts = []
    for md_file in md_files:
        try:
            post_data = generate_html(md_file)
            posts.append(post_data)
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Generated {len(posts)} HTML files")
    print(f"\nNext steps:")
    print(f"1. Run: python3 blog/scripts/update-sitemap.py")
    print(f"2. Deploy to GitHub")

if __name__ == '__main__':
    main()
