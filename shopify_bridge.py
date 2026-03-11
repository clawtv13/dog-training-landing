#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict, Optional
import requests

API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2025-01")

class ShopifyBridge:
    def __init__(self):
        self.store = os.environ["SHOPIFY_STORE"].strip().replace("https://", "").rstrip("/")
        self.client_id = os.environ["SHOPIFY_CLIENT_ID"].strip()
        self.client_secret = os.environ["SHOPIFY_CLIENT_SECRET"].strip()
        self._token: Optional[str] = None

    def token(self) -> str:
        if self._token:
            return self._token
        r = requests.post(
            f"https://{self.store}/admin/oauth/access_token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=30,
        )
        r.raise_for_status()
        self._token = r.json()["access_token"]
        return self._token

    def request(self, method: str, path: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers["X-Shopify-Access-Token"] = self.token()
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")
        r = requests.request(
            method,
            f"https://{self.store}/admin/api/{API_VERSION}/{path.lstrip('/')}",
            headers=headers,
            timeout=30,
            **kwargs,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"{r.status_code}: {r.text}")
        if not r.text:
            return {}
        return r.json()

    def list_products(self, limit: int = 10):
        return self.request("GET", f"products.json?limit={limit}")

    def get_product(self, product_id: int):
        return self.request("GET", f"products/{product_id}.json")

    def update_product(self, product_id: int, fields: Dict[str, Any]):
        payload = {"product": {"id": product_id, **fields}}
        return self.request("PUT", f"products/{product_id}.json", json=payload)

    def list_pages(self, limit: int = 20):
        return self.request("GET", f"pages.json?limit={limit}")

    def create_page(self, title: str, body_html: str, handle: Optional[str] = None):
        page = {"title": title, "body_html": body_html}
        if handle:
            page["handle"] = handle
        return self.request("POST", "pages.json", json={"page": page})

    def list_themes(self):
        return self.request("GET", "themes.json")


def usage():
    print(
        "Usage:\n"
        "  python3 shopify_bridge.py list_products [limit]\n"
        "  python3 shopify_bridge.py get_product <product_id>\n"
        "  python3 shopify_bridge.py update_product <product_id> <json_fields>\n"
        "  python3 shopify_bridge.py list_pages [limit]\n"
        "  python3 shopify_bridge.py create_page <title> <body_html> [handle]\n"
        "  python3 shopify_bridge.py list_themes"
    )


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    bridge = ShopifyBridge()
    cmd = sys.argv[1]
    if cmd == "list_products":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        out = bridge.list_products(limit)
    elif cmd == "get_product":
        out = bridge.get_product(int(sys.argv[2]))
    elif cmd == "update_product":
        product_id = int(sys.argv[2])
        fields = json.loads(sys.argv[3])
        out = bridge.update_product(product_id, fields)
    elif cmd == "list_pages":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        out = bridge.list_pages(limit)
    elif cmd == "create_page":
        title = sys.argv[2]
        body_html = sys.argv[3]
        handle = sys.argv[4] if len(sys.argv) > 4 else None
        out = bridge.create_page(title, body_html, handle)
    elif cmd == "list_themes":
        out = bridge.list_themes()
    else:
        usage()
        sys.exit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
