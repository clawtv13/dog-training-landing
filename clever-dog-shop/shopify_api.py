#!/usr/bin/env python3
"""Shopify API wrapper for Clever Dog Shop"""
import json
import requests
from typing import Any, Dict, Optional, List
import base64
from pathlib import Path

STORE = "8zzpeg-a0.myshopify.com"
CLIENT_ID = "757840172666fadda6c3e528a5efaacd"
CLIENT_SECRET = "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"
API_VERSION = "2025-01"

class ShopifyAPI:
    def __init__(self):
        self._token: Optional[str] = None
    
    def get_token(self) -> str:
        if self._token:
            return self._token
        r = requests.post(
            f"https://{STORE}/admin/oauth/access_token",
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            timeout=30,
        )
        r.raise_for_status()
        self._token = r.json()["access_token"]
        return self._token
    
    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        headers = kwargs.pop("headers", {})
        headers["X-Shopify-Access-Token"] = self.get_token()
        headers["Content-Type"] = "application/json"
        
        url = f"https://{STORE}/admin/api/{API_VERSION}/{endpoint}"
        r = requests.request(method, url, headers=headers, timeout=60, **kwargs)
        
        if r.status_code >= 400:
            print(f"Error {r.status_code}: {r.text}")
            r.raise_for_status()
        
        return r.json() if r.text else {}
    
    # Shop
    def get_shop(self) -> dict:
        return self.request("GET", "shop.json")
    
    def update_shop(self, data: dict) -> dict:
        return self.request("PUT", "shop.json", json={"shop": data})
    
    # Products
    def create_product(self, product: dict) -> dict:
        return self.request("POST", "products.json", json={"product": product})
    
    def get_products(self, limit: int = 50) -> dict:
        return self.request("GET", f"products.json?limit={limit}")
    
    def update_product(self, product_id: int, data: dict) -> dict:
        return self.request("PUT", f"products/{product_id}.json", json={"product": data})
    
    def delete_product(self, product_id: int) -> dict:
        return self.request("DELETE", f"products/{product_id}.json")
    
    # Collections
    def create_collection(self, collection: dict) -> dict:
        return self.request("POST", "custom_collections.json", json={"custom_collection": collection})
    
    def get_collections(self) -> dict:
        return self.request("GET", "custom_collections.json")
    
    def add_product_to_collection(self, collection_id: int, product_id: int) -> dict:
        return self.request("POST", "collects.json", json={
            "collect": {"collection_id": collection_id, "product_id": product_id}
        })
    
    # Pages
    def create_page(self, title: str, body_html: str, handle: str = None) -> dict:
        page = {"title": title, "body_html": body_html}
        if handle:
            page["handle"] = handle
        return self.request("POST", "pages.json", json={"page": page})
    
    def get_pages(self) -> dict:
        return self.request("GET", "pages.json")
    
    def update_page(self, page_id: int, data: dict) -> dict:
        return self.request("PUT", f"pages/{page_id}.json", json={"page": data})
    
    # Themes
    def get_themes(self) -> dict:
        return self.request("GET", "themes.json")
    
    def get_theme_asset(self, theme_id: int, asset_key: str) -> dict:
        return self.request("GET", f"themes/{theme_id}/assets.json?asset[key]={asset_key}")
    
    def update_theme_asset(self, theme_id: int, asset_key: str, value: str) -> dict:
        return self.request("PUT", f"themes/{theme_id}/assets.json", json={
            "asset": {"key": asset_key, "value": value}
        })
    
    # Metafields (for settings)
    def create_metafield(self, namespace: str, key: str, value: str, type: str = "single_line_text_field") -> dict:
        return self.request("POST", "metafields.json", json={
            "metafield": {
                "namespace": namespace,
                "key": key,
                "value": value,
                "type": type
            }
        })
    
    # Policies
    def get_policies(self) -> dict:
        return self.request("GET", "policies.json")


# Initialize
api = ShopifyAPI()

if __name__ == "__main__":
    # Test connection
    shop = api.get_shop()
    print(json.dumps(shop, indent=2))
