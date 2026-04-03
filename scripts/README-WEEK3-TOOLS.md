# Week 3 SEO Tools - Quick Reference

## 🗺️ Sitemap Generator

**Generate sitemaps for all blogs:**
```bash
python3 scripts/generate-sitemap.py --all
```

**Generate for specific blog:**
```bash
python3 scripts/generate-sitemap.py --blog ai-automation
python3 scripts/generate-sitemap.py --blog cleverdogmethod
```

**Automated regeneration (cron):**
```bash
# Run daily at 2 AM
0 2 * * * cd /root/.openclaw/workspace && python3 scripts/generate-sitemap.py --all
```

---

## 🔗 Internal Link Analyzer

**Analyze all blogs:**
```bash
python3 scripts/analyze-internal-links.py --all
```

**Analyze specific blog:**
```bash
python3 scripts/analyze-internal-links.py --blog cleverdogmethod
```

**Output:**
- Console report with metrics
- JSON report saved to `/root/.openclaw/workspace/reports/`

**Metrics tracked:**
- Total posts
- Average links per post
- Orphan pages (no incoming links)
- Weak pages (<3 links)
- Most linked pages
- Recommendations

---

## ✅ Test Suite

**Run all Week 3 tests:**
```bash
python3 scripts/test-seo-week3.py
```

**Tests covered:**
1. Library imports
2. Post categorization (AI blog)
3. Dog training categorization
4. Meta tags generation
5. HTML minification
6. Lazy loading
7. JS deferring
8. Sitemap files
9. Robots.txt files

---

## 🚀 SEO Library Usage

### In Generator Scripts:

```python
# Import
from lib.seo_enhancements import enhance_post_html, categorize_post, generate_meta_tags
from lib.page_speed import optimize_html

# Auto-categorize
category, subcategory = categorize_post(title, content)

# Generate meta tags
meta_html = generate_meta_tags(
    title=post_title,
    description=post_description,
    canonical_url=f"https://example.com/posts/{slug}.html",
    image_url=featured_image_url,
    site_name="Blog Name"
)

# Enhance HTML with SEO features
html = enhance_post_html(
    html_content=html,
    category=category,
    subcategory=subcategory,
    title=post_title,
    url_path=f"/posts/{slug}.html",
    related_posts=[]  # Optional: pass related posts list
)

# Optimize for page speed
html = optimize_html(
    html,
    minify=True,
    lazy_images=True,
    defer_js=True
)
```

---

## 📊 Core Web Vitals Tracking

**Add to HTML pages:**
```html
<script src="/lib/web_vitals.js"></script>
```

**Metrics tracked:**
- LCP (Largest Contentful Paint) - target: <2.5s
- FID (First Input Delay) - target: <100ms
- CLS (Cumulative Layout Shift) - target: <0.1
- Page Load Time
- Detailed timing breakdown

**View in browser console:**
```javascript
// Access tracked metrics
console.log(window.webVitals);
```

---

## 🔧 Page Speed Optimization

### Python API:

```python
from lib.page_speed import minify_html, add_lazy_loading, defer_non_critical_js, optimize_html

# Minify HTML (50%+ reduction)
minified = minify_html(html)

# Add lazy loading to images
html_with_lazy = add_lazy_loading(html)

# Defer JavaScript
html_with_defer = defer_non_critical_js(html)

# Apply all optimizations at once
optimized = optimize_html(
    html,
    minify=True,
    lazy_images=True,
    defer_js=True
)
```

---

## 📁 File Locations

### Scripts:
- `/root/.openclaw/workspace/scripts/generate-sitemap.py`
- `/root/.openclaw/workspace/scripts/analyze-internal-links.py`
- `/root/.openclaw/workspace/scripts/test-seo-week3.py`

### Libraries:
- `/root/.openclaw/workspace/lib/seo_enhancements.py`
- `/root/.openclaw/workspace/lib/page_speed.py`
- `/root/.openclaw/workspace/lib/web_vitals.js`

### Generated Files:
- `/root/.openclaw/workspace/ai-automation-blog/blog-new/sitemap.xml`
- `/root/.openclaw/workspace/ai-automation-blog/blog-new/robots.txt`
- `/root/.openclaw/workspace/dog-training-landing-clean/sitemap.xml`
- `/root/.openclaw/workspace/dog-training-landing-clean/robots.txt`

### Reports:
- `/root/.openclaw/workspace/reports/internal-links-{blog}-{date}.json`
- `/root/.openclaw/workspace/reports/WEEK-3-IMPLEMENTATION-COMPLETE.md`

---

## 🎯 Maintenance Schedule

### Daily:
- Sitemap regeneration (cron at 2 AM)

### Weekly:
- Run internal link analysis
- Review orphan/weak pages
- Check test suite

### Monthly:
- Review Core Web Vitals metrics
- Audit SEO health
- Update categorization keywords if needed

---

## 🐛 Troubleshooting

### Sitemap not generating?
```bash
# Check blog root paths in scripts/generate-sitemap.py
# Ensure HTML files exist
ls -la /root/.openclaw/workspace/dog-training-landing-clean/blog/*.html
```

### Link analyzer shows 0 posts?
```bash
# Verify blog root path is correct
# Check for .html files
find /root/.openclaw/workspace -name "*.html" -type f
```

### SEO enhancements not applying?
```python
# Ensure imports are correct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

# Check for errors in logs
```

### Tests failing?
```bash
# Re-run specific test for more detail
python3 -c "from scripts.test_seo_week3 import test_categorization; test_categorization()"
```

---

## 📚 Further Reading

- [Week 3 Implementation Report](../reports/WEEK-3-IMPLEMENTATION-COMPLETE.md)
- [SEO Enhancements Library](../lib/seo_enhancements.py)
- [Page Speed Utilities](../lib/page_speed.py)
- [Web Vitals Tracker](../lib/web_vitals.js)

---

**Last Updated:** 2026-04-03  
**Version:** 1.0  
**Status:** Production Ready
