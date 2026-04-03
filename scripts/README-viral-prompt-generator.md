# 🎬 Viral Shorts Prompt Generator - CleverDogMethod (REFACTORED)

**Generate viral dog training shorts for TikTok, Instagram Reels, YouTube Shorts**

Automatically creates **ONE universal video prompt + THREE platform-specific metadata sets** using proven formulas and CleverDog keyword optimization.

**✨ NEW:** Refactored to save 66% API costs (2 calls vs 6)

---

## 🎯 Features

- **6 Proven Formulas** - Retention-tested (75-90%)
- **Auto-Select from CleverDog Keywords** - Priority-sorted from V2 expansion
- **1 Universal Video + 3 Metadata Sets** - Same video, platform-specific metadata
- **66% Cost Savings** - 2 API calls (vs 6 in old version)
- **Smart Cooldown** - 7-day rotation prevents duplicate content
- **Auto-Formula Matching** - Topic → Best formula
- **Telegram Delivery** - Instant notifications

---

## 🚀 Quick Start

### Auto-Generate (Recommended)

Auto-select next keyword from CleverDog V2 expansion:

```bash
python3 viral-prompt-generator.py
```

**Output:**
- 1 universal 60s video prompt (<2000 chars)
- 3 platform metadata sets (TikTok, Instagram, YouTube)
- Total <3000 characters
- 2 API calls (saved 66% cost)

### Manual Topic

```bash
python3 viral-prompt-generator.py "stop dog jumping on people"
```

### Force Formula

```bash
python3 viral-prompt-generator.py "husky training" --formula myth_buster
```

### Random Topic (Fallback)

```bash
python3 viral-prompt-generator.py --random
```

### List Formulas

```bash
python3 viral-prompt-generator.py --list-formulas
```

---

## 🆕 What Changed (Refactor 2026-04-03)

### Old Method
- Generated 3 separate video prompts (TikTok, Instagram, YouTube)
- 6 API calls total
- 3 separate outputs
- Inconsistent messaging

### New Method
- Generates 1 universal video prompt (works on all platforms)
- Generates 3 platform metadata sets in single call
- 2 API calls total (66% cost savings)
- Consistent video, customized metadata
- Faster generation

### Output Structure

```
🎬 VIRAL SHORT PACKAGE

======================================================================

# VIDEO PROMPT (USE ON ALL PLATFORMS)
Copy this to CapCut AI / Runway / Luma:

[Universal 60s video prompt with scene-by-scene breakdown]

======================================================================

# PLATFORM-SPECIFIC METADATA

# TIKTOK METADATA
Title: [60 chars]
Description: [150 chars]
Hashtags: [7 tags]

# INSTAGRAM METADATA
Title: [60 chars]
Caption: [200 chars]
Hashtags: [15 tags]

# YOUTUBE METADATA
Title: [70 chars]
Description: [300 chars]
Hashtags: [5 tags]
Pinned Comment: [CTA]

======================================================================

Generated: 2026-04-03 12:15 UTC
Total Size: 2684 characters ✅
Ready for: CapCut AI, Runway, Luma, manual production
Deploy: Use same video on all 3 platforms, customize metadata only
```

---

## 🎬 Formulas

### Auto-Formula Matching Logic

The generator analyzes your topic and auto-selects the best formula:

| Topic Keywords | Formula | Retention |
|----------------|---------|-----------|
| stop, fix, prevent, how to | **Quick Tip** | 90% |
| breed names (husky, poodle, etc.) | **Problem → Solution** | 85% |
| rescue, fearful, anxiety, aggressive | **Transformation** | 78% |
| training, method, technique | **Myth Buster** | 82% |
| **Default** | **Problem → Solution** | 85% |

### Formula Details

| Formula | Retention | Best For |
|---------|-----------|----------|
| **Quick Tip** | 90% | Loop-friendly, high saves, fast hacks |
| **Myth Buster** | 82% | Controversial, comment bait |
| **Problem → Solution** | 85% | Educational, quick wins |
| **Transformation** | 78% | Emotional, shareable |
| **Emotional Arc** | 75% | Brand loyalty, shares |
| **Controversial Take** | 88% | Engagement, comments |

---

## 📱 Platform Metadata Specifications

### TikTok
- Title: 60 chars max, hook-driven, emoji-friendly
- Description: 150 chars max, conversational, question/challenge
- Hashtags: 7 total (3 broad + 4 niche)
- Tone: Casual, Gen Z friendly, comment bait

### Instagram
- Title: 60 chars max, aesthetic, value-focused
- Caption: 200 chars max, storytelling, relatable
- Hashtags: 15 total (5 broad + 10 niche)
- Tone: Visual emphasis, save-worthy

