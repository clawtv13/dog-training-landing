#!/usr/bin/env python3
"""
Complete OAuth flow for Shopify
"""

import requests
import json
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

print("\n" + "="*70)
print("🔐 SHOPIFY OAUTH - COMPLETE FLOW")
print("="*70)

print("\n❓ QUESTION: What is the redirect URI configured in your app?")
print("\nCommon options:")
print("1. https://vitalizen.shop/auth/callback")
print("2. https://vitalizen.shop/shopify/callback") 
print("3. Your local development URL (if testing)")

redirect_uri = input("\nEnter the redirect URI (or press Enter for option 1): ").strip()

if not redirect_uri:
    redirect_uri = "https://vitalizen.shop/auth/callback"

print(f"\n✅ Using redirect URI: {redirect_uri}")

# Build authorization URL
scopes = "read_products,write_products,read_orders,write_orders,read_customers,write_customers,read_content,write_content,read_themes,write_themes"

params = {
    "client_id": CLIENT_ID,
    "scope": scopes,
    "redirect_uri": redirect_uri,
    "state": "vitalizen-oauth"
}

auth_url = f"https://{SHOP_DOMAIN}/admin/oauth/authorize?{urlencode(params)}"

print("\n" + "="*70)
print("STEP 1: Authorize the app")
print("="*70)

print("\n📋 Open this URL in your browser:\n")
print(auth_url)

print("\n" + "="*70)
print("STEP 2: Get the code")
print("="*70)

print("\nAfter authorizing:")
print("1. You'll be redirected to: " + redirect_uri)
print("2. The URL will contain: ?code=XXXXX&...")
print("3. Copy the ENTIRE URL and paste it here")

redirect_url = input("\nPaste the full redirect URL: ").strip()

if redirect_url:
    # Extract code from URL
    parsed = urlparse(redirect_url)
    params = parse_qs(parsed.query)
    
    if 'code' in params:
        code = params['code'][0]
        print(f"\n✅ Authorization code extracted: {code[:20]}...")
        
        # Exchange code for token
        print("\n" + "="*70)
        print("STEP 3: Exchange code for access token")
        print("="*70)
        
        token_url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
        
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }
        
        try:
            response = requests.post(token_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data['access_token']
                scopes = token_data['scope']
                
                print("\n✅ ACCESS TOKEN OBTAINED!")
                print("="*70)
                print(f"Token: {access_token[:30]}...")
                print(f"Scopes: {scopes}")
                
                # Test it
                headers = {
                    "X-Shopify-Access-Token": access_token,
                    "Content-Type": "application/json"
                }
                
                test_url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
                test_response = requests.get(test_url, headers=headers, timeout=10)
                
                if test_response.status_code == 200:
                    shop = test_response.json()['shop']
                    print(f"\n✅ Connected to: {shop['name']}")
                    
                    # Save token
                    creds['access_token'] = access_token
                    creds['scopes'] = scopes
                    creds['api_version'] = '2024-01'
                    
                    with open(CREDS_FILE, 'w') as f:
                        json.dump(creds, f, indent=2)
                    
                    print(f"\n💾 Saved to: {CREDS_FILE}")
                    print("\n✅ SETUP COMPLETE!")
                else:
                    print(f"\n⚠️  Token works but API test failed: {test_response.status_code}")
                
            else:
                print(f"\n❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("\n❌ No 'code' parameter found in URL")
        print(f"URL parameters found: {list(params.keys())}")
else:
    print("\n❌ No URL provided")
