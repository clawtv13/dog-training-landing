#!/usr/bin/env python3
"""
WEEK 2: Content Structure & Internal Linking Implementation
Adds breadcrumbs, related posts, contextual links, navigation, and category hubs
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Set
from bs4 import BeautifulSoup
from html import escape as html_escape

# Configuration
AI_BLOG_ROOT = Path("/root/.openclaw/workspace/ai-automation-blog/blog-new")
DOG_BLOG_ROOT = Path("/root/.openclaw/workspace/dog-training-landing-clean/blog")
SITE_DOMAIN = "https://workless.build"

# Related categories mapping for cross-linking
RELATED_CATEGORY_MAP = {
    "ai-tools/llms": ["tutorials", "case-studies"],
    "ai-tools/no-code-ai": ["solo-founder-strategies/productivity"],
    "ai-tools/automation-platforms": ["solo-founder-strategies", "tutorials"],
    "ai-tools/image-generation": ["case-studies", "tutorials"],
    "solo-founder-strategies": ["ai-tools", "tutorials"],
    "solo-founder-strategies/productivity": ["ai-tools/no-code-ai", "tutorials"],
    "solo-founder-strategies/time-management": ["ai-tools", "tutorials"],
    "solo-founder-strategies/business-systems": ["ai-tools/automation-platforms"],
    "case-studies": ["ai-tools", "solo-founder-strategies"],
    "case-studies/failed-experiments": ["tutorials", "solo-founder-strategies"],
    "case-studies/success-stories": ["ai-tools", "solo-founder-strategies"],
    "tutorials": ["ai-tools", "case-studies"],
}

# Category metadata
CATEGORY_INFO = {
    "ai-tools": {
        "title": "AI Tools & Platforms",
        "description": "In-depth reviews, comparisons, and guides for AI tools that help solo founders build faster and smarter.",
        "keywords": "ai tools, automation platforms, llms, no-code ai, image generation"
    },
    "ai-tools/llms": {
        "title": "Large Language Models (LLMs)",
        "description": "Deep dives into ChatGPT, Claude, GPT-4, and other language models transforming how solo founders work.",
        "keywords": "llms, chatgpt, claude, gpt-4, language models"
    },
    "ai-tools/no-code-ai": {
        "title": "No-Code AI Tools",
        "description": "Build AI-powered apps without coding. Reviews of no-code AI platforms for solo builders.",
        "keywords": "no-code ai, visual ai builders, ai without coding"
    },
    "ai-tools/automation-platforms": {
        "title": "AI Automation Platforms",
        "description": "Zapier, Make, n8n, and AI workflow automation tools to scale your solo business.",
        "keywords": "automation, workflow automation, zapier, make, n8n"
    },
    "ai-tools/image-generation": {
        "title": "AI Image Generation",
        "description": "DALL-E, Midjourney, Stable Diffusion - AI art tools for content creators and marketers.",
        "keywords": "ai art, image generation, dall-e, midjourney, stable diffusion"
    },
    "solo-founder-strategies": {
        "title": "Solo Founder Strategies",
        "description": "Proven strategies for building, scaling, and sustaining a one-person business with AI.",
        "keywords": "solo founder, solopreneur, indie hacker, time management, productivity"
    },
    "solo-founder-strategies/productivity": {
        "title": "Productivity for Solo Founders",
        "description": "Time management, focus techniques, and productivity systems for one-person businesses.",
        "keywords": "productivity, time management, focus, deep work"
    },
    "solo-founder-strategies/time-management": {
        "title": "Time Management for Solopreneurs",
        "description": "Master your schedule, prioritize ruthlessly, and get more done as a solo founder.",
        "keywords": "time management, scheduling, prioritization, calendar blocking"
    },
    "solo-founder-strategies/business-systems": {
        "title": "Business Systems for Solo Founders",
        "description": "Build repeatable systems and processes to scale without a team.",
        "keywords": "business systems, processes, automation, scaling"
    },
    "case-studies": {
        "title": "Case Studies",
        "description": "Real stories from solo founders - successes, failures, and lessons learned.",
        "keywords": "case studies, success stories, failure stories, lessons learned"
    },
    "case-studies/failed-experiments": {
        "title": "Failed Experiments",
        "description": "What didn't work and why - honest breakdowns of failed solo founder experiments.",
        "keywords": "failed experiments, lessons learned, what went wrong"
    },
    "case-studies/success-stories": {
        "title": "Success Stories",
        "description": "How solo founders built profitable businesses with AI tools and automation.",
        "keywords": "success stories, case studies, profitable businesses"
    },
    "tutorials": {
        "title": "Tutorials & Guides",
        "description": "Step-by-step guides and tutorials for building with AI tools as a solo founder.",
        "keywords": "tutorials, guides, how-to, step-by-step"
    }
}


class Post:
    """Represents a blog post with metadata"""
    
    def __init__(self, filepath: Path, root: Path):
        self.filepath = filepath
        self.root = root
        self.relative_path = filepath.relative_to(root)
        self.url_path = str(self.relative_path.parent) if self.relative_path.name == "index.html" else str(self.relative_path.with_suffix(''))
        
        # Parse category structure
        parts = self.url_path.split('/')
        if len(parts) >= 2:
            self.category = parts[0]
            self.subcategory = parts[1] if len(parts) >= 2 else None
            self.is_category_hub = self.relative_path.name == "index.html" and len(parts) <= 2
        else:
            self.category = None
            self.subcategory = None
            self.is_category_hub = False
        
        # Extract title from HTML
        self.title = self._extract_title()
        self.soup = None
    
    def _extract_title(self) -> str:
        """Extract title from HTML"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Try h1 first
                h1 = soup.find('h1')
                if h1:
                    return h1.get_text(strip=True)
                
                # Fallback to title tag
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    # Remove site name suffix
                    return title.split('|')[0].strip()
                
                return self.filepath.stem
        except Exception as e:
            print(f"Error extracting title from {self.filepath}: {e}")
            return self.filepath.stem
    
    def get_soup(self) -> BeautifulSoup:
        """Load and cache BeautifulSoup object"""
        if self.soup is None:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.soup = BeautifulSoup(f.read(), 'html.parser')
        return self.soup


