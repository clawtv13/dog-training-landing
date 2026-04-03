# ⚡ Quick Start Checklist

**For:** n0mad  
**Task:** Blog SEO Restructure Implementation  
**Date:** 2026-04-03

---

## 📖 First: Read This

**Start here:** `/root/.openclaw/workspace/docs/BLOG-SEO-ARCHITECTURE.md`  
**Quick summary:** `/root/.openclaw/workspace/docs/DELIVERABLES-SUMMARY.md`

**Time to review:** 15-20 minutes

---

## ✅ Pre-Implementation Checklist

### **1. Review Deliverables**
- [ ] Read SEO audit reports (skim findings, focus on P0 issues)
- [ ] Review category taxonomy (approve category names)
- [ ] Understand programmatic SEO strategy (approve playbooks)
- [ ] Check technical implementation specs (feasible?)

### **2. Verify Access**
- [ ] Google Search Console access (cleverdogmethod.com)
- [ ] Google Search Console access (workless.build)
- [ ] Netlify deployment access (for _redirects file)
- [ ] Google Analytics 4 (optional but recommended)

### **3. Decision: Which Blog First?**
Choose one:
- [ ] **Option A:** CleverDogMethod first (4 weeks)
- [ ] **Option B:** AI Automation Blog first (4 weeks)
- [ ] **Option C:** Both in parallel (4 weeks, more work)

Recommendation: **Option C** (both blogs have similar structure, can reuse scripts)

### **4. Approve or Request Changes**
- [ ] ✅ **Approve:** Category taxonomy structure
- [ ] ✅ **Approve:** Programmatic SEO pilot (20 pages per blog)
- [ ] ✅ **Approve:** URL structure migration (with 301s)
- [ ] 🔄 **Changes needed:** (list below if any)

**Changes requested:**
```
[Leave blank if approved, or list specific changes]
```

---

## 🚀 Week 1: Infrastructure (Start Here)

### **Day 1: Setup**
- [ ] Create `/root/.openclaw/workspace/dog-training-landing/blog-new/` directory
- [ ] Create subdirectories:
  ```
  blog-new/
    training-basics/
      puppy-training/
      adult-dog-training/
      senior-dog-care/
    behavior-problems/
      barking/
      jumping/
      chewing/
      separation-anxiety/
      aggression/
    advanced-training/
      tricks/
      agility/
      service-dogs/
    breed-guides/
  ```
- [ ] Repeat for AI blog: `/root/.openclaw/workspace/ai-automation-blog/blog-new/`

### **Day 2: Post Migration**
- [ ] Copy posts to new category structure (use `CATEGORY-TAXONOMY-*.json` as reference)
- [ ] Update internal links in moved posts
- [ ] Verify all posts have correct category paths

### **Day 3: 301 Redirects**
- [ ] Create `_redirects` file in site root
- [ ] Add all old→new URL mappings
- [ ] Example:
  ```
  /blog/5-signs-your-dog-is-bored.html /blog/behavior-problems/5-signs-your-dog-is-bored/ 301
  ```
- [ ] Total redirects needed: 20 (CleverDog) + 33 (AI Blog) = 53

### **Day 4: Deploy & Test**
- [ ] Deploy new structure to Netlify
- [ ] Test 5 random redirects with curl:
  ```bash
  curl -I https://cleverdogmethod.com/blog/old-url.html
  # Should show: HTTP/1.1 301 Moved Permanently
  # Location: https://cleverdogmethod.com/blog/category/new-url/
  ```
- [ ] Verify new URLs load correctly
- [ ] Check for broken links (internal link checker)

### **Day 5: Cleanup**
- [ ] Archive old blog directory (backup)
- [ ] Move `blog-new/` to `blog/`
- [ ] Update sitemap.xml manually (temp fix before dynamic generator)
- [ ] Submit updated sitemap to Search Console

**End of Week 1:** ✅ New URL structure live with working redirects

---

## 📅 Week 2: Content Structure

### **Day 1-2: Category Hub Pages**
- [ ] Create 4 category hub pages (CleverDog):
  - `/blog/training-basics/index.html`
  - `/blog/behavior-problems/index.html`
  - `/blog/advanced-training/index.html`
  - `/blog/breed-guides/index.html`
- [ ] Create 4 category hub pages (AI Blog):
  - `/blog/ai-tools/index.html`
  - `/blog/solo-founder-strategies/index.html`
  - `/blog/case-studies/index.html`
  - `/blog/tutorials/index.html`

**Hub page template:**
```html
<h1>[Category Name]</h1>
<p class="lead">[200-word description]</p>

<section class="featured-posts">
  <h2>Featured Guides</h2>
  <!-- Top 3 posts -->
</section>

<section class="all-posts">
  <h2>All Articles</h2>
  <!-- List all posts in category -->
</section>
```

### **Day 3: Breadcrumb UI**
- [ ] Add breadcrumb HTML to post template
- [ ] Add breadcrumb CSS (see `TECHNICAL-SEO-IMPLEMENTATION.md`)
- [ ] Test on 3-5 posts
- [ ] Deploy breadcrumbs site-wide

### **Day 4-5: Internal Linking**
- [ ] Build `generate-related-posts.py` script
- [ ] Run script to generate related post lists for all articles
- [ ] Add "Related Articles" section to all posts (HTML injection)
- [ ] Verify 3-5 links per post

