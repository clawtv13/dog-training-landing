# Performance Tracker

Daily script to calculate quality metrics for blog posts.

## Features

### 1. **Readability Scoring** (0-100)
- Uses `textstat` library with Flesch-Kincaid Reading Ease
- Score 0-100 (100 = easiest to read)
- Analyzes sentence complexity, word length, syllable count

### 2. **SEO Scoring** (0-100)
Comprehensive SEO analysis checking:
- ✅ Meta description exists (20 pts)
- ✅ H1/H2 structure (20 pts)
  - Exactly 1 H1 tag
  - 3+ H2 tags for content structure
- ✅ Internal links (20 pts)
  - 2+ internal links for site navigation
- ✅ Image alt tags (20 pts)
  - All images have descriptive alt text
- ✅ Keyword density (20 pts)
  - 2-3% optimal density of AI-related terms
  - Keywords: ai, automation, agent, llm, tool, build, productivity

### 3. **Topic Clustering**
- Uses TF-IDF feature extraction
- K-means clustering (k=5)
- Smart semantic labeling:
  - **AI Tools** - Tool reviews, API guides, platforms
  - **Ethics** - Privacy, bias, safety, responsible AI
  - **Technical** - Code, implementation, architecture
  - **Business** - Revenue, pricing, growth, founder stories
  - **Random** - Miscellaneous topics

### 4. **Database Updates**
Updates `data/analytics.db` with:
- `readability_score` - Flesch-Kincaid score
- `seo_score` - SEO quality score
- `quality_score` - Average of readability + SEO
- `topic_cluster` - Assigned topic category

**Idempotent:** Only processes posts with NULL scores.

## Installation

```bash
# Install dependencies
pip3 install textstat scikit-learn beautifulsoup4

# Initialize database (if not already done)
python3 scripts/init_analytics_db.py

# Run performance tracker
python3 scripts/performance-tracker.py
```

## Usage

### Daily Run (Recommended)
```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/performance-tracker.py
```

### Add to Cron (Daily at 2 AM)
```bash
0 2 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/performance-tracker.py >> logs/performance-tracker.log 2>&1
```

## Output

### Console Output
```
🔍 PERFORMANCE TRACKER - Starting analysis
Found 28 posts

📊 Phase 2: Scoring 5 unscored posts...

Processing: 2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week
  Readability: 50.4/100
  SEO: 90/100
  Quality: 70.2/100

✅ PERFORMANCE TRACKER - Complete!

📈 Summary:
  Posts scored: 28
  Avg Readability: 42.5/100
  Avg SEO: 76.6/100
  Avg Quality: 59.6/100

🏷️  Topic Distribution:
  Random: 15 posts
  Business: 11 posts
  AI Tools: 2 posts
```

### Log File
Saved to `logs/performance-tracker.log`:
```
[2026-04-02 15:31:48] Scored post X: readability=50.4, seo=90, cluster=Random
```

## Database Schema

```sql
posts (
  id INTEGER PRIMARY KEY,
  slug TEXT UNIQUE,
  published_date TEXT,
  word_count INTEGER,
  readability_score REAL,    -- 0-100
  seo_score REAL,            -- 0-100
  quality_score REAL,        -- Average of above
  topic_cluster TEXT,        -- AI Tools | Ethics | Technical | Business | Random
  prompt_version TEXT,
  created_at TIMESTAMP
)
```

## Query Examples

### Top Quality Posts
```sql
SELECT slug, quality_score, readability_score, seo_score, topic_cluster
FROM posts
WHERE quality_score IS NOT NULL
ORDER BY quality_score DESC
LIMIT 10;
```

### Posts by Topic
```sql
SELECT topic_cluster, COUNT(*) as count, AVG(quality_score) as avg_quality
FROM posts
WHERE topic_cluster IS NOT NULL
GROUP BY topic_cluster
ORDER BY count DESC;
```

### SEO Improvement Candidates
```sql
SELECT slug, seo_score, readability_score
FROM posts
WHERE seo_score < 70
ORDER BY seo_score ASC
LIMIT 10;
```

### Readability Issues
```sql
SELECT slug, readability_score, word_count
FROM posts
WHERE readability_score < 40
ORDER BY readability_score ASC;
```

## Interpretation

### Readability Scores
- **90-100**: Very Easy (5th grade)
- **80-89**: Easy (6th grade)
- **70-79**: Fairly Easy (7th grade)
- **60-69**: Standard (8th-9th grade)
- **50-59**: Fairly Difficult (10th-12th grade)
- **30-49**: Difficult (College)
- **0-29**: Very Difficult (College graduate)

**Target for blog:** 50-70 (Standard to Fairly Easy)

### SEO Scores
- **90-100**: Excellent - Well optimized
- **70-89**: Good - Minor improvements needed
- **50-69**: Fair - Multiple issues to fix
- **0-49**: Poor - Major SEO problems

**Target for blog:** 80+ (Good to Excellent)

### Quality Score
Overall content quality (average of readability + SEO):
- **80-100**: Exceptional
- **70-79**: Great
- **60-69**: Good
- **50-59**: Fair
- **0-49**: Needs improvement

**Target for blog:** 65+ (Good or better)

## Metrics Tracked

Current blog performance (28 posts):
- **Avg Readability:** 42.5/100 (College level - could be simplified)
- **Avg SEO:** 76.6/100 (Good - solid optimization)
- **Avg Quality:** 59.6/100 (Fair - room for improvement)

**Recommendation:** Focus on simplifying language to improve readability scores. SEO is already strong.

## Integration

Works seamlessly with other blog scripts:
- `scripts/growth-tracker.py` - Overall blog metrics
- `scripts/seo-audit.py` - Technical SEO checks
- `scripts/qa-agent.py` - Automated testing
- `scripts/blog-auto-post-v2.py` - Content generation

## Troubleshooting

### "No HTML posts found!"
- Check that posts exist in `blog/posts/*.html`
- Ensure you're running from the correct directory

### "Clustering error"
- Need at least 5 posts for clustering
- Falls back to "Random" category if insufficient data

### "Readability calculation error"
- Ensure text has at least 100 words
- Check for encoding issues in HTML

### Database locked
- Another script is accessing the database
- Wait a few seconds and retry

## Performance

- Processes 28 posts in ~2 seconds
- Lightweight - uses local libraries only
- No external API calls
- Safe for daily cron jobs

## Next Steps

Consider adding:
- Historical trend tracking (quality over time)
- Weekly reports with quality improvements
- Integration with analytics dashboards
- Automated alerts for low-scoring posts
- A/B testing prompt versions by quality score

---

**Last Updated:** 2026-04-02  
**Version:** 1.0  
**Author:** AI Automation Builder Team