def discover_posts(root: Path) -> List[Post]:
    """Discover all HTML posts in a blog directory"""
    posts = []
    for html_file in root.rglob("*.html"):
        if "backup" not in str(html_file):
            post = Post(html_file, root)
            posts.append(post)
    return posts


def generate_breadcrumb_html(category: str, subcategory: str = None, title: str = None) -> str:
    """Generate breadcrumb HTML with schema markup"""
    breadcrumbs = [
        {"name": "Home", "url": "/"},
    ]
    
    # Add category
    if category and category in CATEGORY_INFO:
        breadcrumbs.append({
            "name": CATEGORY_INFO[category]["title"],
            "url": f"/{category}/"
        })
    
    # Add subcategory
    if subcategory:
        cat_path = f"{category}/{subcategory}"
        if cat_path in CATEGORY_INFO:
            breadcrumbs.append({
                "name": CATEGORY_INFO[cat_path]["title"],
                "url": f"/{cat_path}/"
            })
    
    # Add current page (no link)
    if title:
        breadcrumbs.append({"name": title, "url": None})
    
    # Generate HTML
    html_parts = ['<nav aria-label="Breadcrumb" class="breadcrumbs">']
    html_parts.append('  <ol itemscope itemtype="https://schema.org/BreadcrumbList">')
    
    for i, crumb in enumerate(breadcrumbs, 1):
        html_parts.append('    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">')
        if crumb["url"]:
            html_parts.append(f'      <a itemprop="item" href="{crumb["url"]}"><span itemprop="name">{crumb["name"]}</span></a>')
        else:
            html_parts.append(f'      <span itemprop="name">{crumb["name"]}</span>')
        html_parts.append(f'      <meta itemprop="position" content="{i}" />')
        html_parts.append('    </li>')
    
    html_parts.append('  </ol>')
    html_parts.append('</nav>')
    
    return '\n'.join(html_parts)


