# Mind Crimes Generator - Testing Guide

**How to test the skill before production use**

## Prerequisites Check

### 1. Verify Database
```bash
# Check database exists
ls -la /opt/mind-crimes-automation/data/mindcrimes.db

# Check schema
sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db ".schema cases"

# Check for cases
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py stats
```

**Expected output:**
```json
{
  "status": "success",
  "stats": [
    {
      "status": "scraped",
      "count": 1,
      "avg_score": 85.5
    }
  ]
}
```

### 2. Verify Prompts Exist
```bash
ls -la /root/.openclaw/workspace/prompts/RESEARCH-PROMPT-OPTIMIZED.md
ls -la /root/.openclaw/workspace/prompts/CHAPTER-TEMPLATE-OPTIMIZED.md
ls -la /root/.openclaw/workspace/prompts/AUDIT-TECHNICAL-OPTIMIZED.md
ls -la /root/.openclaw/workspace/prompts/AUDIT-NARRATIVE-OPTIMIZED.md
ls -la /root/.openclaw/workspace/prompts/CORRECTIONS-OPTIMIZED.md
```

All should exist (created on 2026-03-31).

### 3. Verify OpenClaw Skills
```bash
# Check installed skills
openclaw skills list | grep -E "(writing-assistant|ai-humanizer|self-review)"
```

All three should be installed.

### 4. Verify Dependencies
```bash
# Check pandoc
which pandoc

# Check Python libraries
python3 -c "import sqlite3, json; print('OK')"

# Check OpenAI key
echo $OPENAI_API_KEY | head -c 20
```

---

## Test 1: Database Helper Script

### Test Check Command
```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py check
```

**If no approved cases:**
```json
{
  "status": "none",
  "message": "No approved cases found"
}
```

**If approved case exists:**
```json
{
  "status": "found",
  "case_id": 123,
  "victim_name": "Sandra Davis",
  ...
}
```

### Test Get Command
```bash
# Get specific case
python3 scripts/generate_book.py get 1
```

Should return full case details or error if not found.

### Test List Command
```bash
# List scraped cases
python3 scripts/generate_book.py list scraped 5
```

Should return array of cases with that status.

### Test Update Command
```bash
# Update case status (use test case)
python3 scripts/generate_book.py update 1 alerted
python3 scripts/generate_book.py get 1 | jq -r '.case_status'
# Should show: alerted

# Change back
python3 scripts/generate_book.py update 1 scraped
```

---

## Test 2: Create Dummy Case for Full Test

### Insert Test Case
```bash
sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db << 'EOF'
INSERT INTO cases (
    case_hash, 
    title, 
    victim_name, 
    victim_age, 
    murder_date, 
    arrest_date, 
    cold_case_years,
    location, 
    state, 
    suspect_name, 
    suspect_age,
    dna_method, 
    source_url, 
    score, 
    status
) VALUES (
    'test_dummy_001',
    'TESTING: Cold Case Solved After 30 Years',
    'Test Victim',
    35,
    '1990-03-15',
    '2024-11-20',
    34,
    'Portland, Oregon',
    'OR',
    'Test Suspect',
    60,
    'genetic genealogy using public databases',
    'https://example.com/test-case',
    75.0,
    'approved'
);
EOF
```

### Verify Insertion
```bash
python3 scripts/generate_book.py check
# Should return the test case
```

### Get Test Case ID
```bash
TEST_CASE_ID=$(python3 scripts/generate_book.py check | jq -r '.case_id')
echo "Test case ID: $TEST_CASE_ID"
```

---

## Test 3: Dry Run (Phase 1-2 Only)

**Test just the research phase to verify prompts and subagent spawning work:**

### Manual Agent Invocation
In Telegram, tell the agent:
```
Generate Mind Crimes book for case {TEST_CASE_ID} - RESEARCH ONLY (stop after Phase 2)
```

### Expected Behavior
1. Agent reads SKILL.md
2. Checks database (finds test case)
3. Creates directories
4. Updates status to 'generating'
5. Loads research prompt
6. Substitutes variables
7. Spawns research subagent
8. Saves output to research.md
9. Reports word count

### Verify Output
```bash
# Check research file created
ls -la /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}/research.md

# Check word count
wc -w /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}/research.md
# Should be 3,000-6,000 words

# Read first 50 lines
head -50 /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}/research.md
```

