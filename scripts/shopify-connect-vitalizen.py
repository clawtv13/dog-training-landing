#!/usr/bin/env python3
"""
Connect to VitaliZen Shopify using client_id + client_secret
Same method we used for Calmora
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

print("\n🔐 CONNECTING TO VITALIZEN SHOPIFY")
print("="*60)
print(f"Store: {SHOP_DOMAIN}")
print(f"Client ID: {CLIENT_ID[:20]}...")

# Method 1: Use client_secret as access token (works for some custom apps)
print("\n1️⃣ Trying client_secret as direct access token...")

headers = {
    "X-Shopify-Access-Token": CLIENT_SECRET,
    "Content-Type": "application/json"
}

url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        shop = response.json()['shop']
        print(f"✅ CONNECTED! Shop: {shop['name']}")
        
        # Save token
        creds['access_token'] = CLIENT_SECRET
        with open(CREDS_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        
        print(f"💾 Token saved")
        exit(0)
    else:
        print(f"❌ Failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Method 2: Try without redirect - direct code exchange
print("\n2️⃣ Trying offline access token generation...")

token_url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"

# Try as if we already have a code
for grant_type in ["client_credentials", "refresh_token", None]:
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    if grant_type:
        payload["grant_type"] = grant_type
    
    try:
        response = requests.post(token_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            
            if access_token:
                print(f"✅ CONNECTED with grant_type={grant_type}!")
                print(f"Token: {access_token[:30]}...")
                
                # Save token
                creds['access_token'] = access_token
                with open(CREDS_FILE, 'w') as f:
                    json.dump(creds, f, indent=2)
                
                print(f"💾 Token saved")
                exit(0)
    except:
        pass

# Method 3: App installation URL with per-user grant
print("\n3️⃣ Installation URL needed...")
print("\nLa app está instalada pero necesito autorización.")
print("\nAbre esta URL en tu navegador:\n")

from urllib.parse import urlencode

params = {
    "client_id": CLIENT_ID,
    "scope": "read_products,write_products,read_orders,write_orders,read_customers,write_customers,read_content,write_content,read_themes,write_themes",
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",  # Out-of-band redirect
    "state": "vitalizen",
}

auth_url = f"https://{SHOP_DOMAIN}/admin/oauth/authorize?{urlencode(params)}"
print(auth_url)

print("\nDespués de autorizar, Shopify te mostrará un CÓDIGO.")
print("Copia ese código y ejecuta:")
print(f"\npython3 {__file__} CÓDIGO_AQUI")

# Check if code provided as argument
import sys
if len(sys.argv) > 1:
    code = sys.argv[1]
    print(f"\n🔄 Exchanging code: {code[:20]}...")
    
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
            
            print(f"✅ TOKEN OBTAINED!")
            print(f"Token: {access_token[:30]}...")
            
            # Test it
            headers = {
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json"
            }
            
            test = requests.get(url, headers=headers)
            
            if test.status_code == 200:
                shop = test.json()['shop']
                print(f"✅ Connected to: {shop['name']}")
                
                # Save
                creds['access_token'] = access_token
                with open(CREDS_FILE, 'w') as f:
                    json.dump(creds, f, indent=2)
                
                print(f"💾 Saved!")
                exit(0)
        else:
            print(f"❌ Exchange failed: {response.status_code}")
            print(response.text[:200])
    except Exception as e:
        print(f"❌ Error: {e}")
