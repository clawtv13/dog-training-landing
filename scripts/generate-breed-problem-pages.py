#!/usr/bin/env python3
"""
Generate programmatic breed × problem pages for CleverDogMethod
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
OUTPUT_DIR = WORKSPACE / 'cleverdogmethod-blog' / 'blog-new' / 'breed-guides'

def load_json(filename):
    """Load JSON data file"""
    with open(DATA_DIR / filename, 'r') as f:
        return json.load(f)

def generate_breed_problem_page(breed, problem, template):
    """Generate a single breed × problem page"""
    
    breed_name = breed['name']
    problem_name = problem['name']
    slug = problem['slug']
    
    # Create title
    title = f"How to Stop {breed_name} {problem_name}"
    
    # Meta description
    meta_desc = f"Is your {breed_name} {problem['description'].split(',')[0]}? Learn why {breed_name}s {slug} and proven training techniques to stop it. Step-by-step guide from certified trainers."
    
    # Generate HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Clever Dog Method</title>
    <meta name="description" content="{meta_desc}">
    <link rel="stylesheet" href="/styles/main.css">
</head>
<body>
    <main class="article-content">
        <article>
            <header>
                <h1>{title}</h1>
                <p class="lead">Is your {breed_name} {problem['description'].split(',')[0]}? You're not alone. {breed_name}s {template['intro'].split('.')[0]}.</p>
            </header>
            
            <section>
                <h2>Why {breed_name}s {problem_name}</h2>
                <p>{template['intro']}</p>
                <p><strong>Breed Characteristics:</strong></p>
                <ul>
                    <li>Energy Level: {breed['energy_level']}/5</li>
                    <li>Trainability: {breed['trainability']}/5</li>
                    <li>Exercise Needs: {breed['exercise_needs']}</li>
                    <li>Original Purpose: {breed['original_purpose']}</li>
                </ul>
            </section>
            
            <section>
                <h2>Common Causes of {problem_name} in {breed_name}s</h2>
                <p>Understanding why your {breed_name} engages in this behavior is the first step to fixing it. Here are the most common causes:</p>
                <ul>
"""
    
    for cause in template['common_causes']:
        html += f"                    <li><strong>{cause.split(' ')[0].capitalize()}:</strong> {cause}</li>\n"
    
    html += f"""                </ul>
                <p>For more details on {problem_name.lower()} in general, see our complete guide to <a href="/behavior-problems/{slug}/">{problem_name} problems</a>.</p>
            </section>
            
            <section>
                <h2>How to Stop {breed_name} {problem_name}: Step-by-Step Training</h2>
                <p>Here's a proven training plan specifically for {breed_name}s:</p>
                <ol>
"""
    
    for i, tip in enumerate(template['training_tips'], 1):
        html += f"                    <li><strong>Step {i}:</strong> {tip}</li>\n"
    
    html += f"""                </ol>
                
                <div class="callout">
                    <h3>💡 Timeline for Results</h3>
                    <p><strong>{template['timeline']}</strong></p>
                    <p>Remember that every dog is different. Some {breed_name}s will improve faster, while others need more time. Consistency is key!</p>
                </div>
            </section>
            
            <section>
                <h2>Prevention Tips for {breed_name} Owners</h2>
                <p>{template['prevention']}</p>
                <p><strong>Daily Exercise Recommendations for {breed_name}s:</strong></p>
                <ul>
                    <li>Physical exercise: {breed['exercise_needs']}</li>
                    <li>Mental stimulation: 15-30 minutes daily</li>
                    <li>Training sessions: 2-3 short sessions per day</li>
                </ul>
            </section>
            
            <section>
                <h2>When to Seek Professional Help</h2>
                <p>While most {problem_name.lower()} issues can be resolved with consistent training, consider consulting a professional dog trainer or veterinary behaviorist if:</p>
                <ul>
                    <li>The behavior is getting worse despite training</li>
                    <li>Your {breed_name} shows signs of aggression or fear</li>
                    <li>You've been training consistently for {template['timeline'].split('-')[0].strip()} without improvement</li>
                    <li>The behavior is causing significant stress to you or your family</li>
                    <li>You suspect an underlying medical issue</li>
                </ul>
                <p>A certified professional can provide personalized guidance for your specific situation.</p>
            </section>
            
            <section class="faq-section">
                <h2>Frequently Asked Questions</h2>
                
                <div class="faq-item">
                    <h3>Why do {breed_name}s {slug} so much?</h3>
                    <p>{template['intro']}</p>
                </div>
                
                <div class="faq-item">
                    <h3>At what age does {breed_name} {problem_name.lower()} typically start?</h3>
                    <p>Most {problem_name.lower()} behavior in {breed_name}s appears between puppyhood and 2 years of age, though it can develop at any stage. Early training and socialization help prevent issues.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Can you completely train {breed_name} to stop {problem_name.lower()}?</h3>
                    <p>Yes, with consistent training and patience. {breed_name}s have a trainability rating of {breed['trainability']}/5. The key is understanding their breed-specific needs and providing appropriate outlets for their natural behaviors.</p>
                </div>
                
                <div class="faq-item">
                    <h3>How long does it take to fix {problem_name.lower()} in {breed_name}s?</h3>
                    <p>Typically {template['timeline']} of consistent training. However, timeline varies based on the dog's age, severity of behavior, and consistency of training.</p>
                </div>
            </section>
            
            <section class="cta-section">
                <h2>Need More Help Training Your {breed_name}?</h2>
                <p>Get breed-specific training tips, behavior guides, and expert advice delivered to your inbox.</p>
                <form class="email-signup" action="/api/subscribe" method="POST">
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <input type="hidden" name="breed" value="{breed['slug']}">
                    <input type="hidden" name="interest" value="{slug}">
                    <button type="submit">Get Free Training Tips</button>
                </form>
            </section>
        </article>
    </main>
</body>
</html>
"""
    
    return html, title