**If this works:** Prompts are correct, subagent spawning works, file paths are correct.

---

## Test 4: Full Generation (All 10 Phases)

**Only run this if Test 3 passed.**

### Start Full Generation
In Telegram:
```
Generate complete Mind Crimes book for case {TEST_CASE_ID}
```

### Monitor Progress
Agent should report:
- Phase 1: Database check ✅
- Phase 2: Research complete (6 min) ✅
- Phase 3: Chapters generating (19 min) ⏳
- Phase 4: Assembly ✅
- Phase 5: Technical audit ✅
- Phase 6: Narrative audit ✅
- Phase 7: Corrections (if needed) ✅
- Phase 8: Quality pipeline ✅
- Phase 9: DOCX conversion ✅
- Phase 10: Cover generation ✅
- Phase 11: Finalization ✅

### Expected Time
~45 minutes total

### Check Output Files
```bash
cd /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}

# Research
ls -lah research.md

# Chapters
ls -lah chapters/

# Audits
ls -lah audits/
cat audits/technical_audit.json
cat audits/narrative_audit.json
cat audits/final_review.json

# Manuscript versions
ls -lah manuscript_*.md
ls -lah manuscript_final.docx

# Cover
ls -lah /opt/mind-crimes-automation/data/covers/${TEST_CASE_ID}.png

# Stats
cat generation_stats.json
```

### Validate Quality
```bash
# Word count
wc -w manuscript_final.md
# Should be 18,000-25,000

# Final grade
cat audits/final_review.json | jq -r '.overall_grade'
# Should be A- or higher

# Errors
cat audits/technical_audit.json | jq -r '.error_count'
# Should be ≤2

# DOCX file size
stat -c%s manuscript_final.docx
# Should be >100KB

# Cover image dimensions
file /opt/mind-crimes-automation/data/covers/${TEST_CASE_ID}.png
# Should be 1024x1792 PNG
```

### Database Check
```bash
python3 scripts/generate_book.py get ${TEST_CASE_ID} | jq -r '.case_status'
# Should be: generated
```

---

## Test 5: Quality Comparison

**Compare test book with Books 4-5 (known good quality)**

### Read Sample from Each
```bash
# Test book
head -100 /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}/manuscript_final.md

# Book 4 (if available)
head -100 /opt/mind-crimes-automation/data/books/book-4/manuscript_final.md
```

### Compare Characteristics

| Metric | Book 4 | Book 5 | Test Book | Pass? |
|--------|--------|--------|-----------|-------|
| Word count | 22,150 | 21,300 | ??? | 18K-25K |
| Grade | A | A- | ??? | ≥A- |
| Errors | 1 | 0 | ??? | ≤2 |
| Generation time | 43 min | 47 min | ??? | ~45 min |
| Cost | $3.82 | $3.95 | ??? | $3-4 |

### Manual Quality Check
- [ ] Prologue hooks reader
- [ ] Chapter 1 establishes victim well
- [ ] Crime scene chapter has good detail
- [ ] Investigation narrative flows logically
- [ ] DNA breakthrough is clear and accurate
- [ ] Arrest scene is compelling
- [ ] Epilogue provides closure
- [ ] No obvious factual errors
- [ ] Consistent tone throughout
- [ ] Professional formatting

---

## Test 6: Error Handling

### Test Timeout Scenario
```bash
# Simulate timeout by setting very short timeout
# (Modify SKILL.md temporarily to timeout=10)
# Run generation, should retry and fail gracefully
```

### Test Quality Gate
```bash
# Insert a poor-quality case (low score)
# Generation should pause at quality gate
# User should receive approval prompt
```

### Test Budget Cap
```bash
# Set DAILY_CAP to very low value (e.g., $1)
# Run generation, should pause when approaching cap
```

---

## Test 7: Cleanup Test Data

**After all tests pass, clean up:**

```bash
# Delete test case from database
sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db << EOF
DELETE FROM cases WHERE case_hash = 'test_dummy_001';
EOF

# Delete test book files
rm -rf /opt/mind-crimes-automation/data/books/${TEST_CASE_ID}
rm -f /opt/mind-crimes-automation/data/covers/${TEST_CASE_ID}.png
```

