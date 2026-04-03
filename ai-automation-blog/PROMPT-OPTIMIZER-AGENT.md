# 🧠 PROMPT OPTIMIZER AGENT

## Purpose

Permanent agent for optimizing any prompt you give it. Use this whenever you need to improve a prompt for ANY project (AI Automation Builder, CleverDogMethod, future projects).

---

## How to Use

**Input:**
```
OPTIMIZE THIS PROMPT:

[paste your current prompt]

TASK: [what it's for]
MODEL: [Claude/GPT/etc]
CURRENT ISSUES: [optional - what's wrong]
```

**Output:**
- Optimized version
- What changed
- Expected improvements

---

## Optimization Framework

### 1. SPECIFICITY UPGRADE

**Before (generic):**
```
Write a blog post about AI automation.
Include examples and make it useful.
```

**After (specific):**
```
Write a 1,200-word blog post about [TOPIC] for solo founders.

STRUCTURE:
- Hook (2 sentences): Specific pain point
- Problem (150 words): Current manual process
- Solution (300 words): How automation fixes it
- Implementation (500 words): 5-step guide with tool names
- Results (150 words): Time/cost saved with numbers
- CTA (100 words): Next action

EXAMPLES REQUIRED:
- Real tool name + price
- Actual time saved (hours → minutes)
- Specific workflow (before/after)

BANNED PHRASES:
- "Imagine a world where..."
- "In today's fast-paced..."
- "Revolutionize"

VOICE:
- Direct: "Here's what works"
- Technical but accessible
- No fluff or filler

Return ONLY HTML content (no wrapper tags).
```

**Improvements:**
- Word count exact (not range)
- Section breakdown with word targets
- Examples specified (not "include examples")
- Banned phrases listed
- Voice guidelines concrete
- Output format clear

---

### 2. CONSTRAINT HIERARCHY

**Structure:**

```
MUST (critical requirements):
- [requirement 1]
- [requirement 2]

SHOULD (important but not critical):
- [guideline 1]
- [guideline 2]

AVOID (explicitly banned):
- [anti-pattern 1]
- [anti-pattern 2]

MAY (optional enhancements):
- [nice-to-have 1]
```

**Example:**

```
MUST:
- Return valid JSON only
- Include all 5 fields (title, summary, score, tags, url)
- Score between 0-40 (integer)

SHOULD:
- Prioritize recent stories (last 24h)
- Favor actionable over theoretical
- Include quantitative data when available

AVOID:
- Generic announcements ("Company X raises $Y")
- Reposted news (check if covered already)
- Hype without substance

MAY:
- Add "breaking: true" flag for urgent stories
- Include "competitor_analysis" if relevant
```

---

### 3. FEW-SHOT EXAMPLES

**When to use:** Complex output format, specific style, or nuanced task

**Template:**

```
[Task description]

EXAMPLES:

Input 1:
[example input]

Expected output 1:
[example output]

Input 2:
[different example input]

Expected output 2:
[different example output]

Now process:
[actual input]
```

**Example:**

```
Score this article for newsletter inclusion.

EXAMPLES:

Input: "OpenAI announces new model"
Output: {
  "score": 15,
  "reason": "Generic announcement, no actionable insight",
  "include": false
}

Input: "I built an AI agent that saves 10h/week on email"
Output: {
  "score": 38,
  "reason": "Specific use case, quantified benefit, actionable",
  "include": true,
  "priority": "high"
}

Now score: [article]
```

---

### 4. CHAIN-OF-THOUGHT PROMPTING

**For complex reasoning tasks:**

```
[Task]

Think through this step-by-step:

1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Check if [validation criteria]
4. Finally, decide [outcome]

Show your reasoning for each step, then provide final answer.
```

**Example:**

```
Decide if this article should be featured in newsletter.

Think through step-by-step:

1. RELEVANCE: Does this help solo founders automate?
   - Yes/No + reason

2. NOVELTY: Is this new information or rehashed?
   - Novel/Derivative + evidence

3. ACTIONABILITY: Can reader implement this week?
   - Immediate/Requires-setup/Theoretical + why

4. IMPACT: How much time/money does this save?
   - High (10h+/week) / Medium (2-10h) / Low (<2h)

Based on scores above, feature? Yes/No + final reasoning.
```

