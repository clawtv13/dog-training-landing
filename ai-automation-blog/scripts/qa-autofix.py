#!/usr/bin/env python3
"""
QA Auto-Fix Agent

Reads bug reports from qa-agent.py and attempts automatic fixes.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BUG_REPORT = WORKSPACE / ".state" / "qa-bugs.json"
BLOG_DIR = WORKSPACE / "blog"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ============================================================================
# BUG ANALYSIS
# ============================================================================

def analyze_bugs():
    """Load and analyze bug report"""
    if not BUG_REPORT.exists():
        print("✅ No bugs found - nothing to fix")
        return []
    
    with open(BUG_REPORT, 'r') as f:
        report = json.load(f)
    
    bugs = report.get('bugs', [])
    
    if not bugs:
        print("✅ No bugs in latest report")
        return []
    
    print(f"🔍 Found {len(bugs)} bug(s) to analyze\n")
    
    return bugs

# ============================================================================
# AUTO-FIX STRATEGIES
# ============================================================================

def autofix_posts_visible(bug):
    """Fix: Posts not visible on homepage"""
    print("🔧 Attempting auto-fix: posts_visible")
    print(f"   Issue: {bug['error']}")
    
    # Possible causes:
    # 1. JavaScript path wrong
    # 2. Posts not in index.json
    # 3. DOM element missing
    
    # Check index.html for posts fetch
    index_file = BLOG_DIR / "index.html"
    
    if not index_file.exists():
        print("   ❌ index.html not found")
        return False
    
    with open(index_file, 'r') as f:
        html = f.read()
    
    # Check fetch path
    if "fetch('posts/index.json')" in html:
        print("   🔧 Fixing: Relative path → Absolute path")
        
        html = html.replace(
            "fetch('posts/index.json')",
            "fetch('/ai-automation-blog/posts/index.json')"
        )
        
        with open(index_file, 'w') as f:
            f.write(html)
        
        # Commit and push
        os.chdir(BLOG_DIR)
        subprocess.run(["git", "add", "index.html"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-fix: Use absolute path for posts JSON"], check=True)
        
        # Push with token
        token = os.getenv("GITHUB_TOKEN", "")
        if token:
            subprocess.run([
                "git", "push",
                f"https://{token}@github.com/clawtv13/ai-automation-blog.git",
                "main"
            ], check=True)
        else:
            subprocess.run(["git", "push"], check=True)
        
        print("   ✅ Fix applied and deployed")
        return True
    
    # Check if posts-container exists
    if 'id="posts-container"' not in html:
        print("   ❌ posts-container element missing - manual fix needed")
        return False
    
    print("   ⚠️  Could not determine cause - manual investigation needed")
    return False

def autofix_json_loads(bug):
    """Fix: JSON loading issues"""
    print("🔧 Attempting auto-fix: json_loads")
    
    index_json = BLOG_DIR / "posts" / "index.json"
    
    if not index_json.exists():
        print("   🔧 Creating empty posts/index.json")
        index_json.parent.mkdir(parents=True, exist_ok=True)
        with open(index_json, 'w') as f:
            json.dump([], f)
        
        # Commit and deploy
        os.chdir(BLOG_DIR)
        subprocess.run(["git", "add", "posts/index.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-fix: Create posts/index.json"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print("   ✅ Fix applied")
        return True
    
    print("   ⚠️  index.json exists but invalid - manual fix needed")
    return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("🤖 QA AUTO-FIX AGENT")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    print()
    
    bugs = analyze_bugs()
    
    if not bugs:
        return
    
    fixed = []
    failed = []
    
    for bug in bugs:
        test_name = bug['test']
        
        print(f"\n{'='*60}")
        print(f"Bug: {test_name}")
        print(f"Error: {bug['error']}")
        print(f"{'='*60}\n")
        
        # Route to appropriate fix function
        success = False
        
        if test_name == "posts_visible":
            success = autofix_posts_visible(bug)
        elif test_name == "json_loads":
            success = autofix_json_loads(bug)
        else:
            print(f"⚠️  No auto-fix available for: {test_name}")
            success = False
        
        if success:
            fixed.append(test_name)
        else:
            failed.append(test_name)
    
    # Report results
    print()
    print("=" * 60)
    print("📊 AUTO-FIX RESULTS")
    print("=" * 60)
    print(f"\n✅ Fixed: {len(fixed)}")
    print(f"❌ Failed: {len(failed)}")
    
    if fixed:
        print("\n✅ Auto-fixed:")
        for f in fixed:
            print(f"   - {f}")
    
    if failed:
        print("\n❌ Manual fix needed:")
        for f in failed:
            print(f"   - {f}")
    
    print()
    
    # Send notification
    if fixed and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        message = f"""✅ **QA Auto-Fix Complete**

Fixed {len(fixed)} bug(s) automatically:
"""
        for f in fixed:
            message += f"• {f}\n"
        
        if failed:
            message += f"\n⚠️  {len(failed)} bug(s) need manual attention"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            requests.post(url, json=payload, timeout=10)
        except:
            pass

if __name__ == "__main__":
    import requests
    main()
