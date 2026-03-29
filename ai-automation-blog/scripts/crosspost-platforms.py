#!/usr/bin/env python3
"""
Cross-post blog articles to multiple platforms
- Medium (5K+ built-in audience)
- Dev.to (900K+ developers)
- Hashnode (growing tech community)

Runs automatically after blog post is published.
"""

import os
import sys
import json
import requests
import re
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

BLOG_DIR = Path(__file__).parent.parent / "blog"
POSTS_DIR = BLOG_DIR / "posts"
STATE_FILE = Path(__file__).parent.parent / ".state" / "crossposted.json"

MEDIUM_TOKEN = os.getenv("MEDIUM_TOKEN", "")
DEVTO_TOKEN = os.getenv("DEVTO_TOKEN", "")
HASHNODE_TOKEN = os.getenv("HASHNODE_TOKEN", "")

BLOG_BASE_URL = "https://aiautomationbuilder.com"
NEWSLETTER_URL = "https://aiautomationbuilder.beehiiv.com"

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_crossposted():
    """Load list of already crossposted articles"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_crossposted(post_slug, platform, url):
    """Save crosspost record"""
    state = load_crossposted()
    
    if post_slug not in state:
        state[post_slug] = {}
    
    state[post_slug][platform] = {
        'url': url,
        'posted_at': datetime.now().isoformat()
    }
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# ============================================================================
# HTML TO MARKDOWN CONVERSION
# ============================================================================

def html_to_markdown(html_content):
    """
    Convert blog post HTML to Markdown for cross-posting
    """
    # Remove script tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    
    # Remove style tags
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # Remove HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # Convert headings
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL)
    
    # Convert paragraphs
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    
    # Convert lists
    html = re.sub(r'<ul[^>]*>', '', html)
    html = re.sub(r'</ul>', '\n', html)
    html = re.sub(r'<ol[^>]*>', '', html)
    html = re.sub(r'</ol>', '\n', html)
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL)
    
    # Convert links
    html = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)
    
    # Convert emphasis
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)
    
    # Convert code
    html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html, flags=re.DOTALL)
    html = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', html, flags=re.DOTALL)
    
    # Remove remaining HTML tags
    html = re.sub(r'<[^>]+>', '', html)
    
    # Clean up whitespace
    markdown = re.sub(r'\n{3,}', '\n\n', html)
    markdown = markdown.strip()
    
    return markdown

# ============================================================================
# PARSE POST
# ============================================================================

def parse_blog_post(post_path):
    """Extract metadata and content from blog post"""
    with open(post_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1).replace(' | AI Automation Builder', '') if title_match else 'Untitled'
    
    # Extract canonical URL
    url_match = re.search(r'<link rel="canonical" href="(.*?)">', html)
    canonical_url = url_match.group(1) if url_match else ''
    
    # Extract keywords (for tags)
    keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', html)
    keywords = keywords_match.group(1) if keywords_match else ''
    tags = [k.strip() for k in keywords.split(',')[:5]]  # Max 5 tags
    
    # Extract content (between article tags or main content div)
    content_match = re.search(r'<article[^>]*>(.*?)</article>', html, flags=re.DOTALL)
    if not content_match:
        content_match = re.search(r'<div class="content"[^>]*>(.*?)</div>', html, flags=re.DOTALL)
    
    html_content = content_match.group(1) if content_match else html
    
    # Convert to Markdown
    markdown_content = html_to_markdown(html_content)
    
    # Add canonical link and CTA footer
    footer = f"""\n\n---

**Want more AI automation tips?**

Subscribe to [AI Automation Builder]({NEWSLETTER_URL}) - Weekly tools & workflows for solopreneurs.

