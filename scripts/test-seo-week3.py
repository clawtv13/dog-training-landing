#!/usr/bin/env python3
"""
Week 3 SEO Integration - Testing & Verification
Tests all Week 3 deliverables
"""

import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from seo_enhancements import categorize_post, categorize_dog_training_post, enhance_post_html, generate_meta_tags
from page_speed import minify_html, add_lazy_loading, defer_non_critical_js, optimize_html

WORKSPACE = Path("/root/.openclaw/workspace")


def test_categorization():
    """Test auto-categorization"""
    print("\n" + "="*60)
    print("TEST 1: Post Categorization")
    print("="*60)
    
    test_cases = [
        ("How to use ChatGPT for automation", "ai-tools/llms"),
        ("Productivity hacks for solo founders", "solo-founder-strategies/productivity"),
        ("Failed startup: What went wrong", "case-studies/failed-experiments"),
        ("Tutorial: Building with no-code AI", "ai-tools/no-code-ai"),
    ]
    
    passed = 0
    for title, expected in test_cases:
        category, subcategory = categorize_post(title)
        result = f"{category}/{subcategory}" if subcategory else category
        status = "✅ PASS" if expected in result else "❌ FAIL"
        print(f"{status} | '{title}' → {result}")
        if expected in result:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_dog_training_categorization():
    """Test dog training categorization"""
    print("\n" + "="*60)
    print("TEST 2: Dog Training Categorization")
    print("="*60)
    
    test_cases = [
        ("puppy socialization", "training/puppy-training"),
        ("stop dog barking", "training/behavior-issues"),
        ("teach sit command", "training/obedience"),
        ("advanced tricks", "training/advanced"),
    ]
    
    passed = 0
    for keyword, expected in test_cases:
        category, subcategory = categorize_dog_training_post(keyword)
        result = f"{category}/{subcategory}"
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} | '{keyword}' → {result}")
        if result == expected:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_meta_tags():
    """Test meta tag generation"""
    print("\n" + "="*60)
    print("TEST 3: Meta Tags Generation")
    print("="*60)
    
    meta_html = generate_meta_tags(
        title="Test Article Title",
        description="This is a test description for SEO purposes.",
        canonical_url="https://example.com/test-post",
        image_url="https://example.com/image.jpg",
        site_name="Test Blog"
    )
    
    required_tags = [
        'og:title',
        'og:description',
        'twitter:card',
        'canonical',
        'viewport',
        'favicon.ico'
    ]
    
    passed = 0
    for tag in required_tags:
        if tag in meta_html:
            print(f"✅ PASS | {tag} present")
            passed += 1
        else:
            print(f"❌ FAIL | {tag} missing")
    
    print(f"\nResult: {passed}/{len(required_tags)} required tags present")
    return passed == len(required_tags)


def test_html_minification():
    """Test HTML minification"""
    print("\n" + "="*60)
    print("TEST 4: HTML Minification")
    print("="*60)
    
    test_html = """
    <html>
        <head>
            <title>  Test  </title>
        </head>
        <body>
            <p>  Hello   World  </p>
        </body>
    </html>
    """
    
    minified = minify_html(test_html)
    
    original_size = len(test_html)
    minified_size = len(minified)
    reduction = ((original_size - minified_size) / original_size) * 100
    
    print(f"Original size: {original_size} bytes")
    print(f"Minified size: {minified_size} bytes")
    print(f"Reduction: {reduction:.1f}%")
    
    if minified_size < original_size and '<html>' in minified:
        print("✅ PASS | HTML successfully minified")
        return True
    else:
        print("❌ FAIL | Minification failed")
        return False


def test_lazy_loading():
    """Test lazy loading addition"""
    print("\n" + "="*60)
    print("TEST 5: Lazy Loading Images")
    print("="*60)
    
    test_html = '<img src="test.jpg" alt="Test"><img src="test2.jpg">'
    result = add_lazy_loading(test_html)
    
    if 'loading="lazy"' in result and result.count('loading="lazy"') == 2:
        print("✅ PASS | Lazy loading added to all images")
        return True
    else:
        print("❌ FAIL | Lazy loading not properly added")
        return False


