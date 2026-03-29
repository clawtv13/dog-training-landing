# AI Automation Builder - Blog Setup

## Quick Setup (5 minutes)

### 1. Create GitHub Repo

```bash
# Go to GitHub.com
# Create new repo: "ai-automation-blog"
# Public repo (for GitHub Pages)
# Don't initialize with README
```

### 2. Connect & Deploy

```bash
cd /root/.openclaw/workspace/ai-automation-blog/blog

# Initialize git
git init
git branch -M main

# Add remote (replace with YOUR username)
git remote add origin https://github.com/YOURUSERNAME/ai-automation-blog.git

# First commit
git add .
git commit -m "Initial blog setup"
git push -u origin main
```

### 3. Enable GitHub Pages

```
1. Go to repo Settings
2. Pages (left sidebar)
3. Source: Deploy from branch "main"
4. Folder: / (root)
5. Save
```

**Wait 2-3 minutes → Site live at:**
```
https://YOURUSERNAME.github.io/ai-automation-blog/
```

---

## Custom Domain (Optional)

### 4. Buy Domain

Buy `aiautomationbuilder.com` from:
- Namecheap ($10/year)
- Cloudflare ($9/year)
- Google Domains

### 5. Configure DNS

Add these records:

```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153

Type: CNAME
Name: www
Value: YOURUSERNAME.github.io
```

### 6. Enable HTTPS

In repo Settings → Pages:
- ✓ Enforce HTTPS

**Wait 24 hours for DNS propagation**

---

## Automation Setup

### 7. Configure Cron

```bash
# Add to crontab -e

# Blog auto-posting - 2 posts per day (10:00 and 16:00 UTC)
0 10 * * * cd /root/.openclaw/workspace/ai-automation-blog && export OPENROUTER_API_KEY="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" && export TELEGRAM_BOT_TOKEN="8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU" && export TELEGRAM_CHAT_ID="8116230130" && python3 scripts/blog-auto-post.py >> logs/blog.log 2>&1

0 16 * * * cd /root/.openclaw/workspace/ai-automation-blog && export OPENROUTER_API_KEY="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" && export TELEGRAM_BOT_TOKEN="8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU" && export TELEGRAM_CHAT_ID="8116230130" && python3 scripts/blog-auto-post.py >> logs/blog.log 2>&1
```

---

## How It Works

### Content Flow:

```
Newsletter research DB
  ↓
Select top scored items (>30 score)
  ↓
Generate 800-1200 word blog post (Claude)
  ↓
Create HTML from template
  ↓
Commit to GitHub
  ↓
GitHub Pages auto-deploys
  ↓
Blog updated (live in 1-2 min)
```

### Automation:

- **10:00 UTC** - First post published
- **16:00 UTC** - Second post published
- **2 posts/day** = 60 posts/month
- **SEO traffic** starts building
- **Newsletter signups** from blog
- **0 manual work**

---

## Features

**Blog:**
- ✅ Responsive design
- ✅ SEO optimized
- ✅ Newsletter signup embedded
- ✅ Related posts
- ✅ Clean URLs

**Automation:**
- ✅ Content from newsletter research
- ✅ Claude-powered writing
- ✅ Auto-deploy GitHub Pages
- ✅ Telegram notifications
- ✅ State tracking (no duplicates)

---

## What You Get

**Blog + Newsletter Together:**

```
Research (automated)
  ├→ High-quality items
  ├→ Blog posts (2/day)
  └→ Newsletter (1/week)

Traffic Sources:
  ├→ Google (blog SEO)
  ├→ Social (blog shares)
  └→ Direct (newsletter)

Conversions:
  Blog → Newsletter signup → Engaged subscriber
```

**Growth engine running 24/7** ✅

---

## Maintenance

**Manual work:** 0 hours/week  
**System handles:** Everything

**You only:**
- Check Telegram notifications
- Approve newsletter draft (5 min/week)
- Watch growth 📈

---

## Cost

- Domain: $10/year (optional)
- GitHub Pages: $0
- Claude API (blog posts): ~$1-2/month
- **Total: $10-30/year** 🎉

---

Ready to deploy!
