#!/usr/bin/env python3
"""
Generate Shopify OAuth install URL for VitaliZen
"""

import json
from pathlib import Path
from urllib.parse import urlencode

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
CLIENT_ID = creds['client_id']

# All scopes
SCOPES = [
    "read_products", "write_products",
    "read_product_listings",
    "read_orders", "write_orders",
    "read_customers", "write_customers",
    "read_content", "write_content",
    "read_themes", "write_themes",
    "read_script_tags", "write_script_tags",
    "read_fulfillments", "write_fulfillments",
    "read_shipping", "write_shipping",
    "read_inventory", "write_inventory",
    "read_price_rules", "write_price_rules",
    "read_marketing_events", "write_marketing_events",
    "read_resource_feedbacks", "write_resource_feedbacks",
    "read_analytics",
    "read_checkouts", "write_checkouts",
]

# OAuth params
params = {
    "client_id": CLIENT_ID,
    "scope": ",".join(SCOPES),
    "redirect_uri": f"https://{SHOP_DOMAIN}/admin/oauth/redirect",
    "state": "vitalizen-oauth-2026",
    "grant_options[]": "per-user"
}

install_url = f"https://{SHOP_DOMAIN}/admin/oauth/authorize?{urlencode(params)}"

print("\n" + "="*70)
print("🔐 SHOPIFY OAUTH INSTALL URL")
print("="*70)
print(f"\nStore: {SHOP_DOMAIN}")
print(f"Client ID: {CLIENT_ID[:20]}...")
print("\n" + "="*70)
print("STEP 1: Install the app")
print("="*70)
print("\n📋 Copy this URL and open it in your browser:\n")
print(install_url)
print("\n" + "="*70)
print("STEP 2: Authorize")
print("="*70)
print("\n1. Click 'Install app' or 'Authorize'")
print("2. After redirect, copy the FULL URL from your browser")
print("3. The URL will contain: ...?code=XXXXX&...")
print("4. Paste that FULL URL here")
print("\n" + "="*70)
print("Waiting for authorization...")
print("="*70)
