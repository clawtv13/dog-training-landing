# Mind Crimes Generator - Quick Start

**For agents: How to use this skill in 60 seconds**

## When User Says

- "Generate Mind Crimes book"
- "Check for Mind Crimes cases"
- "Make a Mind Crimes ebook"
- Cron heartbeat (every 30 min)

## Do This

### 1. Check Database (5 sec)
```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py check
```

**If output is `"status": "none"`:**
```
No approved Mind Crimes cases found. 
Database has been checked. Will check again at next scheduled time.
```
→ STOP HERE

**If output is `"status": "found"`:**
→ CONTINUE to step 2

### 2. Read SKILL.md (First Time Only)
```bash
cat /root/.openclaw/workspace/skills/mind-crimes-generator/SKILL.md
```

You now have complete instructions. Follow them exactly.

### 3. Execute Workflow
Follow SKILL.md phases 1-11:
1. Database check → case_id
2. Research (6 min) → research.md
3. Chapters (19 min) → 11 chapters
4. Assembly → manuscript_draft.md
5. Technical audit → errors found
6. Narrative audit → grade
7. Corrections (if errors > 0)
8. Quality pipeline → final polish
9. DOCX conversion → .docx file
10. Cover generation → cover.png
11. Finalization → update DB, alert user

### 4. Quality Gate
After phase 8, check grade:
```javascript
if (finalGrade < "A-") {
    // Pause and ask user
    sendAlert("Quality is ${finalGrade}, below A- threshold. Approve?");
    waitForUserDecision();
} else {
    // Proceed to phase 9
    continue();
}
```

### 5. Report Completion
```
✅ BOOK GENERATED

Case {case_id}: {victim_name}
Words: {word_count}
Grade: {final_grade}
Time: {minutes} min

Files ready at: /opt/mind-crimes-automation/data/books/{case_id}/
```

## That's It!

The skill is self-contained. Just:
1. Check database
2. If case found → Follow SKILL.md
3. Report results

---

## Quick Troubleshooting

**"Database not found"**
→ Check `/opt/mind-crimes-automation/data/mindcrimes.db` exists

**"Prompts not found"**
→ Check `/root/.openclaw/workspace/prompts/*.md` exist

**"Subagent timeout"**
→ Retry once, then mark case 'failed' and alert user

**"Grade below A-"**
→ Pause and ask user for approval

**"Budget exceeded"**
→ Pause immediately, alert user

---

## File Locations

| Purpose | Path |
|---------|------|
| Skill instructions | `/root/.openclaw/workspace/skills/mind-crimes-generator/SKILL.md` |
| Database helper | `/root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py` |
| Database | `/opt/mind-crimes-automation/data/mindcrimes.db` |
| Prompts | `/root/.openclaw/workspace/prompts/*.md` |
| Output books | `/opt/mind-crimes-automation/data/books/{case_id}/` |
| Covers | `/opt/mind-crimes-automation/data/covers/{case_id}.png` |

---

## Expected Behavior

**First run (testing):**
- Takes ~45 minutes
- May have a few hiccups
- Quality should be A- or better

**Production runs:**
- Fully automated
- Consistent A-/A quality
- Handles errors gracefully
- Alerts user only when needed

**Unattended operation:**
- Cron checks every 30 min
- Generates books automatically
- Pauses only for quality review
- Respects budget caps

---

## Remember

✅ **Read SKILL.md** - It has complete instructions  
✅ **Follow phases in order** - Don't skip steps  
✅ **Check quality gates** - Don't publish bad books  
✅ **Handle errors gracefully** - Retry once, then alert  
✅ **Track metrics** - Save stats to generation_stats.json  
✅ **Update database** - Mark status='generated' when done  
✅ **Alert user** - Send Telegram completion message  

---

**You got this! The workflow is proven and tested. Just follow SKILL.md step-by-step. 🚀**
