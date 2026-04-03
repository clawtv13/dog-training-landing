# Mind Crimes Generator Skill

**Automated end-to-end ebook generation for Mind Crimes true crime series**

## Overview

This skill transforms approved cold case data into publication-ready ebooks automatically. It handles research, writing, editing, quality control, cover design, and file preparation — producing A-grade true crime books in ~45 minutes.

## What It Does

1. **Monitors database** for approved cases (status='approved')
2. **Generates research** (6 min, 3-6K words)
3. **Writes 11 chapters** in parallel (19 min, 16-20K words)
4. **Runs quality audits** (technical + narrative)
5. **Fixes errors automatically** (if any found)
6. **Applies quality pipeline** (writing-assistant, ai-humanizer, self-review)
7. **Converts to DOCX** (KDP-ready format)
8. **Generates cover** (minimalist design via DALL-E 3)
9. **Updates database** (status='generated')
10. **Alerts user** via Telegram

## File Structure

```
mind-crimes-generator/
├── SKILL.md                    # Main execution instructions for agent
├── README.md                   # This file - documentation
├── scripts/
│   └── generate_book.py        # Database helper CLI
└── references/
    └── workflow.md             # Detailed 10-phase breakdown
```

## Prerequisites

### Required Files
- `/opt/mind-crimes-automation/data/mindcrimes.db` - SQLite database
- `/root/.openclaw/workspace/prompts/RESEARCH-PROMPT-OPTIMIZED.md`
- `/root/.openclaw/workspace/prompts/CHAPTER-TEMPLATE-OPTIMIZED.md`
- `/root/.openclaw/workspace/prompts/AUDIT-TECHNICAL-OPTIMIZED.md`
- `/root/.openclaw/workspace/prompts/AUDIT-NARRATIVE-OPTIMIZED.md`
- `/root/.openclaw/workspace/prompts/CORRECTIONS-OPTIMIZED.md`

### Required Skills (OpenClaw)
- `writing-assistant` - Prose improvement
- `ai-humanizer` - Remove AI patterns
- `self-review` - Final quality gate

### Required Tools
- `pandoc` - Markdown to DOCX conversion
- `sqlite3` - Database access
- OpenAI API key - Cover generation

## Usage

### Check for Approved Cases

```bash
python3 scripts/generate_book.py check
```

Output:
```json
{
  "status": "found",
  "case_id": 123,
  "victim_name": "Sandra Davis",
  "score": 87.5
}
```

### Get Case Details

```bash
python3 scripts/generate_book.py get 123
```

### Update Case Status

```bash
python3 scripts/generate_book.py update 123 generating
python3 scripts/generate_book.py update 123 generated
```

Valid statuses: `scraped`, `alerted`, `approved`, `generating`, `generated`, `uploaded`, `live`, `skipped`

### List Cases by Status

```bash
python3 scripts/generate_book.py list approved
python3 scripts/generate_book.py list generated 20
```

### Database Stats

```bash
python3 scripts/generate_book.py stats
```

## Agent Usage

### Manual Trigger

User says:
- "Generate Mind Crimes book for case 123"
- "Check for approved Mind Crimes cases"
- "Generate the next Mind Crimes book"

Agent reads `SKILL.md` and follows workflow.

### Automated (Cron)

Set up OpenClaw cron:
```bash
openclaw cron add "check-mind-crimes" \
  --schedule "*/30 * * * *" \
  --task "Check for approved Mind Crimes cases and generate books" \
  --model sonnet
```

Every 30 minutes, agent:
1. Checks database
2. If approved case found → generates book
3. If no cases → silent (HEARTBEAT_OK)

## Output Files

After generation, each book produces:

```
/opt/mind-crimes-automation/data/books/{case_id}/
├── research.md                 # Research compilation
├── chapters/
│   ├── 00_prologue.md
│   ├── 01_chapter.md
│   ├── 02_chapter.md
│   ...
│   ├── 10_chapter.md
│   └── 11_epilogue.md
├── audits/
│   ├── technical_audit.json
│   ├── narrative_audit.json
│   └── final_review.json
├── manuscript_draft.md         # Combined raw chapters
├── manuscript_corrected.md     # After error fixes
├── manuscript_final.md         # After quality pipeline
├── manuscript_final.docx       # KDP-ready file
└── generation_stats.json       # Metrics

/opt/mind-crimes-automation/data/covers/
└── {case_id}.png               # Book cover (1024x1792)
```

## Quality Gates

Books must meet ALL criteria to auto-publish:

| Metric | Threshold |
|--------|-----------|
| Word count | 18,000 - 25,000 |
| Technical errors | ≤ 2 |
| Narrative grade | ≥ A- (9.0/10) |
| Final grade | ≥ A- |

If any gate fails → alert user, pause for approval.

## Performance

**Per book:**
- Time: ~45 minutes
- Cost: $3.50-$4.00 (Sonnet 4.5 + DALL-E 3)
- Quality: A- to A+ consistently

