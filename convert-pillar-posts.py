#!/usr/bin/env python3
"""
Convert pillar post markdown to HTML with full SEO metadata
"""

import re
from datetime import datetime

# Post configurations
POSTS = [
    {
        "input": "pillar-1-chatgpt-prompts-CONTENT.md",
        "output": "ai-automation-blog/blog/posts/2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html",
        "title": "The 51 ChatGPT Prompts That Save Solopreneurs 15 Hours Every Week",
        "slug": "the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week",
        "description": "51 ChatGPT prompts for business automation. Save 15 hours/week with copy-paste prompts for email, content, planning. Used by 50+ solopreneurs.",
        "keywords": "ChatGPT prompts for business, AI automation, solopreneur productivity, email automation, content creation prompts",
        "category": "AI Automation"
    },
    {
        "input": "pillar-2-email-automation-CONTENT.md",
        "output": "ai-automation-blog/blog/posts/2026-03-31-how-to-automate-email-followups-without-expensive-crm.html",
        "title": "How to Automate Email Follow-Ups Without Expensive CRM (Free Guide)",
        "slug": "how-to-automate-email-followups-without-expensive-crm",
        "description": "Learn how to automate email follow-ups using free tools. Step-by-step tutorial: Gmail + ChatGPT + Zapier. Save $200/month and 10 hours/week.",
        "keywords": "automate email follow-ups, email automation, CRM alternative, solopreneur email, free automation tools",
        "category": "Email Automation"
    },
    {
        "input": "pillar-3-tech-stack-CONTENT.md",
        "output": "ai-automation-blog/blog/posts/2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html",
        "title": "My $50/Month Tech Stack That Replaces Your $500 SaaS Bill",
        "slug": "my-50-month-tech-stack-that-replaces-your-500-saas-bill",
        "description": "Solopreneur tech stack 2026: Run your business on $50/month instead of $500. Complete tool comparison, migration guides, and real cost savings.",
        "keywords": "solopreneur tech stack 2026, cheap SaaS alternatives, budget tech stack, tool comparison, cost optimization",
        "category": "Tech Stack"
    }
]

def markdown_to_html(markdown_text):
    """Convert markdown to HTML"""
    html = markdown_text
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Code blocks
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Paragraphs (any text not in tags becomes <p>)
    lines = html.split('\n')
    processed = []
    in_tag = False
    paragraph = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if paragraph:
                processed.append('<p>' + ' '.join(paragraph) + '</p>')
                paragraph = []
            in_tag = False
            continue
            
        if stripped.startswith('<h') or stripped.startswith('<pre>') or stripped.startswith('<ul>') or stripped.startswith('<ol>'):
            if paragraph:
                processed.append('<p>' + ' '.join(paragraph) + '</p>')
                paragraph = []
            processed.append(stripped)
            in_tag = True
        elif in_tag:
            processed.append(stripped)
            if '</h' in stripped or '</pre>' in stripped or '</ul>' in stripped or '</ol>' in stripped:
                in_tag = False
        else:
            paragraph.append(stripped)
    
    if paragraph:
        processed.append('<p>' + ' '.join(paragraph) + '</p>')
    
    return '\n'.join(processed)

