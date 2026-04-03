# Mind Crimes Generator - Pre-Flight Checklist

**Run through this checklist before first use**

---

## ✅ IMPLEMENTATION STATUS

### Files Created
- [x] `SKILL.md` (24 KB, 829 lines) - Executable workflow
- [x] `README.md` (12 KB, 359 lines) - Documentation
- [x] `scripts/generate_book.py` (12 KB, 290 lines) - Database helper
- [x] `references/workflow.md` (20 KB, 853 lines) - Phase details
- [x] `references/testing-guide.md` (12 KB, 535 lines) - Testing procedures
- [x] `references/quick-start.md` (4 KB, 149 lines) - Agent quick reference
- [x] `IMPLEMENTATION-SUMMARY.md` (16 KB, 500 lines) - What was built
- [x] `CHECKLIST.md` (This file) - Pre-flight verification

**Total:** 7 documentation files + 1 Python script = ~100 KB, ~3,500 lines

---

## 📋 PRE-FLIGHT CHECKLIST

### 1. Database
```bash
# Check database exists
[ ] ls -la /opt/mind-crimes-automation/data/mindcrimes.db

# Verify schema
[ ] sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db ".schema cases"

# Check for cases
[ ] python3 scripts/generate_book.py stats
```

### 2. Prompts
```bash
# Verify all prompts exist
[ ] ls -la /root/.openclaw/workspace/prompts/RESEARCH-PROMPT-OPTIMIZED.md
[ ] ls -la /root/.openclaw/workspace/prompts/CHAPTER-TEMPLATE-OPTIMIZED.md
[ ] ls -la /root/.openclaw/workspace/prompts/AUDIT-TECHNICAL-OPTIMIZED.md
[ ] ls -la /root/.openclaw/workspace/prompts/AUDIT-NARRATIVE-OPTIMIZED.md
[ ] ls -la /root/.openclaw/workspace/prompts/CORRECTIONS-OPTIMIZED.md
```

### 3. OpenClaw Skills
```bash
# Check skills installed
[ ] openclaw skills list | grep writing-assistant
[ ] openclaw skills list | grep ai-humanizer
[ ] openclaw skills list | grep self-review
```

### 4. System Dependencies
```bash
# Check pandoc
[ ] which pandoc

# Check Python libraries
[ ] python3 -c "import sqlite3, json; print('OK')"

# Check OpenAI API key
[ ] echo $OPENAI_API_KEY | head -c 20
```

### 5. Directory Structure
```bash
# Verify output directories exist (or can be created)
[ ] mkdir -p /opt/mind-crimes-automation/data/books/
[ ] mkdir -p /opt/mind-crimes-automation/data/covers/

# Check permissions
[ ] touch /opt/mind-crimes-automation/data/books/test && rm /opt/mind-crimes-automation/data/books/test
```

### 6. Database Helper Script
```bash
# Test all commands
[ ] python3 scripts/generate_book.py check
[ ] python3 scripts/generate_book.py stats
[ ] python3 scripts/generate_book.py list scraped 3

# Verify JSON output format
[ ] python3 scripts/generate_book.py check | jq .
```

### 7. Documentation Review
```bash
# Read key files
[ ] cat IMPLEMENTATION-SUMMARY.md
[ ] cat references/quick-start.md
[ ] head -100 SKILL.md
```

---

## 🧪 TESTING CHECKLIST

### Phase 1: Dry Run (No Real Generation)
```bash
[ ] Insert test case with status='approved'
[ ] Verify `check` command finds it
[ ] Read SKILL.md Phase 1-2 instructions
[ ] Understand variable substitution
[ ] Check research prompt exists
```

### Phase 2: Research Only Test (~8 min)
```bash
[ ] Tell agent: "Generate Mind Crimes book - RESEARCH ONLY"
[ ] Agent checks database ✓
[ ] Agent creates directories ✓
[ ] Agent loads research prompt ✓
[ ] Agent spawns subagent ✓
[ ] Research.md created (3-6K words) ✓
[ ] Word count verified ✓
```

### Phase 3: Full Generation Test (~50 min)
```bash
[ ] Tell agent: "Generate complete Mind Crimes book for case {test_id}"
[ ] Monitor all 10 phases
[ ] Verify each output file created
[ ] Check word count 18K-25K
[ ] Check grade ≥ A-
[ ] Check errors ≤ 2
[ ] Check DOCX created
[ ] Check cover PNG created
[ ] Check database updated to 'generated'
```

