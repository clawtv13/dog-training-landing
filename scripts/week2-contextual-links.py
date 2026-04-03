#!/usr/bin/env python3
"""
WEEK 2 Task 4: Add Contextual Internal Links
Automatically adds 2-3 contextual links per post based on keyword matching
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
from bs4 import BeautifulSoup, NavigableString

AI_BLOG_ROOT = Path("/root/.openclaw/workspace/ai-automation-blog/blog-new")

# Keyword mapping: keyword -> target URL
# Build this from existing posts and high-value pages
KEYWORD_MAP = {
    # AI Tools & LLMs
    "chatgpt": "/ai-tools/llms/",
    "gpt-4": "/ai-tools/llms/",
    "claude": "/ai-tools/llms/",
    "language models": "/ai-tools/llms/",
    "llms": "/ai-tools/llms/",
    "large language model": "/ai-tools/llms/",
    
    # No-code AI
    "no-code ai": "/ai-tools/no-code-ai/",
    "no code": "/ai-tools/no-code-ai/",
    "visual builder": "/ai-tools/no-code-ai/",
    
    # Automation
    "automation": "/ai-tools/automation-platforms/",
    "workflow automation": "/ai-tools/automation-platforms/",
    "zapier": "/ai-tools/automation-platforms/",
    "make.com": "/ai-tools/automation-platforms/",
    "n8n": "/ai-tools/automation-platforms/",
    "automate workflows": "/ai-tools/automation-platforms/",
    
    # Image Generation
    "dall-e": "/ai-tools/image-generation/",
    "midjourney": "/ai-tools/image-generation/",
    "stable diffusion": "/ai-tools/image-generation/",
    "ai image": "/ai-tools/image-generation/",
    "ai art": "/ai-tools/image-generation/",
    "image generation": "/ai-tools/image-generation/",
    
    # Solo Founder
    "solo founder": "/solo-founder-strategies/",
    "solopreneur": "/solo-founder-strategies/",
    "indie hacker": "/solo-founder-strategies/",
    "one-person business": "/solo-founder-strategies/",
    
    # Productivity
    "productivity": "/solo-founder-strategies/productivity/",
    "time management": "/solo-founder-strategies/time-management/",
    "deep work": "/solo-founder-strategies/productivity/",
    "focus": "/solo-founder-strategies/productivity/",
    
    # Business Systems
    "business systems": "/solo-founder-strategies/business-systems/",
    "systems thinking": "/solo-founder-strategies/business-systems/",
    "processes": "/solo-founder-strategies/business-systems/",
    "scale without team": "/solo-founder-strategies/business-systems/",
    
    # Case Studies
    "case study": "/case-studies/",
    "case studies": "/case-studies/",
    "success story": "/case-studies/success-stories/",
    "failure": "/case-studies/failed-experiments/",
    "lessons learned": "/case-studies/failed-experiments/",
    
    # Tutorials
    "tutorial": "/tutorials/",
    "guide": "/tutorials/",
    "how to": "/tutorials/",
    "step-by-step": "/tutorials/",
}


def build_post_keyword_map(root: Path) -> Dict[str, str]:
    """Build keyword map from existing post titles and paths"""
    keyword_map = {}
    
    for html_file in root.rglob("*.html"):
        if "backup" in str(html_file) or html_file.name != "index.html":
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True).lower()
                    url_path = str(html_file.relative_to(root).parent)
                    
                    # Add title phrases as keywords
                    if len(title) > 10:  # Avoid short titles
                        keyword_map[title] = f"/{url_path}/"
                    
                    # Extract key phrases (3-5 words)
                    words = title.split()
                    if len(words) >= 3:
                        for i in range(len(words) - 2):
                            phrase = ' '.join(words[i:i+3])
                            if len(phrase) > 15:  # Meaningful phrases
                                keyword_map[phrase] = f"/{url_path}/"
        except Exception as e:
            continue
    
    return keyword_map


def add_contextual_links_to_html(html_content: str, current_url: str, keyword_map: Dict[str, str], max_links: int = 3) -> str:
    """Add contextual internal links to HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find main content area
    main = soup.find('main') or soup.find('article') or soup.find('div', class_='article-content')
    if not main:
        return html_content
    
    # Find all text paragraphs (skip headers, navigation, etc.)
    paragraphs = main.find_all(['p', 'li'])
    
    links_added = 0
    linked_urls = set()
    
    # Sort keywords by length (longer = more specific)
    sorted_keywords = sorted(keyword_map.keys(), key=len, reverse=True)
    
    for p in paragraphs:
        if links_added >= max_links:
            break
        
        # Skip if paragraph already has links
        if p.find('a'):
            continue
        
        # Get paragraph text
        text = p.get_text()
        text_lower = text.lower()
        
        # Try to find matching keywords
        for keyword in sorted_keywords:
            if links_added >= max_links:
                break
            
            target_url = keyword_map[keyword]
            
            # Skip self-links and already-linked URLs
            if target_url == current_url or target_url in linked_urls:
                continue
            
            # Check if keyword exists in text
            if keyword in text_lower:
                # Find the actual occurrence (case-insensitive)
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                match = pattern.search(text)
                
                if match:
                    # Get the matched text with original case
                    matched_text = match.group(0)
                    
                    # Replace only first occurrence
                    new_html = pattern.sub(f'<a href="{target_url}">{matched_text}</a>', str(p), count=1)
                    new_soup = BeautifulSoup(new_html, 'html.parser')
                    p.replace_with(new_soup)
                    
                    links_added += 1
                    linked_urls.add(target_url)
                    print(f"    🔗 Linked '{matched_text}' -> {target_url}")
                    break  # Move to next paragraph
    
    return str(soup)


def process_post(filepath: Path, root: Path, keyword_map: Dict[str, str]):
    """Add contextual links to a single post"""
    relative_path = filepath.relative_to(root)
    print(f"\n  Processing: {relative_path}")
    
    # Get current URL
    url_path = str(relative_path.parent) if relative_path.name == "index.html" else str(relative_path.with_suffix(''))
    current_url = f"/{url_path}/"
    
    # Read HTML
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Skip category hubs
    if "CollectionPage" in html_content or "<h2>Articles</h2>" in html_content:
        print("    ⏭️  Skipping category hub")
        return
    
    # Add contextual links
    modified_html = add_contextual_links_to_html(html_content, current_url, keyword_map, max_links=3)
    
    # Save if changed
    if modified_html != html_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_html)
        print("    ✅ Contextual links added")
    else:
        print("    ⏭️  No suitable keywords found")


def main():
    """Main execution"""
    print("=" * 70)
    print("WEEK 2 Task 4: Adding Contextual Internal Links")
    print("=" * 70)
    
    if not AI_BLOG_ROOT.exists():
        print(f"⚠️  Blog root not found: {AI_BLOG_ROOT}")
        return
    
    # Build keyword map
    print("\n📝 Building keyword map from posts...")
    post_keywords = build_post_keyword_map(AI_BLOG_ROOT)
    print(f"   Found {len(post_keywords)} post-based keywords")
    
    # Merge with manual keyword map
    all_keywords = {**KEYWORD_MAP, **post_keywords}
    print(f"   Total keywords: {len(all_keywords)}")
    
    # Process all posts
    print("\n🔗 Adding contextual links to posts...")
    html_files = list(AI_BLOG_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if "backup" not in str(f)]
    
    for html_file in html_files:
        try:
            process_post(html_file, AI_BLOG_ROOT, all_keywords)
        except Exception as e:
            print(f"    ⚠️  Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Contextual linking complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
