#!/usr/bin/env python3
"""
Upload Cooling Relief Cap product to VitaliZen Shopify store
"""

import json
import requests
from pathlib import Path

# Load VitaliZen credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

STORE = creds['admin_domain']
ACCESS_TOKEN = creds.get('access_token')
API_VERSION = creds.get('api_version', '2024-01')

if not ACCESS_TOKEN:
    print("❌ No access token found. Run shopify-connect-vitalizen.py first.")
    exit(1)

print(f"🏪 Store: {STORE}")
print(f"🔑 Token: {ACCESS_TOKEN[:20]}...")

# Product data
product_data = {
    "title": "Cooling Relief Cap",
    "body_html": """<p><strong>Beat the heat and find your cool.</strong></p>

<p>The Cooling Relief Cap is engineered for ultimate comfort and rapid cooling. Whether you're battling a migraine, recovering from a workout, or simply seeking respite on a sweltering day, this cap is your personal oasis of chill.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Advanced Cooling Technology:</strong> Utilizes a proprietary gel-pack system that stays colder for longer, providing sustained relief.</li>
<li><strong>Ergonomic, Comfortable Fit:</strong> Designed with adjustable straps and premium materials for a secure, pressure-free fit. One size truly fits all.</li>
<li><strong>Versatile Application:</strong> Perfect for headache relief, post-exercise recovery, fever reduction, or general summer comfort.</li>
<li><strong>Durable & Reusable:</strong> Easily rechargeable in the freezer, ready whenever you need it. Made with high-quality, non-toxic materials.</li>
<li><strong>Sleek, Discreet Design:</strong> Wear it at home, during travel, or even discreetly under a hat for on-the-go relief.</li>
</ul>

<h3>How it Works:</h3>
<p>Simply freeze the internal gel pack for 2-3 hours. Once chilled, insert it into the cap and wear it. The cap's design ensures even distribution of cool therapy to key pressure points, promoting fast relief and relaxation.</p>

<p><strong>Stay cool. Feel better. Live cooler.</strong></p>

<p><em>Care Instructions: Hand wash cap. Remove gel pack before washing. Ensure gel pack is dry before refreezing.</em></p>""",
    "vendor": "VitaliZen",
    "product_type": "Wellness",
    "tags": "cooling, headache relief, migraine, wellness, recovery, summer",
    "status": "draft",  # Start as draft for review
    "options": [
        {
            "name": "Color",
            "values": ["Blue", "Grey", "Black"]
        }
    ],
    "variants": [
        {
            "option1": "Blue",
            "price": "29.99",
            "sku": "CRC-BLU-01",
            "inventory_management": "shopify",
            "inventory_quantity": 100
        },
        {
            "option1": "Grey", 
            "price": "29.99",
            "sku": "CRC-GRY-01",
            "inventory_management": "shopify",
            "inventory_quantity": 100
        },
        {
            "option1": "Black",
            "price": "29.99",
            "sku": "CRC-BLK-01",
            "inventory_management": "shopify",
            "inventory_quantity": 100
        }
    ],
    "metafields_global_title_tag": "Cooling Relief Cap - Instant Headache & Migraine Relief",
    "metafields_global_description_tag": "Beat the heat with the Cooling Relief Cap. Advanced cooling technology for headache relief, workout recovery, and all-day comfort. Reusable, comfortable, and discreet."
}

# Make API request
headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

url = f"https://{STORE}/admin/api/{API_VERSION}/products.json"

print("\n📦 Creating product: Cooling Relief Cap...")

try:
    response = requests.post(url, headers=headers, json={"product": product_data}, timeout=60)
    
    if response.status_code == 201:
        result = response.json()
        product = result['product']
        product_id = product['id']
        
        print(f"\n✅ PRODUCT CREATED!")
        print(f"   ID: {product_id}")
        print(f"   Title: {product['title']}")
        print(f"   Handle: {product['handle']}")
        print(f"   Status: {product['status']}")
        print(f"   Variants: {len(product['variants'])}")
        
        # Save product ID for later use
        output_file = Path("/root/.openclaw/workspace/content/shopify_data/cooling_relief_cap_created.json")
        with open(output_file, 'w') as f:
            json.dump({
                "product_id": product_id,
                "handle": product['handle'],
                "admin_url": f"https://{STORE}/admin/products/{product_id}",
                "created_at": product['created_at'],
                "variants": [{"id": v['id'], "sku": v['sku'], "option1": v['option1']} for v in product['variants']]
            }, f, indent=2)
        
        print(f"\n💾 Product details saved to: {output_file}")
        print(f"\n🔗 Edit in Shopify Admin:")
        print(f"   https://{STORE}/admin/products/{product_id}")
        
    elif response.status_code == 422:
        print(f"\n⚠️  Validation error: {response.status_code}")
        errors = response.json()
        print(json.dumps(errors, indent=2))
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
