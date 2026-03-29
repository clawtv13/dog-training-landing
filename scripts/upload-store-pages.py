#!/usr/bin/env python3
"""
Upload policy/info pages to VitaliZen Shopify store
"""

import json
import requests
from pathlib import Path

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-vitalizen.json")
with open(CREDS_FILE) as f:
    creds = json.load(f)

STORE = creds['admin_domain']
ACCESS_TOKEN = creds['access_token']
API_VERSION = creds.get('api_version', '2024-01')

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def create_page(title, body_html, handle=None):
    url = f"https://{STORE}/admin/api/{API_VERSION}/pages.json"
    page_data = {"title": title, "body_html": body_html}
    if handle:
        page_data["handle"] = handle
    
    response = requests.post(url, headers=headers, json={"page": page_data}, timeout=60)
    return response

def markdown_to_html(md_content):
    """Basic markdown to HTML conversion"""
    import re
    html = md_content
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Lists
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f"<li>{line.strip()[2:]}</li>")
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            if line.strip():
                if not line.startswith('<h'):
                    new_lines.append(f"<p>{line}</p>")
                else:
                    new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    return '\n'.join(new_lines)

print(f"🏪 Store: {STORE}")
print("\n📄 Uploading store pages...")

# Read and upload pages
pages = [
    {"file": "policy_privacy.md", "title": "Privacy Policy", "handle": "privacy-policy"},
    {"file": "policy_refund.md", "title": "Refund Policy", "handle": "refund-policy"},
    {"file": "policy_shipping.md", "title": "Shipping Policy", "handle": "shipping-policy"},
    {"file": "policy_terms.md", "title": "Terms of Service", "handle": "terms-of-service"},
]

created = []
for page in pages:
    filepath = Path(f"/root/.openclaw/workspace/{page['file']}")
    if not filepath.exists():
        print(f"   ⚠️  {page['file']} not found")
        continue
    
    with open(filepath) as f:
        content = f.read()
    
    # Replace "Calmora" with store name if needed
    content = content.replace("Calmora", "VitaliZen")
    
    html = markdown_to_html(content)
    
    response = create_page(page['title'], html, page['handle'])
    
    if response.status_code in [200, 201]:
        result = response.json()
        page_id = result['page']['id']
        print(f"   ✅ {page['title']} created (ID: {page_id})")
        created.append({"id": page_id, "title": page['title'], "handle": page['handle']})
    elif response.status_code == 422:
        # Might already exist
        print(f"   ⚠️  {page['title']}: {response.json().get('errors', 'already exists or validation error')}")
    else:
        print(f"   ❌ {page['title']} failed: {response.status_code}")

print(f"\n📊 Created {len(created)} pages")

# Save results
if created:
    output = Path("/root/.openclaw/workspace/content/shopify_data/store_pages_created.json")
    with open(output, 'w') as f:
        json.dump(created, f, indent=2)
    print(f"💾 Saved to: {output}")
