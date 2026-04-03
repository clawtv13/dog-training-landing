#!/usr/bin/env python3
"""
Week 1 SEO Implementation Script
Creates new directory structure, moves posts, generates redirects, updates internal links

Date: 2026-04-03
"""

import os
import json
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Constants
BASE_DIR = Path("/root/.openclaw/workspace")
CLEVERDOG_DIR = BASE_DIR / "dog-training-landing"
AIBLOG_DIR = BASE_DIR / "ai-automation-blog" / "blog"
DOCS_DIR = BASE_DIR / "docs"

def load_taxonomy(filename: str) -> Dict:
    """Load category taxonomy JSON"""
    with open(DOCS_DIR / filename, 'r') as f:
        return json.load(f)

def create_directory_structure(base_dir: Path, categories: List[Dict]):
    """Create new categorized directory structure"""
    blog_new = base_dir / "blog-new"
    blog_new.mkdir(exist_ok=True)
    
    for category in categories:
        cat_dir = blog_new / category['slug']
        cat_dir.mkdir(exist_ok=True)
        
        # Create subcategories
        for subcat in category.get('subcategories', []):
            subcat_dir = cat_dir / subcat['slug']
            subcat_dir.mkdir(exist_ok=True)
    
    print(f"✅ Created directory structure in {blog_new}")
    return blog_new

def move_post(old_path: Path, new_path: Path):
    """Move post to new location, preserving content"""
    new_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old_path, new_path)
    print(f"   Moved: {old_path.name} → {new_path.relative_to(old_path.parents[2])}")

def get_new_post_path(blog_new: Path, post_assignment: Dict, old_filename: str) -> Path:
    """Calculate new path for a post based on taxonomy"""
    category = post_assignment['category']
    subcategory = post_assignment.get('subcategory')
    
    # Remove .html extension and create directory
    slug = old_filename.replace('.html', '')
    
    if subcategory:
        return blog_new / category / subcategory / slug / "index.html"
    else:
        return blog_new / category / slug / "index.html"

def generate_redirects(post_assignments: List[Dict], old_prefix: str, base_url: str) -> List[str]:
    """Generate 301 redirect rules"""
    redirects = []
    
    for post in post_assignments:
        old_filename = post['filename']
        category = post['category']
        subcategory = post.get('subcategory')
        
        # Old URL
        old_url = f"{old_prefix}/{old_filename}"
        
        # New URL
        slug = old_filename.replace('.html', '')
        if subcategory:
            new_url = f"/blog/{category}/{subcategory}/{slug}/"
        else:
            new_url = f"/blog/{category}/{slug}/"
        
        redirects.append(f"{old_url} {new_url} 301")
    
    return redirects

