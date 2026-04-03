#!/usr/bin/env python3
"""
Generate programmatic tool × use-case pages
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
OUTPUT_DIR = WORKSPACE / 'ai-automation-blog' / 'blog-new' / 'use-cases'

def load_json(filename):
    """Load JSON data file"""
    with open(DATA_DIR / filename, 'r') as f:
        return json.load(f)

def find_tool(tools, slug):
    """Find tool by slug"""
    return next((t for t in tools if t['slug'] == slug), None)

def find_use_case(use_cases, slug):
    """Find use case by slug"""
    return next((uc for uc in use_cases if uc['slug'] == slug), None)

def generate_use_case_page(tool, use_case):
    """Generate a tool × use-case page"""
    
    title = f"{tool['name']} for {use_case['name']}: Complete Guide for Solo Founders (2026)"
    
    meta_desc = f"Learn how to use {tool['name']} for {use_case['name'].lower()}. Complete guide with tips, workflows, and best practices for solo founders."
    
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
                <p class="lead">Want to use {tool['name']} for {use_case['name'].lower()}? Here's everything you need to know to get started and maximize results.</p>
                <p class="byline">By Alex Chen • Published 2026 • 10 min read</p>
            </header>
            
            <section>
                <h2>Why {tool['name']} for {use_case['name']}?</h2>
                <p>{tool['name']} is {tool['best_for'].lower()}, making it an excellent choice for {use_case['name'].lower()}.</p>
                
                <h3>Key Strengths for This Use Case</h3>
                <ul>
"""
    
    for pro in tool['pros'][:3]:
        html += f"                    <li><strong>{pro}</strong> - Essential for {use_case['name'].lower()}</li>\n"
    
    html += f"""                </ul>
                
                <div class="callout">
                    <p><strong>Best For:</strong> {tool['best_for']}</p>
                    <p><strong>Pricing:</strong> {tool['pricing']}</p>
                    <p><strong>Difficulty:</strong> {use_case['difficulty'].capitalize()}</p>
                </div>
            </section>
            
            <section>
                <h2>Getting Started with {tool['name']} for {use_case['name']}</h2>
                <p>Follow these steps to set up {tool['name']} for {use_case['name'].lower()}:</p>
                
                <h3>Step 1: Initial Setup</h3>
                <p>Sign up for {tool['name']} at their website. Start with the free tier if available ({tool['pricing']}).</p>
                
                <h3>Step 2: First Tasks</h3>
                <p>Begin with simple {use_case['name'].lower()} tasks to get comfortable with the interface and workflow.</p>
                
                <h3>Step 3: Optimize Your Workflow</h3>
                <p>As you become more comfortable, optimize your setup for maximum efficiency.</p>
                
                <div class="tip-box">
                    <h4>💡 Pro Tip</h4>
                    <p>Most beginners make the mistake of jumping straight into complex {use_case['name'].lower()} projects. Start simple and build up gradually.</p>
                </div>
            </section>
            
            <section>
                <h2>Best Practices & Workflows</h2>
                <p>Here are proven workflows for using {tool['name']} for {use_case['name'].lower()}:</p>
                
                <h3>Workflow #1: Daily Use</h3>
                <ol>
                    <li>Define your {use_case['name'].lower()} goal for the session</li>
                    <li>Use {tool['name']}'s key features effectively</li>
                    <li>Review and refine output</li>
                    <li>Save templates for reuse</li>
                </ol>
                
                <h3>Workflow #2: Project-Based</h3>
                <ol>
                    <li>Plan your {use_case['name'].lower()} project</li>
                    <li>Break it into manageable chunks</li>
                    <li>Use {tool['name']} iteratively</li>
                    <li>Combine with other tools as needed</li>
                </ol>
                
                <h3>Time-Saving Shortcuts</h3>
                <ul>
                    <li>Save frequently used prompts/templates</li>
                    <li>Learn keyboard shortcuts</li>
                    <li>Use automation where possible</li>
                    <li>Build a swipe file of successful outputs</li>
                </ul>
            </section>
            
            <section>
                <h2>Limitations & Workarounds</h2>
                <p>No tool is perfect. Here's what {tool['name']} doesn't do well for {use_case['name'].lower()}, and how to work around it:</p>
                
                <h3>Known Limitations</h3>
                <ul>
"""
    
    for con in tool['cons']:
        html += f"                    <li>{con}</li>\n"
    
    html += f"""                </ul>
                
                <h3>Workarounds</h3>
                <p>For tasks where {tool['name']} falls short, consider combining it with complementary tools or using manual refinement.</p>
                
                <h3>When to Use Another Tool</h3>
                <p>If your {use_case['name'].lower()} needs include [{', '.join(tool['cons'][:2])}], you might want to explore alternatives like {', '.join([t for t in use_case['relevant_tools'] if t != tool['name']][:2])}.</p>
            </section>
            
            <section>
                <h2>Pricing & ROI</h2>
                <p><strong>Cost:</strong> {tool['pricing']}</p>
                
                <h3>Is It Worth the Investment?</h3>
                <p>For solo founders doing {use_case['name'].lower()}, {tool['name']} typically pays for itself if you:</p>
                <ul>
                    <li>Use it at least 3-4 times per week</li>
                    <li>It saves you 2+ hours per month</li>
                    <li>Quality improvements lead to better outcomes</li>
                </ul>
                
                <h3>Free vs Paid Tiers</h3>
                <p>Start with the free tier to validate it works for your workflow. Upgrade when you hit limitations or need advanced features.</p>
            </section>
            
            <section>
                <h2>Alternatives to Consider</h2>
                <p>While {tool['name']} is excellent for {use_case['name'].lower()}, these alternatives might fit better depending on your needs:</p>
                
                <h3>Alternative Tools</h3>
                <ul>
"""
    
    alternatives = [t for t in use_case['relevant_tools'] if t != tool['name']]
    for alt in alternatives[:3]:
        html += f"                    <li><strong>{alt}</strong> - Good alternative if you need different features</li>\n"
    
    html += f"""                </ul>
                
                <h3>When to Use Each</h3>
                <ul>
                    <li><strong>Use {tool['name']}</strong> if: {tool['best_for'].lower()}</li>
"""
    
    for alt in alternatives[:2]:
        html += f"                    <li><strong>Use {alt}</strong> if: You need a different approach</li>\n"
    
    html += f"""                </ul>
                
"""
    
    if alternatives:
        alt_slug = alternatives[0].lower().replace(' ', '-')
        html += f"""                <p>See our detailed comparison: <a href="/comparisons/{tool['slug']}-vs-{alt_slug}/">{tool['name']} vs {alternatives[0]}</a></p>
"""
    
    html += """
            </section>
            
            <section class="faq-section">
                <h2>Frequently Asked Questions</h2>
                
                <div class="faq-item">
                    <h3>Is {tool['name']} good for {use_case['name'].lower()}?</h3>
                    <p>Yes, {tool['name']} excels at {use_case['name'].lower()} because {tool['best_for'].lower()}. It's particularly good for solo founders who need {tool['pros'][0].lower()}.</p>
                </div>
                
                <div class="faq-item">
                    <h3>How much does {tool['name']} cost for {use_case['name'].lower()}?</h3>
                    <p>{tool['pricing']}. For most solo founders doing {use_case['name'].lower()}, this is a worthwhile investment that pays for itself quickly.</p>
                </div>
                
                <div class="faq-item">
                    <h3>What are the best alternatives to {tool['name']} for {use_case['name'].lower()}?</h3>
                    <p>Top alternatives include {' and '.join(alternatives[:2])}. Each has different strengths - see our comparison guides for details.</p>
                </div>
                
                <div class="faq-item">
                    <h3>How long does it take to learn {tool['name']} for {use_case['name'].lower()}?</h3>
                    <p>Most solo founders become productive within 1-2 weeks. The tool has a {use_case['difficulty']} learning curve, so expect some initial adjustment period.</p>
                </div>
            </section>
            
            <section class="cta-section">
                <h2>Ready to Try {tool['name']} for {use_case['name']}?</h2>
                <p>Get more guides, tool reviews, and automation strategies for solo founders.</p>
                <form class="email-signup" action="/api/subscribe" method="POST">
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <input type="hidden" name="tool" value="{tool['slug']}">
                    <input type="hidden" name="use_case" value="{use_case['slug']}">
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
    """Generate pilot batch of 10 use-case pages"""
    
    # Load data
    tools = load_json('ai-tools.json')
    use_cases = load_json('use-cases.json')
    
    # Pilot batch: 10 tool × use-case combinations
    pilot_pairs = [
        ('claude', 'coding'),
        ('chatgpt', 'content-writing'),
        ('make', 'workflow-automation'),
        ('midjourney', 'product-mockups'),
        ('cursor', 'coding'),
        ('notion', 'project-management'),
        ('perplexity', 'research'),
        ('v0', 'ui-design'),
        ('chatgpt', 'customer-support'),
        ('canva', 'social-media'),
    ]
    
    print("🎯 Generating AI Tool × Use Case Pages (Pilot)")
    print(f"Pages: {len(pilot_pairs)}\n")
    
    generated = []
    
    for tool_slug, use_case_slug in pilot_pairs:
        tool = find_tool(tools, tool_slug)
        use_case = find_use_case(use_cases, use_case_slug)
        
        if not tool:
            print(f"⚠️  Tool not found: {tool_slug}, skipping...")
            continue
        
        if not use_case:
            print(f"⚠️  Use case not found: {use_case_slug}, skipping...")
            continue
        
        # Generate page
        html, title = generate_use_case_page(tool, use_case)
        
        # Enhance with SEO features
        enhanced_html = enhance_post_html(
            html_content=html,
            title=title,
            category='use-cases',
            subcategory=use_case['slug'],
            url_path=f"/use-cases/{tool_slug}-for-{use_case_slug}/",
            related_posts=[
                {'title': f'{tool["name"]} Review', 'url': f'/ai-tools/{tool["category"]}/{tool_slug}/'},
                {'title': f'Best Tools for {use_case["name"]}', 'url': f'/use-cases/{use_case_slug}/'},
            ]
        )
        
        # Save file
        output_path = OUTPUT_DIR / f"{tool_slug}-for-{use_case_slug}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(enhanced_html)
        
        generated.append({
            'tool': tool['name'],
            'use_case': use_case['name'],
            'path': str(output_path.relative_to(WORKSPACE))
        })
        
        print(f"✅ Generated: {tool['name']} for {use_case['name']}")
    
    print(f"\n🎉 Successfully generated {len(generated)} use-case pages!")
    print(f"📁 Output: {OUTPUT_DIR}")
    
    # Save manifest
    manifest_path = OUTPUT_DIR / 'programmatic-manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(generated, f, indent=2)
    
    print(f"📝 Manifest saved: {manifest_path}")

if __name__ == '__main__':
    main()
