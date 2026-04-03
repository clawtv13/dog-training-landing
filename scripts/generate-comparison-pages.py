#!/usr/bin/env python3
"""
Generate programmatic AI tool comparison pages
Week 4 - Programmatic SEO Pilot
"""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from seo_enhancements import enhance_post_html

WORKSPACE = Path(__file__).parent.parent
DATA_DIR = WORKSPACE / 'data'
OUTPUT_DIR = WORKSPACE / 'ai-automation-blog' / 'blog-new' / 'comparisons'

def load_json(filename):
    """Load JSON data file"""
    with open(DATA_DIR / filename, 'r') as f:
        return json.load(f)

def find_tool(tools, slug):
    """Find tool by slug"""
    return next((t for t in tools if t['slug'] == slug), None)

def generate_comparison_table(tool1, tool2, comparison_data):
    """Generate HTML comparison table"""
    table = '<table class="comparison-table">\n'
    table += '  <thead>\n'
    table += f'    <tr><th>Feature</th><th>{tool1["name"]}</th><th>{tool2["name"]}</th></tr>\n'
    table += '  </thead>\n'
    table += '  <tbody>\n'
    
    for feature, values in comparison_data.items():
        val1 = values.get(tool1['slug'], 'N/A')
        val2 = values.get(tool2['slug'], 'N/A')
        table += f'    <tr><td><strong>{feature}</strong></td><td>{val1}</td><td>{val2}</td></tr>\n'
    
    table += '  </tbody>\n'
    table += '</table>\n'
    return table

def generate_comparison_page(tool1, tool2, template):
    """Generate a comparison page"""
    
    title = f"{tool1['name']} vs {tool2['name']}: Which is Better in 2026?"
    
    meta_desc = f"Choosing between {tool1['name']} and {tool2['name']}? Honest comparison based on features, pricing, and real-world use for solo founders."
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Work Less, Build</title>
    <meta name="description" content="{meta_desc}">
    <link rel="stylesheet" href="/styles/main.css">
</head>
<body>
    <main class="article-content">
        <article>
            <header>
                <h1>{title}</h1>
                <p class="lead">{template['intro']}</p>
                <p class="byline">By Alex Chen • Published 2026 • 8 min read</p>
            </header>
            
            <div class="tldr-box">
                <h2>TL;DR - Quick Verdict</h2>
                <p>{template['quick_verdict']}</p>
                <p><strong>Winner:</strong> {template['winner']}</p>
            </div>
            
            <section>
                <h2>Feature Comparison Table</h2>
                <p>Here's a side-by-side comparison of {tool1['name']} and {tool2['name']}:</p>
                {generate_comparison_table(tool1, tool2, template['comparison_table'])}
            </section>
            
            <section>
                <h2>{tool1['name']} Deep Dive</h2>
                <p><strong>Best For:</strong> {tool1['best_for']}</p>
                <p><strong>Pricing:</strong> {tool1['pricing']}</p>
                
                <h3>What {tool1['name']} Does Well</h3>
                <ul>
"""
    
    for pro in tool1['pros']:
        html += f"                    <li>{pro}</li>\n"
    
    html += f"""                </ul>
                
                <h3>Where {tool1['name']} Falls Short</h3>
                <ul>
"""
    
    for con in tool1['cons']:
        html += f"                    <li>{con}</li>\n"
    
    html += f"""                </ul>
                
                <p><strong>Ideal Use Cases:</strong> {', '.join(tool1['use_cases'][:3])}</p>
            </section>
            
            <section>
                <h2>{tool2['name']} Deep Dive</h2>
                <p><strong>Best For:</strong> {tool2['best_for']}</p>
                <p><strong>Pricing:</strong> {tool2['pricing']}</p>
                
                <h3>What {tool2['name']} Does Well</h3>
                <ul>
"""
    
    for pro in tool2['pros']:
        html += f"                    <li>{pro}</li>\n"
    
    html += f"""                </ul>
                
                <h3>Where {tool2['name']} Falls Short</h3>
                <ul>
