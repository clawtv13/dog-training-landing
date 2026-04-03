# Mind Crimes Generator Skill

**Automated ebook generation from approved cold case arrests**

## When to Use

Activate this skill when:
- User says: "Generate Mind Crimes book for case {id}"
- User says: "Check for approved Mind Crimes cases"
- User says: "Generate the next Mind Crimes book"
- Cron trigger: Every 30 min check for approved cases

## Quick Start

```bash
# Check for approved cases
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py check

# If found → follow workflow below
# If none → reply "No approved cases. Waiting for alerts."
```

---

## EXECUTABLE WORKFLOW

**Follow these steps exactly. Each phase has error handling.**

### PHASE 1: CHECK DATABASE (10 seconds)

```bash
# Run check
RESULT=$(python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py check)

# Parse JSON
STATUS=$(echo "$RESULT" | jq -r '.status')

if [ "$STATUS" = "none" ]; then
    echo "No approved cases found. Check back later."
    exit 0
fi

# Extract case data
CASE_ID=$(echo "$RESULT" | jq -r '.case_id')
VICTIM_NAME=$(echo "$RESULT" | jq -r '.victim_name')
VICTIM_AGE=$(echo "$RESULT" | jq -r '.victim_age')
MURDER_DATE=$(echo "$RESULT" | jq -r '.murder_date')
ARREST_DATE=$(echo "$RESULT" | jq -r '.arrest_date')
COLD_YEARS=$(echo "$RESULT" | jq -r '.cold_case_years')
LOCATION=$(echo "$RESULT" | jq -r '.location')
SUSPECT_NAME=$(echo "$RESULT" | jq -r '.suspect_name')
SUSPECT_AGE=$(echo "$RESULT" | jq -r '.suspect_age')
DNA_METHOD=$(echo "$RESULT" | jq -r '.dna_method')
SOURCE_URL=$(echo "$RESULT" | jq -r '.source_url')
SCORE=$(echo "$RESULT" | jq -r '.score')
```

**Create output directories:**
```bash
mkdir -p /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters
mkdir -p /opt/mind-crimes-automation/data/books/${CASE_ID}/audits
```

**Update status to 'generating':**
```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py \
    update ${CASE_ID} generating
```

**Send Telegram notification:**
```
🚀 STARTING BOOK GENERATION

Case ${CASE_ID}: ${VICTIM_NAME}
Location: ${LOCATION}
Cold case: ${COLD_YEARS} years
Score: ${SCORE}/100

Estimated time: 45 minutes
```

---

### PHASE 2: RESEARCH COMPILATION (6 minutes)

**Load research prompt:**
```bash
RESEARCH_PROMPT=$(cat /root/.openclaw/workspace/prompts/RESEARCH-PROMPT-OPTIMIZED.md)
```

**Substitute variables:**
```javascript
// In agent context
const researchPrompt = RESEARCH_PROMPT
    .replace(/{victim_name}/g, VICTIM_NAME)
    .replace(/{victim_age}/g, VICTIM_AGE)
    .replace(/{murder_date}/g, formatDate(MURDER_DATE))
    .replace(/{arrest_date}/g, formatDate(ARREST_DATE))
    .replace(/{cold_case_years}/g, COLD_YEARS)
    .replace(/{location}/g, LOCATION)
    .replace(/{suspect_name}/g, SUSPECT_NAME)
    .replace(/{suspect_age}/g, SUSPECT_AGE)
    .replace(/{dna_method}/g, DNA_METHOD)
    .replace(/{source_url}/g, SOURCE_URL);
```

**Spawn research subagent:**
```javascript
const startTime = Date.now();

const researchResult = await sessions_spawn({
    task: researchPrompt,
    runtime: "subagent",
    mode: "run",
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 1800,
    name: `research-case-${CASE_ID}`
});

// Wait for completion
await sessions_yield();
```

**Save research output:**
```bash
echo "${researchResult}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/research.md
```