### Phase 4: Quality Validation
```bash
[ ] Read first chapter - quality check
[ ] Compare to Books 4-5 (if available)
[ ] Verify professional formatting in DOCX
[ ] Verify cover looks good
[ ] Check no obvious factual errors
[ ] Confirm grade is accurate
```

### Phase 5: Error Handling Tests
```bash
[ ] Test quality gate (insert low-quality case)
[ ] Test timeout recovery (very short timeout)
[ ] Test budget cap (set cap to $1)
[ ] Verify alerts sent correctly
```

### Phase 6: Cleanup
```bash
[ ] Delete test case from database
[ ] Remove test book files
[ ] Remove test cover
[ ] Verify system clean
```

---

## 🚀 PRODUCTION READINESS

### Minimum Requirements
- [ ] 1 successful research-only test
- [ ] 1 successful full generation test
- [ ] Quality grade ≥ A-
- [ ] All output files created correctly
- [ ] No critical errors encountered

### Recommended Requirements
- [ ] 3+ successful full generation tests
- [ ] Quality consistently A- or higher
- [ ] Error handling tested and working
- [ ] Comparison with Books 4-5 shows similar quality
- [ ] All team members understand workflow

### Go/No-Go Decision

**GO if:**
- ✅ All minimum requirements met
- ✅ Test book quality matches expectations
- ✅ Agent follows SKILL.md correctly
- ✅ Error handling works
- ✅ Cost is within budget ($3-4/book)

**NO-GO if:**
- ❌ Quality below A-
- ❌ Cost exceeds $5/book
- ❌ Critical bugs found
- ❌ Agent can't follow workflow
- ❌ Output files missing/corrupted

---

## 📊 SUCCESS METRICS

After first 10 production books, track:

### Quality Metrics
- [ ] Average grade: _____ (Target: ≥ A-)
- [ ] Average word count: _____ (Target: 18K-25K)
- [ ] Average errors: _____ (Target: ≤2)
- [ ] Success rate: _____% (Target: ≥90%)

### Performance Metrics
- [ ] Average generation time: _____ min (Target: ~45)
- [ ] Average cost: $_____ (Target: $3-4)
- [ ] Books per day: _____ (Target: 10-15)

### Operational Metrics
- [ ] Subagent failures: _____ (Target: <5%)
- [ ] Quality gate pauses: _____ (Target: <10%)
- [ ] Manual interventions: _____ (Target: <3/book)

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Problem | Quick Fix |
|---------|-----------|
| "No approved cases" | Check database: `python3 scripts/generate_book.py list scraped` |
| Subagent timeout | Increase timeout in SKILL.md to 2400 |
| Pandoc fails | Install: `apt install pandoc` |
| DALL-E fails | Verify API key: `echo $OPENAI_API_KEY` |
| Grade below A- | Review prompts, consider regenerating |
| Word count low | Check research phase, may need more detail |
| Database locked | Wait 5 sec, retry; check for other processes |

---

## 📞 SUPPORT RESOURCES

| Resource | Location |
|----------|----------|
| Executable workflow | `SKILL.md` |
| Testing guide | `references/testing-guide.md` |
| Quick reference | `references/quick-start.md` |
| Phase details | `references/workflow.md` |
| Implementation summary | `IMPLEMENTATION-SUMMARY.md` |
| Database helper | `scripts/generate_book.py` |

---

## ✅ FINAL SIGN-OFF

Before enabling automation:

- [ ] All checklist items above completed
- [ ] At least 1 successful full test
- [ ] Quality validated and acceptable
- [ ] Cost within budget
- [ ] Team trained on workflow
- [ ] Error handling verified
- [ ] Monitoring/alerts configured

**Signed off by:** _________________  
**Date:** _________________  
**Ready for production:** YES / NO

---

## 🎯 NEXT ACTIONS

1. **Today:**
   - [ ] Run through this checklist
   - [ ] Test database helper
   - [ ] Create test case

2. **This Week:**
   - [ ] Research-only test
   - [ ] Full generation test
   - [ ] Quality validation
   - [ ] Error handling tests

3. **Next Week:**
   - [ ] First production book
   - [ ] Monitor closely
   - [ ] Enable cron automation
   - [ ] Scale gradually

---

**Status:** Ready for testing  
**Last updated:** 2026-04-01  
**Version:** 1.0.0

---

**Good luck! 🚀 The skill is built and ready. Just follow the checklist and you'll be generating books in no time.**
