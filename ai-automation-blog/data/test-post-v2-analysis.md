# Test Post Generation - V2 Prompt Analysis

## Test Setup
**Date:** 2026-04-02  
**Prompt Version:** v2 (readability-focused)  
**Model:** anthropic/claude-sonnet-4  

## Prompt Changes Summary

### Old Prompt Issues:
- ❌ No readability guidelines
- ❌ No sentence length targets
- ❌ No word complexity limits
- ❌ Average Flesch score: 43.3/100 (college level)
- ❌ Complex words: 28% of content

### New Prompt v2 Additions:
- ✅ Target: Flesch Reading Ease 50-70
- ✅ Sentence length: 15-20 words average
- ✅ Paragraph max: 2-3 sentences
- ✅ Active voice requirement (90%)
- ✅ Simple word replacements (utilize → use)
- ✅ Concrete examples over abstract concepts
- ✅ Self-check questions for writer

## Expected Improvements

Based on prompt engineering research:

**Readability Score:**
- Before: 43.3/100 (college level)
- Target: 50-70/100 (8th-9th grade)
- Expected: +15-20 point improvement

**Sentence Length:**
- Before: 14.5 words average (slightly short but varied poorly)
- Target: 15-20 words (with intentional variation)
- Expected: More consistent rhythm

**Complex Words:**
- Before: ~280 per 1000 words (28%)
- Target: <200 per 1000 words (20%)
- Expected: 25-30% reduction

## Validation Checklist

When next post is generated (10:00 UTC tomorrow), verify:

- [ ] Flesch Reading Ease: 50-70
- [ ] Flesch-Kincaid Grade: 8-9
- [ ] Avg sentence length: 15-20 words
- [ ] No sentences over 30 words
- [ ] Paragraphs: 2-3 sentences max
- [ ] Complex words: <20% of total
- [ ] Active voice used throughout
- [ ] Concrete examples (numbers, specifics)

## Sample Comparison

### Old Prompt Style (FK: 43.3):
> "Utilizing sophisticated automation frameworks enables entrepreneurs to systematically optimize resource allocation across operational workflows, thereby facilitating enhanced productivity metrics."

**Issues:** 
- 20+ words
- Complex vocabulary (utilizing, facilitating, systematically)
- Passive construction
- Abstract concepts

### New Prompt v2 Style (Target FK: 50-70):
> "Automation tools help you save time on daily tasks. They handle the boring work. You focus on customers. Sarah saved 15 hours weekly using this exact setup."

**Improvements:**
- 6-12 words per sentence
- Simple vocabulary (help, save, handle)
- Active voice
- Concrete example (Sarah, 15 hours)

## Technical Implementation

### File Structure:
```
prompts/
  └── blog-generation-v2.txt (new prompt with readability focus)

scripts/
  └── blog-auto-post-v2.py (updated to read from prompt file)
```

### Code Changes:
1. Added prompt file loading mechanism
2. Fallback to simple prompt if file missing
3. Placeholder replacement for dynamic data
4. Version tracking in analytics

## Testing Recommendation

**Manual Test (when API key available):**
```bash
cd /root/.openclaw/workspace/ai-automation-blog
export OPENROUTER_API_KEY="your_key_here"
python3 scripts/blog-auto-post-v2.py --test
```

**Automated Test (cron job 10:00 UTC tomorrow):**
- Script will automatically use new prompt
- Monitor first 2-3 posts for readability scores
- Compare against baseline (43.3 → target 50-70)

## Rollback Plan

If readability doesn't improve:
1. Check prompt is being loaded correctly
2. Verify model follows instructions
3. Try alternative phrasing in prompt
4. Consider post-generation rewrite pass

## Success Metrics

**Phase 1 (1-2 days):**
- Readability score > 45 (improvement from 43.3)
- No generation failures

**Phase 2 (3-5 days):**
- Readability score 50-70 (target achieved)
- Consistent quality across posts

**Phase 3 (1 week):**
- Sustained 50-70 scores
- User engagement metrics (if available)
