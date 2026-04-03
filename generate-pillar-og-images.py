#!/usr/bin/env python3
import replicate
import requests
import os

API_TOKEN = "r8_5aYrZi5JVECccCixGxuuCBQ0nUpsluA32YoMQ"
os.environ["REPLICATE_API_TOKEN"] = API_TOKEN

# Post configurations with titles
posts = [
    {
        "title": "The 51 ChatGPT Prompts\nThat Save Solopreneurs\n15 Hours Every Week",
        "subtitle": "Copy-paste ready • Save $800/month",
        "output": "ai-automation-blog/blog/images/og-chatgpt-prompts.png"
    },
    {
        "title": "How to Automate\nEmail Follow-Ups\nWithout Expensive CRM",
        "subtitle": "Free tools • 7-step tutorial • Save $200/month",
        "output": "ai-automation-blog/blog/images/og-email-automation.png"
    },
    {
        "title": "My $50/Month Tech Stack\nThat Replaces Your\n$500 SaaS Bill",
        "subtitle": "Save $5,208/year • Complete comparison guide",
        "output": "ai-automation-blog/blog/images/og-tech-stack.png"
    }
]

print("=" * 60)
print("🎨 GENERATING 3 OG IMAGES FOR PILLAR POSTS")
print("=" * 60)
print()

for idx, post in enumerate(posts, 1):
    print(f"📸 Image {idx}/3: {post['title'][:50]}...")
    
    prompt = f"""
A professional Open Graph social media image for a blog post.

Style: Modern, clean, high-contrast design
Background: Dark (#0A0A0B) with subtle gradient
Accent color: Lime green (#B9FF66)

Layout:
- Top left corner: Small "workless.build" logo text in lime
- Center: Main title in large, bold white text (Space Grotesk font style):
  "{post['title']}"
- Below title: Subtitle in lime green:
  "{post['subtitle']}"
- Bottom: Small decorative element or pattern in lime green

Typography: Bold, sans-serif, highly readable
Composition: Centered, balanced, professional
Quality: High resolution, sharp text, clean edges

NO photos, NO people, NO stock images
ONLY text and geometric design elements
"""
    
    try:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "output_format": "png",
                "num_outputs": 1
            }
        )
        
        image_url = output[0] if isinstance(output, list) else output
        
        print(f"   Downloading from: {image_url[:60]}...")
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(post['output']), exist_ok=True)
            with open(post['output'], 'wb') as f:
                f.write(response.content)
            
            size_kb = len(response.content) // 1024
            print(f"   ✅ Saved: {post['output']} ({size_kb}KB)")
        else:
            print(f"   ❌ Download failed: {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()

print("=" * 60)
print("✅ OG IMAGES GENERATION COMPLETE")
print("=" * 60)
