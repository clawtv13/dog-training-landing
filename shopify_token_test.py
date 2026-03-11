#!/usr/bin/env python3
import os
import sys
import json
import requests

store = os.environ.get("SHOPIFY_STORE", "").strip()
client_id = os.environ.get("SHOPIFY_CLIENT_ID", "").strip()
client_secret = os.environ.get("SHOPIFY_CLIENT_SECRET", "").strip()

missing = [k for k,v in {
    'SHOPIFY_STORE': store,
    'SHOPIFY_CLIENT_ID': client_id,
    'SHOPIFY_CLIENT_SECRET': client_secret,
}.items() if not v]
if missing:
    print("Missing env vars:", ", ".join(missing), file=sys.stderr)
    sys.exit(1)

if store.startswith('https://'):
    store = store.split('://',1)[1]
store = store.rstrip('/')

resp = requests.post(
    f"https://{store}/admin/oauth/access_token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
    timeout=30,
)
print("TOKEN_STATUS", resp.status_code)
if resp.status_code != 200:
    print(resp.text)
    sys.exit(2)

data = resp.json()
access_token = data.get("access_token")
print("SCOPES", data.get("scope"))
print("EXPIRES_IN", data.get("expires_in"))

api = requests.get(
    f"https://{store}/admin/api/2025-01/products.json?limit=3",
    headers={"X-Shopify-Access-Token": access_token},
    timeout=30,
)
print("API_STATUS", api.status_code)
if api.status_code != 200:
    print(api.text)
    sys.exit(3)

products = api.json().get("products", [])
print(json.dumps({
    "ok": True,
    "products_found": len(products),
    "products": [
        {
            "id": p.get("id"),
            "title": p.get("title"),
            "handle": p.get("handle"),
            "status": p.get("status"),
        }
        for p in products
    ]
}, ensure_ascii=False, indent=2))