---

## Production Readiness Checklist

Before using in production:

### Database
- [ ] Real cases scraped and scored
- [ ] At least 1 case has status='approved'
- [ ] Database backups configured

### Prompts
- [ ] All 5 prompt files exist and tested
- [ ] Variables correctly defined in each prompt
- [ ] Prompts produce quality output (verified in tests)

### Skills
- [ ] writing-assistant installed
- [ ] ai-humanizer installed
- [ ] self-review installed
- [ ] All three skills tested individually

### Files & Directories
- [ ] `/opt/mind-crimes-automation/data/books/` exists
- [ ] `/opt/mind-crimes-automation/data/covers/` exists
- [ ] Pandoc installed
- [ ] KDP template exists (if using custom formatting)

### Monitoring
- [ ] Telegram bot configured for alerts
- [ ] Daily spend tracking working
- [ ] Error alerts functioning

### Quality
- [ ] Test book generated successfully
- [ ] Test book meets all quality gates
- [ ] Test book comparable to Books 4-5
- [ ] DOCX formatting looks professional
- [ ] Cover design looks good

### Automation (Optional)
- [ ] Cron job configured for periodic checks
- [ ] Heartbeat checks enabled
- [ ] Budget controls tested

---

## Troubleshooting Common Issues

### "No approved cases found"
**Cause:** No cases with status='approved' in database  
**Fix:** 
```bash
# Check database
python3 scripts/generate_book.py list scraped

# Manually approve a case
python3 scripts/generate_book.py update {case_id} approved
```

### Subagent timeout
**Cause:** Model too slow, network issues, or prompt too complex  
**Fix:**
- Check OpenRouter API status
- Verify API key is valid
- Increase timeout in SKILL.md
- Try with shorter research prompt

### Pandoc conversion fails
**Cause:** Pandoc not installed or markdown syntax errors  
**Fix:**
```bash
# Install pandoc
apt install pandoc

# Test manually
pandoc manuscript_final.md -o test.docx --from markdown --to docx
```

### Cover generation fails
**Cause:** OpenAI API key invalid or rate limit hit  
**Fix:**
```bash
# Check API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Use fallback ImageMagick cover
convert -size 1024x1792 xc:black \
    -gravity center \
    -pointsize 72 -fill white \
    -annotate +0-200 "Test Book" \
    test_cover.png
```

### Quality below A-
**Cause:** Poorly written chapters, too many errors, or weak narrative  
**Fix:**
- Review source case (is it compelling enough?)
- Check research prompt (does it gather enough detail?)
- Check chapter prompts (are instructions clear?)
- Consider regenerating specific chapters

### Word count too low
**Cause:** Chapter prompts not producing enough content  
**Fix:**
- Increase word count targets in chapter prompts (2,000-2,500 instead of 1,800-2,000)
- Add more detail requirements to prompts
- Ensure research phase gathers enough material

### Database locked
**Cause:** Another process accessing database  
**Fix:**
- Wait a few seconds and retry
- Check for other running generation processes
- Use `fuser /opt/mind-crimes-automation/data/mindcrimes.db` to find blocking process

---

## Success Metrics

**Skill is working correctly if:**

✅ **Reliability:** 95%+ generations complete without errors  
✅ **Quality:** All books grade A- or higher  
✅ **Speed:** Average generation time 40-50 minutes  
✅ **Cost:** Average cost $3-4 per book  
✅ **Automation:** Can run unattended for multiple books  
✅ **Error recovery:** Handles failures gracefully, alerts appropriately  

---

## Next Steps After Testing

1. **Run first production book:**
   - Use highest-scoring real case
   - Monitor closely
   - Manual QA review

2. **Compare to previous books:**
   - Quality should match Books 4-5
   - If not, iterate on prompts

3. **Enable automation:**
   - Set up cron for periodic checks
   - Configure budget alerts
   - Test unattended operation

4. **Scale gradually:**
   - 1 book/day for first week
   - 3-5 books/day for second week
   - 10+ books/day once proven stable

5. **Monitor & optimize:**
   - Track generation metrics
   - Identify slow phases
   - Optimize prompts based on results
   - A/B test different approaches

---

**Testing complete = Ready for production! 🚀**
