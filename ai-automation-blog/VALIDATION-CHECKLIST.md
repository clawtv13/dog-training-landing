# Post-Deployment Validation Checklist

**Run this after tomorrow's auto-post (2026-04-03 10:30 UTC)**

## Quick Test

```bash
cd /root/.openclaw/workspace/ai-automation-blog

# Check latest 2 posts were created
ls -lh blog/posts/2026-04-03-*.html

# Test readability scores
python3 << 'SCRIPT'
import re, textstat
from pathlib import Path

posts = sorted(Path('blog/posts').glob('2026-04-03-*.html'), reverse=True)[:2]

print("=" * 70)
print("READABILITY VALIDATION - New Posts")
print("=" * 70)

for post in posts:
    with open(post) as f:
        html = f.read()
    
    content = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if content:
        text = re.sub(r'<[^>]+>', ' ', content.group(1))
        text = ' '.join(text.split())
        
        fk_ease = textstat.flesch_reading_ease(text)
        fk_grade = textstat.flesch_kincaid_grade(text)
        words = textstat.lexicon_count(text)
        sentences = textstat.sentence_count(text)
        avg_len = words / sentences if sentences > 0 else 0
        
        status = "✅ PASS" if 50 <= fk_ease <= 70 else "❌ FAIL"
        
        print(f"\n{post.name}")
        print(f"  Flesch Score: {fk_ease:.1f}/100 {status}")
        print(f"  FK Grade: {fk_grade:.1f}")
        print(f"  Avg Sentence: {avg_len:.1f} words")
        print(f"  Word Count: {words}")

print("\n" + "=" * 70)
SCRIPT
```

## Expected Results

```
2026-04-03-post-1.html
  Flesch Score: 54.2/100 ✅ PASS
  FK Grade: 8.7
  Avg Sentence: 16.8 words
  Word Count: 987

2026-04-03-post-2.html
  Flesch Score: 58.7/100 ✅ PASS
  FK Grade: 8.3
  Avg Sentence: 17.4 words
  Word Count: 1012
```

## If Tests Fail

### Readability Still Low (<50):

1. Check prompt was loaded:
   ```bash
   grep "Using v2 prompt" logs/blog-auto-post-2026-04.log
   ```

2. Review generated content manually:
   ```bash
   # Look at first 500 chars of content
   grep -A20 "<article" blog/posts/2026-04-03-*.html | head -30
   ```

3. Adjust prompt:
   - Increase emphasis on simple words
   - Add more concrete examples
   - Strengthen readability requirements

### Script Errors:

1. Check logs:
   ```bash
   tail -100 logs/blog-auto-post-2026-04.log
   ```

2. Rollback if needed:
   ```bash
   git checkout scripts/blog-auto-post-v2.py
   ```

## Success Criteria

- [ ] Both posts have Flesch score 50-70
- [ ] FK Grade 8-9
- [ ] No generation errors in logs
- [ ] Posts deployed to workless.build
- [ ] Readability improved by 10+ points vs baseline (43.3)

---

**Schedule:** Run at 10:30 UTC on 2026-04-03  
**Baseline:** Flesch 43.3 → Target: 50-70  
**Report results to:** Main agent / n0mad
