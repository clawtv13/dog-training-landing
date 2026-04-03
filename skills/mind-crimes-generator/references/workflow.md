# Mind Crimes Book Generation Workflow

**Complete 10-phase pipeline from database → published ebook**

**Total time:** ~45 minutes per book  
**Cost estimate:** $2.50-$4.00 per book (Sonnet 4.5 pricing)  
**Quality target:** A- minimum (9.0/10 grade)

---

## PHASE 1: DATABASE CHECK & SETUP (10 seconds)

### Check for Approved Cases

```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py check
```

**Expected output:**
```json
{
  "status": "found",
  "case_id": 123,
  "victim_name": "Sandra Davis",
  "victim_age": 28,
  "murder_date": "1986-05-12",
  "arrest_date": "2024-11-08",
  "cold_case_years": 38,
  "location": "Miami, FL",
  "suspect_name": "Robert Johnson",
  "suspect_age": 62,
  "dna_method": "genetic genealogy",
  "source_url": "https://...",
  "score": 87.5
}
```

If `status: "none"` → Exit gracefully with "No approved cases"

### Create Directory Structure

```bash
mkdir -p /opt/mind-crimes-automation/data/books/{case_id}/chapters
mkdir -p /opt/mind-crimes-automation/data/books/{case_id}/audits
```

### Update Status to 'generating'

```bash
python3 scripts/generate_book.py update {case_id} generating
```

---

## PHASE 2: RESEARCH COMPILATION (6 minutes)

### Load Research Prompt

```bash
research_prompt=$(cat /root/.openclaw/workspace/prompts/RESEARCH-PROMPT-OPTIMIZED.md)
```

### Variable Substitution

Replace these placeholders with case data:
- `{victim_name}` → Sandra Davis
- `{victim_age}` → 28
- `{location}` → Miami, FL
- `{murder_date}` → May 12, 1986
- `{arrest_date}` → November 8, 2024
- `{cold_case_years}` → 38 years
- `{suspect_name}` → Robert Johnson
- `{suspect_age}` → 62
- `{dna_method}` → genetic genealogy
- `{source_url}` → [original article]

### Spawn Research Subagent

```javascript
// In OpenClaw agent context
const result = await sessions_spawn({
    task: research_prompt_with_substitutions,
    runtime: "subagent",
    mode: "run",
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 1800,
    name: `research-case-${case_id}`
});

// Wait for completion
await sessions_yield();
```

### Save Research Output

```bash
cat > /opt/mind-crimes-automation/data/books/{case_id}/research.md
```

**Quality check:**
- Word count: 3,000-6,000 words
- Sections: Victim profile, crime details, investigation history, DNA breakthrough, suspect profile
- Sources: At least 3 unique sources cited

---

## PHASE 3: PARALLEL CHAPTER GENERATION (19 minutes)

**Strategy:** 6 parallel subagents, each generating 2 chapters + prologue/epilogue

### Load Chapter Template

```bash
chapter_template=$(cat /root/.openclaw/workspace/prompts/CHAPTER-TEMPLATE-OPTIMIZED.md)
```

### Spawn 6 Parallel Subagents

**Subagent 1: Prologue + Chapter 1**
```
Task: Generate Prologue and Chapter 1

Research context:
{research_content}

Prologue: "The Last Day" (500-800 words)
- Set the scene of the victim's final day
- Build atmosphere and tension
- End with foreshadowing

Chapter 1: "The Victim" (1,800-2,000 words)
- Who was {victim_name}?
- Life, family, hopes, dreams
- Why this case matters
- The day of the murder

Output ONLY the markdown content. No commentary.
```

**Subagent 2: Chapters 2-3**
```
Chapter 2: "The Crime Scene" (1,800-2,000 words)
- Discovery of the body
- Initial investigation
- Forensic evidence collected
- Community reaction

Chapter 3: "The Investigation Begins" (1,800-2,000 words)
- Initial suspects
- Timeline reconstruction
- Witness interviews
- Early theories
```

**Subagent 3: Chapters 4-5**
```
Chapter 4: "Dead Ends" (1,800-2,000 words)
- False leads
- Suspects cleared
- Evidence limitations (pre-DNA era)
- Investigation stalls

Chapter 5: "The Cold Case" (1,800-2,000 words)
- Case goes cold
- Years pass
- Family never gives up
- Detective keeps file open
```

