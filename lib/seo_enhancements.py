#!/usr/bin/env python3
"""
SEO Enhancements Library - Week 2 Internal Linking
Import this into blog generator scripts to automatically add:
- Breadcrumb navigation
- Related posts
- Contextual internal links
- Site-wide navigation

Usage:
    from lib.seo_enhancements import enhance_post_html
    
    enhanced_html = enhance_post_html(
        html_content=post_html,
        category="ai-tools",
        subcategory="llms",
        title="My Post Title",
        all_posts_metadata=posts_list  # optional
    )
"""

from typing import List, Dict, Optional
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Category metadata
CATEGORY_INFO = {
    "ai-tools": {
        "title": "AI Tools & Platforms",
        "description": "AI tools for solo founders",
    },
    "ai-tools/llms": {
        "title": "Large Language Models",
        "description": "ChatGPT, Claude, and other LLMs",
    },
    "ai-tools/no-code-ai": {
        "title": "No-Code AI Tools",
        "description": "Build AI apps without coding",
    },
    "ai-tools/automation-platforms": {
        "title": "AI Automation Platforms",
        "description": "Workflow automation tools",
    },
    "ai-tools/image-generation": {
        "title": "AI Image Generation",
        "description": "DALL-E, Midjourney, Stable Diffusion",
    },
    "solo-founder-strategies": {
        "title": "Solo Founder Strategies",
        "description": "Build and scale as a solopreneur",
    },
    "solo-founder-strategies/productivity": {
        "title": "Productivity",
        "description": "Time management and focus techniques",
    },
    "solo-founder-strategies/time-management": {
        "title": "Time Management",
        "description": "Master your schedule",
    },
    "solo-founder-strategies/business-systems": {
        "title": "Business Systems",
        "description": "Scalable processes",
    },
    "case-studies": {
        "title": "Case Studies",
        "description": "Real solo founder stories",
    },
    "case-studies/failed-experiments": {
        "title": "Failed Experiments",
        "description": "What didn't work and why",
    },
    "case-studies/success-stories": {
        "title": "Success Stories",
        "description": "Profitable solo businesses",
    },
    "tutorials": {
        "title": "Tutorials & Guides",
        "description": "Step-by-step guides",
    }
}

# Keyword to URL mapping for contextual links
CONTEXTUAL_KEYWORDS = {
    "chatgpt": "/ai-tools/llms/",
    "claude": "/ai-tools/llms/",
    "gpt-4": "/ai-tools/llms/",
    "language models": "/ai-tools/llms/",
    "automation": "/ai-tools/automation-platforms/",
    "workflow automation": "/ai-tools/automation-platforms/",
    "zapier": "/ai-tools/automation-platforms/",
    "no-code ai": "/ai-tools/no-code-ai/",
    "dall-e": "/ai-tools/image-generation/",
    "midjourney": "/ai-tools/image-generation/",
    "stable diffusion": "/ai-tools/image-generation/",
    "solo founder": "/solo-founder-strategies/",
    "solopreneur": "/solo-founder-strategies/",
    "productivity": "/solo-founder-strategies/productivity/",
    "time management": "/solo-founder-strategies/time-management/",
    "business systems": "/solo-founder-strategies/business-systems/",
    "case study": "/case-studies/",
    "tutorial": "/tutorials/",
    "guide": "/tutorials/",
}


def generate_breadcrumb_html(category: str, subcategory: Optional[str] = None, title: Optional[str] = None) -> str:
    """Generate breadcrumb HTML with schema markup"""
    breadcrumbs = [{"name": "Home", "url": "/"}]
    
    if category and category in CATEGORY_INFO:
        breadcrumbs.append({
            "name": CATEGORY_INFO[category]["title"],
            "url": f"/{category}/"
        })
    
    if subcategory:
        cat_path = f"{category}/{subcategory}"
        if cat_path in CATEGORY_INFO:
            breadcrumbs.append({
                "name": CATEGORY_INFO[cat_path]["title"],
                "url": f"/{cat_path}/"
            })
    
    if title:
        breadcrumbs.append({"name": title, "url": None})
    
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


def generate_navigation_html(category: Optional[str] = None) -> str:
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


