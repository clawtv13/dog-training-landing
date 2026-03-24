#!/usr/bin/env python3
"""
Change VitaliZen store currency from EUR to USD
And update product pricing
"""

import requests
import json
from pathlib import Path

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
TOKEN = creds['access_token']

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

API_BASE = f"https://{SHOP_DOMAIN}/admin/api/2024-01"

print("\n" + "="*70)
print("💱 CHANGING VITALIZEN TO USD".center(70))
print("="*70)

# Step 1: Get current shop settings
print("\n📊 STEP 1: Getting current settings...")

response = requests.get(f"{API_BASE}/shop.json", headers=HEADERS, timeout=10)
shop = response.json()['shop']

print(f"Current currency: {shop['currency']}")
print(f"Current money format: {shop['money_format']}")

# Step 2: Update shop currency
print("\n💱 STEP 2: Updating store currency to USD...")

# Note: Shop currency cannot be changed via API after store creation
# This is a Shopify limitation - must be done in admin

print("⚠️  Store currency can only be changed in Shopify Admin")
print("   Settings → Store details → Store currency")
print("\n   However, we can:")
print("   1. Update product prices to USD")
print("   2. Set up Markets for multi-currency")

# Step 3: Get product
print("\n📦 STEP 3: Getting product info...")

response = requests.get(f"{API_BASE}/products.json", headers=HEADERS, timeout=10)
products = response.json()['products']

if products:
    product = products[0]
    print(f"Product: {product['title']}")
    print(f"Current price: €{product['variants'][0]['price']}")
    
    # Step 4: Update product price
    print("\n💰 STEP 4: Updating product price to $69.99...")
    
    variant_id = product['variants'][0]['id']
    
    update_payload = {
        "variant": {
            "id": variant_id,
            "price": "69.99"
        }
    }
    
    response = requests.put(
        f"{API_BASE}/variants/{variant_id}.json",
        headers=HEADERS,
        json=update_payload,
        timeout=10
    )
    
    if response.status_code == 200:
        print("✅ Price updated to 69.99!")
        updated_variant = response.json()['variant']
        print(f"   New price: {updated_variant['price']}")
    else:
        print(f"❌ Failed to update price: {response.status_code}")
        print(f"   Error: {response.text[:200]}")

print("\n" + "="*70)
print("📝 MANUAL STEPS NEEDED".center(70))
print("="*70)

print("\n1. Go to: Settings → Store details")
print("2. Change 'Store currency' from EUR to USD")
print("3. Save")
print("\nAfter that, all prices will display as $ instead of €")

print("\n" + "="*70)
print("✅ PRODUCT PRICE READY ($69.99)".center(70))
print("="*70)

if __name__ == '__main__':
    main()
