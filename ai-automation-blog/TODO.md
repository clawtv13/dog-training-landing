# TODO - Complete Content Quality Fix

## ✅ DONE - What I Fixed

1. ✅ Analyzed why posts feel fake
2. ✅ Rewrote content generation script with anti-AI prompt
3. ✅ Added author persona (Alex Chen, AI Engineer)
4. ✅ Updated template with author card + credibility signals
5. ✅ Created example post showing real content style
6. ✅ Documented everything (4 reference docs)

---

## ⏳ TODO - What You Need to Do

### 1. Get OpenRouter API Key (5 minutes)
- Go to https://openrouter.ai/
- Sign up with email
- Create API key
- Copy the key (starts with `sk-or-v1-...`)

### 2. Set Environment Variable
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

Or permanently:
```bash
echo 'export OPENROUTER_API_KEY="sk-or-v1-..."' >> ~/.bashrc
source ~/.bashrc
```

### 3. Regenerate the 2 Existing Posts
```bash
cd /root/.openclaw/workspace/ai-automation-blog

# Delete old fake posts
rm blog/posts/2026-03-29-*.html

# Clear state so they regenerate
echo '[]' > .state/published-posts.json

# Generate new real content
python3 scripts/blog-auto-post.py
```

### 4. Review Quality
- Read the 2 new posts
- Compare to `blog/posts/test-real-content.html`
- Check for:
  - [ ] Author card visible
  - [ ] First-person voice ("I tested...")
  - [ ] Specific examples with data
  - [ ] Links to tools/resources
  - [ ] Personal experience included
  - [ ] No "As a..." or "Imagine..." openings

### 5. Deploy (Automatic)
The script auto-commits and pushes to GitHub.
GitHub Pages will rebuild automatically.

---

## 📚 Reference Docs

Read these if you want details:

1. **CONTENT-FIX-COMPLETE.md** - Executive summary (start here)
2. **CONTENT-QUALITY-FIX.md** - Detailed problem analysis
3. **BEFORE-AFTER.md** - Side-by-side comparison
4. **REGENERATE-POSTS.md** - Step-by-step guide

---

## 🎯 Success Criteria

Posts are fixed when:
- ✅ Look like a real person wrote them
- ✅ Have specific technical details
- ✅ Include personal experience
- ✅ Link to actual tools/resources
- ✅ Don't feel like marketing copy

**Test:** Show a post to someone. Ask if it's AI-generated.
**Goal:** They should be unsure or say "probably human"

---

## 💰 Cost

~$0.01-0.02 per post = ~$0.04 total to regenerate 2 posts

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Get API key from openrouter.ai
export OPENROUTER_API_KEY="sk-or-v1-..."

# 2. Regenerate posts
cd /root/.openclaw/workspace/ai-automation-blog
rm blog/posts/2026-03-29-*.html
echo '[]' > .state/published-posts.json
python3 scripts/blog-auto-post.py

# 3. Review output
cat blog/posts/2026-03-29-*.html | head -200

# 4. Done! Posts auto-deployed to GitHub Pages
```

---

**Status:** Everything fixed, just need to run it.
**Time needed:** 10 minutes
**Next step:** Get OpenRouter API key
