#!/usr/bin/env python3
"""Generate images using OpenRouter API"""

import requests
import json
import base64
from pathlib import Path

API_KEY = "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"
PROMPTS_FILE = "/root/.openclaw/workspace/content/cleverdogmethod/image-prompts.md"
OUTPUT_DIR = Path("/root/.openclaw/workspace/dog-training-landing-clean/blog/images")

def generate_image(prompt, filename):
    """Generate image via OpenRouter"""
    
    response = requests.post(
        "https://openrouter.ai/api/v1/images/generations",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "black-forest-labs/flux-pro",
            "prompt": prompt,
            "n": 1,
            "size": "1200x630"
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['data'][0]['url']
        
        # Download image
        img_response = requests.get(image_url)
        output_path = OUTPUT_DIR / filename
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✅ {filename}")
        return True
    else:
        print(f"❌ {filename}: {response.status_code}")
        return False

print("🎨 Generating CleverDogMethod featured images...")
print("Using: black-forest-labs/flux-pro via OpenRouter\n")

# Parse prompts
with open(PROMPTS_FILE, 'r') as f:
    content = f.read()

# Extract prompts (simple parsing)
import re
prompts = re.findall(r'###\s+\d+\.\s+(.*?)\n```\n(.*?)\n```', content, re.DOTALL)

generated = 0
for title, prompt in prompts[:5]:  # Start with first 5
    filename = title.lower().replace(' ', '-')[:40] + '.jpg'
    if generate_image(prompt.strip(), filename):
        generated += 1

print(f"\n✅ Generated {generated}/5 images")