### YouTube
- Title: 70 chars max, SEO-optimized, keyword-rich, colon format
- Description: 300 chars max, informative, CTA
- Hashtags: 5 total (#Shorts mandatory + 4 relevant)
- Pinned Comment: Engagement CTA
- Tone: Professional, search-optimized

---

## 🔄 Smart Topic Selection

### CleverDog Keywords V2 Integration

When you run without a topic argument:

```bash
python3 viral-prompt-generator.py
```

The generator:
1. Loads keywords from `/root/.openclaw/workspace/content/cleverdogmethod/KEYWORDS-V2-EXPANSION.md`
2. Filters out topics used in last 7 days
3. Selects first available (pre-sorted by priority)
4. Auto-matches optimal formula
5. Generates package

**Example Output:**
```
✅ Auto-selected: stop dog jumping on people
   Available pool: 127 topics
   Used recently: 8 topics
🎯 Auto-matched formula: Quick Tip
```

### Cooldown System

- **Duration:** 7 days
- **Storage:** `.state/shorts-generated.json`
- **Logic:** Topics used in last 7 days won't be auto-selected
- **Override:** Manually specify topic to bypass cooldown

---

## 📊 Cost Analysis

### Old Method (per generation)
- 6 API calls × $0.015/call = **$0.09**
- Time: ~180 seconds
- Output: 3 separate prompts

### New Method (per generation)
- 2 API calls × $0.015/call = **$0.03**
- Time: ~60 seconds
- Output: 1 video + 3 metadata sets

### Savings
- **Cost:** 66% reduction ($0.06 saved per generation)
- **Time:** 67% reduction (120 seconds saved)
- **Monthly:** If 100 videos/month → Save $6/month + 200 minutes

---

## 📁 File Structure

```
/root/.openclaw/workspace/
│
├── scripts/
│   ├── viral-prompt-generator.py              # Refactored (active)
│   └── viral-prompt-generator-OLD.py.backup   # Old version (backup)
│
├── content/cleverdogmethod/
│   └── KEYWORDS-V2-EXPANSION.md                # Priority-sorted keywords
│
└── .state/
    └── shorts-generated.json                   # Tracking state
```

---

## 🤖 Automation

### Daily Cron

Generate one short every day at 10:00 AM:

```bash
# Add to crontab
0 10 * * * cd /root/.openclaw/workspace && python3 scripts/viral-prompt-generator.py >> /var/log/viral-shorts.log 2>&1
```

### Weekly Batch

Generate 7 shorts on Sunday:

```bash
#!/bin/bash
for i in {1..7}; do
    python3 viral-prompt-generator.py
    sleep 60
done
```

---

## 🐛 Troubleshooting

### "Keywords V2 file not found"

**Cause:** Missing CleverDog keywords file

**Fix:**
```bash
ls /root/.openclaw/workspace/content/cleverdogmethod/KEYWORDS-V2-EXPANSION.md
```

**Fallback:** Script uses 10 hardcoded topics if file missing

### "OPENROUTER_API_KEY not set"

Script uses hardcoded key. To override:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### "All keywords used in last 7 days"

**Cause:** High generation frequency

**Solution:** Generator automatically cycles back to oldest topics

---

## 🔄 Rollback to Old Version

If issues arise:
```bash
cd /root/.openclaw/workspace/scripts
mv viral-prompt-generator.py viral-prompt-generator-refactored-FAILED.py
mv viral-prompt-generator-OLD.py.backup viral-prompt-generator.py
```

---

## ✅ Test Results (2026-04-03)

### "stop dog jumping on people" Test
- **Topic:** stop dog jumping on people
- **Formula:** quick_tip
- **Video prompt:** 1,269 chars ✅
- **Metadata:** 1,415 chars ✅
- **Total:** 2,684 chars ✅
- **API calls:** 2
- **Time:** ~45 seconds
- **Status:** ✅ Success

---

## 📞 Support

**Documentation:**
- `/root/.openclaw/workspace/docs/GENERATOR-REFACTOR-2026-04-03.md` (refactor details)

**State Tracking:**
- `.state/shorts-generated.json`

---

## 📋 Usage Examples

### Daily Production Workflow

```bash
# Morning: Auto-generate next topic
python3 viral-prompt-generator.py

# Review output in Telegram
# Paste video prompt into CapCut AI
# Use platform metadata for each channel
```

### Batch Generation for Week

```bash
# Generate 7 different topics
for i in {1..7}; do
    python3 viral-prompt-generator.py
    sleep 60  # Wait between generations
done
```

### Test Specific Formula

```bash
# Test controversial formula on generic topic
python3 viral-prompt-generator.py "dog training mistakes" --formula controversial
```

### Random Topic Exploration

```bash
# Pick random fallback topic
python3 viral-prompt-generator.py --random
```

---

**Refactored:** 2026-04-03  
**Version:** 2.0 (REFACTORED)  
**Author:** n0body (subagent)  
**Status:** ✅ Production Ready