**End of Week 2:** ✅ Category hubs live, breadcrumbs visible, internal linking implemented

---

## 🧪 Week 3: Programmatic SEO Pilot

### **Day 1: Data Preparation**
- [ ] Create `data/breeds.json` (use template from docs)
- [ ] Create `data/behavior-problems.json`
- [ ] Create `data/ai-tools.json`
- [ ] Create `data/use-cases.json`

### **Day 2-3: Generator Scripts**
- [ ] Build `generate-breed-problem-pages.py`
- [ ] Build `generate-comparison-pages.py`
- [ ] Build `generate-use-case-pages.py`
- [ ] Test with 1-2 manual examples

### **Day 4: Generate Test Batch**
- [ ] Generate 20 breed×problem pages (CleverDog)
- [ ] Generate 10 comparison + 10 use case pages (AI Blog)
- [ ] **Manual review:** Check 3-5 pages for quality
- [ ] Fix issues, regenerate if needed

### **Day 5: Deploy & Monitor**
- [ ] Deploy programmatic pages
- [ ] Update sitemap.xml
- [ ] Submit to Search Console
- [ ] Set up tracking spreadsheet:
  ```
  URL | Target Keyword | Indexed? | Ranking | Traffic | Notes
  ```

**End of Week 3:** ✅ 40 new programmatic pages live, monitoring started

---

## 🔧 Week 4: Technical SEO & Polish

### **Day 1-2: Dynamic Sitemap**
- [ ] Build `generate-sitemap.py` script
- [ ] Generate sitemap.xml (both blogs)
- [ ] Verify output (should show 50+ URLs for CleverDog, 70+ for AI Blog)
- [ ] Submit new sitemaps to Search Console

### **Day 3: Schema Enhancements**
- [ ] Add FAQ schema to Q&A posts (5-10 posts per blog)
- [ ] Add HowTo schema to tutorial posts (3-5 posts per blog)
- [ ] Test with Google Rich Results Test

### **Day 4: Meta Tag Cleanup**
- [ ] Remove deprecated `meta keywords` tag (AI Blog)
- [ ] Standardize title tags (Site Name at end, not beginning)
- [ ] Verify OG images exist for all posts

### **Day 5: Final QA**
- [ ] Run full site crawl (Screaming Frog or manual check)
- [ ] Fix any broken links
- [ ] Verify all redirects working
- [ ] Check mobile responsiveness
- [ ] Test page speed (PageSpeed Insights)

**End of Week 4:** ✅ Technical SEO complete, ready for monitoring phase

---

## 📊 30-Day Monitoring (Post-Implementation)

### **Weekly Checks:**
- [ ] **Week 5:** Check indexation status (Search Console)
- [ ] **Week 6:** Track keyword rankings (top 20 pages)
- [ ] **Week 7:** Measure organic traffic growth
- [ ] **Week 8:** Review programmatic page performance

### **Success Metrics:**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Indexed Pages (CleverDog) | 50+ | ___ | ___ |
| Indexed Pages (AI Blog) | 70+ | ___ | ___ |
| Programmatic Pages Indexed | 30+ | ___ | ___ |
| Pages Ranking Top 20 | 6+ | ___ | ___ |
| Organic Traffic Growth | +30% | ___ | ___ |

### **Decision Point (Day 30):**
- [ ] ✅ **Pilot succeeded:** Scale to 100+ pages per blog
- [ ] 🔄 **Needs improvement:** Refine templates, improve content quality
- [ ] ❌ **Pilot failed:** Pause programmatic SEO, focus on existing content

---

## 🆘 Troubleshooting

### **Issue: Redirects not working**
- Check `_redirects` file syntax (Netlify format)
- Verify file is in site root (not in subdirectory)
- Clear CDN cache (Netlify dashboard)

### **Issue: Pages not indexed after 2 weeks**
- Submit URL via Search Console (manual request)
- Check for noindex tags (should only be on drafts)
- Verify sitemap includes new URLs
- Check robots.txt (not blocking pages)

### **Issue: High bounce rate on programmatic pages**
- Add more unique content (not just template)
- Improve internal linking (related posts)
- Better match search intent

### **Issue: Programmatic pages ranking low**
- Check content quality (1000+ words?)
- Add more breed/tool-specific info
- Improve internal linking from high-authority pages

---

## 📞 Need Help?

**Documentation:**
- Main overview: `BLOG-SEO-ARCHITECTURE.md`
- Technical specs: `TECHNICAL-SEO-IMPLEMENTATION.md`
- Programmatic SEO: `PROGRAMMATIC-SEO-CLEVERDOGMETHOD.md` / `PROGRAMMATIC-SEO-AI-AUTOMATION-BLOG.md`

**Questions?**
- Ask n0body (I can clarify anything)
- Reference specific sections in docs

---

## ✅ Final Approval

**Before starting Week 1:**
- [ ] I've reviewed all documentation
- [ ] I approve the category taxonomy structure
- [ ] I approve the programmatic SEO strategy
- [ ] I approve the URL migration plan
- [ ] I have access to all necessary tools (Search Console, Netlify)
- [ ] I'm ready to begin implementation

**Signature:** _______________  
**Date:** _______________

---

**Let's build.** 🚀
