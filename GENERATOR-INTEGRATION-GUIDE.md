# Generator Script Integration Guide
**How to add Week 2 SEO features to blog generators**

---

## Quick Start (3 steps)

### 1. Import the library
```python
from lib.seo_enhancements import enhance_post_html
```

### 2. Classify your topic into category/subcategory
```python
category = "ai-tools"
subcategory = "llms"  # or None
```

### 3. Enhance HTML before saving
```python
enhanced_html = enhance_post_html(
    html_content=post_html,
    category=category,
    subcategory=subcategory,
    title="My Post Title",
    url_path=f"/{category}/{subcategory}/my-post/" if subcategory else f"/{category}/my-post/",
    related_posts=[
        {"title": "Related Post 1", "url": "/category/post1/"},
        {"title": "Related Post 2", "url": "/category/post2/"},
    ]
)
```

That's it! The function adds:
- ✅ Site-wide navigation
- ✅ Breadcrumb navigation (with schema)
- ✅ Related posts section
- ✅ Contextual internal links (2-3)
- ✅ All necessary CSS

---

## Full Integration Example

### For `blog-auto-post-v2.py`:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
from lib.seo_enhancements import enhance_post_html

# Add your existing imports...

# ============================================================================
# CATEGORY CLASSIFICATION
# ============================================================================

def classify_topic(topic: str, content: str = "") -> tuple:
    """
    Classify topic into (category, subcategory)
    Returns: (str, str | None)
    """
    topic_lower = (topic + " " + content).lower()
    
    # AI Tools - LLMs
    if any(k in topic_lower for k in ['chatgpt', 'claude', 'gpt-4', 'llm', 'language model', 'openai']):
        return ('ai-tools', 'llms')
    
    # AI Tools - No-Code
    elif any(k in topic_lower for k in ['no-code', 'visual builder', 'low-code', 'bubble', 'webflow']):
        return ('ai-tools', 'no-code-ai')
    
    # AI Tools - Automation
    elif any(k in topic_lower for k in ['automation', 'zapier', 'workflow', 'n8n', 'make.com']):
        return ('ai-tools', 'automation-platforms')
    
    # AI Tools - Image Generation
    elif any(k in topic_lower for k in ['dall-e', 'midjourney', 'stable diffusion', 'ai art', 'image generation']):
        return ('ai-tools', 'image-generation')
    
    # Solo Founder - Productivity
    elif any(k in topic_lower for k in ['productivity', 'focus', 'deep work', 'pomodoro', 'time blocking']):
        return ('solo-founder-strategies', 'productivity')
    
    # Solo Founder - Time Management
    elif any(k in topic_lower for k in ['time management', 'scheduling', 'calendar', 'prioritization']):
        return ('solo-founder-strategies', 'time-management')
    
    # Solo Founder - Business Systems
    elif any(k in topic_lower for k in ['systems', 'process', 'sop', 'documentation', 'scale without team']):
        return ('solo-founder-strategies', 'business-systems')
    
    # Case Studies - Success Stories
    elif any(k in topic_lower for k in ['success', 'profitable', 'launched', 'built', 'case study']) and 'fail' not in topic_lower:
        return ('case-studies', 'success-stories')
    
    # Case Studies - Failed Experiments
    elif any(k in topic_lower for k in ['failed', 'failure', 'mistake', 'wrong', 'lesson learned']):
        return ('case-studies', 'failed-experiments')
    
    # Tutorials
    elif any(k in topic_lower for k in ['tutorial', 'guide', 'how to', 'step-by-step', 'walkthrough']):
        return ('tutorials', None)
    
    # Default fallback
    else:
        return ('ai-tools', None)


# ============================================================================
# RELATED POSTS HELPER
# ============================================================================