*Originally published at [{BLOG_BASE_URL}]({canonical_url})*
"""
    
    markdown_content += footer
    
    return {
        'title': title,
        'content': markdown_content,
        'tags': tags,
        'canonical_url': canonical_url
    }

# ============================================================================
# MEDIUM
# ============================================================================

def crosspost_to_medium(post_data):
    """
    Cross-post to Medium
    """
    if not MEDIUM_TOKEN:
        print("⚠️  Medium token not set")
        print("   Get one at: https://medium.com/me/settings/security")
        print("   Set: export MEDIUM_TOKEN='your_token'")
        return None
    
    print("📝 Posting to Medium...")
    
    try:
        # Get user ID
        headers = {
            'Authorization': f'Bearer {MEDIUM_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        user_response = requests.get('https://api.medium.com/v1/me', headers=headers)
        
        if user_response.status_code != 200:
            print(f"✗ Medium auth error: {user_response.status_code}")
            return None
        
        user_id = user_response.json()['data']['id']
        
        # Create post
        payload = {
            'title': post_data['title'],
            'contentFormat': 'markdown',
            'content': post_data['content'],
            'tags': post_data['tags'][:3],  # Medium max 3 tags
            'canonicalUrl': post_data['canonical_url'],
            'publishStatus': 'public'
        }
        
        post_response = requests.post(
            f'https://api.medium.com/v1/users/{user_id}/posts',
            headers=headers,
            json=payload
        )
        
        if post_response.status_code == 201:
            data = post_response.json()['data']
            print(f"✅ Posted to Medium: {data['url']}")
            return data['url']
        else:
            print(f"✗ Medium post error: {post_response.status_code}")
            print(f"   Response: {post_response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"✗ Medium error: {e}")
        return None

# ============================================================================
# DEV.TO
# ============================================================================

def crosspost_to_devto(post_data):
    """
    Cross-post to Dev.to
    """
    if not DEVTO_TOKEN:
        print("⚠️  Dev.to token not set")
        print("   Get one at: https://dev.to/settings/extensions")
        print("   Set: export DEVTO_TOKEN='your_token'")
        return None
    
    print("📝 Posting to Dev.to...")
    
    try:
        headers = {
            'api-key': DEVTO_TOKEN,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'article': {
                'title': post_data['title'],
                'body_markdown': post_data['content'],
                'published': True,
                'tags': [t.lower().replace(' ', '') for t in post_data['tags'][:4]],  # Dev.to max 4 tags
                'canonical_url': post_data['canonical_url']
            }
        }
        
        response = requests.post(
            'https://dev.to/api/articles',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Posted to Dev.to: {data['url']}")
            return data['url']
        else:
            print(f"✗ Dev.to error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"✗ Dev.to error: {e}")
        return None

# ============================================================================
# HASHNODE
# ============================================================================

def crosspost_to_hashnode(post_data):
    """
    Cross-post to Hashnode (GraphQL API)
    """
    if not HASHNODE_TOKEN:
        print("⚠️  Hashnode token not set")
        print("   Get one at: https://hashnode.com/settings/developer")
        print("   Set: export HASHNODE_TOKEN='your_token'")
        return None
    
    print("📝 Posting to Hashnode...")
    
    try:
        headers = {
            'Authorization': HASHNODE_TOKEN,
            'Content-Type': 'application/json'
        }
        
        # GraphQL mutation
        query = """
        mutation CreateStory($input: CreateStoryInput!) {
            createPublicationStory(input: $input) {
                post {
                    slug
                    title
                }
            }
        }
        """
        
        variables = {
            'input': {
                'title': post_data['title'],
                'contentMarkdown': post_data['content'],
                'tags': [{'slug': t.lower().replace(' ', '-')} for t in post_data['tags'][:5]],
                'isPartOfPublication': {
                    'publicationId': os.getenv('HASHNODE_PUBLICATION_ID', '')
                },
                'canonicalUrl': post_data['canonical_url']
            }
        }
        
        response = requests.post(
            'https://api.hashnode.com/',
            headers=headers,
            json={'query': query, 'variables': variables}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'createPublicationStory' in data['data']:
                slug = data['data']['createPublicationStory']['post']['slug']
                url = f"https://hashnode.com/@yourusername/{slug}"
                print(f"✅ Posted to Hashnode: {url}")
                return url
            else:
                print(f"✗ Hashnode API error: {data}")
                return None
        else:
            print(f"✗ Hashnode error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ Hashnode error: {e}")
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Cross-post latest blog posts to all platforms
    """
    print("=" * 60)
    print("CROSS-PLATFORM DISTRIBUTION")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    print()
    
    # Get all posts
    if not POSTS_DIR.exists():
        print("⚠️  Posts directory not found")
        return
    
    posts = sorted([p for p in POSTS_DIR.glob('*.html') if p.name != 'index.json'], 
                   reverse=True)
    
    if not posts:
        print("⚠️  No posts found")
        return
    
    # Load crosspost state
    crossposted = load_crossposted()
    
    # Process latest posts (not already crossposted)
    posts_processed = 0
    
    for post_path in posts[:5]:  # Process up to 5 latest posts
        post_slug = post_path.stem
        
        # Check if already crossposted to all platforms
        if post_slug in crossposted:
            already_posted = crossposted[post_slug]
            if all(p in already_posted for p in ['medium', 'devto']):
                continue
        
        print(f"\n📄 Processing: {post_slug}")
        print("-" * 60)
        
        # Parse post
        post_data = parse_blog_post(post_path)
        print(f"   Title: {post_data['title']}")
        print(f"   Tags: {', '.join(post_data['tags'])}")
        print()
        
        # Cross-post to platforms
        results = {}
        
        # Medium
        if post_slug not in crossposted or 'medium' not in crossposted.get(post_slug, {}):
            medium_url = crosspost_to_medium(post_data)
            if medium_url:
                save_crossposted(post_slug, 'medium', medium_url)
                results['medium'] = medium_url
        
        # Dev.to
        if post_slug not in crossposted or 'devto' not in crossposted.get(post_slug, {}):
            devto_url = crosspost_to_devto(post_data)
            if devto_url:
                save_crossposted(post_slug, 'devto', devto_url)
                results['devto'] = devto_url
        
        # Hashnode (optional)
        # if post_slug not in crossposted or 'hashnode' not in crossposted.get(post_slug, {}):
        #     hashnode_url = crosspost_to_hashnode(post_data)
        #     if hashnode_url:
        #         save_crossposted(post_slug, 'hashnode', hashnode_url)
        #         results['hashnode'] = hashnode_url
        
        if results:
            posts_processed += 1
            print()
            print(f"✅ Crossposted to {len(results)} platform(s)")
            print()
    
    print("=" * 60)
    print(f"✅ DISTRIBUTION COMPLETE - {posts_processed} posts processed")
    print("=" * 60)
    print()
    
    if posts_processed == 0:
        print("All recent posts already crossposted ✓")
    else:
        print(f"Successfully distributed {posts_processed} post(s)")
        print()
        print("Impact:")
        print("  • Medium: 5K+ potential readers")
        print("  • Dev.to: 900K+ developer community")
        print("  • Canonical links preserve SEO")
        print("  • Newsletter CTA in each post")
    print()


if __name__ == "__main__":
    main()
