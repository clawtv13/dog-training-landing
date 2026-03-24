#!/usr/bin/env python3
"""
AI-powered blog post generator for cleverdogmethod
Uses OpenRouter API to generate unique, SEO-optimized content
"""

import os
import json
import requests
from datetime import datetime

OPENROUTER_API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Clever Dog Method</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="https://cleverdogmethod.com/blog/{slug}.html">
    <link rel="stylesheet" href="/styles.css">
    
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://cleverdogmethod.com/blog/{slug}.html">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "{title}",
        "description": "{meta_description}",
        "author": {{
            "@type": "Organization",
            "name": "Clever Dog Method"
        }},
        "datePublished": "{date}",
        "dateModified": "{date}"
    }}
    </script>
</head>
<body>
    <nav class="nav">
        <div class="container nav-content">
            <a href="/" class="logo">🐕 Clever Dog Method</a>
            <div style="display: flex; gap: 20px;">
                <a href="/blog/" style="color: #333; text-decoration: none;">Blog</a>
                <a href="https://cleverdog.store" style="color: #333; text-decoration: none;">Shop</a>
            </div>
        </div>
    </nav>
    
    <article class="container" style="max-width: 800px; margin: 80px auto; padding: 40px 20px;">
        <header style="margin-bottom: 40px;">
            <div style="color: #666; font-size: 14px; margin-bottom: 12px;">
                {category} • {read_time} min read • {date_formatted}
            </div>
            <h1 style="font-size: 42px; line-height: 1.2; margin-bottom: 20px; color: #1a1a1a;">{title}</h1>
        </header>
        
        <div style="line-height: 1.8; font-size: 18px; color: #333;">
            {content}
        </div>
        
        <div style="margin-top: 60px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; color: white;">
            <h3 style="margin-bottom: 16px; color: white;">Want the Complete Training System?</h3>
            <p style="margin-bottom: 24px; opacity: 0.95;">Join 67,000+ dog owners using brain training to eliminate behavior problems in days.</p>
            <a href="https://258e5df6f75r1pezy8tb13r53z.hop.clickbank.net" 
               style="display: inline-block; padding: 16px 32px; background: white; color: #667eea; text-decoration: none; border-radius: 8px; font-weight: 600;"
               rel="nofollow">
                Get Instant Access — $47
            </a>
            <div style="margin-top: 12px; font-size: 14px; opacity: 0.9;">60-Day Money-Back Guarantee</div>
        </div>
    </article>
</body>
</html>"""

def generate_content(topic, keywords):
    """Generate blog post content using AI"""
    
    prompt = f"""Write a comprehensive, engaging blog post about: "{topic}"

Target keywords: {keywords}

Requirements:
- 800-1200 words
- Personal, conversational tone (like talking to a friend)
- 8th grade reading level
- Include a personal story or relatable example in the intro
- Explain the science/psychology behind the behavior
- Provide step-by-step practical solutions
- Add prevention tips
- Natural mention of brain training games (no hard sell)
- Use short paragraphs (2-3 sentences max)
- Include specific examples and details

Structure:
1. Hook (personal story or surprising fact)
2. The Problem (why this happens)
3. The Science (dog psychology/behavior)
4. The Solution (step-by-step)
5. Prevention Strategy
6. When to Seek Help (if severe cases)

Write in HTML with proper <h2> headers and <p> tags. Make it engaging and actionable."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        result = response.json()
        
        content = result['choices'][0]['message']['content']
        
        # Clean up if wrapped in markdown code blocks
        if content.startswith('```html'):
            content = content.replace('```html', '').replace('```', '').strip()
        
        return content
        
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def create_slug(title):
    """Convert title to URL-friendly slug"""
    slug = title.lower()
    slug = slug.replace(' ', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    slug = slug[:60]  # Max 60 chars
    return slug

def estimate_read_time(content):
    """Estimate reading time (words / 200 words per minute)"""
    word_count = len(content.split())
    return max(1, round(word_count / 200))

def generate_post(topic, keywords, category="Training"):
    """Generate complete blog post"""
    
    print(f"\n✍️  Generating content for: {topic}")
    
    # Generate content with AI
    content = generate_content(topic, keywords)
    
    if not content:
        print("   ❌ Failed to generate content")
        return None
    
    # Generate metadata
    title = topic
    slug = create_slug(title)
    read_time = estimate_read_time(content)
    meta_description = f"Learn how to handle {keywords.split(',')[0].strip()} with science-backed training methods. Step-by-step guide for dog owners."
    
    # Fill template
    post_html = POST_TEMPLATE.format(
        title=title,
        slug=slug,
        meta_description=meta_description,
        keywords=keywords,
        category=category,
        read_time=read_time,
        date=datetime.now().isoformat(),
        date_formatted=datetime.now().strftime("%B %d, %Y"),
        content=content
    )
    
    post_data = {
        "title": title,
        "slug": slug,
        "keywords": keywords,
        "category": category,
        "html": post_html,
        "word_count": len(content.split())
    }
    
    print(f"   ✅ Generated {post_data['word_count']} words")
    print(f"   📄 Slug: {slug}")
    
    return post_data

def main():
    # Test generation
    test_topic = "Why Smart Dogs Develop Separation Anxiety (And How to Fix It)"
    test_keywords = "separation anxiety, smart dogs, anxiety training"
    
    print("\n🤖 TESTING CONTENT GENERATOR")
    print("="*60)
    
    post = generate_post(test_topic, test_keywords, "Behavior")
    
    if post:
        # Save test output
        test_file = f"/root/.openclaw/workspace/.state/test-post-{post['slug']}.html"
        with open(test_file, 'w') as f:
            f.write(post['html'])
        
        print(f"\n💾 Test post saved to: {test_file}")
        print(f"📊 Stats: {post['word_count']} words, {len(post['keywords'].split(','))} keywords")
    
    return post

if __name__ == '__main__':
    main()
