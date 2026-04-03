#!/usr/bin/env python3
"""
Fix Category Template Inconsistency
Applies modern dark template to all category index pages
"""

import os
import json
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Modern template matching homepage/post design
CATEGORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{{TITLE}} - Work Less, Build</title>
    <meta content="{{DESCRIPTION}}" name="description"/>
    <link href="{{CANONICAL_URL}}" rel="canonical"/>
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{TITLE}}">
    <meta property="og:description" content="{{DESCRIPTION}}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{CANONICAL_URL}}">
    
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {{BREADCRUMB_JSON}}
    </script>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --dark: #0A0A0B;
            --lime: #B9FF66;
            --lime-dark: #9FE054;
            --white: #FFFFFF;
            --gray-900: #1A1A1C;
            --gray-800: #2A2A2C;
            --gray-700: #3A3A3C;
            --gray-400: #9CA3AF;
            --gray-300: #D1D5DB;
            --font-display: 'Space Grotesk', -apple-system, sans-serif;
            --font-body: 'Inter', -apple-system, sans-serif;
        }
        
        body {
            font-family: var(--font-body);
            background: var(--dark);
            color: var(--white);
            line-height: 1.6;
        }
        
        /* Navigation */
        nav {
            background: var(--gray-900);
            border-bottom: 1px solid var(--gray-800);
            padding: 1rem 0;
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
            font-family: var(--font-display);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--lime);
            text-decoration: none;
        }
        
        .nav-menu {
            list-style: none;
            display: flex;
            gap: 2rem;
        }
        
        .nav-menu a {
            color: var(--gray-400);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .nav-menu a:hover,
        .nav-menu a.active {
            color: var(--lime);
        }
        
        /* Breadcrumb */
        .breadcrumb {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
            font-size: 0.9rem;
            color: var(--gray-400);
        }
        
        .breadcrumb a {
            color: var(--lime);
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            text-decoration: underline;
        }
        
        /* Main Content */
        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        h1 {
            font-family: var(--font-display);
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            color: var(--lime);
        }
        
        .category-description {
            font-size: 1.25rem;
            color: var(--gray-400);
            margin-bottom: 3rem;
            max-width: 800px;
        }
        
        /* Subcategories Grid */
        .subcategories {
            margin-bottom: 4rem;
        }
        
        .subcategories h2 {
            font-family: var(--font-display);
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: var(--white);
        }
        
        .subcategories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        
        .subcategory-card {
            background: var(--gray-900);
            border: 1px solid var(--gray-800);
            border-radius: 8px;
            padding: 1.5rem;
            text-decoration: none;
            transition: all 0.2s;
        }
        
        .subcategory-card:hover {
            border-color: var(--lime);
            transform: translateY(-2px);
        }
        
        .subcategory-card h3 {
            font-family: var(--font-display);
            font-size: 1.25rem;
            color: var(--lime);
            margin-bottom: 0.5rem;
        }
        
        .subcategory-card p {
            color: var(--gray-400);
            font-size: 0.9rem;
        }
        
        .subcategory-card .post-count {
            color: var(--gray-400);
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        /* Posts Grid */
        .posts-section h2 {
            font-family: var(--font-display);
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: var(--white);
        }
        
        .posts-grid {
            display: grid;
            gap: 2rem;
        }
        
        .post-card {
            background: var(--gray-900);
            border: 1px solid var(--gray-800);
            border-radius: 8px;
            padding: 2rem;
            text-decoration: none;
            display: block;
            transition: all 0.2s;
        }
        
        .post-card:hover {
            border-color: var(--lime);
            transform: translateX(4px);
        }
        
        .post-card h3 {
            font-family: var(--font-display);
            font-size: 1.5rem;
            color: var(--white);
            margin-bottom: 0.75rem;
        }
        
        .post-card .post-excerpt {
            color: var(--gray-400);
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        
        .post-card .post-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: var(--gray-400);
        }
        
        /* Footer */
        footer {
            background: var(--gray-900);
            border-top: 1px solid var(--gray-800);
            padding: 3rem 0;
            margin-top: 4rem;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            text-align: center;
            color: var(--gray-400);
        }
        
        .footer-content a {
            color: var(--lime);
            text-decoration: none;
        }
        
        .footer-content a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <nav class="main-nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">Work Less, Build</a>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/archive.html">Archive</a></li>
                <li><a href="/about-v2.html">About</a></li>
            </ul>
        </div>
    </nav>
    
    <div class="breadcrumb">
        {{BREADCRUMB_HTML}}
    </div>
    
    <main>
        <h1>{{TITLE}}</h1>
        <p class="category-description">{{DESCRIPTION}}</p>
        
        {{SUBCATEGORIES_HTML}}
        
        <section class="posts-section">
            <h2>Recent Posts</h2>
            <div class="posts-grid">
                {{POSTS_HTML}}
            </div>
        </section>
    </main>
    
    <footer>
        <div class="footer-content">
            <p>&copy; 2025 Work Less, Build. Built with automation.</p>
            <p><a href="/">Home</a> · <a href="/archive.html">Archive</a> · <a href="/about-v2.html">About</a></p>
        </div>
    </footer>
</body>
</html>"""

def get_category_info(category_path):
    """Get category metadata"""
    categories = {
        "ai-tools": {
            "title": "AI Tools & Platforms",
            "description": "In-depth reviews and comparisons of AI tools that help solo founders build faster and smarter."
        },
        "ai-tools/llms": {
            "title": "Large Language Models (LLMs)",
            "description": "Latest developments in ChatGPT, Claude, GPT-4, and other language models transforming how we work."
        },
        "ai-tools/no-code-ai": {
            "title": "No-Code AI Tools",
            "description": "AI tools you can use without coding - perfect for non-technical founders."
        },
        "ai-tools/automation-platforms": {
            "title": "Automation Platforms",
            "description": "Zapier, Make, n8n and other tools to automate your workflows."
        },
        "ai-tools/image-generation": {
            "title": "AI Image Generation",
            "description": "Midjourney, DALL-E, Stable Diffusion and other AI image tools."
        },
        "solo-founder-strategies": {
            "title": "Solo Founder Strategies",
            "description": "Real tactics for building profitable businesses without a team."
        },
        "solo-founder-strategies/business-systems": {
            "title": "Business Systems",
            "description": "Build systems that run your business so you don't have to."
        },
    }
    
    return categories.get(category_path, {
        "title": category_path.split('/')[-1].replace('-', ' ').title(),
        "description": f"Articles about {category_path.split('/')[-1].replace('-', ' ')}."
    })

def find_subcategories(category_dir):
    """Find subcategories in a category directory"""
    subcats = []
    for item in category_dir.iterdir():
        if item.is_dir() and (item / "index.html").exists():
            subcat_name = item.name
            # Count posts in subcategory
            post_count = len([p for p in item.rglob("index.html") if p.parent != item])
            
            info = get_category_info(f"{category_dir.relative_to(BLOG_DIR)}/{subcat_name}")
            subcats.append({
                "name": subcat_name,
                "path": str(item.relative_to(BLOG_DIR)),
                "title": info["title"],
                "description": info["description"],
                "post_count": post_count
            })
    
    return sorted(subcats, key=lambda x: x["name"])

def find_posts(category_dir, limit=10):
    """Find posts in a category (not in subdirectories)"""
    posts = []
    
    for item in category_dir.iterdir():
        if item.is_dir() and item.name not in ["scripts"]:
            post_html = item / "index.html"
            if post_html.exists():
                # Check if this is a direct child (not a subcategory)
                depth = len(item.relative_to(category_dir).parts)
                if depth == 1:
                    # Read post to extract title and excerpt
                    try:
                        html_content = post_html.read_text()
                        
                        # Extract title
                        import re
                        title_match = re.search(r'<title>([^|<]+)', html_content)
                        title = title_match.group(1).strip() if title_match else item.name.replace('-', ' ').title()
                        
                        # Extract excerpt from meta description
                        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', html_content)
                        excerpt = desc_match.group(1) if desc_match else ""
                        
                        posts.append({
                            "title": title,
                            "excerpt": excerpt,
                            "path": str(item.relative_to(BLOG_DIR)),
                            "url": f"/{item.relative_to(BLOG_DIR)}/"
                        })
                    except Exception as e:
                        print(f"Error reading {post_html}: {e}")
    
    return sorted(posts, key=lambda x: x["title"])[:limit]

def build_breadcrumb(category_path):
    """Build breadcrumb navigation"""
    parts = category_path.split('/')
    
    # JSON-LD
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://workless.build"
        }
    ]
    
    path_so_far = ""
    for i, part in enumerate(parts, start=2):
        path_so_far += f"/{part}" if path_so_far else part
        info = get_category_info(path_so_far)
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": info["title"],
            "item": f"https://workless.build/{path_so_far}/"
        })
    
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }, indent=4)
    
    # HTML breadcrumb
    html_parts = ['<a href="/">Home</a>']
    path_so_far = ""
    for part in parts[:-1]:
        path_so_far += f"/{part}" if path_so_far else part
        info = get_category_info(path_so_far)
        html_parts.append(f'<a href="/{path_so_far}/">{info["title"]}</a>')
    
    # Current page (no link)
    info = get_category_info(category_path)
    html_parts.append(f'<span>{info["title"]}</span>')
    
    breadcrumb_html = ' → '.join(html_parts)
    
    return breadcrumb_json, breadcrumb_html

def generate_category_page(category_dir):
    """Generate a category index page"""
    category_path = str(category_dir.relative_to(BLOG_DIR))
    
    info = get_category_info(category_path)
    subcats = find_subcategories(category_dir)
    posts = find_posts(category_dir)
    
    breadcrumb_json, breadcrumb_html = build_breadcrumb(category_path)
    
    # Build subcategories HTML
    subcats_html = ""
    if subcats:
        cards = []
        for subcat in subcats:
            cards.append(f"""
                <a href="/{subcat['path']}/" class="subcategory-card">
                    <h3>{subcat['title']}</h3>
                    <p>{subcat['description']}</p>
                    <div class="post-count">{subcat['post_count']} posts</div>
                </a>
            """)
        
        subcats_html = f"""
        <section class="subcategories">
            <h2>Subcategories</h2>
            <div class="subcategories-grid">
                {''.join(cards)}
            </div>
        </section>
        """
    
    # Build posts HTML
    posts_cards = []
    for post in posts:
        posts_cards.append(f"""
            <a href="{post['url']}" class="post-card">
                <h3>{post['title']}</h3>
                <p class="post-excerpt">{post['excerpt']}</p>
            </a>
        """)
    
    posts_html = ''.join(posts_cards) if posts_cards else "<p style='color: var(--gray-400);'>No posts yet in this category.</p>"
    
    # Fill template
    html = CATEGORY_TEMPLATE.replace("{{TITLE}}", info["title"])
    html = html.replace("{{DESCRIPTION}}", info["description"])
    html = html.replace("{{CANONICAL_URL}}", f"https://workless.build/{category_path}/")
    html = html.replace("{{BREADCRUMB_JSON}}", breadcrumb_json)
    html = html.replace("{{BREADCRUMB_HTML}}", breadcrumb_html)
    html = html.replace("{{SUBCATEGORIES_HTML}}", subcats_html)
    html = html.replace("{{POSTS_HTML}}", posts_html)
    
    # Write file
    output_file = category_dir / "index.html"
    output_file.write_text(html)
    print(f"✅ Generated: {category_path}/index.html")

def main():
    """Main execution"""
    print("🔧 Fixing category template inconsistency...\n")
    
    # Find all category directories
    categories_to_fix = []
    
    for item in BLOG_DIR.rglob("index.html"):
        # Only category index pages (not homepage, not individual posts)
        if item.parent != BLOG_DIR and item.name == "index.html":
            # Check if it's a category (has subdirectories with index.html)
            parent = item.parent
            has_subdirs = any(
                (d / "index.html").exists() 
                for d in parent.iterdir() 
                if d.is_dir()
            )
            
            # Always regenerate category pages
            if parent.relative_to(BLOG_DIR).parts[0] in ["ai-tools", "solo-founder-strategies"]:
                categories_to_fix.append(parent)
    
    # Remove duplicates
    categories_to_fix = list(set(categories_to_fix))
    categories_to_fix.sort()
    
    print(f"Found {len(categories_to_fix)} category pages to fix:\n")
    for cat in categories_to_fix:
        print(f"  - {cat.relative_to(BLOG_DIR)}")
    
    print("\n" + "="*60 + "\n")
    
    # Generate each category page
    for category_dir in categories_to_fix:
        generate_category_page(category_dir)
    
    print(f"\n✅ Fixed {len(categories_to_fix)} category pages!")
    print("\n🎨 All pages now use consistent modern dark template")

if __name__ == "__main__":
    main()
