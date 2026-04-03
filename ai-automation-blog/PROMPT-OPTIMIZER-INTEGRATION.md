# Prompt Optimizer Integration Guide

## 🧠 Overview

The Prompt Optimizer is a learning loop that:
1. Analyzes your best-performing blog posts
2. Extracts patterns (word count, structure, tone)
3. Generates improved prompt variations using AI
4. Runs A/B tests to find the best prompt
5. Automatically promotes winners to production

## 📂 Files Created

```
ai-automation-blog/
├── scripts/
│   ├── prompt-optimizer.py          # Main optimizer script
│   ├── ab-test-integration.py       # A/B test helper module
│   └── blog-auto-post-v2.py         # (needs integration)
└── prompts/
    ├── blog-generation.txt          # Current production prompt
    ├── ab-test.json                 # Active A/B test config
    └── candidates/
        └── v{timestamp}-{1-5}.txt   # Generated prompt candidates
```

## 🚀 Quick Start

### Step 1: Generate Prompt Candidates

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/prompt-optimizer.py optimize
```

This will:
- Analyze your top 10 posts from the last 30 days
- Extract successful patterns
- Generate 5 improved prompt variations
- Setup an A/B test (7 days by default)

**Requirements:**
- At least 3 published posts in `blog/md/`
- `OPENROUTER_API_KEY` environment variable set

### Step 2: Run Blog with A/B Testing

The A/B test integration module (`ab-test-integration.py`) provides helper functions to:
- Select random prompt variants (50/50 A vs B)
- Track which variant was used for each post
- Log quality scores for evaluation

### Step 3: Evaluate Results

After 7 days:

```bash
python3 scripts/prompt-optimizer.py evaluate
```

This will:
- Compare average quality scores for variant A vs B
- If variant B is better by >5 points: promote to production
- Archive the old prompt
- Mark the test as complete

## 🔧 Integration with blog-auto-post-v2.py

To enable A/B testing in your blog generation, add this code to `blog-auto-post-v2.py`:

### Option A: Import the module (recommended)

```python
# At the top of blog-auto-post-v2.py
from ab_test_integration import select_prompt_variant, log_ab_test_result

# In generate_blog_post() function, replace the hardcoded prompt with:
def generate_blog_post(item: Dict) -> Optional[str]:
    # ... existing code ...
    
    # Select prompt variant (A/B test or current)
    variant, prompt_template = select_prompt_variant()
    
    # Build full prompt
    prompt = f"""{prompt_template}

## INPUT
- Title: {item["title"]}
- URL: {item["url"]}
- Summary: {item["summary"]}
- Source: {item["source"]}

## TASK
Generate practical blog post targeting solopreneurs...
"""
    
    # ... rest of generation code ...
    
    # After successful post generation, log the result
    quality_score = calculate_quality_score(content)  # Your existing scoring
    log_ab_test_result(variant, post_slug, quality_score)
    
    # Also save variant to database for tracking
    # (add prompt_variant column to your posts table)
```

### Option B: Manual implementation

Add these functions to `blog-auto-post-v2.py`:

```python
import random

AB_TEST_FILE = WORKSPACE / "prompts" / "ab-test.json"

def load_prompt_for_ab_test() -> Tuple[str, str]:
    """Load prompt, considering active A/B tests"""
    if not AB_TEST_FILE.exists():
        # No test active, use current prompt
        return ('current', read_current_prompt())
    
    with open(AB_TEST_FILE, 'r') as f:
        config = json.load(f)
    
    if config.get('status') != 'active':
        return ('current', read_current_prompt())
    
    # 50/50 split
    variant = random.choice(['A', 'B'])
    
    if variant == 'A':
        prompt = read_current_prompt()
    else:
        candidate_file = config['variants']['B']
        prompt_path = WORKSPACE / "prompts" / "candidates" / candidate_file
        prompt = prompt_path.read_text()
    
    logger.info(f"🔬 Using A/B test variant: {variant}")
    return (variant, prompt)
