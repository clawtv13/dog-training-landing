# Master Content Agent V3 - Quick Start

**5-Minute Setup Guide**

---

## ⚡ TL;DR

```bash
# 1. Set API key
export OPENROUTER_API_KEY="sk-your-key-here"

# 2. Run once
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/master-content-agent.py

# 3. Automate (optional)
crontab -e
# Add: 0 9,17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Done.** System generates 2 SEO-optimized posts/day, quality 70+, costs $3-4/month.

---

## 📋 Prerequisites

- [x] Python 3.8+
- [x] OpenRouter API key
- [x] Newsletter DB with content (score >= 30)
- [x] Git configured for GitHub
- [ ] Optional: Telegram bot token

---

## 🚀 Step-by-Step

### 1. Get API Key

Sign up at [OpenRouter](https://openrouter.ai) → Get API key

### 2. Set Environment Variable

**Option A: Current session**
```bash
export OPENROUTER_API_KEY="sk-..."
```

**Option B: Permanent (add to ~/.bashrc)**
```bash
echo 'export OPENROUTER_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

**Option C: Cron-specific (in crontab)**
```cron
OPENROUTER_API_KEY=sk-...
```

### 3. Test Run

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/master-content-agent.py
```

**Expected output:**
```
🚀 MASTER CONTENT AGENT V3.0
📚 Found 30 unpublished items
🔍 Phase 1: Conducting SEO research...
✍️  Phase 2: Generating SEO-optimized content...
📊 Phase 3: Scoring content quality...
✅ Post published
🚀 Deployed to GitHub
✅ COMPLETE
```

**Time:** 3-5 minutes

### 4. Verify Post

```bash
# Check file created
ls -lh blog/posts/*$(date +%Y-%m-%d)*.html

# Check quality score
jq -r '.[-1] | "\(.title): \(.quality_score)/100"' .state/published-posts.json

# View on GitHub Pages
# https://clawtv13.github.io/ai-automation-blog/
```

### 5. Automate (Optional)

```bash
crontab -e
```

Add:
```cron
# Master Content Agent - 2 posts/day
0 9 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

Save and exit.

---

## 🎯 What It Does

1. **Selects** best unpublished content from newsletter DB (score >= 30)
2. **Researches** SEO keywords, competitor gaps, search intent
3. **Generates** 1000-1400 word post with personal voice
4. **Scores** content quality (0-100) across 7 criteria
5. **Regenerates** if score < 70 (up to 2 times)
6. **Publishes** HTML file with perfect SEO
7. **Deploys** to GitHub Pages automatically
8. **Notifies** via Telegram (optional)

**Quality guarantee:** Every post scores 70+ or regenerates.

---

## 📊 Quality Criteria

| Criterion | Points | What's Checked |
|-----------|--------|----------------|
| Specific Examples | 20 | Concrete examples with names/numbers |
| Real Data | 15 | Stats, measurements, actual data |
| Personal Voice | 15 | Uses "I/you", conversational |
| Actionable Steps | 20 | Clear instructions |
| Proper Structure | 10 | H2/H3 hierarchy |
| No AI Patterns | 10 | No "As a...", "Imagine..." |
| SEO Optimized | 10 | Keywords natural |

**Total:** 100 points  
**Pass:** 70+  
**Excellent:** 85+

---

## 💰 Cost

- **Per post:** $0.05-$0.06
- **2 posts/day:** $0.10-$0.12/day
- **Monthly (60 posts):** $3.00-$3.60

**Models used:**
- SEO research: Claude 3.7 Sonnet (cheap)
- Content: Claude Sonnet 4 (quality)
- Scoring: Claude 3.7 Sonnet (cheap)

---

## 📁 Key Files

```
scripts/master-content-agent.py        # Main script
blog/posts/*.html                      # Generated posts
.state/published-posts.json            # All posts + scores
data/seo-research-cache.json           # SEO cache
logs/master-agent-2026-03.log          # Execution logs
```

---

## 🔍 Monitoring

**Check last run:**
```bash
tail -50 logs/master-agent-$(date +%Y-%m).log
```

**Today's posts:**
```bash
ls blog/posts/*$(date +%Y-%m-%d)*.html
```

**Recent quality scores:**
```bash
jq -r '.[-5:] | .[] | "\(.title[:60])...: \(.quality_score)/100"' .state/published-posts.json
```

**Cron status:**
```bash
crontab -l | grep master-content-agent
```

---

## 🚨 Troubleshooting

### "No content to publish"

**Problem:** Newsletter DB empty

**Fix:**
```bash
cd ../newsletter-ai-automation
python3 scripts/newsletter-sync.py
```

### "API key not set"

**Problem:** Environment variable missing

**Fix:**
```bash
echo $OPENROUTER_API_KEY  # Should output sk-...
export OPENROUTER_API_KEY="sk-..."
```

### "Deployment fails"

**Problem:** Git not configured

**Fix:**
```bash
cd blog/
git status
git push  # Test manually
```

### "Quality always < 70"

**Problem:** Content too generic

**Fix:** Lower threshold (edit script):
```python
MIN_QUALITY_SCORE = 65
```

---

## 📚 Full Documentation

- **MASTER-CONTENT-AGENT.md** - Complete system docs
- **MIGRATION-V2-TO-V3.md** - Upgrade from V2
- **CRON-CONFIG.md** - Automation setup
- **MASTER-AGENT-V3-DELIVERY.md** - Delivery report

**Start with:** MASTER-CONTENT-AGENT.md

---

## ✅ Daily Checklist

**First Week (monitor closely):**

- [ ] Check logs for errors
- [ ] Verify posts created
- [ ] Confirm GitHub deployment
- [ ] Review quality scores (>= 70)
- [ ] Check for duplicate content (should be 0)

**After automation:**

- [ ] Weekly: Review average quality score
- [ ] Monthly: Check total cost vs budget
- [ ] Monthly: Review SEO rankings (Google Search Console)

---

## 🎓 Example Output

**Input (from newsletter DB):**
```
Title: "AI overly affirms users asking for personal advice"
Score: 39
Summary: "Stanford study shows AI chatbots too sycophantic..."
```

**Output (generated post):**
```
Title: "Why Your AI Assistant Is Lying to You (And How to Fix It)"
Quality Score: 87/100
Word Count: 1,247
Keywords: "AI chatbot bias, sycophantic AI, personal advice"
Internal Links: 2
Structure:
  - Hook (personal story)
  - Stanford study breakdown (data)
  - Why this happens (technical)
  - How to spot it (actionable)
  - What to do (steps)
  - Real example
```

**Published at:**
`https://clawtv13.github.io/ai-automation-blog/posts/2026-03-29-why-your-ai-assistant-is-lying-to-you.html`

---

## 🎯 Success Indicators

**Week 1:**
- ✅ 7-14 posts generated
- ✅ All scores >= 70
- ✅ 0 duplicates
- ✅ All deployments successful

**Month 1:**
- ✅ 30-60 posts
- ✅ Average score 75+
- ✅ Cost $3-4
- ✅ 1-2 posts start ranking

**Month 3:**
- ✅ 90-180 posts
- ✅ 5+ posts in top 20
- ✅ Traffic increase
- ✅ Zero manual intervention

---

## 🚀 Next Steps

1. **Now:** Set API key and test run
2. **Today:** Review generated post quality
3. **This week:** Enable cron automation
4. **Next week:** Monitor daily, adjust if needed
5. **Next month:** Review traffic impact

---

## 💡 Pro Tips

1. **Don't edit posts manually** - Breaks voice consistency
2. **Monitor first week closely** - Catch issues early
3. **Trust the scoring system** - It's calibrated well
4. **Review SEO after 30 days** - Rankings take time
5. **Keep V2 as backup** - For first 2 weeks

---

## 📞 Quick Commands

```bash
# Generate 1 post now
python3 scripts/master-content-agent.py

# View logs
tail -f logs/master-agent-$(date +%Y-%m).log

# Check quality scores
jq '.[-10:] | .[] | .quality_score' .state/published-posts.json

# Count posts today
ls blog/posts/*$(date +%Y-%m-%d)*.html | wc -l

# Check cron
crontab -l

# View latest post
ls -lt blog/posts/*.html | head -1

# SEO cache stats
jq 'keys | length' data/seo-research-cache.json
```

---

**That's it!** You now have a fully automated, SEO-optimized content generation system.

**Questions?** Check MASTER-CONTENT-AGENT.md

**Status:** ✅ Production-Ready  
**Version:** 3.0.0
