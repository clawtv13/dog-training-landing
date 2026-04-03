# Mind Crimes Generator - Visual Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MIND CRIMES BOOK GENERATOR                           │
│                      Automated Ebook Pipeline                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ TRIGGER                                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  • User: "Generate Mind Crimes book"                                   │
│  • Cron: Every 30 min check for approved cases                         │
│  • Manual: "Generate book for case {id}"                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DATABASE CHECK (10 seconds)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  python3 scripts/generate_book.py check                                │
│                                                                         │
│  ┌──────────────────┐         ┌──────────────────┐                    │
│  │  No approved     │         │  Approved case   │                    │
│  │  cases found     │──NO─┐   │  found!          │                    │
│  └──────────────────┘     │   └──────────────────┘                    │
│                            │              │                             │
│                            │              YES                           │
│                            │              │                             │
│                    ┌───────▼──────┐      │                             │
│                    │  Exit: "No   │      │                             │
│                    │  approved    │      │                             │
│                    │  cases"      │      │                             │
│                    └──────────────┘      │                             │
│                                           ▼                             │
│  • Create directories: books/{case_id}/chapters                        │
│  • Update DB: status='generating'                                      │
│  • Extract case data: victim, suspect, dates, location                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: RESEARCH COMPILATION (6 minutes)                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: Sonnet 4.5 │ Timeout: 1800s │ Cost: ~$0.40                    │
│                                                                         │
│  1. Load: RESEARCH-PROMPT-OPTIMIZED.md                                 │
│  2. Substitute: {victim_name}, {location}, {dates}, etc.               │
│  3. Spawn subagent: research-case-{id}                                 │
│  4. Generate: 3,000-6,000 words                                        │
│  5. Save: research.md                                                  │
│                                                                         │
│  Output: Timeline, victim profile, crime details, DNA breakthrough,    │
│          suspect info, sources                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: PARALLEL CHAPTER GENERATION (19 minutes)                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: Sonnet 4.5 │ 6 Parallel Subagents │ Cost: ~$2.10              │
│                                                                         │
│  ┌────────────────┬────────────────┬────────────────┐                 │
│  │ Subagent 1     │ Subagent 2     │ Subagent 3     │                 │
│  │ Prologue + Ch1 │ Chapters 2-3   │ Chapters 4-5   │                 │
│  │ 2,300-2,800 w  │ 3,600-4,000 w  │ 3,600-4,000 w  │                 │
│  └────────────────┴────────────────┴────────────────┘                 │
│                                                                         │
│  ┌────────────────┬────────────────┬────────────────┐                 │
│  │ Subagent 4     │ Subagent 5     │ Subagent 6     │                 │
│  │ Chapters 6-7   │ Chapters 8-9   │ Ch 10 + Epilog │                 │
│  │ 3,600-4,000 w  │ 3,600-4,000 w  │ 2,300-2,800 w  │                 │
│  └────────────────┴────────────────┴────────────────┘                 │
│                                                                         │
│  All spawn simultaneously → sessions_yield() → wait for completion     │
│                                                                         │
│  Total output: 16,000-20,000 words (11 chapters)                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: MANUSCRIPT ASSEMBLY (30 seconds)                              │
├─────────────────────────────────────────────────────────────────────────┤
│  cat chapters/group*.md > manuscript_draft.md                          │
│                                                                         │
│  Quality Check:                                                        │
│  ┌─────────────────────────────────────┐                              │
│  │ Word count: 18,000 - 25,000?        │                              │
│  │ • Too low (<18K)  → Alert user      │                              │
│  │ • In range        → Continue        │                              │
│  │ • Too high (>25K) → Alert (may trim)│                              │
│  └─────────────────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: TECHNICAL AUDIT (3 minutes)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: Sonnet 4.5 │ Timeout: 900s │ Cost: ~$0.15                     │
│                                                                         │
│  Load: AUDIT-TECHNICAL-OPTIMIZED.md                                    │
│  Task: Find factual errors, timeline issues, contradictions            │
│                                                                         │
│  Output: technical_audit.json                                          │
│  {                                                                      │
│    "error_count": 1,                                                   │
│    "errors": [                                                         │
│      {                                                                 │
│        "line": 42,                                                     │
│        "chapter": "Chapter 2",                                         │
│        "error": "Age inconsistency",                                   │
│        "fix": "Change 29 to 28"                                        │
│      }                                                                 │
│    ],                                                                  │
│    "grade": "A-"                                                       │
│  }                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: NARRATIVE AUDIT (3 minutes)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: Sonnet 4.5 │ Timeout: 900s │ Cost: ~$0.15                     │
│                                                                         │
│  Load: AUDIT-NARRATIVE-OPTIMIZED.md                                    │
│  Task: Grade storytelling, pacing, engagement, show vs tell            │
│                                                                         │
│  Output: narrative_audit.json                                          │
│  {                                                                      │
│    "overall_grade": "A",                                               │
│    "storytelling": "A",                                                │
│    "pacing": "A-",                                                     │
│    "engagement": "A",                                                  │
│    "improvements": [...]                                               │
│  }                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │ Errors found?         │
                        │ (error_count > 0)     │
                        └───────────────────────┘
                                │       │
                            YES │       │ NO
                                │       │
                ┌───────────────▼───┐   └───────────────┐
                │                   │                   │
                ▼                   │                   ▼
