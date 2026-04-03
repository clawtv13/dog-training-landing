# 🚀 V3 PROMPTS DEPLOYMENT GUIDE

## Overview

18 prompts optimized and ready for production deployment.

**DO NOT deploy all at once.** Roll out in 3 phases for safe testing.

---

## Phase 1: CRITICAL (Deploy Monday)

### 1. CleverDogMethod Blog Generation

**File:** `/root/.openclaw/workspace/scripts/cleverdogmethod-autonomous.py`

**Current location:** Line 144

**Steps:**

1. Backup V2:
```bash
cp /root/.openclaw/workspace/scripts/cleverdogmethod-autonomous.py \
   /root/.openclaw/workspace/scripts/cleverdogmethod-autonomous-v2.py
```

2. Open V3 prompts file:
```bash
nano /root/.openclaw/workspace/ai-automation-blog/PROMPTS-OPTIMIZED-V3.txt
```

3. Find section: "🔴 CLEVERDOGMETHOD BLOG GENERATION"

4. Copy entire optimized prompt (starts with "# CleverDogMethod Blog Post Generation")

5. Replace in script:
```python
# OLD (line 144):
prompt = f"""Write a comprehensive dog training blog post about: {keyword}..."""

# NEW (paste optimized V3):
prompt = f"""# CleverDogMethod Blog Post Generation

## ROLE
Certified professional dog trainer (CPDT-KA)...
[full optimized prompt]
"""
```

6. Test:
```bash
cd /root/.openclaw/workspace
export OPENROUTER_API_KEY="sk-or-v1-..."
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="8116230130"

# Dry run (don't publish)
python3 scripts/cleverdogmethod-autonomous.py --test
```

7. Compare output quality:
- Does it have case studies? (3+)
- Does it cite research? (1+)
- Is voice authoritative?
- Are steps numbered?

8. If yes to all → Deploy:
```bash
# Will run at next cron (20:00 UTC)
# Or run manually:
python3 scripts/cleverdogmethod-autonomous.py
```

9. Monitor first 2 posts (20:00 today, 08:00 tomorrow)

**Expected improvement:**
- Quality: 60-75 → 80-90
- Voice: Bland → Expert
- Examples: Generic → Specific (names, breeds, timeframes)

---

### 2. Newsletter Content Scoring

**File:** `/root/.openclaw/workspace/newsletter-ai-automation/scripts/realtime-research.py`

**Location:** Score calculation function

**Steps:**

1. Backup:
```bash
cp /root/.openclaw/workspace/newsletter-ai-automation/scripts/realtime-research.py \
   /root/.openclaw/workspace/newsletter-ai-automation/scripts/realtime-research-v2.py
```

2. Find V3 prompt in PROMPTS-OPTIMIZED-V3.txt:
   Section: "🔴 NEWSLETTER CONTENT SCORING"

3. Update scoring logic with explicit rubric

4. Test:
```bash
cd /root/.openclaw/workspace/newsletter-ai-automation
python3 scripts/realtime-research.py --test
```

5. Compare 5 articles scored V2 vs V3
   - Should get same scores for same content (consistency)

6. Deploy - will run at 18:00 UTC (2h from now)

**Expected improvement:**
- Consistency: 70% → 95%
- Accuracy: 75% → 90%
- Premium items (35+): 30% → 45%

---

### 3. Master Content SEO Research

**File:** `/root/.openclaw/workspace/ai-automation-blog/scripts/master-content-agent.py`

**Location:** SEO research phase

**Steps:**

1. Backup:
```bash
cp /root/.openclaw/workspace/ai-automation-blog/scripts/master-content-agent.py \
   /root/.openclaw/workspace/ai-automation-blog/scripts/master-content-agent-v2.py
```

2. Find V3 prompt: "🔴 MASTER CONTENT SEO RESEARCH"

3. Replace SEO research prompt in script

4. Test with real topic:
```bash
python3 scripts/master-content-agent.py --topic "AI automation for email" --test-seo
```

5. Verify output includes:
   - Keyword density targets
   - Competition analysis
   - Internal linking opportunities
   - Optimized title examples

6. Deploy - will run tomorrow 10:00 UTC (before blog post)

