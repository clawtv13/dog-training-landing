#!/usr/bin/env python3
"""
Exchange authorization code for access token
"""

import requests
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

def exchange_code(code):
    """Exchange authorization code for access token"""
    
    url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
    
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    
    print("\n🔄 EXCHANGING CODE FOR TOKEN")
    print("="*60)
    print(f"Code: {code[:20]}...")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            scopes = token_data['scope']
            
            print("\n✅ ACCESS TOKEN OBTAINED!")
            print("="*60)
            print(f"Token: {access_token[:30]}...")
            print(f"Scopes: {scopes}")
            
            # Test token
            headers = {
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json"
            }
            
            test_url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
            test_response = requests.get(test_url, headers=headers, timeout=10)
            
            if test_response.status_code == 200:
                shop = test_response.json()['shop']
                
                print(f"\n✅ TOKEN WORKS!")
                print("="*60)
                print(f"Shop: {shop['name']}")
                print(f"Domain: {shop['domain']}")
                print(f"Email: {shop['email']}")
                print(f"Currency: {shop['currency']}")
                
                # Save token
                creds['access_token'] = access_token
                creds['scopes'] = scopes
                creds['api_version'] = '2024-01'
                
                with open(CREDS_FILE, 'w') as f:
                    json.dump(creds, f, indent=2)
                
                print(f"\n💾 Saved to: {CREDS_FILE}")
                print("\n✅ SETUP COMPLETE - READY TO USE SHOPIFY API!")
                
                return access_token
            else:
                print(f"\n⚠️  Token obtained but test failed: {test_response.status_code}")
                return access_token
                
        else:
            print(f"\n❌ Token exchange failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Code provided as argument
        code = sys.argv[1]
    else:
        # Extract from URL
        redirect_url = input("Paste the full redirect URL: ").strip()
        
        if redirect_url:
            parsed = urlparse(redirect_url)
            params = parse_qs(parsed.query)
            
            if 'code' in params:
                code = params['code'][0]
                print(f"\n✅ Code extracted: {code[:20]}...")
            else:
                print("\n❌ No 'code' parameter found in URL")
                sys.exit(1)
        else:
            print("\n❌ No URL provided")
            sys.exit(1)
    
    token = exchange_code(code)
    sys.exit(0 if token else 1)