def create_html_post(post_config):
    """Generate full HTML post from markdown content"""
    
    # Read markdown content
    with open(post_config["input"], 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Remove meta description and front matter if present
    markdown_content = re.sub(r'\*\*Meta Description:.*?\n', '', markdown_content)
    markdown_content = re.sub(r'\*\*Primary Keyword:.*?\n', '', markdown_content)
    markdown_content = re.sub(r'\*\*Target Length:.*?\n', '', markdown_content)
    markdown_content = re.sub(r'\*\*Author:.*?\n', '', markdown_content)
    markdown_content = re.sub(r'\*\*Date:.*?\n', '', markdown_content)
    markdown_content = re.sub(r'^---\n', '', markdown_content, flags=re.MULTILINE)
    
    # Convert markdown to HTML
    content_html = markdown_to_html(markdown_content.strip())
    
    # Count words for schema
    word_count = len(markdown_content.split())
    
    # Current timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Build full HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NK82TJD61G"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-NK82TJD61G');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{post_config["description"]}">
    <meta name="keywords" content="{post_config["keywords"]}">
    <title>{post_config["title"]} | Work Less, Build</title>
    <link rel="canonical" href="https://workless.build/posts/{post_config["slug"]}.html">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{post_config["title"]}">
    <meta property="og:description" content="{post_config["description"]}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://workless.build/posts/{post_config["slug"]}.html">
    <meta property="og:image" content="https://workless.build/og-image.png">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{post_config["title"]}">
    <meta name="twitter:description" content="{post_config["description"]}">
    <meta name="twitter:image" content="https://workless.build/og-image.png">
    
    <!-- Author metadata -->
    <meta name="author" content="Alex Chen">
    <meta name="article:published_time" content="{timestamp}">
    <meta name="article:modified_time" content="{timestamp}">
    <meta name="article:section" content="{post_config["category"]}">
    <meta name="article:tag" content="{post_config["keywords"]}">
    
    <!-- JSON-LD Structured Data for Article -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{post_config["title"]}",
      "description": "{post_config["description"]}",
      "image": "https://workless.build/og-image.png",
      "datePublished": "{timestamp}",
      "dateModified": "{timestamp}",
      "author": {{
        "@type": "Person",
        "name": "Alex Chen"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Work Less, Build",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://workless.build/logo.png"
        }}
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "https://workless.build/posts/{post_config["slug"]}.html"
      }},
      "keywords": "{post_config["keywords"]}",
      "articleSection": "{post_config["category"]}",
      "wordCount": "{word_count}"
    }}
    </script>
    
    <!-- Breadcrumb Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://workless.build/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Articles",
          "item": "https://workless.build/archive.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{post_config["title"]}",
          "item": "https://workless.build/posts/{post_config["slug"]}.html"
        }}
      ]
    }}
    </script>
    
    <!-- Alternate RSS Feed -->
    <link rel="alternate" type="application/rss+xml" title="Work Less, Build RSS Feed" href="https://workless.build/rss.xml">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            line-height: 1.7;
            color: #E8E8E8;
            background: #0A0A0B;
            padding: 20px;
        }}

        .container {{
            max-width: 750px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 60px;
        }}

        .site-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .site-title a {{
            color: #E8E8E8;
            text-decoration: none;
            transition: color 0.2s;
        }}

        .site-title a:hover {{
            color: #B9FF66;
        }}

        .tagline {{
            color: #888;
            font-size: 15px;
        }}

        nav {{
            margin-top: 20px;
        }}

        nav a {{
            color: #888;
            text-decoration: none;
            margin-right: 20px;
            font-size: 15px;
            transition: color 0.2s;
        }}

        nav a:hover {{
            color: #B9FF66;
        }}

        article {{
            margin-bottom: 80px;
        }}

        h1 {{
            font-size: 42px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 20px;
            color: #E8E8E8;
        }}

        .post-meta {{
            color: #888;
            font-size: 14px;
            margin-bottom: 40px;
        }}

        .post-content {{
            font-size: 18px;
            line-height: 1.8;
        }}

        .post-content h2 {{
            font-size: 32px;
            font-weight: 700;
            margin: 50px 0 20px 0;
            color: #E8E8E8;
        }}

        .post-content h3 {{
            font-size: 24px;
            font-weight: 600;
            margin: 40px 0 15px 0;
            color: #E8E8E8;
        }}

        .post-content h4 {{
            font-size: 20px;
            font-weight: 600;
            margin: 30px 0 12px 0;
            color: #B9FF66;
        }}

        .post-content p {{
            margin-bottom: 25px;
        }}

        .post-content a {{
            color: #B9FF66;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s;
        }}

        .post-content a:hover {{
            border-bottom-color: #B9FF66;
        }}

        .post-content strong {{
            color: #E8E8E8;
            font-weight: 600;
        }}

        .post-content ul, .post-content ol {{
            margin: 20px 0 25px 30px;
        }}

        .post-content li {{
            margin-bottom: 10px;
        }}

        .post-content code {{
            background: #1a1a1b;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 16px;
            color: #B9FF66;
        }}

        .post-content pre {{
            background: #1a1a1b;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 25px 0;
            border-left: 4px solid #B9FF66;
        }}

        .post-content pre code {{
            background: none;
            padding: 0;
            color: #E8E8E8;
            font-size: 14px;
        }}

        .cta-box {{
            background: linear-gradient(135deg, #B9FF66 0%, #8FD43F 100%);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            text-align: center;
        }}

        .cta-box h3 {{
            color: #0A0A0B;
            font-size: 24px;
            margin-bottom: 15px;
        }}

        .cta-box p {{
            color: #0A0A0B;
            font-size: 16px;
            margin-bottom: 20px;
        }}

        .cta-button {{
            display: inline-block;
            background: #0A0A0B;
            color: #B9FF66;
            padding: 15px 35px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 18px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(185, 255, 102, 0.3);
        }}

        footer {{
            margin-top: 80px;
            padding-top: 40px;
            border-top: 1px solid #2a2a2b;
            color: #888;
            font-size: 14px;
        }}

        footer a {{
            color: #888;
            text-decoration: none;
            transition: color 0.2s;
        }}

        footer a:hover {{
            color: #B9FF66;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 15px;
            }}

            h1 {{
                font-size: 32px;
            }}

            .post-content {{
                font-size: 17px;
            }}

            .post-content h2 {{
                font-size: 26px;
            }}

            .post-content h3 {{
                font-size: 21px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="site-title">
                <a href="/">Work Less, Build</a>
            </div>
            <p class="tagline">AI automation for solopreneurs who value time over hustle</p>
            <nav>
                <a href="/">Home</a>
                <a href="/archive.html">Articles</a>
                <a href="/about.html">About</a>
            </nav>
        </header>

        <article>
            <h1>{post_config["title"]}</h1>
            
            <div class="post-meta">
                Published on March 31, 2026 by Alex Chen
            </div>

            <div class="post-content">
{content_html}
            </div>

            <div class="cta-box">
                <h3>Ready to Save 15 Hours Every Week?</h3>
                <p>Get all 51 battle-tested prompts, 10 automation blueprints, and 3 detailed case studies. Instant access for $39.</p>
                <a href="https://worklessbuild.gumroad.com/l/odgowv" class="cta-button">Get the Complete Automation Kit →</a>
            </div>
        </article>

        <footer>
            <p>© 2026 Work Less, Build. <a href="/">Home</a> · <a href="/archive.html">Archive</a> · <a href="/about.html">About</a></p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

# Generate all 3 posts
print("=" * 60)
print("🔄 CONVERTING PILLAR POSTS TO HTML")
print("=" * 60)
print("")

for post in POSTS:
    print(f"Processing: {post['input']}")
    
    try:
        # Read markdown
        with open(post["input"], 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Generate HTML
        html_output = create_html_post(post)
        
        # Write output
        with open(post["output"], 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        word_count = len(markdown_content.split())
        print(f"✅ Created: {post['output']}")
        print(f"   Words: {word_count}")
        print(f"   Title: {post['title']}")
        print("")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("")

print("=" * 60)
print("✅ CONVERSION COMPLETE")
print("=" * 60)