**Subagent 4: Chapters 6-7**
```
Chapter 6: "The Breakthrough" (1,800-2,000 words)
- DNA technology advances
- Cold case unit reopens file
- Evidence re-examined
- New possibilities emerge

Chapter 7: "The DNA Detective" (1,800-2,000 words)
- Genetic genealogy explained
- Building family tree
- Narrowing suspects
- The crucial match
```

**Subagent 5: Chapters 8-9**
```
Chapter 8: "Building the Case" (1,800-2,000 words)
- Confirming the suspect
- Gathering corroborating evidence
- Legal strategy
- Preparing for arrest

Chapter 9: "The Arrest" (1,800-2,000 words)
- The moment of confrontation
- Suspect's reaction
- Booking and charges
- Media coverage
```

**Subagent 6: Chapter 10 + Epilogue**
```
Chapter 10: "Justice Delayed" (1,800-2,000 words)
- Trial preparation
- Courtroom drama
- Verdict
- Sentencing

Epilogue: "Aftermath" (500-800 words)
- Family closure
- Impact on community
- DNA revolution in cold cases
- Final reflection
```

### Parallel Execution

```javascript
const chapterTasks = [
    subagent1_prompt,
    subagent2_prompt,
    subagent3_prompt,
    subagent4_prompt,
    subagent5_prompt,
    subagent6_prompt
];

// Spawn all simultaneously
const spawns = chapterTasks.map((task, i) => 
    sessions_spawn({
        task,
        model: "openrouter/anthropic/claude-sonnet-4.5",
        runTimeoutSeconds: 1800,
        name: `chapter-group-${i+1}-case-${case_id}`
    })
);

// Wait for all to complete
await sessions_yield();
```

### Save Chapter Outputs

```bash
# Save each group's output
/opt/mind-crimes-automation/data/books/{case_id}/chapters/00_prologue.md
/opt/mind-crimes-automation/data/books/{case_id}/chapters/01_chapter.md
/opt/mind-crimes-automation/data/books/{case_id}/chapters/02_chapter.md
...
/opt/mind-crimes-automation/data/books/{case_id}/chapters/10_chapter.md
/opt/mind-crimes-automation/data/books/{case_id}/chapters/11_epilogue.md
```

**Quality check:**
- Total word count: 16,000-20,000 words
- Each chapter has clear structure
- Consistent voice and tone
- Smooth narrative flow between chapters

---

## PHASE 4: MANUSCRIPT ASSEMBLY (30 seconds)

### Combine All Chapters

```bash
cd /opt/mind-crimes-automation/data/books/{case_id}

cat chapters/00_prologue.md \
    chapters/01_chapter.md \
    chapters/02_chapter.md \
    chapters/03_chapter.md \
    chapters/04_chapter.md \
    chapters/05_chapter.md \
    chapters/06_chapter.md \
    chapters/07_chapter.md \
    chapters/08_chapter.md \
    chapters/09_chapter.md \
    chapters/10_chapter.md \
    chapters/11_epilogue.md \
    > manuscript_draft.md
```

### Add Metadata

```bash
cat > manuscript_with_metadata.md << EOF
---
title: "Cold Case: The {Victim Name} Murder"
subtitle: "A {Cold Case Years}-Year Quest for Justice"
author: N0MAD
series: Mind Crimes
book_number: {book_number}
case_id: {case_id}
generated: $(date -I)
---

$(cat manuscript_draft.md)
EOF
```

### Calculate Statistics

```bash
word_count=$(wc -w < manuscript_draft.md)
echo "{\"word_count\": $word_count, \"status\": \"assembled\"}" > assembly_stats.json
```

---

## PHASE 5: TECHNICAL AUDIT (3 minutes)

### Load Audit Prompt

```bash
audit_prompt=$(cat /root/.openclaw/workspace/prompts/AUDIT-TECHNICAL-OPTIMIZED.md)
manuscript=$(cat manuscript_draft.md)
```

### Spawn Technical Audit Subagent

```javascript
const auditResult = await sessions_spawn({
    task: `${audit_prompt}\n\nMANUSCRIPT TO AUDIT:\n\n${manuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `audit-technical-case-${case_id}`
});

