#!/usr/bin/env python3
"""
Complete audit of VitaliZen Shopify store
"""

import requests
import json
from pathlib import Path

CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']
TOKEN = creds['access_token']

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

API_BASE = f"https://{SHOP_DOMAIN}/admin/api/2024-01"

def get_shop_info():
    """Get store details"""
    response = requests.get(f"{API_BASE}/shop.json", headers=HEADERS, timeout=10)
    return response.json()['shop'] if response.status_code == 200 else None

def get_products():
    """Get all products"""
    response = requests.get(f"{API_BASE}/products.json", headers=HEADERS, timeout=10)
    return response.json().get('products', []) if response.status_code == 200 else []

def get_orders():
    """Get recent orders"""
    response = requests.get(f"{API_BASE}/orders.json?status=any&limit=50", headers=HEADERS, timeout=10)
    return response.json().get('orders', []) if response.status_code == 200 else []

def get_customers():
    """Get customer count"""
    response = requests.get(f"{API_BASE}/customers/count.json", headers=HEADERS, timeout=10)
    return response.json().get('count', 0) if response.status_code == 200 else 0

def get_themes():
    """Get themes"""
    response = requests.get(f"{API_BASE}/themes.json", headers=HEADERS, timeout=10)
    return response.json().get('themes', []) if response.status_code == 200 else []

def main():
    print("\n" + "="*70)
    print("🔍 VITALIZEN STORE AUDIT".center(70))
    print("="*70)
    
    # Shop Info
    print("\n📊 STORE INFO")
    print("="*70)
    shop = get_shop_info()
    if shop:
        print(f"Name: {shop['name']}")
        print(f"Domain: {shop['domain']}")
        print(f"Email: {shop['email']}")
        print(f"Currency: {shop['currency']}")
        print(f"Plan: {shop['plan_display_name']}")
        print(f"Country: {shop['country_name']}")
        print(f"Password: {'Enabled' if shop['password_enabled'] else 'Disabled'} ✅" if not shop['password_enabled'] else "⚠️  ENABLED (Store not public!)")
    
    # Products
    print("\n📦 PRODUCTS")
    print("="*70)
    products = get_products()
    print(f"Total products: {len(products)}")
    
    for p in products:
        status_icon = "✅" if p['status'] == 'active' else "⚠️"
        print(f"\n{status_icon} {p['title']}")
        print(f"   ID: {p['id']}")
        print(f"   Status: {p['status']}")
        print(f"   Variants: {len(p['variants'])}")
        
        if p['variants']:
            for v in p['variants']:
                price = v.get('price', 'N/A')
                inventory = v.get('inventory_quantity', 0)
                print(f"   • {v['title']}: €{price} (Stock: {inventory})")
        
        print(f"   Images: {len(p['images'])}")
        print(f"   Tags: {p['tags'] if p['tags'] else 'None'}")
    
    # Orders
    print("\n📈 ORDERS & ANALYTICS")
    print("="*70)
    orders = get_orders()
    print(f"Total orders: {len(orders)}")
    
    if orders:
        total_revenue = sum(float(o.get('total_price', 0)) for o in orders)
        print(f"Total revenue: €{total_revenue:.2f}")
        
        print(f"\nRecent orders:")
        for o in orders[:5]:
            print(f"• {o['created_at'][:10]} - €{o['total_price']} ({o['financial_status']})")
    else:
        print("⚠️  No orders yet")
    
    # Customers
    print("\n👥 CUSTOMERS")
    print("="*70)
    customer_count = get_customers()
    print(f"Total customers: {customer_count}")
    
    # Theme
    print("\n🎨 THEMES")
    print("="*70)
    themes = get_themes()
    
    active_theme = next((t for t in themes if t['role'] == 'main'), None)
    
    if active_theme:
        print(f"Active theme: {active_theme['name']}")
        print(f"Theme ID: {active_theme['id']}")
    
    print(f"Total themes: {len(themes)}")
    
    print("\n" + "="*70)
    print("✅ AUDIT COMPLETE".center(70))
    print("="*70)

if __name__ == '__main__':
    main()