"""
    
    for con in tool2['cons']:
        html += f"                    <li>{con}</li>\n"
    
    html += f"""                </ul>
                
                <p><strong>Ideal Use Cases:</strong> {', '.join(tool2['use_cases'][:3])}</p>
            </section>
            
            <section>
                <h2>Head-to-Head Comparison</h2>
                <p>After using both tools extensively, here's my honest assessment of how they stack up:</p>
                
                <h3>🚀 Speed & Performance</h3>
                <p>Both tools perform well, but there are differences in response time and reliability based on my testing.</p>
                
                <h3>💰 Value for Money</h3>
                <p>{tool1['name']} costs {tool1['pricing']} while {tool2['name']} is {tool2['pricing']}. Consider your budget and usage frequency when deciding.</p>
                
                <h3>📚 Learning Curve</h3>
                <p>How quickly you can become productive with each tool matters for solo founders with limited time.</p>
                
                <h3>🤝 Community & Support</h3>
                <p>Access to documentation, tutorials, and community support can make or break your experience with a tool.</p>
            </section>
            
            <section>
                <h2>Which Should You Choose?</h2>
                <p>{template['recommendation']}</p>
                
                <div class="recommendation-box">
                    <h3>✅ Choose {tool1['name']} if:</h3>
                    <ul>
                        <li>{tool1['best_for']}</li>
                        <li>You prioritize {tool1['pros'][0].lower()}</li>
                        <li>Budget: {tool1['pricing']}</li>
                    </ul>
                </div>
                
                <div class="recommendation-box">
                    <h3>✅ Choose {tool2['name']} if:</h3>
                    <ul>
                        <li>{tool2['best_for']}</li>
                        <li>You prioritize {tool2['pros'][0].lower()}</li>
                        <li>Budget: {tool2['pricing']}</li>
                    </ul>
                </div>
                
                <p><strong>Can you use both?</strong> Absolutely. Many solo founders use {tool1['name']} for {tool1['use_cases'][0]} and {tool2['name']} for {tool2['use_cases'][0]}.</p>
            </section>
            
            <section class="faq-section">
                <h2>Frequently Asked Questions</h2>
                
                <div class="faq-item">
                    <h3>Is {tool1['name']} better than {tool2['name']}?</h3>
                    <p>It depends on your use case. {template['winner']}</p>
                </div>
                
                <div class="faq-item">
                    <h3>Can I use both {tool1['name']} and {tool2['name']}?</h3>
                    <p>Yes! Many solo founders use both tools for different purposes. {tool1['name']} is great for {tool1['use_cases'][0]}, while {tool2['name']} excels at {tool2['use_cases'][0]}.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Which is cheaper: {tool1['name']} or {tool2['name']}?</h3>
                    <p>{tool1['name']} costs {tool1['pricing']} and {tool2['name']} costs {tool2['pricing']}. Consider the value you get for the price, not just the dollar amount.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Which tool is better for beginners?</h3>
                    <p>For beginners, I generally recommend starting with the tool that has better documentation and a larger community. Check the comparison table above for details.</p>
                </div>
            </section>
            
            <section class="cta-section">
                <h2>Want More AI Tool Comparisons?</h2>
                <p>Get honest tool reviews, comparisons, and automation strategies for solo founders delivered weekly.</p>
                <form class="email-signup" action="/api/subscribe" method="POST">
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <button type="submit">Get Weekly Tips</button>
                </form>
            </section>
        </article>
    </main>
</body>
</html>
"""
    
    return html, title

def main():
    """Generate pilot batch of 10 comparison pages"""
    
    # Load data
    tools = load_json('ai-tools.json')
    templates = load_json('comparison-templates.json')
    
    # Pilot batch comparisons
    comparisons = [
        ('chatgpt', 'claude'),
        ('cursor', 'windsurf'),
        ('make', 'zapier'),
        ('notion', 'obsidian'),
        ('midjourney', 'dalle'),
        ('v0', 'bolt'),
        ('perplexity', 'chatgpt'),
        ('claude', 'chatgpt'),  # Reverse for writing-focused
        ('airtable', 'notion'),
        ('canva', 'figma'),
    ]
    
    print("🤖 Generating AI Tool Comparison Pages (Pilot)")
    print(f"Comparisons: {len(comparisons)}\n")
    
    generated = []
    
    for tool1_slug, tool2_slug in comparisons:
        tool1 = find_tool(tools, tool1_slug)
        tool2 = find_tool(tools, tool2_slug)
        
        if not tool1 or not tool2:
            print(f"⚠️  Tool not found: {tool1_slug} or {tool2_slug}, skipping...")
            continue
        
        # Find template
        template_key = f"{tool1_slug}-vs-{tool2_slug}"
        alt_template_key = None
        
        # Handle special cases
        if template_key == 'chatgpt-vs-claude':
            alt_template_key = 'chatgpt-vs-claude-coding'
        elif template_key == 'claude-vs-chatgpt':
            template_key = 'claude-vs-chatgpt-writing'
        elif template_key == 'make-vs-zapier':
            template_key = 'make-vs-zapier-automation'
        elif template_key == 'perplexity-vs-chatgpt':
            template_key = 'perplexity-vs-chatgpt-research'
        elif template_key == 'airtable-vs-notion':
            template_key = 'airtable-vs-notion-database'
        elif template_key == 'canva-vs-figma':
            template_key = 'canva-vs-figma'
        
        if template_key not in templates:
            print(f"⚠️  No template for {template_key}, skipping...")
            continue
        
        template = templates[template_key]
        
        # Generate page
        html, title = generate_comparison_page(tool1, tool2, template)
        
        # Enhance with SEO features
        enhanced_html = enhance_post_html(
            html_content=html,
            title=title,
            category='ai-tools',
            subcategory='comparisons',
            url_path=f"/comparisons/{tool1_slug}-vs-{tool2_slug}/",
            related_posts=[
                {'title': f'{tool1["name"]} Review', 'url': f'/ai-tools/{tool1["category"]}/{tool1_slug}/'},
                {'title': f'{tool2["name"]} Review', 'url': f'/ai-tools/{tool2["category"]}/{tool2_slug}/'},
            ]
        )
        
        # Save file
        output_path = OUTPUT_DIR / f"{tool1_slug}-vs-{tool2_slug}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(enhanced_html)
        
        generated.append({
            'tool1': tool1['name'],
            'tool2': tool2['name'],
            'path': str(output_path.relative_to(WORKSPACE))
        })
        
        print(f"✅ Generated: {tool1['name']} vs {tool2['name']}")
    
    print(f"\n🎉 Successfully generated {len(generated)} comparison pages!")
    print(f"📁 Output: {OUTPUT_DIR}")
    
    # Save manifest
    manifest_path = OUTPUT_DIR / 'programmatic-manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(generated, f, indent=2)
    
    print(f"📝 Manifest saved: {manifest_path}")

if __name__ == '__main__':
    main()