**Expected improvement:**
- Rankings: +30% (better keyword targeting)
- CTR: +20% (better titles/meta)
- Internal links: 0-1 → 3-5 per post

---

## Phase 2: HIGH (Deploy Wednesday)

Repeat process for:

4. Master Content Generation Phase 2
5. Email Sequence Architect  
6. Product Creator

**Wait 48h after Phase 1** to validate improvements before deploying Phase 2.

---

## Phase 3: REMAINING (Deploy Friday)

Deploy prompts 7-18 after validating Phase 1 + 2 results.

---

## Testing Checklist (Per Prompt)

Before marking prompt as "deployed":

```
□ Backup V2 version created
□ V3 prompt copied correctly
□ Test run completed (3 samples)
□ Output format valid
□ Quality score measured
□ Compared to V2 baseline
□ No errors/warnings
□ Monitoring enabled
```

---

## Rollback Procedure

If V3 prompt performs worse:

1. Stop automation (if running)
2. Restore V2 backup:
```bash
cp script-v2.py script.py
```
3. Document issue
4. Analyze what went wrong
5. Iterate V3 prompt
6. Re-test before re-deploy

---

## Monitoring (Week 1)

Track these metrics:

**CleverDogMethod:**
- Post quality (subjective 0-10)
- Case studies included? (yes/no)
- Scientific citations? (yes/no)
- Voice authority (weak/medium/strong)

**Newsletter Scoring:**
- Score consistency (same article = same score?)
- Premium items %
- False positives reduced?

**SEO Research:**
- Keywords targeted
- Rankings after 2 weeks
- Internal links per post
- CTR on Google

**Aggregate:**
- Regeneration rate: Target <3%
- Quality average: Target 85+
- Voice consistency: Target 90%+

---

## Expected Timeline

**Monday (deploy Phase 1):**
- 3 critical prompts live
- CleverDogMethod at 20:00 first V3 post
- Newsletter research at 18:00 uses V3 scoring

**Tuesday-Wednesday:**
- Monitor quality
- Check regeneration rate
- Measure voice consistency

**Thursday (if good):**
- Deploy Phase 2 (3 high-priority)
- Continue monitoring

**Next Monday (if good):**
- Deploy Phase 3 (9 remaining)
- System complete V3

**Week 2:**
- All 18 prompts live
- Measure aggregate improvements
- Document learnings
- Iterate framework

---

## Success Criteria

Phase 1 successful if:
- ✅ Quality +20% or more
- ✅ Regenerations <3%
- ✅ No parsing errors
- ✅ Voice consistency >85%

Then proceed to Phase 2.

If not successful:
- Analyze failure
- Adjust prompts
- Re-test
- Don't deploy Phase 2 yet

---

## Quick Deploy Commands

### Deploy CleverDogMethod V3:
```bash
cd /root/.openclaw/workspace
cp scripts/cleverdogmethod-autonomous.py scripts/cleverdogmethod-autonomous-v2.py
# [manually update prompt in script]
python3 scripts/cleverdogmethod-autonomous.py --test
# If good, let cron run at 20:00 UTC
```

### Deploy Newsletter Scoring V3:
```bash
cd /root/.openclaw/workspace/newsletter-ai-automation
cp scripts/realtime-research.py scripts/realtime-research-v2.py
# [manually update scoring logic]
python3 scripts/realtime-research.py --test
# If good, let cron run at 18:00 UTC
```

### Deploy SEO Research V3:
```bash
cd /root/.openclaw/workspace/ai-automation-blog
cp scripts/master-content-agent.py scripts/master-content-agent-v2.py
# [manually update SEO prompt]
python3 scripts/master-content-agent.py --test-seo
# If good, let cron run tomorrow 10:00 UTC
```

---

## Files Reference

- **PROMPTS-OPTIMIZED-V3.txt** - All optimized prompts (source)
- **OPTIMIZATION-RESULTS.md** - What changed and why
- **PROMPT-OPTIMIZER-AGENT.md** - Framework for future
- **COMPLETE-PROMPT-INVENTORY.md** - Full audit

---

Ready to deploy Monday. 🚀