---

### 5. OUTPUT VALIDATION

**Always include:**

```
OUTPUT FORMAT:

Valid:
[example of correct output]

Invalid:
[example of wrong output]

Validation rules:
- [rule 1]
- [rule 2]

If you cannot provide valid output, return:
{"error": "reason", "attempted": "what you tried"}
```

**Example:**

```
Return JSON with article analysis.

VALID OUTPUT:
{
  "score": 35,
  "tags": ["automation", "ai-agents"],
  "summary": "Technical guide to...",
  "include": true
}

INVALID (missing fields):
{
  "score": 35
}

INVALID (wrong type):
{
  "score": "high"  // must be integer 0-40
}

Validation:
- score: integer 0-40
- tags: array of strings, 1-5 items
- summary: string, 50-150 chars
- include: boolean

If article is unreadable or off-topic, return:
{"error": "reason", "raw_title": "..."}
```

---

### 6. ERROR HANDLING

**Template:**

```
[Task]

Handle these edge cases:

IF [condition 1]:
  THEN [action 1]

IF [condition 2]:
  THEN [action 2]

IF none of the above work:
  Return error: [format]
```

**Example:**

```
Generate blog post from research item.

Handle edge cases:

IF source URL is paywalled:
  Generate from title + summary only
  Add disclaimer: "Full source requires subscription"

IF topic is too technical for target audience:
  Simplify without dumbing down
  Add "Technical Explainer" section

IF article is <500 words after generation:
  Expand with related examples
  OR flag for human review

IF generation fails 2x:
  Return: {"error": "generation_failed", "item_id": X, "attempts": 2}
```

---

### 7. PERSONA STRENGTHENING

**Before (weak persona):**
```
Write in a professional but friendly tone.
```

**After (strong persona):**
```
PERSONA: Alex Chen - AI automation engineer

BACKGROUND:
- Built 3 automated businesses to $50K+/month
- <5 hours/week active work
- Non-technical founder turned technical

VOICE PATTERNS:
- "Here's what works" not "you might consider"
- "I built X and learned Y" (personal experience)
- "This is better than Z because [data]" (opinionated)
- Admits limitations: "This won't work if you..."

BANNED (these feel corporate):
- "It's important to note..."
- "At the end of the day..."
- "Leverage synergies"

EXAMPLES OF ALEX CHEN VOICE:

Generic: "Consider automating your email responses"
Alex Chen: "I cut email time from 2h to 15min/day using this automation. Here's the exact setup."

Generic: "Automation can help businesses"
Alex Chen: "Automation isn't about being lazy. It's about building leverage. I'd rather spend 10 hours building a system that saves 100 hours than manually do 100 hours of work."

Write as Alex would write.
```

---

### 8. TOKEN OPTIMIZATION

**Techniques:**

1. **Remove filler:**
   - "Please" → delete
   - "I would like you to" → just state action
   - "In order to" → "To"

2. **Use abbreviations:**
   - "For example" → "E.g."
   - "That is" → "I.e."
   - "Et cetera" → "etc."

3. **Bullet points > paragraphs:**
   ```
   Bad: "The output should be JSON format. It should include a title field, which is a string, and a score field, which should be an integer between 0 and 100."
   
   Good:
   Return JSON:
   - title: string
   - score: integer (0-100)
   ```

4. **"Return ONLY [format]" pattern:**
   ```
   Instead of:
   "Please provide your response in JSON format without any additional text, explanations, or markdown formatting."
   
   Use:
   "Return ONLY valid JSON. No explanations."
   ```

5. **Implicit context:**
   ```
   Instead of:
   "You are an AI assistant helping to generate blog posts. The blog is about AI automation. The target audience is solo founders. The tone should be professional but accessible."
   
   Use:
   "You are writing for workless.build - AI automation blog for solo founders. Professional but accessible."
   ```

---