def generate_breadcrumb_css() -> str:
    """Generate CSS for breadcrumbs"""
    return """
<style>
.breadcrumbs {
    padding: 1rem 0;
    font-size: 0.875rem;
    color: #666;
}
.breadcrumbs ol {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    margin: 0;
    padding: 0;
}
.breadcrumbs li:not(:last-child)::after {
    content: " › ";
    padding: 0 0.5rem;
    color: #999;
}
.breadcrumbs a {
    color: #0066cc;
    text-decoration: none;
}
.breadcrumbs a:hover {
    text-decoration: underline;
}
</style>
"""


def get_related_posts(post: Post, all_posts: List[Post], max_count: int = 5) -> List[Post]:
    """Find related posts using priority algorithm"""
    related = []
    
    # Skip category hubs
    if post.is_category_hub:
        return []
    
    # 1. Same subcategory (max 3)
    if post.subcategory:
        subcategory_posts = [p for p in all_posts 
                             if p.category == post.category 
                             and p.subcategory == post.subcategory 
                             and p.filepath != post.filepath
                             and not p.is_category_hub]
        related.extend(subcategory_posts[:3])
    
    # 2. Same parent category (max 2)
    if len(related) < max_count and post.category:
        category_posts = [p for p in all_posts
                          if p.category == post.category
                          and p.filepath != post.filepath
                          and p not in related
                          and not p.is_category_hub]
        related.extend(category_posts[:2])
    
    # 3. Related categories (cross-linking)
    if len(related) < max_count:
        cat_path = f"{post.category}/{post.subcategory}" if post.subcategory else post.category
        if cat_path in RELATED_CATEGORY_MAP:
            for related_cat in RELATED_CATEGORY_MAP[cat_path]:
                if len(related) >= max_count:
                    break
                
                # Find posts in related category
                related_cat_posts = [p for p in all_posts
                                     if (p.category == related_cat or 
                                         f"{p.category}/{p.subcategory}" == related_cat)
                                     and p not in related
                                     and not p.is_category_hub]
                related.extend(related_cat_posts[:1])
    
    return related[:max_count]


def generate_related_posts_html(related: List[Post]) -> str:
    """Generate HTML for related posts section"""
    if not related:
        return ""
    
    html_parts = ['<section class="related-posts">']
    html_parts.append('  <h2>Related Articles</h2>')
    html_parts.append('  <ul>')
    
    for post in related:
        html_parts.append(f'    <li><a href="/{post.url_path}/">{html_escape(post.title)}</a></li>')
    
    html_parts.append('  </ul>')
    html_parts.append('</section>')
    
    return '\n'.join(html_parts)


def generate_related_posts_css() -> str:
    """Generate CSS for related posts"""
    return """
<style>
.related-posts {
    margin: 3rem 0;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 8px;
}
.related-posts h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #333;
}
.related-posts ul {
    list-style: none;
    padding: 0;
}
.related-posts li {
    margin: 0.75rem 0;
    padding-left: 1.5rem;
    position: relative;
}
.related-posts li::before {
    content: "→";
    position: absolute;
    left: 0;
    color: #0066cc;
}
.related-posts a {
    color: #0066cc;
    text-decoration: none;
    font-weight: 500;
}
.related-posts a:hover {
    text-decoration: underline;
}
</style>
"""


