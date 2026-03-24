#!/usr/bin/env python3
"""
Fix VitaGlow template - add enhancements to correct template
"""

import requests
import json

STORE = "nmd84u-pc.myshopify.com"
TOKEN = "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"
API_VERSION = "2024-01"
BASE_URL = f"https://{STORE}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

THEME_ID = 199985955165

def main():
    print("🔧 Fixing VitaGlow template...")
    
    # Get the vitaglow template
    template_key = "templates/product.vitaglow.json"
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]={template_key}"
    
    print(f"\n1. Fetching: {template_key}")
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"   ❌ Template not found: {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    asset = response.json()['asset']
    template_content = asset['value']
    
    print(f"   ✅ Template found ({len(template_content)} chars)")
    
    # Parse JSON
    try:
        template_json = json.loads(template_content)
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON parse error: {e}")
        return
    
    # Add our section
    if 'sections' not in template_json:
        template_json['sections'] = {}
    
    # Add section
    template_json['sections']['vitalizen-enhancements'] = {
        "type": "vitalizen-enhancements",
        "settings": {}
    }
    
    # Add to order (at the end, before recommendations)
    if 'order' in template_json:
        if 'vitalizen-enhancements' not in template_json['order']:
            # Insert before last element (usually recommendations or related products)
            insert_pos = len(template_json['order']) - 1 if len(template_json['order']) > 1 else len(template_json['order'])
            template_json['order'].insert(insert_pos, 'vitalizen-enhancements')
            print(f"   ✅ Added to order at position {insert_pos}")
    
    # Convert back to JSON
    new_content = json.dumps(template_json, indent=2)
    
    # Update template
    print(f"\n2. Updating template...")
    update_url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    update_data = {
        "asset": {
            "key": template_key,
            "value": new_content
        }
    }
    
    update_response = requests.put(update_url, headers=HEADERS, json=update_data)
    
    if update_response.status_code == 200:
        print("   ✅ Template updated successfully!")
        print("\n3. Section added to order:")
        if 'order' in template_json:
            for i, section_id in enumerate(template_json['order']):
                marker = "⭐" if section_id == 'vitalizen-enhancements' else "  "
                print(f"   {marker} {i+1}. {section_id}")
        
        print("\n✅ DONE!")
        print("\n🌐 Refresh your product page:")
        print("   https://vitalizen.shop/products/vitaglow-pro-led-face-mask")
        print("\n⚠️  If changes not visible:")
        print("   1. Hard refresh (Ctrl+F5 or Cmd+Shift+R)")
        print("   2. Try incognito window")
        print("   3. Clear Shopify cache (can take 5-10 min)")
    else:
        print(f"   ❌ Update failed: {update_response.status_code}")
        print(f"   Response: {update_response.text}")

if __name__ == "__main__":
    main()