def get_related_posts(category: str, subcategory: str = None, limit: int = 5) -> list:
    """
    Get related posts from your database/file system
    
    Returns: [{"title": "...", "url": "..."}, ...]
    """
    related = []
    
    # Option 1: Query from database
    if ANALYTICS_DB and ANALYTICS_DB.exists():
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        # Same subcategory first
        if subcategory:
            cursor.execute("""
                SELECT title, url_path FROM posts 
                WHERE category = ? AND subcategory = ?
                ORDER BY published_date DESC LIMIT 3
            """, (category, subcategory))
            related.extend([{"title": r[0], "url": r[1]} for r in cursor.fetchall()])
        
        # Then same category
        if len(related) < limit:
            cursor.execute("""
                SELECT title, url_path FROM posts 
                WHERE category = ? AND subcategory IS NULL OR subcategory != ?
                ORDER BY published_date DESC LIMIT ?
            """, (category, subcategory or "", limit - len(related)))
            related.extend([{"title": r[0], "url": r[1]} for r in cursor.fetchall()])
        
        conn.close()
    
    # Option 2: Discover from file system
    else:
        from pathlib import Path
        import re
        
        blog_root = Path(BLOG_DIR) / "blog-new"
        
        # Find posts in same category
        category_dir = blog_root / category / (subcategory or "")
        if category_dir.exists():
            for html_file in category_dir.rglob("index.html"):
                if len(related) >= limit:
                    break
                
                # Extract title from HTML
                with open(html_file) as f:
                    match = re.search(r'<h1[^>]*>(.*?)</h1>', f.read())
                    if match:
                        title = match.group(1)
                        url = str(html_file.relative_to(blog_root).parent)
                        related.append({"title": title, "url": f"/{url}/"})
    
    return related[:limit]


# ============================================================================
# MODIFIED GENERATION FUNCTION
# ============================================================================

def generate_and_publish_post(topic: str):
    """Generate post with SEO enhancements"""
    
    # 1. Generate post HTML (your existing logic)
    post_html = generate_post_content(topic)  # Your function
    post_title = extract_title(post_html)
    slug = slugify(post_title)
    
    # 2. Classify into category/subcategory
    category, subcategory = classify_topic(topic, post_html)
    logger.info(f"Classified as: {category}/{subcategory or 'root'}")
    
    # 3. Get related posts
    related_posts = get_related_posts(category, subcategory, limit=5)
    logger.info(f"Found {len(related_posts)} related posts")
    
    # 4. Build URL path
    if subcategory:
        url_path = f"/{category}/{subcategory}/{slug}/"
        output_dir = BLOG_DIR / "blog-new" / category / subcategory / slug
    else:
        url_path = f"/{category}/{slug}/"
        output_dir = BLOG_DIR / "blog-new" / category / slug
    
    # 5. Enhance with SEO features
    enhanced_html = enhance_post_html(
        html_content=post_html,
        category=category,
        subcategory=subcategory,
        title=post_title,
        url_path=url_path,
        related_posts=related_posts
    )
    
    # 6. Save to categorized path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"
    output_file.write_text(enhanced_html)
    
    logger.info(f"✅ Post saved to: {output_file}")
    logger.info(f"   URL: {url_path}")
    
    # 7. Your existing logic (git commit, analytics, etc.)
    # ...
    
    return output_file


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else get_topic_from_queue()
    generate_and_publish_post(topic)
```

---

## Category Definitions

### AI Automation Blog

```
ai-tools/
├── llms/              # ChatGPT, Claude, GPT-4, language models
├── no-code-ai/        # Visual builders, Bubble, no-code platforms
├── automation-platforms/  # Zapier, Make, n8n, workflow automation
└── image-generation/  # DALL-E, Midjourney, Stable Diffusion

solo-founder-strategies/
├── productivity/      # Focus, deep work, time blocking
├── time-management/   # Scheduling, calendars, prioritization
└── business-systems/  # SOPs, processes, scaling

case-studies/
├── success-stories/   # Profitable launches, wins
└── failed-experiments/  # Lessons learned, mistakes

tutorials/             # How-to guides, step-by-step
```

---

## Testing Your Integration

### 1. Generate a test post
```bash
python3 scripts/blog-auto-post-v2.py "How to use ChatGPT for automation"
```

### 2. Check the output
```bash
# Find the generated file
find blog-new/ -name "index.html" -mtime -1

# Verify it has all features
grep -c "breadcrumbs" blog-new/ai-tools/llms/how-to-use-chatgpt-for-automation/index.html
grep -c "related-posts" blog-new/ai-tools/llms/how-to-use-chatgpt-for-automation/index.html
grep -c "main-nav" blog-new/ai-tools/llms/how-to-use-chatgpt-for-automation/index.html
```

### 3. Count internal links
```python
python3 << 'EOF'
from bs4 import BeautifulSoup

