#!/usr/bin/env python3
"""
YouTube login via Playwright - Save session for later use
Run this ONCE to login, then reuse session for uploads
"""

from playwright.sync_api import sync_playwright
import sys
import time
from pathlib import Path

def login_youtube(channel: str):
    """
    Interactive login to YouTube
    Saves session for future use
    
    Args:
        channel: 'calmora' or 'moneystack'
    """
    
    session_file = f"/root/.openclaw/workspace/.credentials/youtube-{channel}-session.json"
    
    print(f"\n🎭 YouTube Login Setup for: {channel.upper()}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # Launch browser (visible so you can login)
        browser = p.chromium.launch(
            headless=False,  # Show browser
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        print("\n📺 Opening YouTube Studio...")
        page.goto('https://studio.youtube.com', wait_until='networkidle')
        
        print("\n👤 Por favor:")
        print("   1. Login con tu cuenta de Google")
        print("   2. Selecciona el canal correcto")
        print("   3. Cuando veas YouTube Studio dashboard, presiona ENTER aquí\n")
        
        input("Presiona ENTER cuando estés logged in y veas el dashboard... ")
        
        # Check if actually logged in
        current_url = page.url
        
        if 'studio.youtube.com' in current_url and 'ServiceLogin' not in current_url:
            print("\n✅ Login exitoso!")
            
            # Save session state
            context.storage_state(path=session_file)
            print(f"💾 Sesión guardada: {session_file}")
            
            # Test: get channel name
            try:
                # Try to find channel name in page
                time.sleep(2)
                page_content = page.content()
                
                if 'channel' in page_content.lower():
                    print("✅ Sesión válida - Channel detectado")
                else:
                    print("⚠️  Sesión guardada pero no pude confirmar channel")
            
            except Exception as e:
                print(f"⚠️  Sesión guardada (error verificando: {e})")
            
            print("\n🎯 Próximos pasos:")
            print("   - Esta sesión durará semanas")
            print("   - No necesitas login manual de nuevo")
            print("   - Uploads usarán esta sesión automáticamente")
            
        else:
            print("\n❌ Login fallido o incompleto")
            print(f"   URL actual: {current_url}")
            print("   Intenta de nuevo")
            browser.close()
            sys.exit(1)
        
        browser.close()
        
        return session_file


def verify_session(channel: str):
    """
    Verify saved session still works
    """
    
    session_file = f"/root/.openclaw/workspace/.credentials/youtube-{channel}-session.json"
    
    if not Path(session_file).exists():
        print(f"❌ No session found for {channel}")
        print(f"   Run: python3 youtube-playwright-login.py {channel}")
        return False
    
    print(f"\n🔍 Verificando sesión guardada: {channel.upper()}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Load saved session
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()
        
        try:
            page.goto('https://studio.youtube.com', wait_until='networkidle', timeout=15000)
            
            current_url = page.url
            
            if 'studio.youtube.com' in current_url and 'ServiceLogin' not in current_url:
                print(f"✅ Sesión válida para {channel}")
                browser.close()
                return True
            else:
                print(f"❌ Sesión expirada para {channel}")
                print(f"   URL: {current_url}")
                print(f"   Re-login needed")
                browser.close()
                return False
        
        except Exception as e:
            print(f"❌ Error verificando sesión: {e}")
            browser.close()
            return False


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("\n📋 Usage:")
        print("   Login:  python3 youtube-playwright-login.py [channel]")
        print("   Verify: python3 youtube-playwright-login.py verify [channel]")
        print("\n   Channels: calmora, moneystack")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'verify':
        if len(sys.argv) < 3:
            print("❌ Specify channel: verify calmora|moneystack")
            sys.exit(1)
        
        channel = sys.argv[2]
        verify_session(channel)
    
    else:
        # Assume command is channel name
        channel = command
        
        if channel not in ['calmora', 'moneystack']:
            print(f"❌ Unknown channel: {channel}")
            print("   Available: calmora, moneystack")
            sys.exit(1)
        
        login_youtube(channel)
