# Migration Guide: V2 → V3

**Upgrading from blog-auto-post-v2.py to master-content-agent.py**

---

## 🎯 Why Migrate?

| Problem in V2 | Solution in V3 |
|---------------|----------------|
| SEO added as afterthought | SEO research BEFORE writing |
| No quality control | Auto-scoring + regeneration |
| Generic AI voice | Personal Alex Chen persona |
| Manual keyword stuffing | Natural keyword embedding |
| No internal linking | Auto-detected & added |
| Variable quality | 70+ score guaranteed |

**Bottom line:** V3 writes content that actually ranks.

---

## ⚙️ Step-by-Step Migration

### 1. Backup Current System

```bash
cd /root/.openclaw/workspace/ai-automation-blog

# Backup V2 script
cp scripts/blog-auto-post-v2.py scripts/blog-auto-post-v2.py.backup

# Backup state
cp -r .state .state.backup.$(date +%Y%m%d)

# Backup logs
tar -czf logs/v2-logs-backup-$(date +%Y%m%d).tar.gz logs/*.log
```

### 2. Verify Prerequisites

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check required packages
python3 -c "import requests, sqlite3, hashlib"

# Verify API key
echo $OPENROUTER_API_KEY  # Should output sk-...

# Check newsletter DB
ls -lh /root/.openclaw/workspace/newsletter-ai-automation/database/newsletter.db
```

### 3. Install V3

```bash
# V3 is already in place at:
# scripts/master-content-agent.py

# Make executable
chmod +x scripts/master-content-agent.py

# Create required directories
mkdir -p data logs .state
```

### 4. Test Run (Dry Run)

```bash
# Test V3 generation
python3 scripts/master-content-agent.py

# Should see:
# 🔍 Phase 1: Conducting SEO research...
# ✍️  Phase 2: Generating SEO-optimized content...
# 📊 Phase 3: Scoring content quality...
# etc.
```

### 5. Update Cron Jobs

**Old cron (V2):**
```cron
0 9,17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/blog-auto-post-v2.py >> logs/cron.log 2>&1
```

**New cron (V3):**
```cron
0 9,17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Update crontab:**
```bash
crontab -e

# Replace old line with new line
# Save and exit
```

**Verify:**
```bash
crontab -l | grep master-content-agent
```

### 6. Monitor First Week

**Check logs daily:**
```bash
tail -f logs/master-agent-$(date +%Y-%m).log
```

**Look for:**
- ✅ Quality scores >= 70
- ✅ No duplicate content
- ✅ GitHub deployments succeed
- ✅ Posts render correctly

**Red flags:**
- ❌ Scores consistently < 70 (adjust thresholds)
- ❌ Deployment failures (check git config)
- ❌ API timeout errors (check API key)

### 7. Decommission V2 (After 2 Weeks)

```bash
# Once confident V3 works:
# Remove V2 from cron
crontab -e  # Delete V2 line

# Archive V2 script
mv scripts/blog-auto-post-v2.py scripts/archive/

# Keep backups for 30 days
```

---

## 🔄 State Compatibility

### V2 State Files

```
.state/
├── published-posts.json       # ✅ Compatible (V3 reads this)
├── analytics.json             # ⚠️  V3 doesn't use (safe to keep)
├── errors.json                # ⚠️  V3 doesn't use (safe to keep)
├── content-queue.json         # ⚠️  V3 doesn't use (safe to keep)
└── health-status.json         # ⚠️  V3 doesn't use (safe to keep)
```

### V3 State Files

```
.state/
├── published-posts.json       # ✅ Shared with V2
├── content-fingerprints.json  # 🆕 New (duplicate detection)

data/
└── seo-research-cache.json    # 🆕 New (SEO cache)
```

**Migration notes:**
- V3 reads existing `published-posts.json` → no data loss
- V2 files remain for analytics/debugging
- V3 adds new files for enhanced features

---

## 🎚️ Configuration Changes

### V2 Configuration

```python
# blog-auto-post-v2.py
POSTS_PER_DAY = 2
MIN_QUALITY_SCORE = 30        # Newsletter score
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 5
```

### V3 Configuration

```python
# master-content-agent.py
MIN_QUALITY_SCORE = 70        # Content quality (not newsletter!)
TARGET_QUALITY_SCORE = 85
MAX_REGENERATION_ATTEMPTS = 2
MIN_NEWSLETTER_SCORE = 30     # Newsletter filter (same as V2)
```

**Key difference:** V3 has TWO quality thresholds:
1. `MIN_NEWSLETTER_SCORE` = source content filter
2. `MIN_QUALITY_SCORE` = generated content filter

---

## 🧪 Testing Checklist

### Before Full Deployment

- [ ] V3 test run completes without errors
- [ ] Generated post has quality score >= 70
- [ ] Post appears in `posts/` directory
- [ ] `posts/index.json` updates correctly
- [ ] GitHub commit succeeds
- [ ] Post renders on https://clawtv13.github.io/ai-automation-blog/
- [ ] SEO meta tags present in HTML
- [ ] Internal links work (if added)
- [ ] Telegram notification sent (if configured)

### After First Week

- [ ] 7+ posts generated successfully
- [ ] Average quality score >= 75
- [ ] 0 duplicate content detected
- [ ] All deployments successful
- [ ] No API budget overruns (< $0.50/week)

---

## 🚨 Rollback Plan

**If V3 has issues, rollback to V2:**

### Option A: Immediate Rollback