def generate_navigation_html(category: str = None) -> str:
    """Generate site-wide navigation menu"""
    nav_items = [
        ("Home", "/"),
        ("AI Tools", "/ai-tools/"),
        ("Solo Founder", "/solo-founder-strategies/"),
        ("Case Studies", "/case-studies/"),
        ("Tutorials", "/tutorials/"),
    ]
    
    html_parts = ['<nav class="main-nav">']
    html_parts.append('  <div class="nav-container">')
    html_parts.append('    <a href="/" class="nav-logo">Work Less, Build</a>')
    html_parts.append('    <ul class="nav-menu">')
    
    for name, url in nav_items:
        active = ' class="active"' if category and url.strip('/').startswith(category) else ''
        html_parts.append(f'      <li><a href="{url}"{active}>{name}</a></li>')
    
    html_parts.append('    </ul>')
    html_parts.append('  </div>')
    html_parts.append('</nav>')
    
    return '\n'.join(html_parts)


def generate_navigation_css() -> str:
    """Generate CSS for navigation"""
    return """
<style>
.main-nav {
    background: #fff;
    border-bottom: 1px solid #e5e5e5;
    padding: 1rem 0;
    margin-bottom: 2rem;
}
.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.nav-logo {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111;
    text-decoration: none;
}
.nav-menu {
    list-style: none;
    display: flex;
    gap: 2rem;
    margin: 0;
    padding: 0;
}
.nav-menu a {
    color: #666;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}
.nav-menu a:hover,
.nav-menu a.active {
    color: #0066cc;
}
</style>
"""


