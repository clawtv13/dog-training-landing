#!/usr/bin/env python3
"""
Exchange authorization code for access token
"""

import requests
import json
from pathlib import Path

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

print("\n" + "="*70)
print("🔐 SHOPIFY TOKEN EXCHANGE")
print("="*70)

print("\nSince the app is now installed, we can exchange the authorization code")
print("for an access token.")

print("\n" + "="*70)
print("STEP 1: Get the authorization code")
print("="*70)

print("\nVisit this URL in your browser:")
print(f"\nhttps://{SHOP_DOMAIN}/admin/apps")

print("\nYou should see your installed app. The fact that it's installed means")
print("Shopify already has an access token for it.")

print("\n" + "="*70)
print("OPTION A: Get Admin API Access Token (Easiest)")
print("="*70)

print("\n1. In Shopify Admin, go to: Settings → Apps and sales channels")
print("2. Click 'Develop apps'")
print("3. Click your app name")
print("4. Go to 'API credentials' tab")
print("5. Find 'Admin API access token'")
print("6. Copy that token")

token = input("\nPaste the Admin API access token here: ").strip()

if token:
    if token.startswith('shpat_'):
        print("\n✅ Token received!")
        
        # Test it
        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }
        
        url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                shop = response.json()['shop']
                
                print("\n✅ TOKEN WORKS!")
                print("="*70)
                print(f"Shop: {shop['name']}")
                print(f"Domain: {shop['domain']}")
                print(f"Email: {shop['email']}")
                
                # Save it
                creds['access_token'] = token
                creds['api_version'] = '2024-01'
                
                with open(CREDS_FILE, 'w') as f:
                    json.dump(creds, f, indent=2)
                
                print(f"\n💾 Saved to: {CREDS_FILE}")
                print("\n✅ SETUP COMPLETE!")
                
            else:
                print(f"\n❌ Token invalid: {response.status_code}")
                print(response.text[:200])
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("\n⚠️  Token should start with 'shpat_'")
        print(f"You entered: {token[:20]}...")
else:
    print("\n❌ No token provided")
