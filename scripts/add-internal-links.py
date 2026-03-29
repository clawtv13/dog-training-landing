#!/usr/bin/env python3
"""
Internal Linking Script - CleverDogMethod
Automatically adds contextual links between related blog posts
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

BLOG_DIR = Path("/root/.openclaw/workspace/dog-training-landing-clean/blog")

# Topic clusters with related keywords
TOPIC_CLUSTERS = {
    "puppy_training": {
        "keywords": ["puppy", "puppies", "socialization", "first week", "8 weeks"],
        "posts": []
    },
    "barking": {
        "keywords": ["barking", "bark", "noise", "quiet", "vocal"],
        "posts": []
    },
    "biting": {
        "keywords": ["biting", "bite", "nipping", "teeth", "chewing"],
        "posts": []
    },
    "anxiety": {
        "keywords": ["anxiety", "anxious", "nervous", "fear", "stress"],
        "posts": []
    },
    "training_basics": {
        "keywords": ["command", "sit", "stay", "come", "recall", "obedience"],
        "posts": []
    },
    "behavior_problems": {
        "keywords": ["jumping", "pulling", "aggression", "reactive", "destructive"],
        "posts": []
    },
    "enrichment": {
        "keywords": ["brain games", "mental stimulation", "enrichment", "snuffle", "puzzle"],
        "posts": []
    }
}

def extract_keywords(html_content):
    """Extract title and main keywords from post"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get title
    title_tag = soup.find('h1')
    title = title_tag.get_text() if title_tag else ""
    
    # Get first paragraph
    first_p = soup.find('p')
    intro = first_p.get_text() if first_p else ""
    
    # Get all h2 headings
    h2s = [h2.get_text() for h2 in soup.find_all('h2')]
    
    combined = f"{title} {intro} {' '.join(h2s)}".lower()
    
    return combined, title

def categorize_posts():
    """Scan all posts and categorize them"""
    
    print("📚 Scanning blog posts...")
    
    for post_file in BLOG_DIR.glob("*.html"):
        with open(post_file, 'r') as f:
            content = f.read()
        
        keywords_text, title = extract_keywords(content)
        
        # Find matching clusters
        post_clusters = []
        for cluster_name, cluster_data in TOPIC_CLUSTERS.items():
            keyword_matches = sum(1 for kw in cluster_data["keywords"] if kw in keywords_text)
            if keyword_matches >= 2:
                post_clusters.append(cluster_name)
        
        # Add to clusters
        for cluster in post_clusters:
            TOPIC_CLUSTERS[cluster]["posts"].append({
                "file": post_file.name,
                "title": title,
                "slug": post_file.stem
            })
    
    # Print results
    for cluster_name, cluster_data in TOPIC_CLUSTERS.items():
        print(f"\n{cluster_name}: {len(cluster_data['posts'])} posts")
        for post in cluster_data['posts'][:3]:
            print(f"  - {post['title'][:50]}...")

def add_related_posts_section(html_content, current_slug):
    """Add 'Related Posts' section at the end of content"""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find current post cluster
    current_clusters = []
    for cluster_name, cluster_data in TOPIC_CLUSTERS.items():
        if any(p['slug'] == current_slug for p in cluster_data['posts']):
            current_clusters.append(cluster_name)
    
    if not current_clusters:
        return html_content
    
    # Get related posts (max 3)
    related = []
    for cluster in current_clusters:
        for post in TOPIC_CLUSTERS[cluster]['posts']:
            if post['slug'] != current_slug and post not in related:
                related.append(post)
                if len(related) >= 3:
                    break
        if len(related) >= 3:
            break
    
    if not related:
        return html_content
    
    # Create related posts HTML
    related_html = """
    <div class="related-posts" style="
        background: #f8f9fa;
        padding: 30px;
        border-radius: 12px;
        margin: 50px 0 30px 0;
    ">
        <h3 style="font-size: 24px; margin-bottom: 20px; color: #333;">
            📚 Related Articles You Might Like
        </h3>
        <div style="display: grid; gap: 15px;">
    """
    
    for post in related:
        related_html += f"""
        <a href="/blog/{post['slug']}.html" style="
            display: block;
            padding: 15px 20px;
            background: white;
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        " onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
            <strong style="color: #667eea;">→</strong> {post['title']}
        </a>
        """
    
    related_html += """
        </div>
    </div>
    """
    
    # Insert before closing body tag or last section
    body_close = html_content.rfind('</body>')
    if body_close != -1:
        html_content = html_content[:body_close] + related_html + html_content[body_close:]
    
    return html_content

def add_inline_links(html_content, current_slug):
    """Add 2-3 contextual inline links within content"""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find current clusters
    current_clusters = []
    for cluster_name, cluster_data in TOPIC_CLUSTERS.items():
        if any(p['slug'] == current_slug for p in cluster_data['posts']):
            current_clusters.append(cluster_name)
    
    # Get related posts
    related = []
    for cluster in current_clusters:
        for post in TOPIC_CLUSTERS[cluster]['posts']:
            if post['slug'] != current_slug:
                related.append(post)
    
    if len(related) < 2:
        return str(soup)
    
    # Find paragraphs to add links
    paragraphs = soup.find_all('p')
    links_added = 0
    max_links = 3
    
    for p in paragraphs:
        if links_added >= max_links:
            break
        
        p_text = p.get_text().lower()
        
        # Try to match related post keywords
        for post in related:
            if links_added >= max_links:
                break
            
            # Check if any keywords from post title appear in paragraph
            title_words = post['title'].lower().split()
            for word in title_words:
                if len(word) > 5 and word in p_text:
                    # Add link
                    link_html = f' <a href="/blog/{post["slug"]}.html">{post["title"]}</a>'
                    
                    # Insert link at end of paragraph
                    new_p = BeautifulSoup(f'{p}{link_html}', 'html.parser')
                    p.replace_with(new_p)
                    
                    links_added += 1
                    break
    
    return str(soup)

def process_all_posts():
    """Process all posts and add internal links"""
    
    print("\n🔗 Adding internal links to all posts...\n")
    
    processed = 0
    
    for post_file in BLOG_DIR.glob("*.html"):
        slug = post_file.stem
        
        with open(post_file, 'r') as f:
            content = f.read()
        
        # Add related posts section
        content = add_related_posts_section(content, slug)
        
        # Add inline links (optional - can be aggressive)
        # content = add_inline_links(content, slug)
        
        # Save
        with open(post_file, 'w') as f:
            f.write(content)
        
        processed += 1
        print(f"✅ {slug}")
    
    print(f"\n✅ Processed {processed} posts")

def main():
    categorize_posts()
    
    choice = input("\n\nAdd related posts sections to all posts? (y/n): ")
    if choice.lower() == 'y':
        process_all_posts()
    else:
        print("Skipped.")

if __name__ == '__main__':
    main()