def generate_related_posts_html(related: List[Dict[str, str]]) -> str:
    """
    Generate HTML for related posts section
    
    Args:
        related: List of dicts with 'title' and 'url' keys
    """
    if not related:
        return ""
    
    html_parts = ['<section class="related-posts">']
    html_parts.append('  <h2>Related Articles</h2>')
    html_parts.append('  <ul>')
    
    for post in related:
        title = post.get('title', 'Untitled')
        url = post.get('url', '#')
        html_parts.append(f'    <li><a href="{url}">{title}</a></li>')
    
    html_parts.append('  </ul>')
    html_parts.append('</section>')
    
    return '\n'.join(html_parts)


def add_contextual_links(html_content: str, current_url: str, max_links: int = 3) -> str:
    """
    Add contextual internal links to HTML content
    
    Args:
        html_content: The HTML to enhance
        current_url: URL of current post (to avoid self-links)
        max_links: Maximum number of contextual links to add
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find main content
    main = soup.find('main') or soup.find('article') or soup.find('div', class_='article-content')
    if not main:
        return html_content
    
    paragraphs = main.find_all(['p', 'li'])
    links_added = 0
    linked_urls = set()
    
    # Sort keywords by length (longer = more specific)
    sorted_keywords = sorted(CONTEXTUAL_KEYWORDS.keys(), key=len, reverse=True)
    
    for p in paragraphs:
        if links_added >= max_links:
            break
        
        if p.find('a'):  # Skip if already has links
            continue
        
        text = p.get_text()
        text_lower = text.lower()
        
        for keyword in sorted_keywords:
            if links_added >= max_links:
                break
            
            target_url = CONTEXTUAL_KEYWORDS[keyword]
            
            if target_url == current_url or target_url in linked_urls:
                continue
            
            if keyword in text_lower:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                match = pattern.search(text)
                
                if match:
                    matched_text = match.group(0)
                    new_html = pattern.sub(f'<a href="{target_url}">{matched_text}</a>', str(p), count=1)
                    new_soup = BeautifulSoup(new_html, 'html.parser')
                    p.replace_with(new_soup)
                    
                    links_added += 1
                    linked_urls.add(target_url)
                    break
    
    return str(soup)


def generate_styles() -> str:
    """Generate CSS for navigation, breadcrumbs, and related posts"""
    return """
<style>
/* Navigation */
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

/* Breadcrumbs */
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

/* Related Posts */
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


