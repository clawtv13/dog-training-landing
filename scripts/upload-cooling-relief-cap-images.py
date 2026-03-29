#!/usr/bin/env python3
"""
Upload images for Cooling Relief Cap product
"""

import json
import requests
import base64
from pathlib import Path

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")
with open(CREDS_FILE) as f:
    creds = json.load(f)

STORE = creds['admin_domain']
ACCESS_TOKEN = creds['access_token']
API_VERSION = creds.get('api_version', '2024-01')

# Load product info
PRODUCT_FILE = Path("/root/.openclaw/workspace/content/shopify_data/cooling_relief_cap_created.json")
with open(PRODUCT_FILE) as f:
    product_info = json.load(f)

PRODUCT_ID = product_info['product_id']

print(f"🏪 Store: {STORE}")
print(f"📦 Product ID: {PRODUCT_ID}")

# Image paths
IMAGE_DIR = Path("/root/.openclaw/workspace/uploaded_images/cooling-relief-cap")
images = [
    {"filename": "main.jpg", "alt": "Cooling Relief Cap - Main Product Image", "position": 1},
    {"filename": "lifestyle1.jpg", "alt": "Cooling Relief Cap - Lifestyle Image 1", "position": 2},
    {"filename": "lifestyle2.jpg", "alt": "Cooling Relief Cap - Lifestyle Image 2", "position": 3},
    {"filename": "feature.jpg", "alt": "Cooling Relief Cap - Feature Highlight", "position": 4},
    {"filename": "packaging.jpg", "alt": "Cooling Relief Cap - Packaging", "position": 5},
]

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("\n🖼️  Uploading images...")

uploaded = []
for img in images:
    filepath = IMAGE_DIR / img['filename']
    
    if not filepath.exists():
        print(f"   ⚠️  {img['filename']} not found, skipping")
        continue
    
    # Read and encode image
    with open(filepath, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Upload via API
    url = f"https://{STORE}/admin/api/{API_VERSION}/products/{PRODUCT_ID}/images.json"
    
    payload = {
        "image": {
            "attachment": image_data,
            "filename": img['filename'],
            "alt": img['alt'],
            "position": img['position']
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            image_id = result['image']['id']
            print(f"   ✅ {img['filename']} uploaded (ID: {image_id})")
            uploaded.append({
                "id": image_id,
                "filename": img['filename'],
                "src": result['image']['src']
            })
        else:
            print(f"   ❌ {img['filename']} failed: {response.status_code}")
            print(f"      {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ {img['filename']} error: {e}")

print(f"\n📊 Uploaded {len(uploaded)}/{len(images)} images")

# Update product info with image IDs
product_info['images'] = uploaded
with open(PRODUCT_FILE, 'w') as f:
    json.dump(product_info, f, indent=2)

print(f"💾 Updated: {PRODUCT_FILE}")