### 9. MODEL-SPECIFIC OPTIMIZATION

**Claude (Sonnet/Opus):**
- Loves structured XML-like tags: `<examples>...</examples>`
- Responds well to "think step-by-step"
- Verbose by default, need "Return ONLY [format]"
- Strong at following complex instructions

**GPT (4/4.5):**
- Prefers JSON structures
- System message + user message split useful
- Good at creative tasks
- Can be overly cautious, need explicit permission

**Optimization:**

For Claude:
```
<task>Generate blog post</task>

<requirements>
- 1,200 words
- Include examples
</requirements>

<voice>
Direct and practical
</voice>

Think through the structure first, then write.
Return ONLY HTML content.
```

For GPT:
```
Generate a 1,200-word blog post.

Requirements:
- Include specific examples
- Direct and practical voice

Output: HTML only (no explanations)
```

---

### 10. QUALITY METRICS

**Define success criteria:**

```
This prompt is successful if:
- ✅ Output requires <5% regeneration rate
- ✅ Quality score consistently 70+/100
- ✅ Zero parsing errors
- ✅ Follows voice guidelines 90%+ of time
- ✅ Token cost within $0.08/run

Regenerate if:
- Quality score <70
- Missing required fields
- Wrong output format
- AI clichés detected
```

---

## OPTIMIZATION CHECKLIST

Use this when improving any prompt:

```
□ SPECIFICITY
  □ Exact word count (not range)
  □ Section breakdown with targets
  □ Examples specified (not "include examples")
  □ Output format crystal clear

□ CONSTRAINTS
  □ MUST requirements listed
  □ SHOULD guidelines clear
  □ AVOID anti-patterns explicit
  □ MAY optional items noted

□ EXAMPLES
  □ Few-shot samples if complex format
  □ Both good and bad examples
  □ Edge cases covered

□ VALIDATION
  □ Valid output example shown
  □ Invalid output examples shown
  □ Validation rules listed
  □ Error format specified

□ PERSONA
  □ Strong voice guidelines
  □ Specific examples of voice
  □ Banned phrases listed
  □ Background context given

□ EFFICIENCY
  □ Filler words removed
  □ Bullet points used
  □ Token count minimized
  □ "Return ONLY" pattern used

□ ERROR HANDLING
  □ Edge cases identified
  □ IF/THEN logic clear
  □ Fallback behavior specified

□ QUALITY
  □ Success criteria defined
  □ Regeneration triggers clear
  □ Cost targets specified
```

---

## BEFORE/AFTER EXAMPLES

### Example 1: Blog Post Generation

**BEFORE (generic, 42 tokens):**
```
Write a blog post about the topic provided.
Make it informative and engaging.
Include examples and use a professional tone.
```

**AFTER (specific, 156 tokens but 3x better output):**
```
Write 1,200-word blog post: [TOPIC]

STRUCTURE:
- Hook (2 sent): Specific problem
- Problem (150w): Current manual process
- Solution (300w): Automation approach
- Steps (500w): 5-step implementation
- Results (150w): Time saved (hours)
- CTA (100w): Next action

MUST include:
- Tool name + price
- Before/after time comparison
- Code snippet if technical

VOICE:
- "Here's what works" (not "you might consider")
- Personal experience references
- Data-backed claims

BANNED:
- "Imagine a world..."
- "In today's fast-paced..."

Return ONLY HTML (no wrapper tags).
```

**Improvements:**
- Exact word count (not vague "informative")
- Section breakdown (not "engaging")
- Required elements specified
- Voice examples (not "professional")
- Banned phrases explicit
- Output format clear

**Expected results:**
- Quality: +40% (more consistent output)
- Cost: Same (token increase worth it)
- Regeneration: -60% (fewer do-overs)

---

### Example 2: Research Scoring

**BEFORE (ambiguous, 38 tokens):**
```
Score this article for newsletter relevance.
Consider if it's useful for the target audience.
Return a score and explanation.
```

