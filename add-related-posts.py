#!/usr/bin/env python3
"""
Add Related Posts section to blog posts
"""

import json
import re
from pathlib import Path

# Load posts index to get related posts
with open('ai-automation-blog/blog/posts/index.json', 'r') as f:
    all_posts = json.load(f)

# Define related posts for each pillar post
related_posts_map = {
    "2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html": [
        "2026-03-31-how-to-automate-email-followups-without-expensive-crm.html",
        "2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html",
        "2026-03-29-how-solo-founders-are-building-milliondollar-businesses-with-ai-tools-in-2026.html"
    ],
    "2026-03-31-how-to-automate-email-followups-without-expensive-crm.html": [
        "2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html",
        "2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html",
        "2026-03-29-how-solo-founders-are-building-milliondollar-businesses-with-ai-tools-in-2026.html"
    ],
    "2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html": [
        "2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html",
        "2026-03-31-how-to-automate-email-followups-without-expensive-crm.html",
        "2026-03-29-how-solo-founders-are-building-milliondollar-businesses-with-ai-tools-in-2026.html"
    ]
}

def get_post_info(filename):
    """Get post info from index.json"""
    for post in all_posts:
        if filename in post['url']:
            return post
    return None

def generate_related_posts_html(related_filenames):
    """Generate HTML for related posts section"""
    
    html = '''
            <div class="related-posts-section">
                <h2 class="related-posts-title">📚 Keep Reading</h2>
                <div class="related-posts-grid">
'''
    
    for filename in related_filenames[:3]:  # Max 3 related posts
        post_info = get_post_info(filename)
        if not post_info:
            continue
        
        # Truncate excerpt to 100 chars
        excerpt = post_info['excerpt'][:100] + '...' if len(post_info['excerpt']) > 100 else post_info['excerpt']
        
        html += f'''
                    <div class="related-post-card">
                        <div class="related-post-category">{post_info.get('category', 'Article')}</div>
                        <h3 class="related-post-title">
                            <a href="{post_info['url']}">{post_info['title']}</a>
                        </h3>
                        <p class="related-post-excerpt">{excerpt}</p>
                        <div class="related-post-meta">
                            <span class="related-post-time">{post_info['readTime']} min read</span>
                            <a href="{post_info['url']}" class="related-post-link">Read more →</a>
                        </div>
                    </div>
'''
    
    html += '''
                </div>
            </div>

            <style>
                .related-posts-section {
                    margin: 80px 0 40px 0;
                    padding-top: 60px;
                    border-top: 2px solid #2a2a2b;
                }

                .related-posts-title {
                    font-family: 'Space Grotesk', -apple-system, sans-serif;
                    font-size: 32px;
                    font-weight: 700;
                    color: #E8E8E8;
                    text-align: center;
                    margin-bottom: 40px;
                }

                .related-posts-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 30px;
                    margin-bottom: 40px;
                }

                .related-post-card {
                    background: rgba(26, 26, 28, 0.6);
                    border: 1px solid #2a2a2b;
                    border-radius: 12px;
                    padding: 30px;
                    transition: all 0.2s ease;
                    position: relative;
                    overflow: hidden;
                }

                .related-post-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: #B9FF66;
                    transform: scaleX(0);
                    transform-origin: left;
                    transition: transform 0.2s ease;
                }

                .related-post-card:hover::before {
                    transform: scaleX(1);
                }

                .related-post-card:hover {
                    transform: translateY(-4px);
                    border-color: #B9FF66;
                    box-shadow: 0 8px 24px rgba(185, 255, 102, 0.15);
                }

                .related-post-category {
                    font-size: 12px;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    color: #B9FF66;
                    background: rgba(185, 255, 102, 0.1);
                    padding: 6px 12px;
                    border-radius: 6px;
                    display: inline-block;
                    margin-bottom: 15px;
                }

                .related-post-title {
                    font-family: 'Space Grotesk', -apple-system, sans-serif;
                    font-size: 20px;
                    font-weight: 700;
                    line-height: 1.3;
                    margin-bottom: 12px;
                }

                .related-post-title a {
                    color: #E8E8E8;
                    text-decoration: none;
                    transition: color 0.2s ease;
                }

                .related-post-title a:hover {
                    color: #B9FF66;
                }

                .related-post-excerpt {
                    color: #9CA3AF;
                    font-size: 15px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                }

                .related-post-meta {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding-top: 15px;
                    border-top: 1px solid #2a2a2b;
                }

                .related-post-time {
                    font-size: 14px;
                    color: #6B7280;
                }

                .related-post-link {
                    font-size: 14px;
                    font-weight: 600;
                    color: #B9FF66;
                    text-decoration: none;
                    transition: transform 0.2s ease;
                    display: inline-block;
                }

                .related-post-link:hover {
                    transform: translateX(4px);
                }

                @media (max-width: 1024px) {
                    .related-posts-grid {
                        grid-template-columns: repeat(2, 1fr);
                        gap: 24px;
                    }
                    
                    .related-post-card:last-child {
                        grid-column: 1 / -1;
                        max-width: 50%;
                        margin: 0 auto;
                    }
                }

                @media (max-width: 768px) {
                    .related-posts-section {
                        margin: 60px 0 30px 0;
                        padding-top: 40px;
                    }

                    .related-posts-title {
                        font-size: 26px;
                        margin-bottom: 30px;
                    }

                    .related-posts-grid {
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }

                    .related-post-card {
                        padding: 24px;
                    }

                    .related-post-card:last-child {
                        grid-column: 1;
                        max-width: 100%;
                    }

                    .related-post-title {
                        font-size: 18px;
                    }
                }
            </style>
'''
    
    return html

# Process each pillar post
posts_dir = Path('ai-automation-blog/blog/posts')

print("=" * 60)
print("🔗 ADDING RELATED POSTS SECTIONS")
print("=" * 60)
print()

for post_file, related_files in related_posts_map.items():
    post_path = posts_dir / post_file
    
    if not post_path.exists():
        print(f"❌ Not found: {post_file}")
        continue
    
    print(f"Processing: {post_file}")
    
    # Read post HTML
    with open(post_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check if already has related posts section
    if 'related-posts-section' in html_content:
        print(f"   ⏭️  Already has related posts section")
        continue
    
    # Generate related posts HTML
    related_html = generate_related_posts_html(related_files)
    
    # Insert before the CTA box (or before footer if no CTA box)
    if '<div class="cta-box">' in html_content:
        # Insert before CTA box
        html_content = html_content.replace(
            '<div class="cta-box">',
            related_html + '\n            <div class="cta-box">'
        )
    else:
        # Insert before footer
        html_content = html_content.replace(
            '</article>',
            related_html + '\n        </article>'
        )
    
    # Write updated HTML
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   ✅ Added {len(related_files)} related posts")
    print()

print("=" * 60)
print("✅ RELATED POSTS SECTIONS ADDED")
print("=" * 60)