**Capacity:**
- Maximum: 32 books/day (24/7 operation)
- Realistic: 10-15 books/day (human oversight)
- Budget-aware: Auto-pauses at daily cap

## Error Handling

### Subagent Timeout
- Auto-retry once
- If second failure → mark case 'failed'
- Alert user via Telegram

### Quality Below Threshold
- Pause generation
- Alert user with grade
- Options: publish anyway / regenerate / skip

### Budget Exceeded
- Stop immediately
- Mark case 'paused'
- Resume next day at 00:00 UTC

### Database Lock
- Retry 3x with 1s delay
- If still locked → fail gracefully

## Integration with Existing System

This skill completes the Mind Crimes automation pipeline:

```
[Web Scraper] → [Scorer] → [Alert] → [n0mad Approval] → [THIS SKILL] → [KDP Upload] → [Live]
     ↓              ↓          ↓              ↓                ↓              ↓          ↓
  scraper.py   scorer.py  telegram.py    manual      generate_book    kdp_api.py   PROFIT
```

**Before this skill:**
- Manual book writing (8-12 hours)
- Inconsistent quality
- Bottleneck at n0mad

**After this skill:**
- Automated book writing (45 min)
- Consistent A- quality
- n0mad only approves cases, doesn't write

## Testing

### Test with Dummy Case

```bash
# Insert test case
sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db << EOF
INSERT INTO cases (
    case_hash, title, victim_name, victim_age, 
    murder_date, arrest_date, cold_case_years,
    location, state, suspect_name, suspect_age,
    dna_method, source_url, score, status
) VALUES (
    'test123',
    'Test Case: Jane Doe Murder',
    'Jane Doe',
    32,
    '1990-06-15',
    '2024-12-01',
    34,
    'Portland, OR',
    'OR',
    'John Smith',
    58,
    'genetic genealogy',
    'https://test.com',
    85.0,
    'approved'
);
EOF

# Generate book
# (Agent: "Generate Mind Crimes book")

# Verify output
ls -la /opt/mind-crimes-automation/data/books/*/manuscript_final.docx
```

### Validate Quality

```bash
# Check word count
wc -w /opt/mind-crimes-automation/data/books/{case_id}/manuscript_final.md

# Check grade
cat /opt/mind-crimes-automation/data/books/{case_id}/audits/final_review.json | jq -r '.overall_grade'

# Check errors
cat /opt/mind-crimes-automation/data/books/{case_id}/audits/technical_audit.json | jq -r '.error_count'
```

## Troubleshooting

### "No approved cases found"
- Check database: `sqlite3 /opt/mind-crimes-automation/data/mindcrimes.db "SELECT * FROM cases WHERE status='approved'"`
- Verify scraper is running
- Check if cases need manual approval

### Subagent fails repeatedly
- Check OpenAI API key: `echo $OPENAI_API_KEY`
- Verify model availability: `openrouter/anthropic/claude-sonnet-4.5`
- Check rate limits

### DOCX conversion fails
- Install pandoc: `apt install pandoc`
- Check template exists: `ls /root/.openclaw/workspace/templates/kdp-template.docx`

### Cover generation fails
- Verify OpenAI API key
- Check DALL-E 3 rate limits
- Fallback to ImageMagick text cover

## Configuration

Edit skill behavior in `SKILL.md`:

```markdown
## CONFIGURATION

# Quality thresholds
MINIMUM_GRADE = "A-"        # Don't publish below this
MINIMUM_WORDS = 18000
MAXIMUM_WORDS = 25000
MAX_ERRORS = 2

# Cost controls
DAILY_CAP = 50.0            # USD
ALERT_THRESHOLD = 0.8       # Alert at 80% of cap

# Timeouts
RESEARCH_TIMEOUT = 1800     # 30 min
CHAPTER_TIMEOUT = 1800      # 30 min per subagent
AUDIT_TIMEOUT = 900         # 15 min
```

## Metrics & Monitoring

Track in `generation_stats.json`:
```json
{
  "case_id": 123,
  "victim_name": "Sandra Davis",
  "word_count": 22150,
  "final_grade": "A",
  "generation_time_minutes": 43,
  "total_cost": 3.82,
  "subagents_spawned": 12,
  "errors_fixed": 1,
  "status": "generated",
  "timestamp": "2024-12-02T15:30:00Z"
}
```

## Future Enhancements

- [ ] Parallel book generation (2-3 books simultaneously)
- [ ] A/B test different chapter structures
- [ ] Automatic KDP upload integration
- [ ] Automatic Gumroad product creation
- [ ] Tweet generation for book launch
- [ ] Email sequence generation for subscribers
- [ ] Cover design variants (test which sells best)
- [ ] Audiobook script generation
- [ ] Translation to Spanish/French/German

## License

Proprietary - Mind Crimes automation system

## Author

n0mad - OpenClaw agent automation

## Version

1.0.0 - Initial production release (2024-12-02)

---

**This skill is the final piece that makes Mind Crimes fully automated.**
