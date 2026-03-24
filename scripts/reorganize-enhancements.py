#!/usr/bin/env python3
"""
Reorganize VitaliZen enhancements - split into separate sections
and insert at correct positions
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

# Individual enhancement sections
ENHANCEMENTS = {
    "vz-price-comparison": {
        "code": '''
<div class="vz-comparison-enhanced" style="margin: 60px 0;">
  <h2 style="text-align: center; font-size: 32px; font-weight: 800; margin-bottom: 40px;">
    VitaGlow Pro vs. Competitors
  </h2>
  <table style="width: 100%; max-width: 800px; margin: 0 auto; border-collapse: collapse; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
    <thead>
      <tr style="background: #667eea; color: white;">
        <th style="padding: 20px; text-align: left; font-size: 18px; border: 1px solid #ddd;">Feature</th>
        <th style="padding: 20px; text-align: center; font-size: 18px; border: 1px solid #ddd;">VitaGlow Pro ✅</th>
        <th style="padding: 20px; text-align: center; font-size: 18px; border: 1px solid #ddd;">Leading Brands</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background: #f8f9fa;">
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">💰 Price</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center; color: #28a745; font-weight: 700; font-size: 20px;">$69.99</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center; color: #dc3545; text-decoration: line-through;">$400-500+</td>
      </tr>
      <tr>
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">🌈 Wavelengths</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">7 colors</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">2-3 colors</td>
      </tr>
      <tr style="background: #f8f9fa;">
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">👔 Includes Neck</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">✅ Yes (included)</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">❌ Extra $400+</td>
      </tr>
      <tr>
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">🔬 Clinical Research</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">✅ Yes</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">✅ Yes</td>
      </tr>
      <tr style="background: #f8f9fa;">
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">🔋 Battery Life</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">1200mAh</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">Variable</td>
      </tr>
      <tr>
        <td style="padding: 16px; border: 1px solid #ddd; font-weight: 600;">🛡️ Guarantee</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">90-Day</td>
        <td style="padding: 16px; border: 1px solid #ddd; text-align: center;">30-Day</td>
      </tr>
    </tbody>
  </table>
  <p style="text-align: center; margin-top: 32px; font-size: 18px; color: #666;">
    <strong style="color: #28a745;">You save $330-430</strong> vs. leading brands
  </p>
</div>
''',
        "position": "after:comparison_table_7TPgji"
    },
    
    "vz-cta-purple": {
        "code": '''
<div class="vz-cta-block" style="
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
  margin: 40px 0;
">
  <h2 style="font-size: 36px; font-weight: 800; margin-bottom: 16px;">
    Ready to Transform Your Skin?
  </h2>
  <p style="font-size: 20px; margin-bottom: 32px; opacity: 0.9;">
    Join 1,200+ customers who already made the switch
  </p>
  <a href="#MainContent" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); return false;" class="vz-cta-button" style="
    display: inline-block;
    background: white;
    color: #764ba2;
    padding: 18px 48px;
    font-size: 20px;
    font-weight: 700;
    border-radius: 50px;
    text-decoration: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.2s;
  " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
    Get Yours Now — $69.99
  </a>
  <div style="margin-top: 24px; font-size: 14px; opacity: 0.8;">
    🚚 Free Shipping | 🛡️ 90-Day Guarantee | ⭐ Trusted by 1,200+
  </div>
</div>
''',
        "position": "after:image_slider_QLWBKA"
    },
    
    "vz-countdown": {
        "code": '''
<div class="vz-countdown" style="
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 20px;
  text-align: center;
  border-radius: 12px;
  margin: 40px 20px;
  box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
">
  <div style="font-size: 18px; font-weight: 600; margin-bottom: 12px;">
    🔥 SPRING SALE ENDS IN:
  </div>
  <div id="vzCountdown" style="
    font-size: 36px;
    font-weight: 800;
    font-family: 'Courier New', monospace;
    letter-spacing: 4px;
  ">
    00:00:00
  </div>
  <div style="font-size: 14px; margin-top: 12px; opacity: 0.9;">
    Don't miss 30% off — Back to $99 after timer ends
  </div>
</div>

<script>
  function updateCountdown() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setHours(24, 0, 0, 0);
    const diff = tomorrow - now;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    const elem = document.getElementById('vzCountdown');
    if(elem) {
      elem.textContent = String(hours).padStart(2, '0') + ':' + 
        String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
    }
  }
  updateCountdown();
  setInterval(updateCountdown, 1000);
</script>
''',
        "position": "before:testimonials_eBpEXx"
    },
    
    "vz-sticky-cart": {
        "code": '''
<style>
  .vz-sticky-cart {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
    padding: 16px 20px;
    display: none;
    align-items: center;
    justify-content: space-between;
    z-index: 9999;
    animation: slideUp 0.3s ease-out;
  }
  
  @keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
  
  .vz-sticky-cart.visible {
    display: flex;
  }
  
  .vz-sticky-cart-info {
    flex: 1;
  }
  
  .vz-sticky-cart-title {
    font-size: 14px;
    font-weight: 600;
    color: #333;
    margin: 0 0 4px 0;
  }
  
  .vz-sticky-cart-price {
    font-size: 18px;
    font-weight: 700;
    color: #28a745;
    margin: 0;
  }
  
  .vz-sticky-cart-button {
    background: #667eea;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .vz-sticky-cart-button:hover {
    background: #5568d3;
  }
  
  @media (min-width: 769px) {
    .vz-sticky-cart {
      display: none !important;
    }
  }
</style>

<div class="vz-sticky-cart" id="vzStickyCart">
  <div class="vz-sticky-cart-info">
    <p class="vz-sticky-cart-title">VitaGlow Pro LED Mask</p>
    <p class="vz-sticky-cart-price">$69.99</p>
  </div>
  <button class="vz-sticky-cart-button" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
    Add to Cart ↑
  </button>
</div>

<script>
  if (window.innerWidth <= 768) {
    window.addEventListener('scroll', function() {
      const stickyCart = document.getElementById('vzStickyCart');
      if (stickyCart && window.pageYOffset > 500) {
        stickyCart.classList.add('visible');
      } else if(stickyCart) {
        stickyCart.classList.remove('visible');
      }
    });
  }
</script>
''',
        "position": "end"
    },
    
    "vz-exit-popup": {
        "code": '''
<style>
  .vz-exit-popup {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    z-index: 10000;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.3s;
  }
  
  .vz-exit-popup.show {
    display: flex;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .vz-exit-content {
    background: white;
    padding: 40px;
    border-radius: 16px;
    max-width: 500px;
    text-align: center;
    position: relative;
    animation: slideDown 0.4s;
  }
  
  @keyframes slideDown {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  .vz-exit-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    font-size: 32px;
    cursor: pointer;
    color: #999;
    line-height: 1;
  }
  
  .vz-exit-close:hover {
    color: #333;
  }
</style>

<div class="vz-exit-popup" id="vzExitPopup">
  <div class="vz-exit-content">
    <button class="vz-exit-close" onclick="document.getElementById('vzExitPopup').classList.remove('show')">&times;</button>
    <h2 style="font-size: 32px; font-weight: 800; margin-bottom: 16px; color: #333;">
      Wait! Don't Leave Yet 👋
    </h2>
    <p style="font-size: 18px; color: #666; margin-bottom: 24px;">
      Get <strong style="color: #f5576c;">15% off</strong> your first VitaGlow Pro
    </p>
    <div style="margin-bottom: 24px;">
      <input type="email" placeholder="Enter your email" required style="
        width: 100%;
        padding: 16px;
        font-size: 16px;
        border: 2px solid #ddd;
        border-radius: 8px;
        margin-bottom: 16px;
      ">
      <button onclick="alert('Check your email for 15% off code!'); document.getElementById('vzExitPopup').classList.remove('show');" style="
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px;
        font-size: 18px;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      ">
        Get My 15% Off Code
      </button>
    </div>
    <p style="font-size: 12px; color: #999;">
      Plus: Free skincare tips & exclusive deals
    </p>
  </div>
</div>

<script>
  let exitIntentShown = false;
  if (window.innerWidth > 768) {
    document.addEventListener('mouseleave', function(e) {
      const popup = document.getElementById('vzExitPopup');
      if (e.clientY < 50 && !exitIntentShown && popup) {
        popup.classList.add('show');
        exitIntentShown = true;
      }
    });
    
    const popup = document.getElementById('vzExitPopup');
    if(popup) {
      popup.addEventListener('click', function(e) {
        if (e.target === this) {
          this.classList.remove('show');
        }
      });
    }
  }
</script>
''',
        "position": "end"
    }
}

def create_section(section_name, code):
    """Create individual section"""
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    
    section_content = f'''
{{% comment %}}
  VitaliZen Enhancement: {section_name}
{{% endcomment %}}

{code}
'''
    
    data = {
        "asset": {
            "key": f"sections/{section_name}.liquid",
            "value": section_content
        }
    }
    
    response = requests.put(url, headers=HEADERS, json=data)
    return response.status_code == 200

def update_template():
    """Update template with properly positioned sections"""
    print("\n📋 Updating template order...")
    
    template_key = "templates/product.vitaglow.json"
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]={template_key}"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"   ❌ Failed to get template")
        return False
    
    template_json = json.loads(response.json()['asset']['value'])
    
    # Remove old vitalizen-enhancements if exists
    if 'vitalizen-enhancements' in template_json.get('sections', {}):
        del template_json['sections']['vitalizen-enhancements']
    
    if 'vitalizen-enhancements' in template_json.get('order', []):
        template_json['order'].remove('vitalizen-enhancements')
    
    # Add new sections
    for section_name, details in ENHANCEMENTS.items():
        # Add to sections
        template_json['sections'][section_name] = {
            "type": section_name,
            "settings": {}
        }
        
        # Find position
        position = details['position']
        
        if position == "end":
            template_json['order'].append(section_name)
        elif position.startswith("after:"):
            target = position.split(":")[1]
            try:
                idx = template_json['order'].index(target)
                template_json['order'].insert(idx + 1, section_name)
            except ValueError:
                template_json['order'].append(section_name)
        elif position.startswith("before:"):
            target = position.split(":")[1]
            try:
                idx = template_json['order'].index(target)
                template_json['order'].insert(idx, section_name)
            except ValueError:
                template_json['order'].append(section_name)
    
    # Update template
    update_url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    update_data = {
        "asset": {
            "key": template_key,
            "value": json.dumps(template_json, indent=2)
        }
    }
    
    update_response = requests.put(update_url, headers=HEADERS, json=update_data)
    
    if update_response.status_code == 200:
        print("   ✅ Template updated")
        print("\n📍 New section order:")
        for i, section_id in enumerate(template_json['order']):
            marker = "⭐" if section_id.startswith('vz-') else "  "
            print(f"   {marker} {i+1}. {section_id}")
        return True
    else:
        print(f"   ❌ Failed: {update_response.status_code}")
        return False

def main():
    print("="*60)
    print("  REORGANIZING VITALIZEN ENHANCEMENTS")
    print("="*60)
    
    print("\n1. Creating individual sections...")
    for section_name, details in ENHANCEMENTS.items():
        if create_section(section_name, details['code']):
            print(f"   ✅ {section_name}")
        else:
            print(f"   ❌ {section_name}")
    
    update_template()
    
    print("\n" + "="*60)
    print("✅ REORGANIZATION COMPLETE")
    print("="*60)
    print("\n🌐 Refresh page (hard refresh!):")
    print("   https://vitalizen.shop/products/vitaglow-pro-led-face-mask")
    print("\n⌨️  Ctrl+F5 or Cmd+Shift+R")

if __name__ == "__main__":
    main()