def test_js_defer():
    """Test JS deferring"""
    print("\n" + "="*60)
    print("TEST 6: JavaScript Deferring")
    print("="*60)
    
    test_html = '<script src="app.js"></script><script src="lib.js"></script>'
    result = defer_non_critical_js(test_html)
    
    if 'defer' in result and result.count('defer') == 2:
        print("✅ PASS | Defer added to scripts")
        return True
    else:
        print("❌ FAIL | Defer not properly added")
        return False


def test_sitemap_existence():
    """Test sitemap files exist"""
    print("\n" + "="*60)
    print("TEST 7: Sitemap Files")
    print("="*60)
    
    sitemaps = [
        WORKSPACE / "ai-automation-blog" / "blog-new" / "sitemap.xml",
        WORKSPACE / "dog-training-landing-clean" / "sitemap.xml"
    ]
    
    passed = 0
    for sitemap in sitemaps:
        if sitemap.exists():
            print(f"✅ PASS | {sitemap.name} exists at {sitemap.parent.name}")
            passed += 1
        else:
            print(f"❌ FAIL | {sitemap.name} missing")
    
    print(f"\nResult: {passed}/{len(sitemaps)} sitemaps exist")
    return passed == len(sitemaps)


def test_robots_txt():
    """Test robots.txt files"""
    print("\n" + "="*60)
    print("TEST 8: Robots.txt Files")
    print("="*60)
    
    robots_files = [
        WORKSPACE / "ai-automation-blog" / "blog-new" / "robots.txt",
        WORKSPACE / "dog-training-landing-clean" / "robots.txt"
    ]
    
    passed = 0
    for robots_file in robots_files:
        if robots_file.exists():
            content = robots_file.read_text()
            if 'Sitemap:' in content and 'User-agent:' in content:
                print(f"✅ PASS | {robots_file.name} valid at {robots_file.parent.name}")
                passed += 1
            else:
                print(f"❌ FAIL | {robots_file.name} invalid format")
        else:
            print(f"❌ FAIL | {robots_file.name} missing")
    
    print(f"\nResult: {passed}/{len(robots_files)} robots.txt files valid")
    return passed == len(robots_files)


def test_library_imports():
    """Test that all libraries import correctly"""
    print("\n" + "="*60)
    print("TEST 9: Library Imports")
    print("="*60)
    
    libraries = {
        "seo_enhancements": ["categorize_post", "enhance_post_html", "generate_meta_tags"],
        "page_speed": ["minify_html", "optimize_html", "add_lazy_loading"],
    }
    
    passed = 0
    total = sum(len(funcs) for funcs in libraries.values())
    
    for lib, functions in libraries.items():
        for func in functions:
            try:
                module = __import__(lib)
                if hasattr(module, func):
                    print(f"✅ PASS | {lib}.{func} available")
                    passed += 1
                else:
                    print(f"❌ FAIL | {lib}.{func} not found")
            except Exception as e:
                print(f"❌ FAIL | {lib} import error: {e}")
    
    print(f"\nResult: {passed}/{total} library functions available")
    return passed == total


def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print(" WEEK 3 SEO INTEGRATION - TEST SUITE")
    print(" " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("="*70)
    
    tests = [
        ("Library Imports", test_library_imports),
        ("Post Categorization", test_categorization),
        ("Dog Training Categorization", test_dog_training_categorization),
        ("Meta Tags Generation", test_meta_tags),
        ("HTML Minification", test_html_minification),
        ("Lazy Loading", test_lazy_loading),
        ("JS Deferring", test_js_defer),
        ("Sitemap Files", test_sitemap_existence),
        ("Robots.txt Files", test_robots_txt),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ TEST ERROR: {e}")
            results.append((name, False))
    
    # Final summary
    print("\n" + "="*70)
    print(" FINAL SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {name}")
    
    print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed ({(passed_count/total_count)*100:.1f}%)")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Week 3 implementation complete.")
        return True
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review issues above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