await sessions_yield();
```

### Expected Output Format

```json
{
  "error_count": 3,
  "errors": [
    {
      "line": 42,
      "chapter": "Chapter 2",
      "type": "factual_error",
      "error": "Victim age stated as 29, should be 28",
      "fix": "Change age from 29 to 28"
    },
    {
      "line": 156,
      "chapter": "Chapter 4",
      "type": "timeline_inconsistency",
      "error": "Murder date given as May 13, but earlier stated as May 12",
      "fix": "Change to May 12 throughout"
    },
    {
      "line": 287,
      "chapter": "Chapter 7",
      "type": "unsupported_claim",
      "error": "States suspect was 'known to police' but no evidence provided",
      "fix": "Remove claim or add supporting details"
    }
  ],
  "grade": "B+",
  "notes": "Generally accurate, minor errors need correction"
}
```

### Save Audit Report

```bash
cat > audits/technical_audit.json
```

---

## PHASE 6: NARRATIVE AUDIT (3 minutes)

### Load Narrative Audit Prompt

```bash
narrative_prompt=$(cat /root/.openclaw/workspace/prompts/AUDIT-NARRATIVE-OPTIMIZED.md)
```

### Spawn Narrative Audit Subagent

```javascript
const narrativeResult = await sessions_spawn({
    task: `${narrative_prompt}\n\nMANUSCRIPT TO AUDIT:\n\n${manuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `audit-narrative-case-${case_id}`
});

await sessions_yield();
```

### Expected Output Format

```json
{
  "overall_grade": "A-",
  "grades": {
    "storytelling": "A",
    "pacing": "A-",
    "show_vs_tell": "B+",
    "emotional_impact": "A",
    "engagement": "A-"
  },
  "strengths": [
    "Strong opening that hooks reader",
    "Excellent character development",
    "Clear narrative arc"
  ],
  "improvements": [
    "Chapter 4 drags in middle section - tighten",
    "More sensory details in crime scene chapter",
    "Epilogue could be more reflective"
  ],
  "recommendation": "Publish with minor revisions"
}
```

### Save Narrative Audit

```bash
cat > audits/narrative_audit.json
```

---

## PHASE 7: CORRECTIONS (0-3 minutes)

**Conditional:** Only if technical errors > 0

### Load Corrections Prompt

```bash
corrections_prompt=$(cat /root/.openclaw/workspace/prompts/CORRECTIONS-OPTIMIZED.md)
errors=$(cat audits/technical_audit.json | jq -r '.errors')
```

### Spawn Corrections Subagent

```javascript
if (error_count > 0) {
    const correctedResult = await sessions_spawn({
        task: `${corrections_prompt}

MANUSCRIPT:
${manuscript}

ERRORS TO FIX:
${JSON.stringify(errors, null, 2)}

Output: Corrected manuscript in markdown format.`,
        model: "openrouter/anthropic/claude-sonnet-4.5",
        runTimeoutSeconds: 900,
        name: `corrections-case-${case_id}`
    });
    
    await sessions_yield();
    
    // Save corrected version
    fs.writeFileSync('manuscript_corrected.md', correctedResult.output);
} else {
    // No errors, copy draft to corrected
    fs.copyFileSync('manuscript_draft.md', 'manuscript_corrected.md');
}
```

---

## PHASE 8: QUALITY PIPELINE (10 minutes)

**Use installed OpenClaw skills for final polish**

### Step 1: Writing Assistant (4 min)

```javascript
const improvedResult = await sessions_spawn({
    task: `Improve this true crime manuscript. Focus on:
- Tightening prose
- Improving flow between chapters
- Enhancing emotional impact
- Maintaining factual accuracy

MANUSCRIPT:
${correctedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `quality-1-writing-case-${case_id}`
});

await sessions_yield();
fs.writeFileSync('manuscript_improved.md', improvedResult.output);
```

### Step 2: AI Humanizer (4 min)

```javascript
const humanizedResult = await sessions_spawn({
    task: `Humanize this text. Remove AI patterns like:
- Overuse of "As" at sentence starts
- Generic transitions
- Passive voice overuse
- Robotic pacing

Make it sound natural and human-written.

TEXT:
${improvedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `quality-2-humanize-case-${case_id}`
});

await sessions_yield();
fs.writeFileSync('manuscript_humanized.md', humanizedResult.output);
```

### Step 3: Self-Review (2 min)

```javascript
const reviewResult = await sessions_spawn({
    task: `Final quality check. Grade this manuscript:

CRITERIA:
- Storytelling quality (1-10)
- Factual accuracy (1-10)
- Reader engagement (1-10)
- Overall polish (1-10)

Provide final grade (A+/A/A-/B+/B/B-/C)

MANUSCRIPT:
${humanizedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 600,
    name: `quality-3-review-case-${case_id}`
});

await sessions_yield();
fs.writeFileSync('manuscript_final.md', humanizedManuscript);
fs.writeFileSync('audits/final_review.json', reviewResult.output);
```

### Quality Gate Check

```javascript
const finalGrade = parseFinalGrade(reviewResult.output);
const gradeValue = gradeToNumber(finalGrade); // A- = 9.0, B+ = 8.5, etc.

if (gradeValue < 9.0) {
    // Alert user - below threshold
    await sendTelegramAlert(`⚠️ QUALITY ALERT

Case ${case_id}: ${victim_name}
Grade: ${finalGrade} (below A- threshold)

Options:
1. Publish anyway
2. Regenerate chapters
3. Skip case

/approve_${case_id} | /regenerate_${case_id} | /skip_${case_id}`);
    
    // Pause here, wait for user decision
    return { status: "awaiting_approval", case_id, grade: finalGrade };
}
```

---

## PHASE 9: DOCX CONVERSION (30 seconds)

### Convert with Pandoc

```bash
cd /opt/mind-crimes-automation/data/books/{case_id}

pandoc manuscript_final.md \
    -o manuscript_final.docx \
    --from markdown \
    --to docx \
    --reference-doc=/root/.openclaw/workspace/templates/kdp-template.docx \
    --toc \
    --toc-depth=1
```

**KDP template includes:**
- 6x9 inch page size
- 0.5" margins
- Chapter headers styled
- Page numbers
- Professional formatting

### Verify DOCX

```bash
# Check file created
if [ -f manuscript_final.docx ]; then
    file_size=$(stat -f%z manuscript_final.docx 2>/dev/null || stat -c%s manuscript_final.docx)
    echo "{\"status\": \"success\", \"file_size\": $file_size}" > conversion_status.json
else
    echo "{\"status\": \"failed\"}" > conversion_status.json
fi
```

---

## PHASE 10: COVER GENERATION (30 seconds)

### Call OpenAI DALL-E 3 API

```javascript
const openai = require('openai');

const bookTitle = `Cold Case: The ${victim_name} Murder`;
const bookNumber = case_data.book_number || 1;
const accentColors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7', '#A8E6CF'];
const accentColor = accentColors[(bookNumber - 1) % accentColors.length];

const coverPrompt = `Minimalist true crime book cover design:

LAYOUT:
- Background: Solid black (#000000)
- Title: "${bookTitle}" in bold white Bebas Neue font, centered, 72pt
- Accent: Single ${accentColor} horizontal line, 4px thick, centered below title
- Badge: "MIND CRIMES #${bookNumber}" in top right corner, small white text
- Author: "N0MAD" at bottom center, 24pt white text

STYLE:
- Ultra-minimalist
- High contrast black and white
- Clean typography
- Readable at thumbnail size (500px wide)
- No photos, no illustrations
- Professional, modern, sleek

DIMENSIONS: 1024x1792 (portrait, 9:16 ratio for ebook)`;

const response = await openai.images.generate({
    model: "dall-e-3",
    prompt: coverPrompt,
    size: "1024x1792",
    quality: "standard",
    n: 1
});

const imageUrl = response.data[0].url;

// Download and save
const imageBuffer = await fetch(imageUrl).then(r => r.buffer());
fs.writeFileSync(`/opt/mind-crimes-automation/data/covers/${case_id}.png`, imageBuffer);
```

### Backup Cover (if AI fails)

```bash
# Use ImageMagick to generate simple text cover
convert -size 1024x1792 xc:black \
    -gravity center \
    -pointsize 72 -fill white -font Bebas-Neue \
    -annotate +0-200 "Cold Case:\n${victim_name}" \
    -pointsize 24 -fill white \
    -annotate +0+800 "N0MAD" \
    -fill "${accent_color}" -draw "rectangle 200,600,824,604" \
    /opt/mind-crimes-automation/data/covers/${case_id}_backup.png
```

---

## PHASE 11: FINALIZATION (5 seconds)

### Update Database

```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py \
    update {case_id} generated
```

### Calculate Final Stats

```javascript
const stats = {
    case_id: case_id,
    victim_name: victim_name,
    word_count: wordCount,
    final_grade: finalGrade,
    generation_time_minutes: Math.round((Date.now() - startTime) / 60000),
    total_cost: calculateCost(tokenUsage),
    subagents_spawned: 12,
    errors_fixed: technicalAudit.error_count,
    status: "generated"
};

fs.writeFileSync('generation_stats.json', JSON.stringify(stats, null, 2));
```

### Send Telegram Completion Alert

```javascript
await sendTelegramAlert(`✅ BOOK GENERATED

**Case ${case_id}: ${victim_name}**

📊 Stats:
- Words: ${wordCount.toLocaleString()}
- Grade: ${finalGrade}
- Time: ${stats.generation_time_minutes} min
- Cost: $${stats.total_cost.toFixed(2)}
- Errors fixed: ${stats.errors_fixed}

📁 Files ready:
- Manuscript: manuscript_final.docx
- Cover: covers/${case_id}.png

[Upload to KDP] [Review Files] [Generate Next]`);
```

---

## ERROR HANDLING & EDGE CASES

### Subagent Timeout

```javascript
try {
    const result = await sessions_spawn({...options, runTimeoutSeconds: 1800});
    await sessions_yield();
} catch (error) {
    if (error.type === 'timeout') {
        // Retry once
        console.log('Subagent timed out, retrying...');
        const retryResult = await sessions_spawn({...options});
        await sessions_yield();
    } else {
        // Hard fail
        await markCaseFailed(case_id, error.message);
        throw error;
    }
}
```

### Quality Below Threshold

```javascript
if (finalGrade < 'A-') {
    // Don't auto-publish
    await updateCaseStatus(case_id, 'review_needed');
    await alertUser(case_id, finalGrade);
    // Wait for manual approval
    return { status: 'paused', reason: 'quality_review' };
}
```

### Budget Exceeded

```javascript
const dailySpend = await getDailySpend();
if (dailySpend > DAILY_CAP) {
    await updateCaseStatus(case_id, 'paused');
    await alertUser(`Budget cap reached: $${dailySpend}/$${DAILY_CAP}`);
    return { status: 'paused', reason: 'budget' };
}
```

### Database Lock

```javascript
let retries = 3;
while (retries > 0) {
    try {
        await updateDatabase(case_id, status);
        break;
    } catch (error) {
        if (error.code === 'SQLITE_BUSY') {
            retries--;
            await sleep(1000);
        } else {
            throw error;
        }
    }
}
```

---

## SUCCESS CRITERIA CHECKLIST

Book is considered complete when ALL conditions met:

- ✅ Research: 3,000-6,000 words
- ✅ Chapters: 11 total (prologue + 10 chapters + epilogue)
- ✅ Word count: 18,000-25,000 words
- ✅ Technical errors: ≤2
- ✅ Narrative grade: ≥ A- (9.0/10)
- ✅ .docx file created
- ✅ Cover image generated
- ✅ Database status: 'generated'
- ✅ User notified via Telegram

---

## PERFORMANCE BENCHMARKS

**Based on Books 4-5 production:**

| Phase | Time | Model | Cost |
|-------|------|-------|------|
| Research | 6 min | Sonnet 4.5 | $0.40 |
| Chapters (6 parallel) | 19 min | Sonnet 4.5 | $2.10 |
| Technical Audit | 3 min | Sonnet 4.5 | $0.15 |
| Narrative Audit | 3 min | Sonnet 4.5 | $0.15 |
| Corrections | 3 min | Sonnet 4.5 | $0.20 |
| Quality Pipeline | 10 min | Sonnet 4.5 | $0.60 |
| DOCX Conversion | 30 sec | Local | $0.00 |
| Cover Generation | 30 sec | DALL-E 3 | $0.04 |
| Finalization | 5 sec | Local | $0.00 |
| **TOTAL** | **~45 min** | | **$3.64** |

**Throughput:** 32 books/day (if running 24/7)  
**Realistic:** 10-15 books/day (with human oversight)

---

## NEXT STEPS AFTER GENERATION

1. **Manual QA** (5 min):
   - Skim manuscript for obvious errors
   - Check cover looks good
   - Verify all files present

2. **Upload to KDP**:
   - Use KDP API or manual upload
   - Set price ($2.99-$4.99)
   - Publish to Amazon

3. **Upload to Gumroad**:
   - Create product
   - Set price ($4.99)
   - Add to email list automation

4. **Marketing**:
   - Tweet thread about case
   - Email subscribers
   - Update website

5. **Move to Next Case**:
   - Mark current case 'live'
   - Check for next approved case
   - Repeat workflow

---

**This workflow is proven, tested, and ready for production automation.**
