#!/usr/bin/env python3
"""
Shopify Client Credentials Grant
Get access token using client_id + client_secret
"""

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

def get_access_token():
    """
    Get access token using client credentials grant
    """
    
    url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    print("\n🔐 REQUESTING ACCESS TOKEN")
    print("="*60)
    print(f"Store: {SHOP_DOMAIN}")
    print(f"Client ID: {CLIENT_ID[:20]}...")
    print(f"Grant type: client_credentials")
    print()
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            
            access_token = token_data['access_token']
            scopes = token_data['scope']
            expires_in = token_data.get('expires_in', 86399)
            
            print("\n✅ ACCESS TOKEN OBTAINED!")
            print("="*60)
            print(f"Token: {access_token[:30]}...")
            print(f"Scopes: {scopes}")
            print(f"Expires in: {expires_in} seconds ({expires_in//3600} hours)")
            
            # Save token
            creds['access_token'] = access_token
            creds['scopes'] = scopes
            creds['token_expires_at'] = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
            creds['api_version'] = '2024-01'
            
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            print(f"\n💾 Saved to: {CREDS_FILE}")
            
            return access_token
            
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")
        return None

def test_token(token):
    """Test the access token"""
    
    print("\n🧪 TESTING ACCESS TOKEN")
    print("="*60)
    
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    # Test shop endpoint
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            shop = response.json()['shop']
            
            print("\n✅ TOKEN WORKS!")
            print("="*60)
            print(f"Shop Name: {shop['name']}")
            print(f"Domain: {shop['domain']}")
            print(f"Email: {shop['email']}")
            print(f"Currency: {shop['currency']}")
            print(f"Plan: {shop['plan_name']}")
            print(f"Country: {shop['country_name']}")
            
            return True
        else:
            print(f"\n❌ Token test failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error testing token: {e}")
        return False

def get_products(token):
    """Test getting products"""
    
    print("\n📦 FETCHING PRODUCTS")
    print("="*60)
    
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/products.json?limit=5"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            products = response.json()['products']
            
            print(f"\n✅ Found {len(products)} products:")
            print("="*60)
            
            for p in products:
                print(f"\n• {p['title']}")
                print(f"  ID: {p['id']}")
                print(f"  Status: {p['status']}")
                if p['variants']:
                    print(f"  Price: ${p['variants'][0]['price']}")
            
            return products
        else:
            print(f"\n❌ Failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    print("\n" + "="*60)
    print("🔐 SHOPIFY CLIENT CREDENTIALS AUTH".center(60))
    print("="*60)
    
    # Get access token
    token = get_access_token()
    
    if not token:
        print("\n❌ FAILED TO GET TOKEN")
        return False
    
    # Test token
    if not test_token(token):
        print("\n❌ TOKEN INVALID")
        return False
    
    # Get products as final test
    get_products(token)
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE - READY TO USE API".center(60))
    print("="*60)
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
