#!/usr/bin/env python3
"""
Simple test - try accessing Shopify directly
"""

import requests
import json
from pathlib import Path

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_SECRET = creds['client_secret']

print(f"\n🧪 TESTING: {SHOP_DOMAIN}")
print("="*60)

# According to memory, Calmora worked with these credentials
# Let's try using client_secret as the access token directly

headers = {
    "X-Shopify-Access-Token": CLIENT_SECRET,
    "Content-Type": "application/json"
}

url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/products.json?limit=1"

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        products = response.json().get('products', [])
        print(f"\n✅ SUCCESS! Found {len(products)} products")
        
        if products:
            print(f"\nFirst product: {products[0]['title']}")
        
        # Save as working token
        creds['access_token'] = CLIENT_SECRET
        with open(CREDS_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        
        print(f"\n💾 Saved working token")
        
    else:
        print(f"\n❌ Failed: {response.status_code}")
        print(f"Error: {response.text[:300]}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
