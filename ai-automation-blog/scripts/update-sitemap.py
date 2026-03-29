#!/usr/bin/env python3
"""
Update sitemap.xml to include HTML, TXT, and MD versions of all posts
Runs automatically after generating AI versions
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def update_sitemap():
    """Regenerate sitemap with all formats"""
    
    blog_dir = Path('/root/.openclaw/workspace/ai-automation-blog/blog')
    sitemap_path = blog_dir / 'sitemap.xml'
    
    # Create fresh sitemap
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    def add_url(loc, priority='0.8'):
        url = ET.SubElement(urlset, 'url')
        loc_el = ET.SubElement(url, 'loc')
        loc_el.text = loc
        lastmod_el = ET.SubElement(url, 'lastmod')
        lastmod_el.text = today
        priority_el = ET.SubElement(url, 'priority')
        priority_el.text = priority
    
    # Homepage
    add_url('https://workless.build/', '1.0')
    
    # Static pages
    add_url('https://workless.build/about.html', '0.8')
    add_url('https://workless.build/archive.html', '0.7')
    add_url('https://workless.build/resources.html', '0.7')
    
    # Special AI files
    add_url('https://workless.build/llm.txt', '0.9')
    add_url('https://workless.build/robots.json', '0.5')
    
    # Get all posts
    posts_dir = blog_dir / 'posts'
    html_posts = sorted([p for p in posts_dir.glob('*.html') if 'EXAMPLE' not in p.name])
    
    for post in html_posts:
        slug = post.stem
        
        # HTML version (highest priority)
        add_url(f'https://workless.build/posts/{post.name}', '0.9')
        
        # TXT version (AI crawlers)
        if (posts_dir / f'{slug}.txt').exists():
            add_url(f'https://workless.build/posts/{slug}.txt', '0.8')
        
        # MD version (LLM training)
        if (blog_dir / 'md' / f'{slug}.md').exists():
            add_url(f'https://workless.build/md/{slug}.md', '0.8')
    
    # Pretty print XML
    ET.indent(urlset, space='  ')
    tree = ET.ElementTree(urlset)
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    
    # Count URLs
    total_urls = len(html_posts) * 3 + 6
    
    print(f"✅ Sitemap updated: {total_urls} URLs")
    print(f"  - {len(html_posts)} HTML posts")
    print(f"  - {len(html_posts)} TXT versions")
    print(f"  - {len(html_posts)} MD versions")
    print(f"  - 6 special pages (homepage, about, llm.txt, etc.)")
    
    return True

if __name__ == '__main__':
    update_sitemap()