```

## 📊 Database Schema Extension

Add a `prompt_variant` column to track which variant generated each post:

```sql
ALTER TABLE posts ADD COLUMN prompt_variant TEXT DEFAULT 'current';
```

Then update your post insertion code:

```python
c.execute('''
    INSERT INTO posts (slug, title, date, word_count, quality_score, prompt_variant)
    VALUES (?, ?, ?, ?, ?, ?)
''', (slug, title, date, word_count, quality_score, variant))
```

## 🔄 Automated Workflow (Optional)

Add to cron for weekly optimization:

```bash
# Run prompt optimizer every Sunday at 2 AM
0 2 * * 0 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/prompt-optimizer.py optimize

# Evaluate tests that are >7 days old every Monday at 3 AM
0 3 * * 1 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/prompt-optimizer.py evaluate
```

## 📈 How A/B Testing Works

1. **Test Creation**: When you run `optimize`, the script:
   - Creates `prompts/ab-test.json` with variant A (current) and B (best candidate)
   - Sets status to "active" with 7-day duration

2. **During Test**: Each time blog-auto-post-v2.py runs:
   - Randomly selects variant A or B (50/50)
   - Generates post using selected prompt
   - Logs quality score to `ab-test.json`

3. **Evaluation**: When you run `evaluate`:
   - Compares average quality scores
   - If B wins by >5 points: promotes to production
   - Archives old prompt with timestamp
   - Marks test as "completed"

## 🎯 Quality Score Calculation

The script uses a basic quality score formula:

```
quality_score = 50 + (word_count / 50)
```

**Recommendations for better scoring:**
- Track engagement metrics (views, time on page, shares)
- Import from Google Analytics or your analytics platform
- Update scores in the database periodically
- Consider: readability, SEO score, user feedback

## 🧪 Testing the Integration

Test the A/B module independently:

```bash
cd /root/.openclaw/workspace/ai-automation-blog/scripts
python3 ab-test-integration.py
```

Expected output:
```
🔬 A/B Test Integration Module
============================================================
🔬 Active A/B Test: test_20260402
   Started: 2026-04-02
   Ends: 2026-04-09
   
   Variant A: 3 posts, avg quality 72.50
   Variant B: 2 posts, avg quality 78.30

Selected variant: B
Prompt preview: You are an expert tech blogger writing engaging, conversational content for solopreneurs who want to leverage AI automation...
✅ Test complete
```

## 🐛 Troubleshooting

### "Not enough posts for analysis"
- Need at least 3 posts in `blog/md/`
- Run blog generation first to create posts

### "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY="your-key-here"
# Or add to ~/.bashrc for persistence
```

### "Database not found"
- Script auto-creates `scripts/blog.db`
- If missing, run optimizer once to initialize

### A/B test not activating
- Check `prompts/ab-test.json` exists and has `"status": "active"`
- Verify test end_date is in the future
- Check logs in `logs/prompt-optimizer-*.log`

## 📚 Advanced Usage

### Custom test duration
Edit `prompt-optimizer.py`:
```python
AB_TEST_DURATION_DAYS = 14  # Change from default 7 days
```

### More prompt candidates
```python
NUM_CANDIDATES = 10  # Generate 10 instead of 5
```

### Manual prompt editing
1. Generate candidates: `python3 scripts/prompt-optimizer.py optimize`
2. Review candidates in `prompts/candidates/v*-*.txt`
3. Edit your favorite candidate manually
4. Update `prompts/ab-test.json` to point to your edited file
5. Run blog generation to test it

### Force promotion without A/B test
```bash
# Copy best candidate directly to production
cp prompts/candidates/v20260402-120000-3.txt prompts/blog-generation.txt
```

## 🎓 Best Practices

1. **Run weekly**: Optimize every 7-14 days as you accumulate data
2. **Track external metrics**: Import real engagement data from analytics
3. **Review candidates**: Don't blindly trust AI - read generated prompts
4. **Iterate gradually**: Small improvements compound over time
5. **Document wins**: Note what worked in `prompts/` README

## 🔗 Related Files

- `scripts/blog-auto-post-v2.py` - Main blog generation script
- `scripts/master-content-agent.py` - Content orchestrator
- `PROMPTS-SYSTEM.md` - Overall prompt strategy documentation

---

**Created**: 2026-04-02  
**Last Updated**: 2026-04-02  
**Status**: ✅ Ready for integration