def add_breadcrumbs_to_post(post: Post):
    """Add breadcrumb navigation to a post"""
    soup = post.get_soup()
    
    # Check if breadcrumbs already exist
    existing = soup.find('nav', class_='breadcrumbs')
    if existing:
        print(f"  ⏭️  Breadcrumbs already exist in {post.relative_path}")
        return False
    
    # Generate breadcrumb HTML
    breadcrumb_html = generate_breadcrumb_html(post.category, post.subcategory, post.title)
    breadcrumb_soup = BeautifulSoup(breadcrumb_html, 'html.parser')
    
    # Find insertion point (after opening body tag)
    body = soup.find('body')
    if not body:
        print(f"  ⚠️  No <body> tag found in {post.relative_path}")
        return False
    
    # Insert breadcrumbs as first child of body
    body.insert(0, breadcrumb_soup)
    
    # Add CSS if not present
    head = soup.find('head')
    if head and not soup.find('style', string=re.compile('breadcrumbs')):
        css_soup = BeautifulSoup(generate_breadcrumb_css(), 'html.parser')
        head.append(css_soup)
    
    # Save
    with open(post.filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  ✅ Added breadcrumbs to {post.relative_path}")
    return True


def add_related_posts_to_post(post: Post, all_posts: List[Post]):
    """Add related posts section to a post"""
    soup = post.get_soup()
    
    # Check if related posts already exist
    existing = soup.find('section', class_='related-posts')
    if existing:
        print(f"  ⏭️  Related posts already exist in {post.relative_path}")
        return False
    
    # Get related posts
    related = get_related_posts(post, all_posts)
    if not related:
        print(f"  ⚠️  No related posts found for {post.relative_path}")
        return False
    
    # Generate related posts HTML
    related_html = generate_related_posts_html(related)
    related_soup = BeautifulSoup(related_html, 'html.parser')
    
    # Find insertion point (before closing body tag, or end of main/article)
    insertion_point = soup.find('main') or soup.find('article') or soup.find('body')
    if not insertion_point:
        print(f"  ⚠️  No insertion point found in {post.relative_path}")
        return False
    
    # Append related posts
    insertion_point.append(related_soup)
    
    # Add CSS if not present
    head = soup.find('head')
    if head and not soup.find('style', string=re.compile('related-posts')):
        css_soup = BeautifulSoup(generate_related_posts_css(), 'html.parser')
        head.append(css_soup)
    
    # Save
    with open(post.filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  ✅ Added {len(related)} related posts to {post.relative_path}")
    return True


def add_navigation_to_post(post: Post):
    """Add site-wide navigation to a post"""
    soup = post.get_soup()
    
    # Check if navigation already exists
    existing = soup.find('nav', class_='main-nav')
    if existing:
        print(f"  ⏭️  Navigation already exists in {post.relative_path}")
        return False
    
    # Generate navigation HTML
    nav_html = generate_navigation_html(post.category)
    nav_soup = BeautifulSoup(nav_html, 'html.parser')
    
    # Find insertion point (as first child of body)
    body = soup.find('body')
    if not body:
        print(f"  ⚠️  No <body> tag found in {post.relative_path}")
        return False
    
    # Insert navigation as first child
    body.insert(0, nav_soup)
    
    # Add CSS if not present
    head = soup.find('head')
    if head and not soup.find('style', string=re.compile('main-nav')):
        css_soup = BeautifulSoup(generate_navigation_css(), 'html.parser')
        head.append(css_soup)
    
    # Save
    with open(post.filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  ✅ Added navigation to {post.relative_path}")
    return True


def create_category_hub(root: Path, category_path: str):
    """Create a category hub page"""
    category_parts = category_path.split('/')
    category = category_parts[0]
    subcategory = category_parts[1] if len(category_parts) > 1 else None
    
    # Get category info
    info = CATEGORY_INFO.get(category_path, {
        "title": category_path.replace('-', ' ').title(),
        "description": f"Articles about {category_path}",
        "keywords": category_path.replace('/', ', ')
    })
    
    # Create directory
    hub_dir = root / category_path
    hub_dir.mkdir(parents=True, exist_ok=True)
    hub_file = hub_dir / "index.html"
    
    # Skip if already exists
    if hub_file.exists():
        print(f"  ⏭️  Hub already exists: {category_path}/index.html")
        return False
    
    # Find posts in this category
    posts = discover_posts(root)
    category_posts = [p for p in posts 
                      if p.category == category 
                      and (subcategory is None or p.subcategory == subcategory)
                      and not p.is_category_hub]
    
    # Find subcategories
    subcategories = set()
    if not subcategory:  # Top-level category
        for p in posts:
            if p.category == category and p.subcategory:
                subcategories.add(p.subcategory)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{info['title']} - Work Less, Build</title>
    <meta name="description" content="{info['description']}">
    <meta name="keywords" content="{info['keywords']}">
    <link rel="canonical" href="{SITE_DOMAIN}/{category_path}/">
    
    <!-- Schema.org Article markup -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "headline": "{info['title']}",
      "description": "{info['description']}",
      "url": "{SITE_DOMAIN}/{category_path}/",
      "isPartOf": {{
        "@type": "WebSite",
        "name": "Work Less, Build",
        "url": "{SITE_DOMAIN}"
      }}
    }}
    </script>
    
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{SITE_DOMAIN}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{info['title']}",
          "item": "{SITE_DOMAIN}/{category_path}/"
        }}
      ]
    }}
    </script>
</head>
<body>
    {generate_navigation_html(category)}
    {generate_breadcrumb_html(category, subcategory)}
    
    <main style="max-width: 1200px; margin: 0 auto; padding: 2rem;">
      <h1>{info['title']}</h1>
      <p class="lead" style="font-size: 1.25rem; color: #666; margin: 1rem 0 2rem;">{info['description']}</p>
      
      {generate_subcategories_html(subcategories, category) if subcategories else ""}
      
      <section class="articles">
        <h2>Articles</h2>
        <ul style="list-style: none; padding: 0;">
"""
    
    for post in category_posts[:50]:  # Limit to 50 posts
        html += f'          <li style="margin: 1rem 0;"><a href="/{post.url_path}/" style="color: #0066cc; text-decoration: none; font-weight: 500;">{html_escape(post.title)}</a></li>\n'
    
    html += """        </ul>
      </section>
    </main>
    
    {navigation_css}
    {breadcrumb_css}