def main():
    """Generate pilot batch of 20 breed × problem pages"""
    
    # Load data
    breeds = load_json('breeds.json')
    problems = load_json('behavior-problems.json')
    templates = load_json('breed-problem-templates.json')
    
    # Pilot batch: top 10 breeds × top 2 problems
    pilot_breeds = breeds[:10]
    pilot_problems = problems[:2]  # Barking and Jumping
    
    print("🐕 Generating CleverDogMethod Breed × Problem Pages (Pilot)")
    print(f"Breeds: {len(pilot_breeds)}")
    print(f"Problems: {len(pilot_problems)}")
    print(f"Total pages: {len(pilot_breeds) * len(pilot_problems)}\n")
    
    generated = []
    
    for breed in pilot_breeds:
        for problem in pilot_problems:
            template_key = f"{breed['slug']}-{problem['slug']}"
            
            if template_key not in templates:
                print(f"⚠️  No template for {template_key}, skipping...")
                continue
            
            template = templates[template_key]
            
            # Generate page
            html, title = generate_breed_problem_page(breed, problem, template)
            
            # Enhance with SEO features
            enhanced_html = enhance_post_html(
                html_content=html,
                title=title,
                category='breed-guides',
                subcategory=breed['slug'],
                url_path=f"/breed-guides/{breed['slug']}/{problem['slug']}/",
                related_posts=[
                    {'title': f'{breed["name"]} Training Guide', 'url': f'/breed-guides/{breed["slug"]}/'},
                    {'title': f'General {problem["name"]} Solutions', 'url': f'/behavior-problems/{problem["slug"]}/'},
                ]
            )
            
            # Save file
            output_path = OUTPUT_DIR / breed['slug'] / f"{problem['slug']}.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(enhanced_html)
            
            generated.append({
                'breed': breed['name'],
                'problem': problem['name'],
                'path': str(output_path.relative_to(WORKSPACE))
            })
            
            print(f"✅ Generated: {breed['name']} × {problem['name']}")
    
    print(f"\n🎉 Successfully generated {len(generated)} pages!")
    print(f"📁 Output: {OUTPUT_DIR}")
    
    # Save manifest
    manifest_path = OUTPUT_DIR / 'programmatic-manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(generated, f, indent=2)
    
    print(f"📝 Manifest saved: {manifest_path}")

if __name__ == '__main__':
    main()