**AFTER (structured, 124 tokens):**
```
Score article for "AI Automation Insights" newsletter.

AUDIENCE: Solo founders learning AI automation

SCORING (0-40 scale):
- Relevance (0-10): Helps solo founders automate?
- Novelty (0-10): New info or rehashed?
- Actionability (0-10): Can implement this week?
- Impact (0-10): Time/money saved?

MUST flag if:
- Generic announcement (score <15)
- Theoretical only (no implementation)
- Requires team/enterprise (not solo-friendly)

Return JSON:
{
  "score": 35,
  "breakdown": {"relevance": 9, "novelty": 8, ...},
  "include": true,
  "reason": "Specific automation saves 10h/week"
}

Return ONLY JSON.
```

**Improvements:**
- Scoring rubric explicit (not "consider if useful")
- Scale defined (0-40, not vague)
- Flags specified (not "relevant")
- Output format exact
- Validation implicit

**Expected results:**
- Consistency: +50% (same article scored same)
- Cost: +$0.005 (worth it for consistency)
- Parsing errors: -90% (JSON format clear)

---

### Example 3: Email Generation

**BEFORE (vague, 31 tokens):**
```
Write an email for the newsletter sequence.
Keep it conversational and valuable.
Include a clear call to action.
```

**AFTER (detailed, 178 tokens):**
```
Write email #{N} of {TOTAL} for {SEQUENCE_NAME}.

CONTEXT:
- Previous: {PREVIOUS_SUMMARY}
- Subscriber: {STAGE} (awareness/consideration/decision)

EMAIL:

Subject (40-50 chars):
- Curiosity-driven
- No clickbait
- Open-rate optimized

Body (250-350 words):
- Personal tone (from Alex)
- Value before ask
- Single clear CTA
- Short paragraphs (2-3 lines)

WELCOME SEQUENCE STRATEGY:
Email 1: Welcome + quick win
Email 2: Core value resource
Email 3: Story/case study
Email 4: Tool recommendation
Email 5: Soft product intro

Return JSON:
{
  "subject": "...",
  "preview": "First 50 chars",
  "body": "...",
  "cta_text": "...",
  "cta_url": "..."
}

Return ONLY JSON.
```

**Improvements:**
- Sequence context given (not "newsletter sequence")
- Subject requirements specific (not "conversational")
- Body length exact (not vague)
- Strategy per email type
- Output structure clear

**Expected results:**
- Relevance: +35% (sequence-aware)
- Open rate: +15% (better subjects)
- Cost: +$0.01 (worth it for better emails)

---

## PROMPT TESTING METHODOLOGY

**When you optimize a prompt:**

1. **Baseline Test (3 runs):**
   - Run current prompt 3x
   - Measure: quality score, cost, time, regeneration rate

2. **Optimization:**
   - Apply framework
   - Improve based on checklist

3. **Comparison Test (3 runs):**
   - Run optimized prompt 3x
   - Measure same metrics

4. **Analysis:**
   - Quality delta
   - Cost delta
   - Time delta
   - Regeneration delta

5. **Decision:**
   - Deploy if: quality +10% OR cost -20% OR regen -30%
   - Iterate if: mixed results
   - Rollback if: worse on 2+ metrics

---

## COST-BENEFIT ANALYSIS

**When is optimization worth it?**

✅ **Optimize if:**
- Prompt runs >10x/week (frequency matters)
- Current regeneration rate >10%
- Output quality inconsistent
- Parsing errors common
- Task is critical (blog posts, emails)

⏸️ **Maybe optimize:**
- Runs 1-10x/week
- Current quality acceptable but not great
- Non-critical task

❌ **Don't optimize if:**
- Runs <1x/week (not worth time)
- Current quality already 90%+
- One-off task

**ROI Calculation:**

```
Time investment: 30-60 min to optimize
Benefit: Better output + fewer regenerations

Break-even: If prompt saves 2+ hours over next month, optimize.
```

---

## QUICK OPTIMIZATION TEMPLATES

### Template 1: Content Generation

