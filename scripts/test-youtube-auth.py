#!/usr/bin/env python3
"""
Test YouTube authentication with cookies
"""

import json
import requests
from pathlib import Path

def test_youtube_login(channel: str):
    """
    Test if YouTube cookies are valid
    """
    
    # Load cookies
    cookies_file = Path("/root/.openclaw/workspace/.credentials/cookies.json")
    with open(cookies_file) as f:
        data = json.load(f)
    
    yt_cookies = data[channel]["youtube"]
    
    # Build cookie dict for requests
    cookie_dict = {
        'SID': yt_cookies['SID'],
        'HSID': yt_cookies['HSID'],
        'SSID': yt_cookies['SSID'],
        'APISID': yt_cookies['APISID'],
        'SAPISID': yt_cookies['SAPISID']
    }
    
    # Test authentication
    print(f"\n🔐 Testing YouTube auth for: {channel.upper()}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        # Try to access YouTube Studio (requires auth)
        response = requests.get(
            'https://studio.youtube.com',
            cookies=cookie_dict,
            headers=headers,
            timeout=10,
            allow_redirects=False
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Check if authenticated
        if response.status_code == 200:
            if 'studio.youtube.com' in response.url or 'studio' in response.text.lower():
                print("\n✅ SUCCESS: Cookies válidos - Logged in!")
                return True
        
        elif response.status_code == 302 or response.status_code == 303:
            redirect = response.headers.get('Location', '')
            if 'accounts.google.com' in redirect:
                print("\n❌ FAIL: Redirige a login - Cookies inválidos o expirados")
                return False
            else:
                print(f"\n✅ SUCCESS: Redirect válido: {redirect}")
                return True
        
        else:
            print(f"\n⚠️ UNKNOWN: Status {response.status_code}")
            print(f"URL: {response.url}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == '__main__':
    import sys
    
    channel = sys.argv[1] if len(sys.argv) > 1 else 'moneystack'
    
    result = test_youtube_login(channel)
    
    if result:
        print(f"\n🚀 Ready to upload to {channel.upper()} YouTube!")
    else:
        print(f"\n⚠️ Cookies need refresh for {channel}")
