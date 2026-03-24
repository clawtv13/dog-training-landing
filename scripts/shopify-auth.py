#!/usr/bin/env python3
"""
Get Shopify API access token for VitaliZen store
Uses custom app credentials (client_id + client_secret)
"""

import requests
import json
from pathlib import Path

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

def get_access_token():
    """
    For custom apps with client_id/client_secret,
    Shopify uses admin API access tokens that are auto-generated
    when the app is installed.
    
    However, if this is a custom app, the access token should have
    been provided during app creation in Shopify admin.
    
    Let's try to get store info to verify credentials work.
    """
    
    # Try using client_secret as access token (common pattern)
    headers = {
        "X-Shopify-Access-Token": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    
    # Test API call
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            shop_data = response.json()
            print("✅ AUTHENTICATION SUCCESSFUL")
            print(f"\n📊 STORE INFO:")
            print(f"   Name: {shop_data['shop']['name']}")
            print(f"   Domain: {shop_data['shop']['domain']}")
            print(f"   Email: {shop_data['shop']['email']}")
            print(f"   Currency: {shop_data['shop']['currency']}")
            print(f"   Plan: {shop_data['shop']['plan_name']}")
            
            # Save token
            creds['access_token'] = CLIENT_SECRET
            creds['api_version'] = '2024-01'
            
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            print(f"\n💾 Access token saved to: {CREDS_FILE}")
            
            return CLIENT_SECRET
            
        elif response.status_code == 401:
            print("❌ AUTHENTICATION FAILED")
            print(f"   Status: {response.status_code}")
            print(f"   Error: Unauthorized - invalid credentials")
            print(f"\n📝 SOLUTION:")
            print("   1. Go to Shopify Admin → Apps → Develop apps")
            print("   2. Click your custom app")
            print("   3. Go to 'API credentials' tab")
            print("   4. Copy the 'Admin API access token' (starts with shpat_)")
            print("   5. Replace client_secret with that token")
            return None
            
        else:
            print(f"❌ API ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_api_access(token):
    """Test various API endpoints"""
    
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    print("\n🧪 TESTING API ENDPOINTS:")
    print("="*60)
    
    endpoints = [
        ("Products", f"https://{SHOP_DOMAIN}/admin/api/2024-01/products.json?limit=5"),
        ("Orders", f"https://{SHOP_DOMAIN}/admin/api/2024-01/orders.json?limit=5"),
        ("Customers", f"https://{SHOP_DOMAIN}/admin/api/2024-01/customers.json?limit=5"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get(name.lower(), []))
                print(f"✅ {name}: {count} found")
            else:
                print(f"❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")

if __name__ == '__main__':
    print("\n🔐 SHOPIFY API AUTHENTICATION")
    print("="*60)
    print(f"Store: {SHOP_DOMAIN}")
    print(f"Client ID: {CLIENT_ID[:20]}...")
    print()
    
    token = get_access_token()
    
    if token:
        test_api_access(token)
        print("\n✅ SETUP COMPLETE - Ready to use Shopify API")
    else:
        print("\n❌ SETUP FAILED - Check credentials")
