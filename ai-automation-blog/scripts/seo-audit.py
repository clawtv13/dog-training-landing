#!/usr/bin/env python3
"""
SEO Audit Script for AI Automation Builder Blog
Validates SEO elements, structured data, performance metrics
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser

BLOG_DIR = Path("/root/.openclaw/workspace/ai-automation-blog/blog")
POSTS_DIR = BLOG_DIR / "posts"

class SEOAuditor(HTMLParser):
    """Parse HTML and extract SEO elements"""
    
    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.has_h1 = False
        self.h1_count = 0
        self.h2_count = 0
        self.images_without_alt = []
        self.links = []
        self.has_canonical = False
        self.has_structured_data = False
        self.word_count = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Check meta tags
        if tag == 'meta':
            name = attrs_dict.get('name') or attrs_dict.get('property')
            content = attrs_dict.get('content')
            if name and content:
                self.meta_tags[name] = content
        
        # Check canonical
        if tag == 'link' and attrs_dict.get('rel') == 'canonical':
            self.has_canonical = True
        
        # Check headings
        if tag == 'h1':
            self.has_h1 = True
            self.h1_count += 1
        if tag == 'h2':
            self.h2_count += 1
        
        # Check images
        if tag == 'img':
            if 'alt' not in attrs_dict or not attrs_dict['alt']:
                self.images_without_alt.append(attrs_dict.get('src', 'unknown'))
        
        # Check links
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        
        # Check structured data
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.has_structured_data = True
    
    def handle_data(self, data):
        # Count words in content
        words = len(re.findall(r'\w+', data))
        self.word_count += words


def audit_post(filepath):
    """Audit a single post for SEO compliance"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = SEOAuditor()
    parser.feed(content)
    
    issues = []
    warnings = []
    
    # Required meta tags
    required_meta = ['description', 'keywords', 'og:title', 'og:description', 'twitter:card']
    for meta in required_meta:
        if meta not in parser.meta_tags:
            issues.append(f"Missing meta tag: {meta}")
    
    # Meta description length
    if 'description' in parser.meta_tags:
        desc_len = len(parser.meta_tags['description'])
        if desc_len < 120:
            warnings.append(f"Meta description too short ({desc_len} chars, recommended 120-160)")
        elif desc_len > 160:
            warnings.append(f"Meta description too long ({desc_len} chars, recommended 120-160)")
    
    # Canonical URL
    if not parser.has_canonical:
        issues.append("Missing canonical URL")
    
    # H1 tag
    if not parser.has_h1:
        issues.append("Missing H1 tag")
    elif parser.h1_count > 1:
        warnings.append(f"Multiple H1 tags found ({parser.h1_count})")
    
    # Structured data
    if not parser.has_structured_data:
        issues.append("Missing JSON-LD structured data")
    
    # Images without alt text
    if parser.images_without_alt:
        warnings.append(f"{len(parser.images_without_alt)} images without alt text")
    
    # Word count
    if parser.word_count < 300:
        warnings.append(f"Low word count ({parser.word_count} words, recommended 800+)")
    
    # Internal links
    internal_links = [l for l in parser.links if l.startswith('/') or 'aiautomationbuilder.com' in l]
    if len(internal_links) < 2:
        warnings.append(f"Few internal links ({len(internal_links)})")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'meta_tags': parser.meta_tags,
        'word_count': parser.word_count,
        'h1_count': parser.h1_count,
        'h2_count': parser.h2_count,
        'images_without_alt': len(parser.images_without_alt),
        'internal_links': len(internal_links)
    }


def main():
    print("🔍 SEO Audit Report for AI Automation Builder Blog")
    print("=" * 60)
    
    posts = list(POSTS_DIR.glob("*.html"))
    total_issues = 0
    total_warnings = 0
    
    for post in posts:
        print(f"\n📄 {post.name}")
        print("-" * 60)
        
        result = audit_post(post)
        
        if result['issues']:
            print("❌ CRITICAL ISSUES:")
            for issue in result['issues']:
                print(f"   • {issue}")
            total_issues += len(result['issues'])
        
        if result['warnings']:
            print("⚠️  WARNINGS:")
            for warning in result['warnings']:
                print(f"   • {warning}")
            total_warnings += len(result['warnings'])
        
        if not result['issues'] and not result['warnings']:
            print("✅ All SEO checks passed!")
        
        print(f"\n📊 Stats:")
        print(f"   • Word count: {result['word_count']}")
        print(f"   • H1 tags: {result['h1_count']}")
        print(f"   • H2 tags: {result['h2_count']}")
        print(f"   • Internal links: {result['internal_links']}")
        print(f"   • Images without alt: {result['images_without_alt']}")
    
    print("\n" + "=" * 60)
    print(f"📈 SUMMARY: {len(posts)} posts audited")
    print(f"   • {total_issues} critical issues")
    print(f"   • {total_warnings} warnings")
    
    if total_issues == 0:
        print("✅ All posts pass critical SEO checks!")
    else:
        print("⚠️  Fix critical issues before deployment")
    
    # Check infrastructure
    print("\n🛠️  INFRASTRUCTURE CHECK:")
    sitemap = BLOG_DIR / "sitemap.xml"
    robots = BLOG_DIR / "robots.txt"
    rss = BLOG_DIR / "rss.xml"
    
    print(f"   • sitemap.xml: {'✅' if sitemap.exists() else '❌ MISSING'}")
    print(f"   • robots.txt: {'✅' if robots.exists() else '❌ MISSING'}")
    print(f"   • rss.xml: {'✅' if rss.exists() else '❌ MISSING'}")
    
    print("\n✅ SEO audit complete!")


if __name__ == "__main__":
    main()
