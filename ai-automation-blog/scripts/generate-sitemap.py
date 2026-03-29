#!/usr/bin/env python3
"""
Dynamic Sitemap Generator for AI Automation Builder Blog
Automatically generates sitemap.xml from posts directory
"""

import os
import json
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

BLOG_DIR = Path("/root/.openclaw/workspace/ai-automation-blog/blog")
POSTS_DIR = BLOG_DIR / "posts"
SITEMAP_PATH = BLOG_DIR / "sitemap.xml"
BASE_URL = "https://aiautomationbuilder.com"


class TitleExtractor(HTMLParser):
    """Extract title from HTML"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
    
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.split("|")[0].strip()


def extract_title(filepath):
    """Extract title from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = TitleExtractor()
    parser.feed(content)
    return parser.title


def get_file_date(filepath):
    """Get file modification date in ISO format"""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def generate_sitemap():
    """Generate sitemap.xml from posts"""
    
    print("🔄 Generating sitemap.xml...")
    
    # Start sitemap XML
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  
  <!-- Homepage -->
  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  
'''.format(base_url=BASE_URL, today=datetime.now().strftime('%Y-%m-%d'))
    
    # Add blog posts
    posts = sorted(POSTS_DIR.glob("*.html"), reverse=True)
    
    for post in posts:
        filename = post.name
        title = extract_title(post)
        date = get_file_date(post)
        
        post_url = f"{BASE_URL}/posts/{filename}"
        
        sitemap_content += f'''  <!-- {title} -->
  <url>
    <loc>{post_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <news:news>
      <news:publication>
        <news:name>AI Automation Builder</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>{date}</news:publication_date>
      <news:title>{title}</news:title>
    </news:news>
  </url>
  
'''
    
    sitemap_content += "</urlset>\n"
    
    # Write sitemap
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✅ Sitemap generated: {SITEMAP_PATH}")
    print(f"📊 Total URLs: {len(posts) + 1} (1 homepage + {len(posts)} posts)")


def generate_rss():
    """Generate RSS feed from posts"""
    
    RSS_PATH = BLOG_DIR / "rss.xml"
    
    print("🔄 Generating rss.xml...")
    
    rss_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>AI Automation Builder</title>
    <link>{base_url}</link>
    <description>AI automation tools, workflows, and tutorials for solopreneurs. Learn to build faster with AI.</description>
    <language>en-us</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <atom:link href="{base_url}/rss.xml" rel="self" type="application/rss+xml"/>
    <generator>AI Automation Builder</generator>
    <copyright>{year} AI Automation Builder</copyright>
    <category>AI automation</category>
    <category>Solopreneur tools</category>
    <category>AI workflows</category>
    <image>
      <url>{base_url}/logo.png</url>
      <title>AI Automation Builder</title>
      <link>{base_url}</link>
    </image>
    
'''.format(
        base_url=BASE_URL,
        build_date=datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        year=datetime.now().year
    )
    
    # Add posts
    posts = sorted(POSTS_DIR.glob("*.html"), reverse=True)[:10]  # Latest 10 posts
    
    for post in posts:
        filename = post.name
        title = extract_title(post)
        date = get_file_date(post)
        post_url = f"{BASE_URL}/posts/{filename}"
        
        # Convert date to RFC-822 format
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        pub_date = date_obj.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        rss_content += f'''    <!-- {title} -->
    <item>
      <title>{title}</title>
      <link>{post_url}</link>
      <guid isPermaLink="true">{post_url}</guid>
      <pubDate>{pub_date}</pubDate>
      <dc:creator>AI Automation Builder</dc:creator>
      <category>AI Automation</category>
      <description><![CDATA[{title}]]></description>
    </item>
    
'''
    
    rss_content += "  </channel>\n</rss>\n"
    
    # Write RSS
    with open(RSS_PATH, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"✅ RSS feed generated: {RSS_PATH}")
    print(f"📊 Total items: {len(posts)}")


def main():
    print("🚀 AI Automation Builder - Sitemap Generator")
    print("=" * 60)
    
    generate_sitemap()
    generate_rss()
    
    print("\n✅ All files generated successfully!")
    print("\nNext steps:")
    print("1. Submit sitemap to Google Search Console")
    print("2. Validate at: https://www.xml-sitemaps.com/validate-xml-sitemap.html")
    print("3. Test RSS feed at: https://validator.w3.org/feed/")


if __name__ == "__main__":
    main()
