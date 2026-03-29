#!/usr/bin/env python3
"""
Add product to Shopify collection
"""

import json
import requests
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
COLLECTION_ID = 703486394717  # ID for "Página de inicio"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

url = f"https://{STORE}/admin/api/{API_VERSION}/collects.json"

payload = {
    "collect": {
        "collection_id": COLLECTION_ID,
        "product_id": PRODUCT_ID
    }
}

print(f"➕ Adding product {PRODUCT_ID} to collection {COLLECTION_ID}...")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 201:
        result = response.json()
        collect_id = result['collect']['id']
        print(f"✅ Product added to collection. Collect ID: {collect_id}")
        
        # Optionally save this info if needed later
        product_info['collected_in'] = COLLECTION_ID
        with open(PRODUCT_FILE, 'w') as f:
            json.dump(product_info, f, indent=2)
        print(f"💾 Updated product info with collection data: {PRODUCT_FILE}")
        
    elif response.status_code == 422:
        # This often means the product is already in the collection
        error_details = response.json()
        print(f"⚠️  Validation error: {response.status_code}")
        print(f"   Details: {error_details.get('errors', 'Unknown error')}")
        if "already exist" in str(error_details):
            print("   Product may already be in this collection.")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