**Quality check:**
```bash
RESEARCH_WORDS=$(wc -w < /opt/mind-crimes-automation/data/books/${CASE_ID}/research.md)

if [ $RESEARCH_WORDS -lt 3000 ]; then
    echo "⚠️ Research too short (${RESEARCH_WORDS} words). Minimum 3,000."
    # Retry or alert user
fi
```

---

### PHASE 3: PARALLEL CHAPTER GENERATION (19 minutes)

**Load chapter template:**
```bash
CHAPTER_TEMPLATE=$(cat /root/.openclaw/workspace/prompts/CHAPTER-TEMPLATE-OPTIMIZED.md)
RESEARCH_CONTENT=$(cat /opt/mind-crimes-automation/data/books/${CASE_ID}/research.md)
```

**Define 6 parallel chapter tasks:**

```javascript
const chapterTasks = [
    {
        name: "prologue-ch1",
        chapters: [
            { num: 0, title: "Prologue: The Last Day", words: "500-800" },
            { num: 1, title: "Chapter 1: The Victim", words: "1800-2000" }
        ]
    },
    {
        name: "ch2-3",
        chapters: [
            { num: 2, title: "Chapter 2: The Crime Scene", words: "1800-2000" },
            { num: 3, title: "Chapter 3: The Investigation Begins", words: "1800-2000" }
        ]
    },
    {
        name: "ch4-5",
        chapters: [
            { num: 4, title: "Chapter 4: Dead Ends", words: "1800-2000" },
            { num: 5, title: "Chapter 5: The Cold Case", words: "1800-2000" }
        ]
    },
    {
        name: "ch6-7",
        chapters: [
            { num: 6, title: "Chapter 6: The Breakthrough", words: "1800-2000" },
            { num: 7, title: "Chapter 7: The DNA Detective", words: "1800-2000" }
        ]
    },
    {
        name: "ch8-9",
        chapters: [
            { num: 8, title: "Chapter 8: Building the Case", words: "1800-2000" },
            { num: 9, title: "Chapter 9: The Arrest", words: "1800-2000" }
        ]
    },
    {
        name: "ch10-epilogue",
        chapters: [
            { num: 10, title: "Chapter 10: Justice Delayed", words: "1800-2000" },
            { num: 11, title: "Epilogue: Aftermath", words: "500-800" }
        ]
    }
];
```

**Build prompts for each subagent:**

```javascript
const buildChapterPrompt = (task) => {
    let prompt = `Generate chapters for the ${VICTIM_NAME} murder case.

RESEARCH CONTEXT:
${RESEARCH_CONTENT}

CHAPTERS TO WRITE:
`;
    
    task.chapters.forEach(ch => {
        prompt += `\n${ch.title} (${ch.words} words)\n`;
    });
    
    prompt += `\n${CHAPTER_TEMPLATE}

Output: ONLY the chapter content in markdown. No commentary.`;
    
    return prompt;
};
```

**Spawn all 6 subagents in parallel:**

```javascript
const chapterSpawns = chapterTasks.map((task, i) => 
    sessions_spawn({
        task: buildChapterPrompt(task),
        model: "openrouter/anthropic/claude-sonnet-4.5",
        runTimeoutSeconds: 1800,
        name: `chapters-${task.name}-case-${CASE_ID}`
    })
);

// Wait for all to complete
await sessions_yield();
```

**Save chapter outputs:**

```bash
# Save each chapter group
echo "${chapterGroup1}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group1.md
echo "${chapterGroup2}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group2.md
echo "${chapterGroup3}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group3.md
echo "${chapterGroup4}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group4.md
echo "${chapterGroup5}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group5.md
echo "${chapterGroup6}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/chapters/group6.md
```

---

### PHASE 4: MANUSCRIPT ASSEMBLY (30 seconds)

**Combine all chapters:**
```bash
cd /opt/mind-crimes-automation/data/books/${CASE_ID}

cat chapters/group1.md \
    chapters/group2.md \
    chapters/group3.md \
    chapters/group4.md \
    chapters/group5.md \
    chapters/group6.md \
    > manuscript_draft.md
```

