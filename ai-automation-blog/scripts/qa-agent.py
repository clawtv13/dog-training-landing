#!/usr/bin/env python3
"""
QA Agent - Automated Testing & Bug Detection

Verifies the blog is working correctly after deployment.
Tests homepage, posts, links, JavaScript, and reports bugs.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_URL = "https://clawtv13.github.io/ai-automation-blog/"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

STATE_DIR = Path(__file__).parent.parent / ".state"
BUG_REPORT = STATE_DIR / "qa-bugs.json"
STATE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# TEST SUITE
# ============================================================================

class QATest:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.passed = False
        self.error = None
        self.details = None

class QAAgent:
    def __init__(self):
        self.tests = []
        self.bugs = []
        self.warnings = []
        
    def add_test(self, test):
        self.tests.append(test)
        
    def run_all_tests(self):
        print("=" * 60)
        print("🔍 QA AGENT - AUTOMATED TESTING")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Target: {BASE_URL}")
        print("=" * 60)
        print()
        
        # Wait for deploy to finish
        print("⏳ Waiting 30s for deployment to complete...")
        time.sleep(30)
        
        # Run all tests
        for test in self.tests:
            self.run_test(test)
        
        # Report results
        self.generate_report()
        
    def run_test(self, test):
        print(f"\n🧪 {test.name}")
        print(f"   {test.description}")
        
        try:
            if test.name == "homepage_loads":
                self.test_homepage_loads(test)
            elif test.name == "posts_visible":
                self.test_posts_visible(test)
            elif test.name == "post_pages_load":
                self.test_post_pages_load(test)
            elif test.name == "json_loads":
                self.test_json_loads(test)
            elif test.name == "javascript_executing":
                self.test_javascript_executing(test)
            elif test.name == "links_work":
                self.test_links_work(test)
            elif test.name == "mobile_responsive":
                self.test_mobile_responsive(test)
            elif test.name == "seo_tags":
                self.test_seo_tags(test)
                
            if test.passed:
                print(f"   ✅ PASSED")
            else:
                print(f"   ❌ FAILED: {test.error}")
                self.bugs.append({
                    'test': test.name,
                    'error': test.error,
                    'details': test.details,
                    'severity': 'high',
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            test.passed = False
            test.error = str(e)
            print(f"   ❌ ERROR: {e}")
            self.bugs.append({
                'test': test.name,
                'error': str(e),
                'severity': 'critical',
                'timestamp': datetime.now().isoformat()
            })
    
    # ========================================================================
    # TEST IMPLEMENTATIONS
    # ========================================================================
    
    def test_homepage_loads(self, test):
        """Test that homepage returns HTTP 200"""
        r = requests.get(BASE_URL, timeout=10)
        
        if r.status_code != 200:
            test.error = f"Homepage returned {r.status_code}"
            return
        
        if len(r.content) < 1000:
            test.error = f"Homepage too small ({len(r.content)} bytes)"
            return
            
        test.passed = True
        test.details = f"{len(r.content)} bytes, {r.status_code}"
    
    def test_posts_visible(self, test):
        """Test that posts appear on homepage"""
        r = requests.get(BASE_URL, timeout=10)
        html = r.text
        
        # Check for post container
        if 'posts-container' not in html and 'posts-grid' not in html:
            test.error = "Posts container not found in HTML"
            return
        
        # Check for post cards (should have at least title tags in posts)
        if html.count('<h3>') < 2:  # At least 2 posts
            test.error = "Less than 2 posts visible"
            test.details = f"Found {html.count('<h3>')} h3 tags"
            return
        
        test.passed = True
        test.details = f"Found {html.count('<h3>')} post titles"
    
    def test_post_pages_load(self, test):
        """Test that individual post pages load"""
        # Get posts from index.json
        index_url = urljoin(BASE_URL, "posts/index.json")
        r = requests.get(index_url, timeout=10)
        
        if r.status_code != 200:
            test.error = f"index.json returned {r.status_code}"
            return
        
        posts = r.json()
        
        if len(posts) == 0:
            test.error = "No posts in index.json"
            return
        
        # Test first 3 posts
        failed = []
        for post in posts[:3]:
            post_url = urljoin(BASE_URL, post['url'].lstrip('/'))
            try:
                pr = requests.get(post_url, timeout=10)
                if pr.status_code != 200:
                    failed.append(f"{post['title']}: {pr.status_code}")
            except Exception as e:
                failed.append(f"{post['title']}: {e}")
        
        if failed:
            test.error = f"{len(failed)} posts failed to load"
            test.details = failed
            return
        
        test.passed = True
        test.details = f"Tested {min(3, len(posts))} posts, all loaded"
    
    def test_json_loads(self, test):
        """Test that posts/index.json is valid"""
        index_url = urljoin(BASE_URL, "posts/index.json")
        r = requests.get(index_url, timeout=10)
        
        if r.status_code != 200:
            test.error = f"index.json returned {r.status_code}"
            return
        
        try:
            posts = r.json()
        except:
            test.error = "index.json is not valid JSON"
            return
        
        if not isinstance(posts, list):
            test.error = "index.json is not an array"
            return
        
        if len(posts) == 0:
            self.warnings.append("index.json is empty (no posts)")
        
        # Check post structure
        for post in posts:
            if 'title' not in post or 'url' not in post:
                test.error = "Post missing required fields (title, url)"
                test.details = post
                return
        
        test.passed = True
        test.details = f"{len(posts)} posts in index"
    
    def test_javascript_executing(self, test):
        """Test that JavaScript loads posts dynamically"""
        r = requests.get(BASE_URL, timeout=10)
        html = r.text
        
        # Check for fetch call
        if "fetch('/ai-automation-blog/posts/index.json')" not in html and \
           "fetch('posts/index.json')" not in html:
            test.error = "JavaScript fetch not found"
            return
        
        # Check that posts-container exists
        if 'id="posts-container"' not in html:
            test.error = "posts-container element not found"
            return
        
        test.passed = True
        test.details = "JavaScript fetch found, DOM target exists"
    
    def test_links_work(self, test):
        """Test that important links work"""
        links_to_test = [
            "about.html",
            "archive.html", 
            "resources.html"
        ]
        
        failed = []
        for link in links_to_test:
            url = urljoin(BASE_URL, link)
            try:
                r = requests.get(url, timeout=10)
                if r.status_code != 200:
                    failed.append(f"{link}: {r.status_code}")
            except Exception as e:
                failed.append(f"{link}: {e}")
        
        if failed:
            test.error = f"{len(failed)} links failed"
            test.details = failed
            return
        
        test.passed = True
        test.details = f"Tested {len(links_to_test)} links, all work"
    
    def test_mobile_responsive(self, test):
        """Test mobile viewport meta tag"""
        r = requests.get(BASE_URL, timeout=10)
        html = r.text
        
        if 'name="viewport"' not in html:
            test.error = "Viewport meta tag missing"
            return
        
        if 'width=device-width' not in html:
            self.warnings.append("Viewport may not be properly configured")
        
        test.passed = True
        test.details = "Viewport meta tag present"
    
    def test_seo_tags(self, test):
        """Test basic SEO tags present"""
        r = requests.get(BASE_URL, timeout=10)
        html = r.text
        
        missing = []
        
        checks = {
            '<title>': 'Title tag',
            'name="description"': 'Meta description',
            'property="og:': 'Open Graph tags'
        }
        
        for check, name in checks.items():
            if check not in html:
                missing.append(name)
        
        if missing:
            test.error = f"Missing SEO tags: {', '.join(missing)}"
            return
        
        test.passed = True
        test.details = "All basic SEO tags present"
    
    # ========================================================================
    # REPORTING
    # ========================================================================
    
    def generate_report(self):
        print()
        print("=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        passed = sum(1 for t in self.tests if t.passed)
        failed = len(self.tests) - passed
        
        print(f"\n✅ Passed: {passed}/{len(self.tests)}")
        print(f"❌ Failed: {failed}/{len(self.tests)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for w in self.warnings:
                print(f"   - {w}")
        
        if self.bugs:
            print(f"\n❌ BUGS FOUND: {len(self.bugs)}")
            for bug in self.bugs:
                print(f"\n   Bug: {bug['test']}")
                print(f"   Error: {bug['error']}")
                if bug.get('details'):
                    print(f"   Details: {bug['details']}")
            
            # Save bugs to file
            self.save_bugs()
            
            # Send Telegram alert
            self.send_telegram_alert()
        else:
            print("\n🎉 NO BUGS FOUND - ALL TESTS PASSED!")
        
        print()
        print("=" * 60)
        
        # Exit with error code if tests failed
        if failed > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    
    def save_bugs(self):
        """Save bugs to JSON file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'bugs': self.bugs,
            'warnings': self.warnings,
            'tests_run': len(self.tests),
            'tests_passed': sum(1 for t in self.tests if t.passed),
            'tests_failed': sum(1 for t in self.tests if not t.passed)
        }
        
        with open(BUG_REPORT, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Bug report saved: {BUG_REPORT}")
    
    def send_telegram_alert(self):
        """Send Telegram notification about bugs"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return
        
        message = f"""🚨 **QA Agent - Bugs Detected**

❌ {len(self.bugs)} bug(s) found in blog deployment
⚠️  {len(self.warnings)} warning(s)

Bugs:
"""
        
        for bug in self.bugs[:3]:  # First 3 bugs
            message += f"\n• **{bug['test']}**\n  {bug['error']}\n"
        
        if len(self.bugs) > 3:
            message += f"\n...and {len(self.bugs) - 3} more\n"
        
        message += f"\nCheck: {BUG_REPORT}"
        message += f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
        
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

# ============================================================================
# MAIN
# ============================================================================

def main():
    qa = QAAgent()
    
    # Add all tests
    qa.add_test(QATest("homepage_loads", "Homepage returns HTTP 200"))
    qa.add_test(QATest("json_loads", "posts/index.json is valid JSON"))
    qa.add_test(QATest("javascript_executing", "JavaScript loads posts"))
    qa.add_test(QATest("posts_visible", "Posts appear on homepage"))
    qa.add_test(QATest("post_pages_load", "Individual post pages load"))
    qa.add_test(QATest("links_work", "About/Archive/Resources links work"))
    qa.add_test(QATest("mobile_responsive", "Mobile viewport configured"))
    qa.add_test(QATest("seo_tags", "SEO meta tags present"))
    
    # Run all tests
    qa.run_all_tests()

if __name__ == "__main__":
    main()
