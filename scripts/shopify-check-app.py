#!/usr/bin/env python3
"""
Check Shopify app configuration
"""

import json
from pathlib import Path

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']

print("\n" + "="*70)
print("🔍 CHECKING APP CONFIGURATION")
print("="*70)
print(f"\nStore: {SHOP_DOMAIN}")
print(f"Client ID: {CLIENT_ID}")

print("\n" + "="*70)
print("POSSIBLE REDIRECT URIs:")
print("="*70)

# Common redirect URI patterns
redirect_options = [
    f"https://{SHOP_DOMAIN}/admin/apps",
    f"https://vitalizen.shop/auth/callback",
    f"https://vitalizen.shop/shopify/callback",
    f"https://{SHOP_DOMAIN}/admin",
    "https://localhost:3000/auth/callback",
]

for i, uri in enumerate(redirect_options, 1):
    print(f"\n{i}. {uri}")

print("\n" + "="*70)
print("NEED TO KNOW:")
print("="*70)
print("\n1. Where is this app configured?")
print("   - Shopify Partners Dashboard?")
print("   - Shopify Admin (Custom App)?")
print("   - External development environment?")

print("\n2. What is the 'App URL' or 'Allowed redirection URL(s)' in the app settings?")

print("\n" + "="*70)
print("ALTERNATIVE SOLUTION:")
print("="*70)
print("\nIf this is a CUSTOM APP created in Shopify Admin:")
print("1. Go to: Settings → Apps and sales channels")
print("2. Click 'Develop apps'")
print("3. Find your app")
print("4. Click 'API credentials' tab")
print("5. Look for 'Admin API access token'")
print("6. Copy that token (starts with shpat_)")
print("7. Paste it here:")

token_input = input("\nAdmin API access token (or press Enter to skip): ").strip()

if token_input.startswith('shpat_'):
    creds['access_token'] = token_input
    with open(CREDS_FILE, 'w') as f:
        json.dump(creds, f, indent=2)
    print("\n✅ Token saved!")
    print(f"📁 Saved to: {CREDS_FILE}")
    
    # Test it
    import requests
    headers = {
        "X-Shopify-Access-Token": token_input,
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            shop = response.json()['shop']
            print(f"\n✅ SUCCESS! Connected to: {shop['name']}")
        else:
            print(f"\n❌ Token invalid: {response.status_code}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
else:
    print("\n⏭️  Skipped token input")
