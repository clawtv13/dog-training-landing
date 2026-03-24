#!/usr/bin/env python3
"""
Try direct authentication methods for Shopify
"""

import requests
import json
import base64
from pathlib import Path

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

def try_basic_auth():
    """Try Basic Auth with client_id:client_secret"""
    print("\n1️⃣ Trying Basic Auth...")
    
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Basic Auth works!")
            return response.json()
        else:
            print(f"❌ Basic Auth failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def try_bearer_token():
    """Try using client_secret as Bearer token"""
    print("\n2️⃣ Trying Bearer token (client_secret)...")
    
    headers = {
        "Authorization": f"Bearer {CLIENT_SECRET}",
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Bearer token works!")
            return response.json()
        else:
            print(f"❌ Bearer token failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def try_token_exchange():
    """Try token exchange endpoint"""
    print("\n3️⃣ Trying token exchange...")
    
    url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Token exchange works!")
            return response.json()
        else:
            print(f"❌ Token exchange failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def try_storefront_api():
    """Try Storefront API (different endpoint)"""
    print("\n4️⃣ Trying Storefront API...")
    
    headers = {
        "X-Shopify-Storefront-Access-Token": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/api/2024-01/graphql.json"
    
    query = """
    {
        shop {
            name
            primaryDomain {
                url
            }
        }
    }
    """
    
    try:
        response = requests.post(url, json={"query": query}, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Storefront API works!")
            return response.json()
        else:
            print(f"❌ Storefront API failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def try_api_key_header():
    """Try X-Shopify-Access-Token with various formats"""
    print("\n5️⃣ Trying different header formats...")
    
    attempts = [
        CLIENT_SECRET,
        CLIENT_ID,
        f"{CLIENT_ID}:{CLIENT_SECRET}",
    ]
    
    for i, token in enumerate(attempts, 1):
        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }
        
        url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ Attempt {i} works! Token format: {token[:20]}...")
                return response.json()
            else:
                print(f"❌ Attempt {i} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Attempt {i} error: {e}")
    
    return None

def main():
    print("\n🔐 SHOPIFY AUTHENTICATION - ALL METHODS")
    print("="*60)
    print(f"Store: {SHOP_DOMAIN}")
    print(f"Client ID: {CLIENT_ID[:20]}...")
    print(f"Client Secret: {CLIENT_SECRET[:20]}...")
    
    methods = [
        try_basic_auth,
        try_bearer_token,
        try_token_exchange,
        try_storefront_api,
        try_api_key_header
    ]
    
    for method in methods:
        result = method()
        if result:
            print("\n" + "="*60)
            print("✅ SUCCESS!")
            print("="*60)
            print(json.dumps(result, indent=2))
            
            # Save working config
            creds['access_token'] = CLIENT_SECRET
            creds['auth_method'] = method.__name__
            
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            print(f"\n💾 Saved working config to: {CREDS_FILE}")
            return True
    
    print("\n" + "="*60)
    print("❌ ALL METHODS FAILED")
    print("="*60)
    print("\n📝 You need to:")
    print("1. Go to Shopify Admin → Apps → Develop apps")
    print("2. Find your custom app")
    print("3. Click 'API credentials' tab")
    print("4. Copy the 'Admin API access token' (starts with shpat_)")
    print("5. Give me that token")
    
    return False

if __name__ == '__main__':
    main()