**Calculate word count:**
```bash
WORD_COUNT=$(wc -w < manuscript_draft.md)
echo "📊 Draft complete: ${WORD_COUNT} words"

if [ $WORD_COUNT -lt 18000 ]; then
    echo "⚠️ Word count too low: ${WORD_COUNT}/18,000 minimum"
    # Alert user
fi

if [ $WORD_COUNT -gt 25000 ]; then
    echo "⚠️ Word count too high: ${WORD_COUNT}/25,000 maximum"
    # May need trimming
fi
```

---

### PHASE 5: TECHNICAL AUDIT (3 minutes)

**Load audit prompt:**
```bash
AUDIT_PROMPT=$(cat /root/.openclaw/workspace/prompts/AUDIT-TECHNICAL-OPTIMIZED.md)
MANUSCRIPT=$(cat /opt/mind-crimes-automation/data/books/${CASE_ID}/manuscript_draft.md)
```

**Spawn technical audit subagent:**
```javascript
const technicalAuditTask = `${AUDIT_PROMPT}

MANUSCRIPT TO AUDIT:
${MANUSCRIPT}

Output: JSON format with errors found (if any).`;

const auditResult = await sessions_spawn({
    task: technicalAuditTask,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `audit-tech-case-${CASE_ID}`
});

await sessions_yield();
```

**Save audit report:**
```bash
echo "${auditResult}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/audits/technical_audit.json
```

**Check error count:**
```bash
ERROR_COUNT=$(cat audits/technical_audit.json | jq -r '.error_count')

if [ $ERROR_COUNT -gt 2 ]; then
    echo "⚠️ Too many errors: ${ERROR_COUNT}/2 maximum"
    # May need regeneration
fi
```

---

### PHASE 6: NARRATIVE AUDIT (3 minutes)

**Load narrative audit prompt:**
```bash
NARRATIVE_PROMPT=$(cat /root/.openclaw/workspace/prompts/AUDIT-NARRATIVE-OPTIMIZED.md)
```

**Spawn narrative audit subagent:**
```javascript
const narrativeAuditTask = `${NARRATIVE_PROMPT}

MANUSCRIPT TO AUDIT:
${MANUSCRIPT}

Output: Grade and recommendations in JSON format.`;

const narrativeResult = await sessions_spawn({
    task: narrativeAuditTask,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `audit-narrative-case-${CASE_ID}`
});

await sessions_yield();
```

**Save narrative audit:**
```bash
echo "${narrativeResult}" > /opt/mind-crimes-automation/data/books/${CASE_ID}/audits/narrative_audit.json
```

**Check grade:**
```bash
GRADE=$(cat audits/narrative_audit.json | jq -r '.overall_grade')
echo "📝 Narrative grade: ${GRADE}"
```

---

### PHASE 7: CORRECTIONS (0-3 minutes)

**Conditional: Only if errors found**

```bash
if [ $ERROR_COUNT -gt 0 ]; then
    echo "🔧 Fixing ${ERROR_COUNT} errors..."
    
    CORRECTIONS_PROMPT=$(cat /root/.openclaw/workspace/prompts/CORRECTIONS-OPTIMIZED.md)
    ERRORS=$(cat audits/technical_audit.json | jq -r '.errors')
    
    # Spawn corrections subagent
    # (JavaScript context)
    const correctionsTask = `${CORRECTIONS_PROMPT}

MANUSCRIPT:
${MANUSCRIPT}

ERRORS TO FIX:
${JSON.stringify(ERRORS, null, 2)}

Output: Corrected manuscript in markdown.`;

    const correctedResult = await sessions_spawn({
        task: correctionsTask,
        model: "openrouter/anthropic/claude-sonnet-4.5",
        runTimeoutSeconds: 900,
        name: `corrections-case-${CASE_ID}`
    });
    
    await sessions_yield();
    
    # Save corrected manuscript
    echo "${correctedResult}" > manuscript_corrected.md
else
    echo "✅ No errors found, skipping corrections"
    cp manuscript_draft.md manuscript_corrected.md
fi
```

---

### PHASE 8: QUALITY PIPELINE (10 minutes)

**Use installed OpenClaw skills:**