```bash
# 1. Stop V3 cron
crontab -e  # Comment out V3 line

# 2. Re-enable V2 cron
crontab -e  # Uncomment V2 line

# 3. Restore V2 script (if deleted)
cp scripts/blog-auto-post-v2.py.backup scripts/blog-auto-post-v2.py

# 4. Test V2
python3 scripts/blog-auto-post-v2.py
```

### Option B: Parallel Run (Safer)

```bash
# Run BOTH V2 and V3 in parallel for 1 week

# Crontab:
0 9 * * * python3 scripts/master-content-agent.py >> logs/v3-cron.log 2>&1
0 17 * * * python3 scripts/blog-auto-post-v2.py >> logs/v2-cron.log 2>&1

# Compare results after 7 days
# Keep the better one
```

---

## 📊 Quality Comparison

### Before (V2)

**Sample V2 post:**
```
Title: "New AI Tool Announced"
Content: Generic summary of tool features
SEO: Added after (keyword stuffing)
Quality: Variable (30-80)
Voice: AI corporate-speak
```

### After (V3)

**Sample V3 post:**
```
Title: "How I Automated My Inbox with AI (Saved 8hrs/week)"
Content: 
  - Personal story with data
  - Step-by-step tutorial
  - Real screenshots/examples
  - Mistakes to avoid section
SEO: Integrated from start (natural keywords)
Quality: Guaranteed 70+ (scored & regenerated)
Voice: Alex Chen personal style
```

---

## 🎯 Migration Timeline

### Week 1: Testing
- ✅ Day 1: Install V3, test run
- ✅ Day 2-3: Monitor first 2-3 posts
- ✅ Day 4-7: Compare V2 vs V3 quality

### Week 2: Parallel Run
- ✅ Run both V2 and V3 (different times)
- ✅ Compare SEO, quality scores, engagement
- ✅ Verify no duplicate content

### Week 3: Full V3 Migration
- ✅ Disable V2 cron
- ✅ V3 becomes primary
- ✅ Monitor closely

### Week 4: Cleanup
- ✅ Archive V2 files
- ✅ Document lessons learned
- ✅ Optimize V3 settings if needed

---

## 🔧 Troubleshooting

### Issue: "No content to publish"

**Cause:** Newsletter DB empty or all items used

**Fix:**
```bash
# Check newsletter DB
python3 -c "
import sqlite3
conn = sqlite3.connect('/root/.openclaw/workspace/newsletter-ai-automation/database/newsletter.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM content_items WHERE total_score >= 30 AND featured_in_edition IS NULL')
print(f'Available items: {c.fetchone()[0]}')
"

# If 0, run newsletter sync first
cd ../newsletter-ai-automation
python3 scripts/newsletter-sync.py
```

### Issue: "Quality score always < 70"

**Cause:** Content too generic or AI-patterns detected

**Fix:**
1. Check logs for specific feedback
2. Adjust persona in script
3. Lower threshold temporarily:
   ```python
   MIN_QUALITY_SCORE = 65  # In master-content-agent.py
   ```

### Issue: "SEO research fails"

**Cause:** API timeout or cache corruption

**Fix:**
```bash
# Clear SEO cache
rm data/seo-research-cache.json

# Test API
python3 -c "
import os, requests
headers = {'Authorization': f'Bearer {os.getenv(\"OPENROUTER_API_KEY\")}'}
r = requests.post('https://openrouter.ai/api/v1/chat/completions', 
                  headers=headers, 
                  json={'model': 'anthropic/claude-3.7-sonnet', 
                        'messages': [{'role': 'user', 'content': 'test'}]})
print(r.status_code)
"
```

### Issue: "Deployment fails"

**Cause:** Git auth or network

**Fix:**
```bash
cd blog/

# Check git status
git status

# Test push
git pull
git push

# If auth fails, check SSH keys or token
```

---

## 💰 Cost Comparison

### V2 Costs
- ~$0.04/post
- ~$2.40/month (60 posts)

### V3 Costs
- ~$0.05-$0.06/post
- ~$3.00-$3.60/month (60 posts)

**Increase:** ~$0.60/month (+25%)

**Why worth it:**
- Quality guarantee (70+ score)
- SEO research included
- Auto-regeneration
- Internal linking
- Duplicate prevention

**ROI:** Better rankings = more traffic = pays for itself

---

## ✅ Success Metrics

**Track these to measure migration success:**

### Week 1
- [ ] All V3 posts score >= 70
- [ ] 0 deployment failures
- [ ] 0 duplicate content

### Month 1
- [ ] Average quality score >= 75
- [ ] 1+ posts rank in top 20 for target keyword
- [ ] Total cost < $4/month

### Month 3
- [ ] 5+ posts rank in top 10
- [ ] Organic traffic up 20%
- [ ] 0 manual intervention needed

---

## 📞 Support

**Issues during migration?**

1. Check logs: `logs/master-agent-*.log`
2. Review this guide
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. Rollback to V2 if critical

**Post-migration optimization:**

1. Review quality scores weekly
2. Adjust thresholds if needed
3. Monitor SEO rankings (Google Search Console)
4. Compare V2 vs V3 traffic after 30 days

---

**Migration Checklist:**

- [ ] Backup V2 system
- [ ] Test V3 manually
- [ ] Update cron job
- [ ] Monitor first week
- [ ] Compare results after 2 weeks
- [ ] Decommission V2 after 1 month
- [ ] Document lessons learned

**Status:** Ready to migrate  
**Risk:** Low (V2 backup available)  
**Expected downtime:** 0 (parallel run possible)