def update_internal_links(file_path: Path, redirect_map: Dict[str, str]):
    """Update internal links in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = content
    changes = 0
    
    # Find all href="/blog/..." patterns
    for old_url, new_url in redirect_map.items():
        # Try different patterns
        patterns = [
            f'href="{old_url}"',
            f"href='{old_url}'",
            f'href="{old_url.replace("/blog/", "")}"',  # Relative URLs
        ]
        
        for pattern in patterns:
            if pattern in updated:
                replacement = pattern.replace(old_url, new_url)
                updated = updated.replace(pattern, replacement)
                changes += 1
    
    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"   Updated {changes} links in {file_path.name}")
    
    return changes

def create_category_hub_page(blog_new: Path, category: Dict, posts: List[Dict], site_name: str, base_url: str) -> Path:
    """Create category hub/index page"""
    cat_dir = blog_new / category['slug']
    index_path = cat_dir / "index.html"
    
    # Find posts in this category
    category_posts = [p for p in posts if p['category'] == category['slug']]
    
    # Generate post list HTML
    posts_html = ""
    for post in category_posts[:10]:  # Show top 10
        title = post.get('title', post['filename'].replace('.html', '').replace('-', ' ').title())
        slug = post['filename'].replace('.html', '')
        subcategory = post.get('subcategory')
        
        if subcategory:
            url = f"{base_url}/blog/{category['slug']}/{subcategory}/{slug}/"
        else:
            url = f"{base_url}/blog/{category['slug']}/{slug}/"
        
        posts_html += f'        <li><a href="{url}">{title}</a></li>\n'
    
    # Subcategories HTML
    subcats_html = ""
    for subcat in category.get('subcategories', []):
        subcats_html += f'      <li><a href="{base_url}/blog/{category["slug"]}/{subcat["slug"]}/">{subcat["name"]}</a></li>\n'
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category['name']} - {site_name}</title>
    <meta name="description" content="{category['description']}">
    <link rel="canonical" href="{base_url}/blog/{category['slug']}/">
    
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
          "item": "{base_url}"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{category['name']}",
          "item": "{base_url}/blog/{category['slug']}/"
        }}
      ]
    }}
    </script>
</head>
<body>
    <nav aria-label="Breadcrumb" class="breadcrumbs">
      <ol>
        <li><a href="{base_url}">Home</a> › </li>
        <li>{category['name']}</li>
      </ol>
    </nav>
    
    <main>
      <h1>{category['name']}</h1>
      <p class="lead">{category['description']}</p>
      
      <section class="featured-posts">
        <h2>Articles in {category['name']}</h2>
        <ul>
{posts_html}
        </ul>
      </section>
      
      {"<section class='subcategories'><h2>Subcategories</h2><ul>" + subcats_html + "</ul></section>" if subcats_html else ""}
    </main>
</body>
</html>"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   Created category hub: {category['slug']}/index.html")
    return index_path

def implement_cleverdog():
    """Implement CleverDogMethod blog restructure"""
    print("\n🐕 CleverDogMethod Implementation\n" + "="*50)
    
    taxonomy = load_taxonomy("CATEGORY-TAXONOMY-CLEVERDOGMETHOD.json")
    
    # 1. Create directory structure
    print("\n1️⃣  Creating directory structure...")
    blog_new = create_directory_structure(CLEVERDOG_DIR, taxonomy['categories'])
    
    # 2. Move posts
    print("\n2️⃣  Moving posts to new structure...")
    blog_old = CLEVERDOG_DIR / "blog"
    post_assignments = taxonomy['postAssignments']
    
    for post in post_assignments:
        old_path = blog_old / post['filename']
        if old_path.exists():
            new_path = get_new_post_path(blog_new, post, post['filename'])
            move_post(old_path, new_path)
    
    # 3. Generate redirects
    print("\n3️⃣  Generating 301 redirects...")
    redirects = generate_redirects(post_assignments, "/blog", taxonomy['baseUrl'])
    
    redirects_file = CLEVERDOG_DIR / "_redirects"
    with open(redirects_file, 'w') as f:
        f.write("# CleverDogMethod Blog SEO Restructure - 2026-04-03\n")
        f.write("# Old URLs → New categorized URLs\n\n")
        f.write("\n".join(redirects))
    
    print(f"   Created {len(redirects)} redirect rules in _redirects")
    
    # 4. Create redirect map for internal link updates
    print("\n4️⃣  Updating internal links...")
    redirect_map = {}
    for line in redirects:
        parts = line.split()
        if len(parts) >= 2:
            redirect_map[parts[0]] = parts[1]
    
    # Update links in all moved posts
    total_changes = 0
    for post_dir in blog_new.rglob("*/"):
        index_file = post_dir / "index.html"
        if index_file.exists() and index_file.is_file():
            changes = update_internal_links(index_file, redirect_map)
            total_changes += changes
    
    print(f"   Updated {total_changes} internal links")
    
    # 5. Create category hub pages
    print("\n5️⃣  Creating category hub pages...")
    for category in taxonomy['categories']:
        create_category_hub_page(
            blog_new, 
            category, 
            post_assignments,
            "CleverDogMethod",
            taxonomy['baseUrl']
        )
    
    print(f"\n✅ CleverDogMethod implementation complete!")
    print(f"   - {len(post_assignments)} posts moved")
    print(f"   - {len(redirects)} redirects created")
    print(f"   - {len(taxonomy['categories'])} category hubs created")
    print(f"   - {total_changes} internal links updated")

def implement_aiblog():
    """Implement AI Automation Blog restructure"""
    print("\n🤖 AI Automation Blog Implementation\n" + "="*50)
    
    taxonomy = load_taxonomy("CATEGORY-TAXONOMY-AI-AUTOMATION-BLOG.json")
    
    # 1. Create directory structure
    print("\n1️⃣  Creating directory structure...")
    blog_new = AIBLOG_DIR.parent / "blog-new"
    blog_new.mkdir(exist_ok=True)
    
    for category in taxonomy['categories']:
        cat_dir = blog_new / category['slug']
        cat_dir.mkdir(exist_ok=True)
        
        for subcat in category.get('subcategories', []):
            subcat_dir = cat_dir / subcat['slug']
            subcat_dir.mkdir(exist_ok=True)
    
    print(f"✅ Created directory structure in {blog_new}")
    
    # 2. Move posts (skip duplicates and off-topic)
    print("\n2️⃣  Moving posts to new structure...")
    blog_posts = AIBLOG_DIR / "posts"
    post_assignments = taxonomy['postAssignments']
    
    skip_notes = taxonomy.get('recommendations', {})
    duplicates = skip_notes.get('duplicates', [])
    off_topic = skip_notes.get('offTopic', [])
    
    moved_count = 0
    for post in post_assignments:
        filename = post['filename']
        
        # Skip duplicates and off-topic
        if filename in duplicates[1:]:  # Keep first, skip rest
            print(f"   Skipped (duplicate): {filename}")
            continue
        if filename in off_topic:
            print(f"   Skipped (off-topic): {filename}")
            continue
        
        old_path = blog_posts / filename
        if old_path.exists():
            # Remove date prefix from slug
            slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename.replace('.html', ''))
            
            category = post['category']
            subcategory = post.get('subcategory')
            
            if subcategory:
                new_path = blog_new / category / subcategory / slug / "index.html"
            else:
                new_path = blog_new / category / slug / "index.html"
            
            move_post(old_path, new_path)
            moved_count += 1
    
    # 3. Generate redirects
    print("\n3️⃣  Generating 301 redirects...")
    redirects = []
    
    for post in post_assignments:
        if post['filename'] in duplicates[1:] or post['filename'] in off_topic:
            continue
        
        filename = post['filename']
        old_url = f"/blog/posts/{filename}"
        
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename.replace('.html', ''))
        category = post['category']
        subcategory = post.get('subcategory')
        
        if subcategory:
            new_url = f"/blog/{category}/{subcategory}/{slug}/"
        else:
            new_url = f"/blog/{category}/{slug}/"
        
        redirects.append(f"{old_url} {new_url} 301")
    
    redirects_file = AIBLOG_DIR.parent / "_redirects"
    with open(redirects_file, 'w') as f:
        f.write("# AI Automation Blog SEO Restructure - 2026-04-03\n")
        f.write("# Old URLs → New categorized URLs\n\n")
        f.write("\n".join(redirects))
    
    print(f"   Created {len(redirects)} redirect rules in _redirects")
    
    # 4. Update internal links
    print("\n4️⃣  Updating internal links...")
    redirect_map = {}
    for line in redirects:
        parts = line.split()
        if len(parts) >= 2:
            redirect_map[parts[0]] = parts[1]
    
    total_changes = 0
    for post_dir in blog_new.rglob("*/"):
        index_file = post_dir / "index.html"
        if index_file.exists() and index_file.is_file():
            changes = update_internal_links(index_file, redirect_map)
            total_changes += changes
    
    print(f"   Updated {total_changes} internal links")
    
    # 5. Create category hub pages
    print("\n5️⃣  Creating category hub pages...")
    for category in taxonomy['categories']:
        create_category_hub_page(
            blog_new,
            category,
            post_assignments,
            "Work Less, Build",
            taxonomy['baseUrl']
        )
    
    print(f"\n✅ AI Automation Blog implementation complete!")
    print(f"   - {moved_count} posts moved")
    print(f"   - {len(redirects)} redirects created")
    print(f"   - {len(taxonomy['categories'])} category hubs created")
    print(f"   - {total_changes} internal links updated")

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("  WEEK 1: Blog SEO Infrastructure Implementation")
    print("  Date: 2026-04-03")
    print("="*60)
    
    # Implement both blogs
    implement_cleverdog()
    print("\n" + "-"*60 + "\n")
    implement_aiblog()
    
    print("\n" + "="*60)
    print("  ✅ Week 1 Implementation Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review blog-new directories")
    print("  2. Test a few posts manually")
    print("  3. Move blog-new → blog (replace old)")
    print("  4. Deploy _redirects to Netlify")
    print("  5. Test redirects with curl")
    print("\n")

if __name__ == "__main__":
    main()
