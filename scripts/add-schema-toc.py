#!/usr/bin/env python3
"""
Add FAQ Schema + Table of Contents to CleverDogMethod posts
Improves SEO visibility (featured snippets, People Also Ask boxes)
"""

import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

BLOG_DIR = Path("/root/.openclaw/workspace/dog-training-landing-clean/blog")

def generate_toc(soup):
    """Generate table of contents from H2/H3 headings"""
    
    headings = soup.find_all(['h2', 'h3'])
    
    if len(headings) < 3:
        return None  # Not worth TOC for short posts
    
    toc_html = """
    <div class="table-of-contents" style="
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 20px 25px;
        margin: 30px 0;
        border-radius: 8px;
    ">
        <h3 style="margin-top: 0; font-size: 18px; color: #333;">📋 Jump to Section:</h3>
        <ul style="margin: 15px 0 0 0; padding-left: 20px; line-height: 2;">
    """
    
    for i, heading in enumerate(headings):
        # Create anchor ID
        anchor_id = f"section-{i+1}"
        heading['id'] = anchor_id
        
        heading_text = heading.get_text()
        indent = "margin-left: 20px;" if heading.name == 'h3' else ""
        
        toc_html += f"""
        <li style="{indent}">
            <a href="#{anchor_id}" style="color: #667eea; text-decoration: none;">
                {heading_text}
            </a>
        </li>
        """
    
    toc_html += """
        </ul>
    </div>
    """
    
    return toc_html

def extract_faqs(soup, title):
    """Generate FAQ items from post content"""
    
    faqs = []
    
    # Common question patterns
    question_starters = [
        "how to", "why does", "what is", "when should", "can i", 
        "should i", "is it", "do dogs", "are dogs"
    ]
    
    # Look for H2s that are questions
    for h2 in soup.find_all('h2'):
        h2_text = h2.get_text().lower()
        
        if any(starter in h2_text for starter in question_starters) or "?" in h2_text:
            # This is a question - next paragraph is answer
            question = h2.get_text()
            
            # Find next paragraph
            next_elem = h2.find_next('p')
            if next_elem:
                answer = next_elem.get_text()[:300]  # Limit answer length
                
                faqs.append({
                    "question": question,
                    "answer": answer
                })
    
    # If no H2 questions found, generate from title
    if not faqs and "how to" in title.lower():
        # Extract first 2 paragraphs as generic FAQ
        paragraphs = soup.find_all('p')[:2]
        if len(paragraphs) >= 2:
            faqs.append({
                "question": title,
                "answer": paragraphs[0].get_text()[:300]
            })
    
    return faqs

def create_faq_schema(faqs):
    """Create JSON-LD FAQ schema markup"""
    
    if not faqs:
        return None
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for faq in faqs[:5]:  # Max 5 FAQs
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def create_article_schema(soup, url):
    """Create Article schema for better Google indexing"""
    
    title_tag = soup.find('h1')
    title = title_tag.get_text() if title_tag else "Dog Training Guide"
    
    # Extract estimated reading time
    text_content = soup.get_text()
    word_count = len(text_content.split())
    reading_time = max(1, word_count // 200)  # Assume 200 words/min
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "author": {
            "@type": "Organization",
            "name": "Clever Dog Method"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Clever Dog Method",
            "logo": {
                "@type": "ImageObject",
                "url": "https://cleverdogmethod.com/logo.png"
            }
        },
        "datePublished": datetime.now().isoformat(),
        "dateModified": datetime.now().isoformat(),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },
        "wordCount": word_count,
        "timeRequired": f"PT{reading_time}M"
    }
    
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def add_last_updated(soup):
    """Add 'Last Updated' timestamp"""
    
    updated_html = f"""
    <p style="
        color: #666;
        font-size: 14px;
        font-style: italic;
        margin: 10px 0 20px 0;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 5px;
    ">
        ✍️ <strong>Last Updated:</strong> {datetime.now().strftime("%B %d, %Y")}
    </p>
    """
    
    # Insert after H1
    h1 = soup.find('h1')
    if h1:
        h1.insert_after(BeautifulSoup(updated_html, 'html.parser'))

def process_post(filepath):
    """Add TOC + Schema to single post"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Generate TOC
    toc = generate_toc(soup)
    if toc:
        # Insert after first paragraph
        first_p = soup.find('p')
        if first_p:
            first_p.insert_after(BeautifulSoup(toc, 'html.parser'))
    
    # 2. Add Last Updated
    add_last_updated(soup)
    
    # 3. Generate FAQ Schema
    title_tag = soup.find('h1')
    title = title_tag.get_text() if title_tag else ""
    
    faqs = extract_faqs(soup, title)
    if faqs:
        faq_schema = create_faq_schema(faqs)
        
        # Insert in <head> (or before </body> if no head)
        head = soup.find('head')
        if head:
            head.append(BeautifulSoup(faq_schema, 'html.parser'))
        else:
            soup.append(BeautifulSoup(faq_schema, 'html.parser'))
    
    # 4. Add Article Schema
    url = f"https://cleverdogmethod.com/blog/{filepath.stem}.html"
    article_schema = create_article_schema(soup, url)
    
    head = soup.find('head')
    if head:
        head.append(BeautifulSoup(article_schema, 'html.parser'))
    
    # 5. Save
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return {
        "file": filepath.name,
        "toc_added": bool(toc),
        "faqs_found": len(faqs) if faqs else 0
    }

def main():
    print("📊 Adding Schema + TOC to CleverDogMethod posts...\n")
    
    results = []
    
    for post_file in BLOG_DIR.glob("*.html"):
        result = process_post(post_file)
        results.append(result)
        
        status = "✅" if result["toc_added"] else "⚠️"
        print(f"{status} {result['file']}: TOC={result['toc_added']}, FAQs={result['faqs_found']}")
    
    print(f"\n✅ Processed {len(results)} posts")
    
    # Summary
    posts_with_toc = sum(1 for r in results if r['toc_added'])
    total_faqs = sum(r['faqs_found'] for r in results)
    
    print(f"\n📊 Summary:")
    print(f"   Posts with TOC: {posts_with_toc}/{len(results)}")
    print(f"   Total FAQ items: {total_faqs}")

if __name__ == '__main__':
    main()
