#!/usr/bin/env python3
"""
Dynamic XML Sitemap Generator
Generates sitemaps for AI Automation Blog and CleverDogMethod

Usage:
    python3 generate-sitemap.py --blog ai-automation
    python3 generate-sitemap.py --blog cleverdogmethod
    python3 generate-sitemap.py --all
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")

BLOGS = {
    "ai-automation": {
        "root": WORKSPACE / "ai-automation-blog" / "blog-new",
        "base_url": "https://workless.build",
        "output": WORKSPACE / "ai-automation-blog" / "blog-new" / "sitemap.xml"
    },
    "cleverdogmethod": {
        "root": WORKSPACE / "dog-training-landing-clean" / "blog",
        "base_url": "https://cleverdogmethod.com",
        "output": WORKSPACE / "dog-training-landing-clean" / "sitemap.xml"
    }
}


def get_file_modified_date(file_path: Path) -> str:
    """Get file modification date in ISO format"""
    try:
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')


def find_categories(blog_root: Path) -> list:
    """Find all category directories"""
    categories = []
    if not blog_root.exists():
        return categories
    
    for item in blog_root.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
            categories.append(str(item.relative_to(blog_root)))
            
            # Find subcategories
            for subitem in item.iterdir():
                if subitem.is_dir() and not subitem.name.startswith('.'):
                    categories.append(str(subitem.relative_to(blog_root)))
    
    return categories


def find_all_posts(blog_root: Path) -> list:
    """Find all HTML posts recursively"""
    posts = []
    if not blog_root.exists():
        return posts
    
    for html_file in blog_root.rglob("*.html"):
        # Skip index and special pages
        if html_file.name in ['index.html', '404.html', 'search.html']:
            continue
        
        rel_path = html_file.relative_to(blog_root)
        posts.append({
            'path': str(rel_path),
            'full_path': html_file,
            'lastmod': get_file_modified_date(html_file)
        })
    
    return posts


def add_url(parent: Element, loc: str, priority: str, changefreq: str, lastmod: str = None):
    """Add URL entry to sitemap"""
    url = SubElement(parent, 'url')
    SubElement(url, 'loc').text = loc
    SubElement(url, 'priority').text = priority
    SubElement(url, 'changefreq').text = changefreq
    if lastmod:
        SubElement(url, 'lastmod').text = lastmod


def generate_sitemap(blog_name: str):
    """Generate sitemap for a specific blog"""
    
    if blog_name not in BLOGS:
        print(f"❌ Unknown blog: {blog_name}")
        print(f"Available blogs: {', '.join(BLOGS.keys())}")
        return False
    
    config = BLOGS[blog_name]
    blog_root = config['root']
    base_url = config['base_url']
    output_file = config['output']
    
    print(f"\n📍 Generating sitemap for: {blog_name}")
    print(f"   Root: {blog_root}")
    print(f"   Base URL: {base_url}")
    
    # Create XML structure
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Homepage
    add_url(urlset, base_url + '/', '1.0', 'daily', datetime.now().strftime('%Y-%m-%d'))
    
    # Category pages
    categories = find_categories(blog_root)
    print(f"   Found {len(categories)} categories")
    for category in categories:
        category_url = base_url + '/' + category + '/'
        add_url(urlset, category_url, '0.9', 'weekly')
    
    # All posts
    posts = find_all_posts(blog_root)
    print(f"   Found {len(posts)} posts")
    for post in posts:
        post_url = base_url + '/' + post['path']
        add_url(urlset, post_url, '0.8', 'monthly', post['lastmod'])
    
    # Generate pretty XML
    xml_str = minidom.parseString(tostring(urlset, encoding='unicode')).toprettyxml(indent="  ")
    
    # Remove extra blank lines
    xml_lines = [line for line in xml_str.split('\n') if line.strip()]
    xml_str = '\n'.join(xml_lines)
    
    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"✅ Sitemap saved: {output_file}")
    print(f"   Total URLs: {len(categories) + len(posts) + 1}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Generate XML sitemaps for blogs')
    parser.add_argument('--blog', type=str, help='Blog name (ai-automation or cleverdogmethod)')
    parser.add_argument('--all', action='store_true', help='Generate sitemaps for all blogs')
    
    args = parser.parse_args()
    
    if args.all:
        print("🗺️  Generating sitemaps for all blogs...")
        success_count = 0
        for blog_name in BLOGS.keys():
            if generate_sitemap(blog_name):
                success_count += 1
        print(f"\n✅ Generated {success_count}/{len(BLOGS)} sitemaps")
    elif args.blog:
        generate_sitemap(args.blog)
    else:
        print("Usage:")
        print("  python3 generate-sitemap.py --blog ai-automation")
        print("  python3 generate-sitemap.py --blog cleverdogmethod")
        print("  python3 generate-sitemap.py --all")
        sys.exit(1)


if __name__ == '__main__':
    main()