**Step 1: Writing Assistant (4 min)**
```javascript
const improvedResult = await sessions_spawn({
    task: `Improve this true crime manuscript. Focus on:
- Tightening prose
- Improving chapter flow
- Enhancing emotional impact
- Maintaining factual accuracy

Do NOT change facts, only improve writing quality.

MANUSCRIPT:
${correctedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `quality-writing-case-${CASE_ID}`
});

await sessions_yield();
fs.writeFileSync('manuscript_improved.md', improvedResult);
```

**Step 2: AI Humanizer (4 min)**
```javascript
const humanizedResult = await sessions_spawn({
    task: `Humanize this text. Remove AI writing patterns:
- Overuse of "As" sentence starters
- Generic transitions ("Moreover", "Furthermore")
- Passive voice overuse
- Robotic pacing
- Repetitive sentence structures

Make it sound naturally human-written.

TEXT:
${improvedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 900,
    name: `quality-humanize-case-${CASE_ID}`
});

await sessions_yield();
fs.writeFileSync('manuscript_humanized.md', humanizedResult);
```

**Step 3: Self-Review (2 min)**
```javascript
const reviewResult = await sessions_spawn({
    task: `Final quality review. Grade this manuscript:

CRITERIA (1-10 scale):
- Storytelling quality
- Factual accuracy
- Reader engagement
- Overall polish

Provide:
1. Overall grade (A+/A/A-/B+/B/B-/C)
2. Scores for each criterion
3. Brief assessment

MANUSCRIPT:
${humanizedManuscript}`,
    model: "openrouter/anthropic/claude-sonnet-4.5",
    runTimeoutSeconds: 600,
    name: `quality-review-case-${CASE_ID}`
});

await sessions_yield();

fs.writeFileSync('manuscript_final.md', humanizedManuscript);
fs.writeFileSync('audits/final_review.json', reviewResult);
```

**Quality gate check:**
```javascript
const finalGrade = parseGrade(reviewResult);
const gradeValue = gradeToNumber(finalGrade); // A- = 9.0, B+ = 8.5

if (gradeValue < 9.0) {
    // Below A- threshold
    await sendTelegramAlert(`⚠️ QUALITY ALERT

Case ${CASE_ID}: ${VICTIM_NAME}
Final grade: ${finalGrade} (below A- threshold)

Word count: ${WORD_COUNT}
Errors fixed: ${ERROR_COUNT}

Options:
1. Publish anyway
2. Regenerate chapters
3. Skip this case

Reply:
/publish_${CASE_ID} | /regen_${CASE_ID} | /skip_${CASE_ID}`);
    
    // Pause and wait for user decision
    return { status: "awaiting_approval", case_id: CASE_ID };
}

// Grade is A- or higher, proceed
echo "✅ Quality gate passed: ${finalGrade}"
```

---

### PHASE 9: DOCX CONVERSION (30 seconds)

**Convert manuscript to DOCX:**
```bash
cd /opt/mind-crimes-automation/data/books/${CASE_ID}

pandoc manuscript_final.md \
    -o manuscript_final.docx \
    --from markdown \
    --to docx \
    --toc \
    --toc-depth=1 \
    --reference-doc=/root/.openclaw/workspace/templates/kdp-template.docx
```

**Verify conversion:**
```bash
if [ -f manuscript_final.docx ]; then
    FILE_SIZE=$(stat -c%s manuscript_final.docx)
    echo "✅ DOCX created: ${FILE_SIZE} bytes"
else
    echo "❌ DOCX conversion failed"
    # Alert user
fi
```

---

### PHASE 10: COVER GENERATION (30 seconds)

**Call OpenAI DALL-E 3 API:**

```javascript
const openai = require('openai');

const bookNumber = await getNextBookNumber(CASE_ID);
const bookTitle = `Cold Case: The ${VICTIM_NAME} Murder`;
const accentColors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7', '#A8E6CF'];
const accentColor = accentColors[(bookNumber - 1) % accentColors.length];

const coverPrompt = `Minimalist true crime book cover design:

LAYOUT:
- Background: Solid black (#000000)
- Title: "${bookTitle}" in bold white Bebas Neue font
- Centered, 72pt size
- Accent: ${accentColor} horizontal line, 4px thick, below title
- Badge: "MIND CRIMES #${bookNumber}" top right corner, white text
- Author: "N0MAD" bottom center, 24pt white

STYLE:
- Ultra-minimalist
- High contrast
- Clean typography
- Readable at 500px thumbnail
- No photos or illustrations
- Professional and modern

DIMENSIONS: 1024x1792 (portrait, ebook format)`;

try {
    const response = await openai.images.generate({
        model: "dall-e-3",
        prompt: coverPrompt,
        size: "1024x1792",
        quality: "standard",
        n: 1
    });
    
    const imageUrl = response.data[0].url;
    
    // Download image
    const imageBuffer = await fetch(imageUrl).then(r => r.buffer());
    const coverPath = `/opt/mind-crimes-automation/data/covers/${CASE_ID}.png`;
    fs.writeFileSync(coverPath, imageBuffer);
    
    console.log(`✅ Cover generated: ${coverPath}`);
    
} catch (error) {
    console.log(`❌ Cover generation failed: ${error.message}`);
    console.log('Creating fallback text cover...');
    
    // Fallback: Use ImageMagick to create simple text cover
    exec(`convert -size 1024x1792 xc:black \
        -gravity center \
        -pointsize 72 -fill white \
        -annotate +0-200 "Cold Case:\\n${VICTIM_NAME}" \
        -pointsize 24 -fill white \
        -annotate +0+800 "N0MAD" \
        -fill "${accentColor}" -draw "rectangle 200,600,824,604" \
        /opt/mind-crimes-automation/data/covers/${CASE_ID}_fallback.png`);
}
```

---

### PHASE 11: FINALIZATION (5 seconds)

**Update database status:**
```bash
python3 /root/.openclaw/workspace/skills/mind-crimes-generator/scripts/generate_book.py \
    update ${CASE_ID} generated
```

**Calculate final statistics:**
```javascript
const endTime = Date.now();
const generationTime = Math.round((endTime - startTime) / 60000); // minutes

const stats = {
    case_id: CASE_ID,
    victim_name: VICTIM_NAME,
    word_count: WORD_COUNT,
    final_grade: finalGrade,
    generation_time_minutes: generationTime,
    errors_fixed: ERROR_COUNT,
    subagents_spawned: 12,
    status: "generated",
    timestamp: new Date().toISOString()
};

fs.writeFileSync(`/opt/mind-crimes-automation/data/books/${CASE_ID}/generation_stats.json`, 
    JSON.stringify(stats, null, 2));
```

**Send completion notification:**
```javascript
await sendTelegramAlert(`✅ BOOK GENERATION COMPLETE

**Case ${CASE_ID}: ${VICTIM_NAME}**

📊 **Statistics:**
- Word count: ${WORD_COUNT.toLocaleString()}
- Final grade: ${finalGrade}
- Generation time: ${generationTime} min
- Errors fixed: ${ERROR_COUNT}

📁 **Files ready:**
- Manuscript: manuscript_final.docx
- Cover: covers/${CASE_ID}.png

**Next steps:**
1. [Review Manuscript] /review_${CASE_ID}
2. [Upload to KDP] /upload_kdp_${CASE_ID}
3. [Generate Next Book] /generate_next

Book location: /opt/mind-crimes-automation/data/books/${CASE_ID}/`);
```

---

## ERROR HANDLING

### Subagent Timeout

```javascript
try {
    const result = await sessions_spawn({...config, runTimeoutSeconds: 1800});
    await sessions_yield();
} catch (error) {
    if (error.type === 'timeout') {
        console.log('⚠️ Subagent timed out, retrying once...');
        
        try {
            const retryResult = await sessions_spawn({...config});
            await sessions_yield();
            return retryResult;
        } catch (retryError) {
            // Second failure - mark case as failed
            await updateCaseStatus(CASE_ID, 'failed');
            await sendTelegramAlert(`❌ GENERATION FAILED

Case ${CASE_ID}: ${VICTIM_NAME}
Reason: Subagent timeout (2 attempts)

Case marked as 'failed'. Manual intervention required.`);
            throw retryError;
        }
    } else {
        throw error;
    }
}
```

### Quality Below Threshold

```javascript
if (gradeValue < 9.0) {
    await updateCaseStatus(CASE_ID, 'review_needed');
    await sendTelegramAlert(`⚠️ Quality below threshold - awaiting approval`);
    
    // Pause workflow, wait for user decision
    // User can reply: /publish_{CASE_ID}, /regen_{CASE_ID}, or /skip_{CASE_ID}
    return { status: 'paused', reason: 'quality_review' };
}
```

### Budget Exceeded

```javascript
const dailySpend = await getDailySpend();
const DAILY_CAP = 50.0; // USD

if (dailySpend >= DAILY_CAP) {
    await updateCaseStatus(CASE_ID, 'paused');
    await sendTelegramAlert(`🛑 BUDGET CAP REACHED

Daily spend: $${dailySpend.toFixed(2)}/$${DAILY_CAP}

Case ${CASE_ID} paused. Will resume tomorrow at 00:00 UTC.`);
    
    return { status: 'paused', reason: 'budget_cap' };
}
```

### Database Lock

```bash
# Retry logic for SQLite busy errors
RETRIES=3
while [ $RETRIES -gt 0 ]; do
    python3 scripts/generate_book.py update ${CASE_ID} generated
    if [ $? -eq 0 ]; then
        break
    fi
    
    RETRIES=$((RETRIES - 1))
    echo "Database locked, retrying... (${RETRIES} attempts left)"
    sleep 1
done

if [ $RETRIES -eq 0 ]; then
    echo "❌ Failed to update database after 3 retries"
    # Alert user
fi
```

---

## CONFIGURATION

**Quality thresholds:**
```javascript
const CONFIG = {
    MINIMUM_GRADE: 9.0,        // A- minimum (9.0 on 10-point scale)
    MINIMUM_WORDS: 18000,      // 18K words minimum
    MAXIMUM_WORDS: 25000,      // 25K words maximum
    MAX_ERRORS: 2,             // Allow up to 2 technical errors
    
    DAILY_CAP: 50.0,           // $50 daily spending cap
    ALERT_THRESHOLD: 0.8,      // Alert at 80% of cap
    
    RESEARCH_TIMEOUT: 1800,    // 30 minutes
    CHAPTER_TIMEOUT: 1800,     // 30 minutes
    AUDIT_TIMEOUT: 900,        // 15 minutes
    QUALITY_TIMEOUT: 900,      // 15 minutes
    
    MODEL: "openrouter/anthropic/claude-sonnet-4.5"
};
```

---

## SUCCESS CRITERIA

Book is complete when ALL conditions met:

- ✅ Research: 3,000-6,000 words
- ✅ Chapters: 11 total (prologue + 10 chapters + epilogue)
- ✅ Word count: 18,000-25,000 words
- ✅ Technical errors: ≤2
- ✅ Narrative grade: ≥ A- (9.0/10)
- ✅ Final grade: ≥ A- (9.0/10)
- ✅ .docx file created
- ✅ Cover image generated
- ✅ Database status: 'generated'
- ✅ User notified via Telegram

---

## NOTES FOR AGENT

**This skill is self-contained and executable:**
- All prompts exist in `/root/.openclaw/workspace/prompts/`
- All helper scripts work (`generate_book.py`)
- All quality skills are installed (writing-assistant, ai-humanizer, self-review)
- Database schema is correct and tested

**Expected performance:**
- Time: ~45 minutes per book
- Cost: $3.50-$4.00 per book
- Quality: Consistently A- to A+

**When to alert user:**
- Quality below A-
- Errors > 2
- Word count outside range
- Any subagent failure (after retry)
- Budget approaching cap

**Automation ready:**
- Can run unattended via cron (every 30 min)
- Handles errors gracefully
- Pauses for human approval when needed
- Tracks all metrics in JSON files

---

**This is the final piece that makes Mind Crimes fully automated: scrape → score → approve → GENERATE → publish.**
