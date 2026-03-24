#!/usr/bin/env python3
"""
Shopify OAuth flow for VitaliZen store
Uses client_id + client_secret to get access token
"""

import requests
import json
from pathlib import Path
from urllib.parse import urlencode

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
SHOP_NAME = SHOP_DOMAIN.replace('.myshopify.com', '')
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

def get_install_url():
    """
    Generate OAuth install URL
    User needs to visit this URL to authorize the app
    """
    
    scopes = "read_products,write_products,read_orders,write_orders,read_customers,write_customers,read_content,write_content,read_themes,write_themes"
    redirect_uri = "https://vitalizen.shop/admin/oauth/callback"  # Adjust if needed
    
    params = {
        "client_id": CLIENT_ID,
        "scope": scopes,
        "redirect_uri": redirect_uri,
        "state": "vitalizen-auth-2026"
    }
    
    install_url = f"https://{SHOP_DOMAIN}/admin/oauth/authorize?{urlencode(params)}"
    
    return install_url

def exchange_code_for_token(code):
    """
    Exchange authorization code for access token
    """
    
    url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            
            print("✅ ACCESS TOKEN OBTAINED")
            print(f"   Token: {access_token[:20]}...")
            
            # Save token
            creds['access_token'] = access_token
            creds['api_version'] = '2024-01'
            
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            print(f"💾 Saved to: {CREDS_FILE}")
            
            return access_token
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def check_custom_app_token():
    """
    For custom apps, the token might already be available
    in Shopify admin without OAuth flow
    """
    
    print("\n🔍 CHECKING IF CUSTOM APP...")
    print("="*60)
    
    # Try using client_secret as potential admin token
    # (Some custom apps work this way)
    
    headers = {
        "X-Shopify-Access-Token": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ CLIENT_SECRET WORKS AS ACCESS TOKEN!")
            
            creds['access_token'] = CLIENT_SECRET
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            return True
        else:
            print("❌ Client secret is not a valid access token")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n🔐 SHOPIFY OAUTH SETUP")
    print("="*60)
    print(f"Store: {SHOP_DOMAIN}")
    print(f"Client ID: {CLIENT_ID[:20]}...")
    
    # First, check if this is a custom app where client_secret works
    if check_custom_app_token():
        print("\n✅ AUTHENTICATION SUCCESSFUL")
        print("   Using client_secret as access token")
        return
    
    print("\n📝 OAUTH FLOW REQUIRED")
    print("="*60)
    print("\nYou need to authorize the app. Two options:\n")
    
    print("OPTION A: Get Admin API Access Token (Easiest)")
    print("-" * 60)
    print("1. Go to: https://admin.shopify.com/store/{}/apps".format(SHOP_NAME))
    print("2. Click 'Develop apps' (or 'App development')")
    print("3. Find your custom app")
    print("4. Click 'API credentials' tab")
    print("5. Look for 'Admin API access token'")
    print("6. Copy that token (starts with shpat_)")
    print("7. Paste it here when I ask for it")
    
    print("\n\nOPTION B: OAuth Flow (More complex)")
    print("-" * 60)
    print("1. Visit this URL in your browser:")
    print(f"   {get_install_url()}")
    print("2. Authorize the app")
    print("3. Copy the 'code' parameter from redirect URL")
    print("4. Paste it here")
    
    print("\n\n❓ Which option do you prefer?")
    print("   Type 'A' for Admin API token")
    print("   Type 'B' for OAuth flow")
    print("   Type 'Q' to quit")
    
    choice = input("\nChoice: ").strip().upper()
    
    if choice == 'A':
        print("\n📋 Paste your Admin API access token here:")
        token = input("Token: ").strip()
        
        if token.startswith('shpat_'):
            creds['access_token'] = token
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            
            print("\n✅ Token saved!")
            print("   Testing API access...")
            
            # Test it
            headers = {
                "X-Shopify-Access-Token": token,
                "Content-Type": "application/json"
            }
            
            url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                shop = response.json()['shop']
                print(f"\n✅ SUCCESS! Connected to: {shop['name']}")
            else:
                print(f"\n❌ Token invalid: {response.status_code}")
        else:
            print("❌ Invalid token format (should start with shpat_)")
    
    elif choice == 'B':
        print("\n📋 Paste the authorization code here:")
        code = input("Code: ").strip()
        
        token = exchange_code_for_token(code)
        
        if token:
            print("✅ OAuth successful!")
        else:
            print("❌ OAuth failed")
    
    else:
        print("Exiting...")

if __name__ == '__main__':
    main()