```
Write [WORD_COUNT]-word [CONTENT_TYPE] about [TOPIC].

AUDIENCE: [WHO]
PURPOSE: [WHAT_THEY_GET]

STRUCTURE:
- Section 1 ([X words]): [PURPOSE]
- Section 2 ([X words]): [PURPOSE]
- Section 3 ([X words]): [PURPOSE]

MUST include:
- [REQUIRED_ELEMENT_1]
- [REQUIRED_ELEMENT_2]

VOICE:
- [VOICE_PATTERN_1]
- [VOICE_PATTERN_2]

BANNED:
- [ANTI_PATTERN_1]
- [ANTI_PATTERN_2]

Return ONLY [FORMAT].
```

### Template 2: Analysis/Scoring

```
Analyze [INPUT] for [PURPOSE].

CRITERIA:
- [CRITERION_1] (0-10): [DEFINITION]
- [CRITERION_2] (0-10): [DEFINITION]
- [CRITERION_3] (0-10): [DEFINITION]

MUST flag if:
- [RED_FLAG_1]
- [RED_FLAG_2]

Return JSON:
{
  "score": [0-X],
  "breakdown": {...},
  "decision": true/false,
  "reason": "..."
}

Return ONLY JSON.
```

### Template 3: Curation/Selection

```
Select best [N] items from [COLLECTION] for [PURPOSE].

SELECTION CRITERIA:
1. [CRITERION_1]
2. [CRITERION_2]
3. [CRITERION_3]

AVOID:
- [EXCLUDE_1]
- [EXCLUDE_2]

Return JSON array:
[
  {
    "id": X,
    "title": "...",
    "reason": "Why selected",
    "priority": "high|medium|low"
  }
]

Return ONLY JSON.
```

---

## USAGE EXAMPLES

### How to Optimize a New Prompt

**You have:**
```
Write a social media post about this article.
```

**Ask the optimizer:**
```
OPTIMIZE THIS PROMPT:

Current: "Write a social media post about this article."

TASK: Generate Twitter/LinkedIn posts for blog promotion
MODEL: Claude Sonnet 4.5
CURRENT ISSUES: Too generic, inconsistent quality, no voice

TARGET:
- Platform-specific (Twitter 280 chars, LinkedIn 150 words)
- Strong hook (first 10 words critical)
- Alex Chen voice
- Include link + CTA
```

**Get back:**
```
Generate social post promoting blog article.

INPUT:
- Article title: {TITLE}
- Article URL: {URL}
- Key takeaway: {SUMMARY}

PLATFORM: [Twitter | LinkedIn]

TWITTER (280 chars):
- Hook (first 40 chars): Controversial or surprising
- Value prop (80 chars): What reader gets
- CTA (40 chars): Action + emoji
- Link: {URL}
- Hashtags: 2-3 relevant

Example:
"Most AI automation advice is wrong.

Here's what actually works for solo founders (tested on 3 businesses):

→ [insight]

Read the breakdown: [link]

#AIAutomation #SoloFounder"

LINKEDIN (150 words):
- Hook question or bold claim
- Problem (2 sentences)
- Solution preview (3 sentences)
- CTA: "Read the full guide: [link]"

VOICE:
- Direct, no fluff
- Data/results mentioned
- Personal experience hints

Return JSON:
{
  "platform": "twitter",
  "text": "...",
  "expected_engagement": "2-5%"
}

Return ONLY JSON.
```

---

## MAINTENANCE

**Keep this framework updated:**

1. **After each project:**
   - Document what worked
   - Add new techniques discovered
   - Update examples

2. **Monthly review:**
   - Check which prompts have highest quality
   - Analyze what makes them work
   - Apply learnings to framework

3. **Continuous improvement:**
   - Test new prompt patterns
   - Benchmark against industry
   - Iterate framework

---

## WHEN TO USE THIS AGENT

✅ **Use for:**
- Optimizing any existing prompt
- Creating new production prompts
- Troubleshooting prompt issues
- Improving consistency
- Reducing costs
- Any AI automation project

---

**This framework is now your prompt optimization system.**

Use it for AI Automation Builder, CleverDogMethod, or any future project.

Save 30-60 min per prompt optimization with this structured approach.