┌─────────────────────────────────┐│   ┌─────────────────────────────────┐
│ PHASE 7: CORRECTIONS (3 min)   ││   │ PHASE 7: SKIP (0 sec)           │
├─────────────────────────────────┤│   ├─────────────────────────────────┤
│ Model: Sonnet 4.5               ││   │ No errors found!                │
│ Cost: ~$0.20                    ││   │                                 │
│                                 ││   │ Copy draft to corrected:        │
│ Load: CORRECTIONS-OPTIMIZED.md  ││   │ cp manuscript_draft.md \        │
│                                 ││   │    manuscript_corrected.md      │
│ Fix all technical errors        ││   └─────────────────────────────────┘
│                                 ││                   │
│ Save: manuscript_corrected.md   ││                   │
└─────────────────────────────────┘│                   │
                │                   │                   │
                └───────────────────┴───────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 8: QUALITY PIPELINE (10 minutes)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: Sonnet 4.5 │ 3 Sequential Steps │ Cost: ~$0.60                │
│                                                                         │
│  ┌────────────────────────────────────────┐                            │
│  │ Step 1: writing-assistant (4 min)      │                            │
│  │ • Improve prose and flow               │                            │
│  │ • Tighten structure                    │                            │
│  │ • Enhance emotional impact             │                            │
│  │ Output: manuscript_improved.md         │                            │
│  └────────────────────────────────────────┘                            │
│                     │                                                   │
│                     ▼                                                   │
│  ┌────────────────────────────────────────┐                            │
│  │ Step 2: ai-humanizer (4 min)           │                            │
│  │ • Remove AI patterns                   │                            │
│  │ • Natural voice                        │                            │
│  │ • Vary sentence structures             │                            │
│  │ Output: manuscript_humanized.md        │                            │
│  └────────────────────────────────────────┘                            │
│                     │                                                   │
│                     ▼                                                   │
│  ┌────────────────────────────────────────┐                            │
│  │ Step 3: self-review (2 min)            │                            │
│  │ • Final quality check                  │                            │
│  │ • Generate overall grade               │                            │
│  │ Output: manuscript_final.md +          │                            │
│  │         final_review.json              │                            │
│  └────────────────────────────────────────┘                            │
│                     │                                                   │
│                     ▼                                                   │
│            ┌──────────────────┐                                        │
│            │ QUALITY GATE     │                                        │
│            │ Grade ≥ A- ?     │                                        │
│            └──────────────────┘                                        │
│                │         │                                              │
│            YES │         │ NO                                           │
│                │         │                                              │
│     ┌──────────▼───┐     └─────────────────┐                          │
│     │ PASS         │                       │                          │
│     │ Continue to  │         ┌─────────────▼───────────────┐          │
│     │ Phase 9      │         │ PAUSE                        │          │
│     └──────────────┘         │ • Send Telegram alert        │          │
│                              │ • Grade: {grade}             │          │
│                              │ • Options: Publish/Regen/Skip│          │
│                              │ • Wait for user decision     │          │
│                              └──────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 9: DOCX CONVERSION (30 seconds)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  pandoc manuscript_final.md -o manuscript_final.docx                   │
│      --from markdown                                                   │
│      --to docx                                                         │
│      --toc                                                             │
│      --reference-doc=kdp-template.docx                                 │
│                                                                         │
│  Output: manuscript_final.docx (KDP-ready)                             │
│                                                                         │
│  ✓ 6x9 page size                                                       │
│  ✓ Professional formatting                                             │
│  ✓ Table of contents                                                   │
│  ✓ Chapter headers                                                     │
│  ✓ Page numbers                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 10: COVER GENERATION (30 seconds)                                │
├─────────────────────────────────────────────────────────────────────────┤
│  Model: DALL-E 3 │ Cost: ~$0.04                                        │
│                                                                         │
│  Minimalist Design:                                                    │
│  ┌─────────────────────────────────────────┐                          │
│  │ ╔════════════════════════════════════╗  │  MIND CRIMES #5          │
│  │ ║                                    ║  │                          │
│  │ ║           COLD CASE:               ║  │                          │
│  │ ║       The [Name] Murder            ║  │                          │
│  │ ║                                    ║  │                          │
│  │ ║  ═══════════════════════════════   ║  │  ← Colored accent        │
│  │ ║                                    ║  │                          │
│  │ ║                                    ║  │                          │
│  │ ║                                    ║  │                          │
│  │ ║             N0MAD                  ║  │                          │
│  │ ╚════════════════════════════════════╝  │                          │
│  └─────────────────────────────────────────┘                          │
│                                                                         │
│  • Black background (#000000)                                          │
│  • White text (Bebas Neue font)                                        │
│  • Accent line color rotates (red, teal, yellow, purple, green)        │
│  • 1024x1792 resolution (ebook format)                                 │
│                                                                         │
│  Fallback: If DALL-E fails → ImageMagick text cover                    │
│                                                                         │
│  Output: covers/{case_id}.png                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 11: FINALIZATION (5 seconds)                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  1. Update database:                                                   │
│     python3 scripts/generate_book.py update {case_id} generated        │
│                                                                         │
│  2. Save statistics:                                                   │
│     generation_stats.json:                                             │
│     {                                                                   │
│       "case_id": 123,                                                  │
│       "victim_name": "Sandra Davis",                                   │
│       "word_count": 22150,                                             │
│       "final_grade": "A",                                              │
│       "generation_time_minutes": 43,                                   │
│       "total_cost": 3.82,                                              │
│       "errors_fixed": 1,                                               │
│       "status": "generated"                                            │
│     }                                                                   │
│                                                                         │
│  3. Send Telegram alert:                                               │
│     ✅ BOOK GENERATED                                                  │
│     Case 123: Sandra Davis                                             │
│     Words: 22,150                                                      │
│     Grade: A                                                           │
│     Time: 43 min                                                       │
│     Files: books/123/manuscript_final.docx                             │
│                                                                         │
│     [Review] [Upload to KDP] [Generate Next]                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ COMPLETE! 🎉                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│  Total time: ~45 minutes                                               │
│  Total cost: ~$3.50-$4.00                                              │
│  Quality: A- to A+                                                     │
│  Output: Ready-to-publish ebook                                        │
│                                                                         │
│  Next steps:                                                           │
│  1. Manual QA review (5 min)                                           │
│  2. Upload to KDP                                                      │
│  3. Set price & publish                                                │
│  4. Check for next approved case                                       │
└─────────────────────────────────────────────────────────────────────────┘

                            ┌─────────────────────┐
                            │ Check for next case?│
                            └─────────────────────┘
                                      │
                                 YES  │  NO → Done
                                      │
                            ┌─────────▼─────────┐
                            │ Loop back to      │
                            │ Phase 1           │
                            └───────────────────┘


═══════════════════════════════════════════════════════════════════════════
                          ERROR HANDLING FLOWS
═══════════════════════════════════════════════════════════════════════════

Subagent Timeout:
  Try once → Fails → Retry → Fails again → Mark case 'failed' → Alert user

Quality Below A-:
  Grade check → Fails → Pause → Alert user → Wait for approval

Budget Exceeded:
  Check before each phase → Over limit → Pause → Alert → Resume tomorrow

Database Locked:
  Try → Locked → Wait 1s → Retry (3x) → Still locked → Alert user

═══════════════════════════════════════════════════════════════════════════
                              SYSTEM METRICS
═══════════════════════════════════════════════════════════════════════════

Performance (per book):
  Time:     ~45 minutes
  Cost:     $3.50-$4.00
  Words:    18,000-25,000
  Quality:  A- to A+ (consistently)

Capacity:
  Sequential:  32 books/day (theoretical max)
  Realistic:   10-15 books/day (with oversight)
  Monthly:     200-450 books (automated)

Quality Gates:
  ✓ Word count: 18K-25K
  ✓ Technical errors: ≤2
  ✓ Narrative grade: ≥A-
  ✓ Final grade: ≥A-

═══════════════════════════════════════════════════════════════════════════
```
