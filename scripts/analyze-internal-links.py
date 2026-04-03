#!/usr/bin/env python3
"""
Internal Link Analysis Tool
Analyzes internal linking structure of blog posts

Usage:
    python3 analyze-internal-links.py --blog ai-automation
    python3 analyze-internal-links.py --blog cleverdogmethod
    python3 analyze-internal-links.py --all
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")

BLOGS = {
    "ai-automation": {
        "root": WORKSPACE / "ai-automation-blog" / "blog-new",
        "base_url": "https://workless.build"
    },
    "cleverdogmethod": {
        "root": WORKSPACE / "dog-training-landing-clean" / "blog",
        "base_url": "https://cleverdogmethod.com"
    }
}


def extract_internal_links(html_content: str, base_domain: str) -> list:
    """
    Extract all internal links from HTML content
    Returns list of relative URLs
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Skip external, anchors, mailto
        if href.startswith('http') and base_domain not in href:
            continue
        if href.startswith('#') or href.startswith('mailto:'):
            continue
        
        # Normalize to relative path
        if href.startswith('http'):
            href = '/' + href.split(base_domain)[1].lstrip('/')
        
        links.append(href)
    
    return links


def find_all_posts(blog_root: Path) -> list:
    """Find all HTML posts"""
    posts = []
    if not blog_root.exists():
        return posts
    
    for html_file in blog_root.rglob("*.html"):
        if html_file.name in ['index.html', '404.html', 'search.html']:
            continue
        
        posts.append(html_file)
    
    return posts


def analyze_internal_links(blog_name: str):
    """Analyze internal link structure for a blog"""
    
    if blog_name not in BLOGS:
        print(f"❌ Unknown blog: {blog_name}")
        return None
    
    config = BLOGS[blog_name]
    blog_root = config['root']
    base_url = config['base_url']
    base_domain = base_url.replace('https://', '').replace('http://', '')
    
    print(f"\n🔗 Analyzing internal links: {blog_name}")
    print(f"   Root: {blog_root}")
    
    posts = find_all_posts(blog_root)
    print(f"   Found {len(posts)} posts")
    
    if not posts:
        print("   ⚠️  No posts found")
        return None
    
    # Data structures
    links_per_post = {}
    incoming_links = defaultdict(int)
    outgoing_links = defaultdict(list)
    
    # Analyze each post
    for post_path in posts:
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            rel_path = '/' + str(post_path.relative_to(blog_root))
            internal_links = extract_internal_links(html, base_domain)
            
            links_per_post[rel_path] = internal_links
            outgoing_links[rel_path] = internal_links
            
            for link in internal_links:
                incoming_links[link] += 1
        
        except Exception as e:
            print(f"   ⚠️  Error analyzing {post_path.name}: {e}")
            continue
    
    # Calculate metrics
    total_posts = len(links_per_post)
    total_links = sum(len(links) for links in links_per_post.values())
    avg_links = total_links / total_posts if total_posts > 0 else 0
    
    # Find issues
    orphan_pages = [p for p, incoming in links_per_post.items() 
                    if incoming_links.get(p, 0) == 0]
    weak_pages = [p for p, links in links_per_post.items() if len(links) < 3]
    strong_pages = sorted(incoming_links.items(), key=lambda x: -x[1])[:10]
    
    # Generate report
    report = {
        "blog": blog_name,
        "analyzed_at": datetime.now().isoformat(),
        "summary": {
            "total_posts": total_posts,
            "total_internal_links": total_links,
            "avg_links_per_post": round(avg_links, 2),
            "orphan_pages_count": len(orphan_pages),
            "weak_pages_count": len(weak_pages)
        },
        "most_linked_pages": [
            {"url": url, "incoming_links": count} 
            for url, count in strong_pages if count > 0
        ],
        "orphan_pages": orphan_pages[:20],  # Limit output
        "weak_pages": weak_pages[:20],
        "recommendations": []
    }
    
    # Add recommendations
    if avg_links < 5:
        report["recommendations"].append(
            f"⚠️  Average links per post ({avg_links:.1f}) is below target (5+). "
            "Add more contextual internal links."
        )
    
    if len(orphan_pages) > 0:
        report["recommendations"].append(
            f"⚠️  {len(orphan_pages)} orphan pages (no incoming links). "
            "Link to these pages from related content."
        )
    
    if len(weak_pages) > total_posts * 0.3:
        report["recommendations"].append(
            f"⚠️  {len(weak_pages)} pages have <3 internal links. "
            "Strengthen internal linking structure."
        )
    
    if not report["recommendations"]:
        report["recommendations"].append("✅ Internal linking structure looks healthy!")
    
    # Print report
    print("\n📊 INTERNAL LINK ANALYSIS REPORT")
    print("=" * 60)
    print(f"Blog: {blog_name}")
    print(f"Total Posts: {report['summary']['total_posts']}")
    print(f"Total Internal Links: {report['summary']['total_internal_links']}")
    print(f"Avg Links/Post: {report['summary']['avg_links_per_post']}")
    print(f"Orphan Pages: {report['summary']['orphan_pages_count']}")
    print(f"Weak Pages (<3 links): {report['summary']['weak_pages_count']}")
    
    print("\n🏆 Most Linked Pages:")
    for page in report["most_linked_pages"][:5]:
        print(f"   {page['incoming_links']:3d} ← {page['url']}")
    
    if orphan_pages:
        print(f"\n⚠️  Orphan Pages (first 5):")
        for page in orphan_pages[:5]:
            print(f"   {page}")
    
    if weak_pages:
        print(f"\n⚠️  Weak Pages (first 5):")
        for page in weak_pages[:5]:
            print(f"   {page} ({len(links_per_post[page])} links)")
    
    print("\n💡 Recommendations:")
    for rec in report["recommendations"]:
        print(f"   {rec}")
    
    # Save report
    report_file = WORKSPACE / "reports" / f"internal-links-{blog_name}-{datetime.now().strftime('%Y%m%d')}.json"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved: {report_file}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Analyze internal link structure')
    parser.add_argument('--blog', type=str, help='Blog name (ai-automation or cleverdogmethod)')
    parser.add_argument('--all', action='store_true', help='Analyze all blogs')
    
    args = parser.parse_args()
    
    if args.all:
        print("🔗 Analyzing all blogs...")
        for blog_name in BLOGS.keys():
            analyze_internal_links(blog_name)
    elif args.blog:
        analyze_internal_links(args.blog)
    else:
        print("Usage:")
        print("  python3 analyze-internal-links.py --blog ai-automation")
        print("  python3 analyze-internal-links.py --blog cleverdogmethod")
        print("  python3 analyze-internal-links.py --all")
        sys.exit(1)


if __name__ == '__main__':
    main()