def enhance_post_html(
    html_content: str,
    category: str,
    subcategory: Optional[str] = None,
    title: Optional[str] = None,
    url_path: Optional[str] = None,
    related_posts: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Enhance post HTML with all Week 2 SEO features
    
    Args:
        html_content: Original HTML content
        category: Post category (e.g., "ai-tools")
        subcategory: Post subcategory (e.g., "llms")
        title: Post title
        url_path: Current post URL path (for avoiding self-links)
        related_posts: List of related posts [{"title": "...", "url": "..."}]
    
    Returns:
        Enhanced HTML with navigation, breadcrumbs, related posts, and contextual links
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Add navigation as first child of body
    nav_html = generate_navigation_html(category)
    nav_soup = BeautifulSoup(nav_html, 'html.parser')
    body = soup.find('body')
    if body:
        nav_node = nav_soup.find('nav')
        if nav_node:
            body.insert(0, nav_node)
    
    # 2. Add breadcrumbs after navigation
    breadcrumb_html = generate_breadcrumb_html(category, subcategory, title)
    breadcrumb_soup = BeautifulSoup(breadcrumb_html, 'html.parser')
    breadcrumb_node = breadcrumb_soup.find('nav')
    if body and breadcrumb_node:
        # Insert after first element (navigation)
        body.insert(1, breadcrumb_node)
    
    # 3. Add related posts before closing body
    if related_posts:
        related_html = generate_related_posts_html(related_posts)
        related_soup = BeautifulSoup(related_html, 'html.parser')
        main = soup.find('main') or soup.find('article') or body
        if main:
            main.append(related_soup)
    
    # 4. Add CSS to head
    head = soup.find('head')
    if head:
        style_soup = BeautifulSoup(generate_styles(), 'html.parser')
        head.append(style_soup)
    
    # 5. Add contextual links
    current_url = url_path or f"/{category}/{subcategory}/" if subcategory else f"/{category}/"
    enhanced = add_contextual_links(str(soup), current_url, max_links=3)
    
    return enhanced


def categorize_dog_training_post(keyword: str, content: str = "") -> tuple:
    """
    Auto-categorize dog training post based on keywords
    Returns: (category, subcategory) for CleverDogMethod blog
    """
    keyword_lower = keyword.lower()
    content_lower = content.lower()
    combined = f"{keyword_lower} {content_lower}"
    
    # Puppy training
    if any(kw in combined for kw in ['puppy', 'puppies', 'young dog', 'new dog']):
        return ('training', 'puppy-training')
    # Behavior issues
    elif any(kw in combined for kw in ['barking', 'aggression', 'biting', 'jumping', 'reactive', 'anxiety', 'separation']):
        return ('training', 'behavior-issues')
    # Obedience
    elif any(kw in combined for kw in ['sit', 'stay', 'come', 'heel', 'commands', 'obedience']):
        return ('training', 'obedience')
    # Advanced training
    elif any(kw in combined for kw in ['tricks', 'advanced', 'agility', 'service dog']):
        return ('training', 'advanced')
    # Default
    else:
        return ('training', 'general')


def categorize_post(topic: str, content: str = "") -> tuple:
    """
    Auto-categorize post based on keywords in topic/content
    Returns: (category, subcategory)
    """
    topic_lower = topic.lower()
    content_lower = content.lower()
    combined = f"{topic_lower} {content_lower}"
    
    # AI Tools detection
    if any(kw in combined for kw in ['chatgpt', 'claude', 'gpt-4', 'llm', 'language model']):
        return ('ai-tools', 'llms')
    elif any(kw in combined for kw in ['no-code', 'zapier', 'make.com', 'bubble']):
        return ('ai-tools', 'no-code-ai')
    elif any(kw in combined for kw in ['automation', 'workflow', 'integration']):
        return ('ai-tools', 'automation-platforms')
    elif any(kw in combined for kw in ['dall-e', 'midjourney', 'stable diffusion', 'image generation']):
        return ('ai-tools', 'image-generation')
    elif any(kw in combined for kw in ['ai tool', 'ai platform', 'artificial intelligence']):
        return ('ai-tools', None)
    
    # Solo Founder Strategies
    elif any(kw in combined for kw in ['productivity', 'focus', 'time block', 'pomodoro']):
        return ('solo-founder-strategies', 'productivity')
    elif any(kw in combined for kw in ['time management', 'calendar', 'schedule']):
        return ('solo-founder-strategies', 'time-management')
    elif any(kw in combined for kw in ['system', 'process', 'sop', 'standard operating']):
        return ('solo-founder-strategies', 'business-systems')
    elif any(kw in combined for kw in ['solo founder', 'solopreneur', 'indie hacker']):
        return ('solo-founder-strategies', None)
    
    # Case Studies
    elif any(kw in combined for kw in ['failed', 'mistake', 'lesson learned', 'what went wrong']):
        return ('case-studies', 'failed-experiments')
    elif any(kw in combined for kw in ['success', 'profitable', 'revenue', 'mrr', 'case study']):
        return ('case-studies', 'success-stories')
    elif 'case study' in combined:
        return ('case-studies', None)
    
    # Tutorials
    elif any(kw in combined for kw in ['tutorial', 'guide', 'how to', 'step by step']):
        return ('tutorials', None)
    
    # Default fallback
    return ('tutorials', None)


def generate_meta_tags(title: str, description: str, canonical_url: str, 
                       image_url: str = None, site_name: str = "Work Less, Build", 
                       article_date: str = None) -> str:
    """
    Generate comprehensive meta tags including Open Graph, Twitter Cards, and favicon
    
    Args:
        title: Page title
        description: Meta description (150-160 chars recommended)
        canonical_url: Canonical URL of the page
        image_url: Featured image URL
        site_name: Site name for Open Graph
        article_date: Publication date in ISO format
    """
    from datetime import datetime
    
    if not image_url:
        image_url = f"https://{canonical_url.split('/')[2]}/images/og-default.jpg"
    
    if not article_date:
        article_date = datetime.now().isoformat()
    
    meta_html = f"""
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    
    <!-- Meta Tags -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="googlebot" content="index, follow">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="{site_name}">
    <meta property="og:image" content="{image_url}">
    <meta property="article:published_time" content="{article_date}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    
    <!-- Canonical -->
    <link rel="canonical" href="{canonical_url}">
"""
    
    return meta_html


# Convenience function for generator scripts
def get_related_posts_for_category(category: str, subcategory: Optional[str] = None, limit: int = 5) -> List[Dict[str, str]]:
    """
    Get related posts based on category (stub - implement with actual post discovery)
    Generator scripts can override this with their own post database
    """
    # This is a placeholder - actual implementation should query the post database
    return []
