#!/usr/bin/env python3
"""
Week 1 Implementation Verification & QA
Checks all deliverables are complete

Date: 2026-04-03
"""

import os
from pathlib import Path
import json
from xml.etree import ElementTree as ET

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check(condition, message):
    """Print check result"""
    if condition:
        print(f"   {GREEN}✅{RESET} {message}")
        return True
    else:
        print(f"   {RED}❌{RESET} {message}")
        return False

def count_files(directory: Path, pattern: str) -> int:
    """Count files matching pattern"""
    return len(list(directory.rglob(pattern)))

def verify_cleverdog():
    """Verify CleverDogMethod implementation"""
    print(f"\n🐕 {GREEN}CleverDogMethod Verification{RESET}\n" + "="*50)
    
    base_dir = Path("/root/.openclaw/workspace/dog-training-landing")
    blog_new = base_dir / "blog-new"
    
    checks_passed = 0
    total_checks = 0
    
    # 1. Directory structure
    print("\n1️⃣  Directory Structure")
    total_checks += 1
    checks_passed += check(blog_new.exists(), "blog-new directory created")
    
    categories = ["training-basics", "behavior-problems", "advanced-training", "breed-guides"]
    for cat in categories:
        total_checks += 1
        checks_passed += check((blog_new / cat).exists(), f"Category: {cat}")
    
    # 2. Posts moved
    print("\n2️⃣  Posts Moved")
    post_count = count_files(blog_new, "**/index.html") - len(categories)  # Exclude category hubs
    total_checks += 1
    checks_passed += check(post_count >= 14, f"Posts moved: {post_count}/14")
    
    # 3. Redirects
    print("\n3️⃣  Redirects")
    redirects_file = base_dir / "_redirects"
    total_checks += 1
    if redirects_file.exists():
        with open(redirects_file, 'r') as f:
            redirect_count = len([l for l in f.readlines() if l.strip() and not l.startswith('#')])
        checks_passed += check(redirect_count >= 14, f"Redirect rules: {redirect_count}/14")
    else:
        check(False, "_redirects file exists")
    
    # 4. Category hubs
    print("\n4️⃣  Category Hub Pages")
    for cat in categories:
        total_checks += 1
        hub_file = blog_new / cat / "index.html"
        checks_passed += check(hub_file.exists(), f"Hub page: {cat}/index.html")
    
    # 5. Sitemap
    print("\n5️⃣  Sitemap")
    sitemap_file = base_dir / "sitemap.xml"
    total_checks += 1
    if sitemap_file.exists():
        tree = ET.parse(sitemap_file)
        root = tree.getroot()
        url_count = len(root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
        checks_passed += check(url_count >= 19, f"Sitemap URLs: {url_count} (expected 19+)")
    else:
        check(False, "sitemap.xml exists")
    
    print(f"\n📊 Score: {checks_passed}/{total_checks} checks passed")
    return checks_passed == total_checks

def verify_aiblog():
    """Verify AI Automation Blog implementation"""
    print(f"\n🤖 {GREEN}AI Automation Blog Verification{RESET}\n" + "="*50)
    
    base_dir = Path("/root/.openclaw/workspace/ai-automation-blog")
    blog_new = base_dir / "blog-new"
    
    checks_passed = 0
    total_checks = 0
    
    # 1. Directory structure
    print("\n1️⃣  Directory Structure")
    total_checks += 1
    checks_passed += check(blog_new.exists(), "blog-new directory created")
    
    categories = ["ai-tools", "solo-founder-strategies", "case-studies", "tutorials"]
    for cat in categories:
        total_checks += 1
        checks_passed += check((blog_new / cat).exists(), f"Category: {cat}")
    
    # 2. Posts moved
    print("\n2️⃣  Posts Moved")
    post_count = count_files(blog_new, "**/index.html") - len(categories)  # Exclude category hubs
    total_checks += 1
    checks_passed += check(post_count >= 14, f"Posts moved: {post_count}/14 (excluding duplicates/off-topic)")
    
    # 3. Redirects
    print("\n3️⃣  Redirects")
    redirects_file = base_dir / "_redirects"
    total_checks += 1
    if redirects_file.exists():
        with open(redirects_file, 'r') as f:
            redirect_count = len([l for l in f.readlines() if l.strip() and not l.startswith('#')])
        checks_passed += check(redirect_count >= 14, f"Redirect rules: {redirect_count}/14")
    else:
        check(False, "_redirects file exists")
    
    # 4. Category hubs
    print("\n4️⃣  Category Hub Pages")
    for cat in categories:
        total_checks += 1
        hub_file = blog_new / cat / "index.html"
        checks_passed += check(hub_file.exists(), f"Hub page: {cat}/index.html")
    
    # 5. Sitemap
    print("\n5️⃣  Sitemap")
    sitemap_file = base_dir / "sitemap.xml"
    total_checks += 1
    if sitemap_file.exists():
        tree = ET.parse(sitemap_file)
        root = tree.getroot()
        url_count = len(root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
        checks_passed += check(url_count >= 19, f"Sitemap URLs: {url_count} (expected 19+)")
    else:
        check(False, "sitemap.xml exists")
    
    print(f"\n📊 Score: {checks_passed}/{total_checks} checks passed")
    return checks_passed == total_checks

def print_next_steps():
    """Print next steps for deployment"""
    print(f"\n{YELLOW}📋 Next Steps:{RESET}\n")
    print("1. Manual Review:")
    print("   - Check 2-3 posts in blog-new (verify HTML preserved)")
    print("   - Verify category hub pages look good")
    print("")
    print("2. Test Redirects Locally:")
    print("   cd /root/.openclaw/workspace/dog-training-landing")
    print("   # Serve blog-new and test URLs")
    print("")
    print("3. Deploy to Staging (if available):")
    print("   - Move blog-new → blog (backup old first)")
    print("   - Deploy _redirects file")
    print("   - Test 5-10 random redirects with curl")
    print("")
    print("4. Deploy to Production:")
    print("   git add blog/ _redirects sitemap.xml")
    print("   git commit -m 'Week 1: Blog SEO restructure'")
    print("   git push")
    print("")
    print("5. Post-Deployment:")
    print("   - Submit updated sitemaps to Google Search Console")
    print("   - Monitor indexation (24-48h)")
    print("   - Check for 404s in Search Console")
    print("")

def main():
    """Run verification"""
    print("\n" + "="*60)
    print(f"  {GREEN}Week 1 Implementation Verification{RESET}")
    print("  Date: 2026-04-03")
    print("="*60)
    
    cleverdog_ok = verify_cleverdog()
    aiblog_ok = verify_aiblog()
    
    print("\n" + "="*60)
    if cleverdog_ok and aiblog_ok:
        print(f"  {GREEN}✅ All Checks Passed!{RESET}")
        print("="*60)
        print_next_steps()
    else:
        print(f"  {RED}⚠️  Some Checks Failed{RESET}")
        print("="*60)
        print("\nReview failed checks above and re-run implementation script if needed.\n")

if __name__ == "__main__":
    main()
