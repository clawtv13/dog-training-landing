# PENDING: Video Analytics Tracker + Script Optimizer

_Created: 2026-03-21 | Status: Idea / Backlog_

---

## Concept

Build automated system that tracks video performance across YouTube, TikTok, and Instagram, then uses that data to optimize future script generation.

---

## System Components

### 1. Analytics Tracker (`track-analytics.py`)
- Extracts metrics from YouTube, TikTok, IG APIs
- Saves to JSON with timestamp
- Runs daily via cron
- Output: `/workspace/analytics/{channel}-metrics.json`

### 2. Pattern Analyzer (`analyze-patterns.py`)
- Reads historical analytics
- Identifies top 20% performers
- Generates insights (hook types, structure, length, CTA patterns)
- Output: Markdown report with recommendations

### 3. Script Generator (Enhanced)
- Reads pattern insights
- Generates scripts based on proven patterns
- Avoids elements from low performers
- Adapts to what works for each channel

---

## Feedback Loop

```
VIDEO → ANALYTICS → INSIGHTS → OPTIMIZED SCRIPTS → BETTER VIDEOS
```

---

## Metrics to Track

| Metric | Platform | Importance |
|--------|----------|------------|
| Views | All | High |
| Likes | All | Medium |
| Comments | All | Medium |
| Shares | TikTok, IG | High (virality indicator) |
| Watch time % | YouTube | Critical |
| CTR (link clicks) | All | Critical (for funnel) |
| Saves | IG | High (intent signal) |

---

## Pattern Analysis Examples

**Hook Analysis:**
- "If you..." → 2x views vs "Do you...?"
- "Why your X..." → 1.8x vs "How to X"
- Shocking statements → 3x vs questions

**Structure:**
- Problem-solution → 1.5x vs educational list
- Authority-backed (Navy SEAL, NASA) → 2.5x vs generic
- 48-52s videos → better retention than 60s

**CTA:**
- Urgency ("tonight") → 1.7x CTR vs no urgency
- Specific ("link in bio") → 1.4x vs vague

---

## API Requirements

### YouTube Data API v3
- Free tier: 10,000 quota units/day
- Needed scopes: `youtube.readonly`
- Docs: https://developers.google.com/youtube/v3

### TikTok API
- Research API availability (may require TikTok Business)
- Alternative: Scraping via unofficial methods

### Instagram Graph API
- Requires Facebook Business account
- Complex authentication
- Alternative: Manual CSV export

---

## Implementation Timeline

**When to build:**
- After 30+ videos published (need baseline data)
- When manual analysis becomes tedious
- Before scaling to paid ads

**Effort:** 1-2 days development  
**Maintenance:** Minimal (automated)  
**ROI:** High (better scripts = more views = more revenue)

---

## Dependencies

- Python libraries: `requests`, `pandas`, `matplotlib` (for visualization)
- YouTube API key
- TikTok credentials (if API available)
- Instagram credentials (if API available)
- Cron setup for daily runs

---

## Future Enhancements

- Real-time alerts when video goes viral (>100K views in 24h)
- A/B testing framework (test 2 hooks for same topic)
- Competitor analysis (track competitor videos in same niche)
- AI thumbnail analyzer (correlate thumbnail style with views)
- Sentiment analysis of comments (what people love/hate)

---

## Next Steps (When Ready)

1. Publish 30 videos across CALMORA + MONEYSTACK
2. Collect manual metrics for baseline
3. Build tracker scripts
4. Implement automation
5. Start optimization loop

**Status:** Deferred until content production phase complete.