</body>
</html>""".format(
        navigation_css=generate_navigation_css(),
        breadcrumb_css=generate_breadcrumb_css()
    )
    
    # Write file
    with open(hub_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✅ Created category hub: {category_path}/index.html ({len(category_posts)} posts)")
    return True


def generate_subcategories_html(subcategories: Set[str], parent_category: str) -> str:
    """Generate HTML for subcategories section"""
    if not subcategories:
        return ""
    
    html = '<section class="subcategories" style="margin: 2rem 0;">\n'
    html += '  <h2>Browse by Topic</h2>\n'
    html += '  <ul style="list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem;">\n'
    
    for subcat in sorted(subcategories):
        cat_path = f"{parent_category}/{subcat}"
        info = CATEGORY_INFO.get(cat_path, {
            "title": subcat.replace('-', ' ').title(),
            "description": ""
        })
        html += f'    <li style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">\n'
        html += f'      <a href="/{cat_path}/" style="color: #0066cc; text-decoration: none; font-weight: 600;">{info["title"]}</a>\n'
        if info.get("description"):
            html += f'      <p style="margin: 0.5rem 0 0; font-size: 0.875rem; color: #666;">{info["description"]}</p>\n'
        html += '    </li>\n'
    
    html += '  </ul>\n'
    html += '</section>\n'
    return html


def main():
    """Main execution"""
    print("=" * 70)
    print("WEEK 2: Content Structure & Internal Linking Implementation")
    print("=" * 70)
    
    # Process AI Blog
    print("\n📁 AI AUTOMATION BLOG")
    print("-" * 70)
    
    if AI_BLOG_ROOT.exists():
        ai_posts = discover_posts(AI_BLOG_ROOT)
        print(f"Found {len(ai_posts)} posts\n")
        
        # Task 1: Create category hubs
        print("Task 1: Creating category hub pages...")
        hubs_created = 0
        for cat_path in CATEGORY_INFO.keys():
            if create_category_hub(AI_BLOG_ROOT, cat_path):
                hubs_created += 1
        print(f"✅ Created {hubs_created} category hubs\n")
        
        # Refresh post list (includes new hubs)
        ai_posts = discover_posts(AI_BLOG_ROOT)
        
        # Task 2 & 7: Add breadcrumbs and navigation
        print("Task 2 & 7: Adding breadcrumbs and navigation...")
        breadcrumbs_added = 0
        navigation_added = 0
        for post in ai_posts:
            if add_breadcrumbs_to_post(post):
                breadcrumbs_added += 1
            if add_navigation_to_post(post):
                navigation_added += 1
        print(f"✅ Added breadcrumbs to {breadcrumbs_added} posts")
        print(f"✅ Added navigation to {navigation_added} posts\n")
        
        # Task 3: Add related posts
        print("Task 3: Adding related posts...")
        related_added = 0
        for post in ai_posts:
            if not post.is_category_hub:
                if add_related_posts_to_post(post, ai_posts):
                    related_added += 1
        print(f"✅ Added related posts to {related_added} posts\n")
    else:
        print(f"⚠️  AI Blog root not found: {AI_BLOG_ROOT}\n")
    
    # CleverDog blog (flat structure - skip for now)
    print("\n📁 CLEVERDOG METHOD BLOG")
    print("-" * 70)
    if DOG_BLOG_ROOT.exists():
        print("⚠️  CleverDog blog has flat structure - skipping for now")
        print("   (Run categorization script first)\n")
    else:
        print(f"⚠️  CleverDog blog root not found: {DOG_BLOG_ROOT}\n")
    
    print("=" * 70)
    print("✅ WEEK 2 IMPLEMENTATION COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Task 4: Add contextual internal links (requires keyword mapping)")
    print("2. Task 5: Update generator scripts to include new features")
    print("3. Task 6: Enhanced schema markup (most posts already have it)")
    print("4. Verification: Check 5+ internal links per post")


if __name__ == "__main__":
    main()