file = "blog-new/ai-tools/llms/how-to-use-chatgpt-for-automation/index.html"
with open(file) as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

internal_links = len([a for a in soup.find_all('a') if a.get('href', '').startswith('/')])
print(f"Internal links: {internal_links}")
print("✅ PASS" if internal_links >= 5 else "❌ FAIL")
EOF
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'lib.seo_enhancements'"

**Solution:** Make sure `lib/` is in Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from seo_enhancements import enhance_post_html
```

### "No related posts found"

**Solution:** Related posts are optional. The function works fine without them:
```python
enhanced_html = enhance_post_html(
    html_content=post_html,
    category=category,
    subcategory=subcategory,
    title=title,
    url_path=url_path,
    related_posts=None  # or []
)
```

### "Breadcrumbs show wrong category"

**Solution:** Check your category classification logic. Print debug info:
```python
category, subcategory = classify_topic(topic)
print(f"DEBUG: Topic '{topic}' -> {category}/{subcategory}")
```

### "HTML looks broken (unclosed tags)"

**Solution:** BeautifulSoup sometimes reformats HTML. Use `formatter="html"`:
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
# ... modifications ...
return soup.prettify(formatter="html")  # or str(soup)
```

---

## Advanced: Custom Related Posts Logic

If you want more control over related posts:

```python
def get_related_posts_advanced(
    category: str,
    subcategory: str = None,
    current_slug: str = None,
    limit: int = 5
) -> list:
    """
    Advanced related posts with priority scoring
    """
    from pathlib import Path
    import re
    
    blog_root = Path(BLOG_DIR) / "blog-new"
    candidates = []
    
    # Priority 1: Same subcategory (excluding current)
    if subcategory:
        subcat_dir = blog_root / category / subcategory
        for html_file in subcat_dir.rglob("index.html"):
            if current_slug and current_slug in str(html_file):
                continue
            candidates.append((html_file, 3))  # priority score
    
    # Priority 2: Same category, different subcategory
    cat_dir = blog_root / category
    for html_file in cat_dir.rglob("index.html"):
        if current_slug and current_slug in str(html_file):
            continue
        if html_file not in [c[0] for c in candidates]:
            candidates.append((html_file, 2))
    
    # Priority 3: Related categories (cross-linking)
    related_categories = {
        "ai-tools": ["tutorials", "case-studies"],
        "solo-founder-strategies": ["ai-tools", "tutorials"],
        "case-studies": ["ai-tools", "solo-founder-strategies"],
        "tutorials": ["ai-tools"],
    }
    
    for related_cat in related_categories.get(category, []):
        related_dir = blog_root / related_cat
        if related_dir.exists():
            for html_file in related_dir.rglob("index.html"):
                if len(candidates) >= limit * 2:  # Don't over-fetch
                    break
                if html_file not in [c[0] for c in candidates]:
                    candidates.append((html_file, 1))
    
    # Sort by priority, extract titles
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    related = []
    for html_file, priority in candidates[:limit]:
        with open(html_file) as f:
            match = re.search(r'<h1[^>]*>(.*?)</h1>', f.read())
            if match:
                title = match.group(1)
                url = str(html_file.relative_to(blog_root).parent)
                related.append({"title": title, "url": f"/{url}/"})
    
    return related
```

---

## Performance Tips

### 1. Cache keyword map
```python
# Load once at startup
from lib.seo_enhancements import CONTEXTUAL_KEYWORDS

# Add custom keywords
CONTEXTUAL_KEYWORDS.update({
    "custom keyword": "/custom/url/",
    # ...
})
```

### 2. Batch processing
```python
# Process multiple posts at once
posts = get_posts_to_enhance()
for post in posts:
    enhanced = enhance_post_html(...)
    save_post(enhanced, post.path)
```

### 3. Skip if already enhanced
```python
# Check for existing enhancements
if '<nav class="breadcrumbs">' in post_html:
    logger.info("Already enhanced, skipping")
    continue
```

---

## Questions?

**Check:**
- `WEEK-2-IMPLEMENTATION-SUMMARY.md` - Full implementation details
- `lib/seo_enhancements.py` - Source code with docstrings
- `scripts/week2-internal-linking.py` - Reference implementation

**Still stuck?** Add debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

enhanced = enhance_post_html(...)  # Will print debug info
```
