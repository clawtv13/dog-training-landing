# Technical Audit Prompt - True Crime Book

## 📋 PRE-AUDIT CHECKLIST

Before starting the audit:

- [ ] Load and read **research document** (factual source material)
- [ ] Extract key facts into audit reference sheet:
  - Character names (full names, nicknames, spellings)
  - Important dates (crime date, trial, sentencing, birth/death dates)
  - Location names (cities, streets, buildings - exact spellings)
  - Timeline anchors (ages at key events, time spans)
  - Verifiable facts (case numbers, official titles, historical events)
- [ ] Note any conflicting information in source material
- [ ] Identify fact-checkable claims in the manuscript

---

## 🔍 SYSTEMATIC REVIEW ORDER

Review the manuscript in this sequence:

1. **Prologue** → Check tone-setting facts
2. **Chapter 1-N** → Sequential review (maintain timeline tracking)
3. **Epilogue** → Verify outcome facts
4. **Front/Back Matter** → Dates, dedications, author notes

**During review:** Track timeline on a separate timeline document as you go.

---

## ✅ VERIFICATION CATEGORIES

### **CATEGORY 1: Character Accuracy** (CRITICAL)

Check every occurrence:
- [ ] Name spelling consistent throughout (first, middle, last, nicknames)
- [ ] Character descriptions consistent (eye color, height, distinguishing features)
- [ ] Titles/roles accurate and consistent (Detective vs. Officer, Dr. vs. Mr.)
- [ ] Family relationships correct (daughter vs stepdaughter, brother vs half-brother)

**Common errors to watch:**
- Name spelling variations (e.g., "Johnston" vs "Johnson")
- Pronoun inconsistencies for same character
- Age contradictions within same timeframe
- Character confusion (attributing actions/quotes to wrong person)

---

### **CATEGORY 2: Timeline Consistency** (CRITICAL)

**Verification methodology:**
1. Create a master timeline with all dated events
2. For each date mentioned, calculate:
   - Days/months/years between events
   - Character ages at that point
   - Day of week (if mentioned - verify with perpetual calendar)
3. Cross-check narrative time descriptors ("three weeks later", "the next morning")

Check:
- [ ] **Explicit dates** match historical calendar (e.g., "Tuesday, June 15, 1994" - was 6/15/94 actually a Tuesday?)
- [ ] **Age calculations** are mathematically correct (birth year + event year = stated age)
- [ ] **Time spans** are internally consistent ("two years later" matches actual date math)
- [ ] **Season/weather references** match the stated date (no "snow in August" in Texas)
- [ ] **Sequential logic** preserved (events happen in correct order)

**Math verification example:**
```
Claim: "Sarah was 32 when arrested in 2005"
Verify: Birth year 1973? → 2005 - 1973 = 32 ✓
Cross-check: "born in summer 1972" elsewhere? → CONTRADICTION ✗
```

**Common timeline errors:**
- Age inconsistencies (character aging wrong number of years)
- Impossible sequences ("the next day" spanning different months)
- Historical event mismatches (referencing events that hadn't happened yet)
- Daylight/time-of-day errors (sun setting at wrong time for date/location)

---

### **CATEGORY 3: Location Accuracy** (HIGH PRIORITY)

Check:
- [ ] City/state names spelled correctly
- [ ] Street names exist and spelled correctly (Google Maps verify)
- [ ] Geographic logic (distances, travel times, relative positions)
- [ ] Location descriptions match reality (if verifiable)
- [ ] Jurisdiction accuracy (correct police department, county, court)

**Common errors:**
- Misspelled city/street names
- Impossible travel times
- Wrong jurisdictional details (wrong county courthouse)
- Anachronistic location references (business that didn't exist yet)

---

### **CATEGORY 4: Factual Accuracy** (HIGH PRIORITY)

Cross-reference against research document:
- [ ] Crime details (date, weapon, method)
- [ ] Legal proceedings (charges, verdict, sentence)
- [ ] Official titles and roles
- [ ] Quoted material (court testimony, news reports)
- [ ] Historical context facts

**Common errors:**
- Charge names (e.g., "murder" vs "involuntary manslaughter")
- Sentence details (years stated incorrectly)
- Misattributed quotes
- Conflating multiple events

---

### **CATEGORY 5: Language & Grammar** (MODERATE PRIORITY)

Check:
- [ ] Spelling errors (spellcheck won't catch: "their" vs "there", "lead" vs "led")
- [ ] Grammar errors (subject-verb agreement, tense consistency)
- [ ] Punctuation (dialogue tags, comma splices, em-dash usage)
- [ ] Capitalization (proper nouns, titles, after colons)
- [ ] Homophone errors (affect/effect, discreet/discrete)

**True crime-specific language checks:**
- Legal terminology used correctly
- Law enforcement jargon accurate
- Medical/forensic terms precise

---

## 🚨 PRIORITY LEVELS

### **CRITICAL** (Must fix before publication)
- Factually incorrect information about the crime/case
- Name misspellings (real people involved)
- Timeline contradictions that break narrative logic
- Defamatory errors

### **HIGH** (Should fix)
- Location errors
- Age inconsistencies
- Title/role inaccuracies
- Confusing contradictions

### **MODERATE** (Fix if time permits)
- Minor grammar issues
- Stylistic inconsistencies
- Unclear phrasing
- Repetitive word choice

### **MINOR** (Nice to have)
- Oxford comma inconsistencies
- Minor stylistic preferences
- Formatting variations

---

## 📊 ERROR REPORTING FORMAT

Use this standardized format:

```
| Severity | Location | Error Type | Current Text | Issue | Proposed Fix | Verification |
|----------|----------|------------|--------------|-------|--------------|--------------|
| CRITICAL | Ch 3, p42, para 2 | Timeline | "arrested July 15, 1993" | Date was actually July 16, 1993 per police report | Change to "July 16, 1993" | Cross-ref: Police Report #93-1847 |
| HIGH | Ch 5, p78, para 4 | Name | "Detective Johnson" | Character's name is "Johnston" elsewhere | Standardize to "Johnston" | Research doc lists "Det. Robert Johnston" |
| MODERATE | Ch 2, p28, para 1 | Grammar | "The evidence was laying on the table" | Incorrect verb form | Change "laying" to "lying" | Grammar rule: lay/lie |
```

**For each error include:**
1. **Severity level** (Critical/High/Moderate/Minor)
2. **Precise location** (Chapter, page if available, paragraph)
3. **Error type** (Timeline/Name/Location/Factual/Language)
4. **Current text** (exact quote showing error)
5. **Issue** (what's wrong)
6. **Proposed fix** (specific correction)
7. **Verification source** (how you confirmed the error)

---

## ✓ VERIFICATION STEPS

### Timeline Math Double-Check Process:
1. List all dated events chronologically
2. Calculate spans between events
3. Verify ages at each point
4. Check narrative time markers ("three weeks later")
5. Confirm seasonal references match dates
6. Verify day-of-week if mentioned (use perpetual calendar)

### Name Verification Process:
1. Create master character list with canonical spellings
2. Search manuscript for each name (including variations)
3. Flag all variations
4. Cross-reference with research doc for correct spelling
5. Standardize throughout

### Location Verification Process:
1. List all mentioned locations
2. Google Maps search for existence/spelling
3. Check distances/travel times for logic
4. Verify jurisdiction details (county, police dept)

### Factual Cross-Reference Process:
1. Identify all fact claims
2. Match against research document
3. Flag unsupported claims
4. Note conflicting information
5. Request clarification for unverifiable claims

---

## 📝 EXAMPLE ERROR REPORTS

**Good Error Report (CRITICAL):**
```
Severity: CRITICAL
Location: Chapter 7, Page 104, Paragraph 3
Error Type: Timeline/Age Inconsistency
Current Text: "When Maria testified in 2001, she was 28 years old."
Issue: Maria was born May 12, 1975 (per research doc). In 2001, she would be 25-26, not 28.
Proposed Fix: Change to "she was 26 years old" OR verify birth year is actually 1973
Verification: Birth certificate copy in research folder shows DOB: 05/12/1975
Math: 2001 - 1975 = 26 years (or 25 if before May 12)
```

**Good Error Report (HIGH):**
```
Severity: HIGH
Location: Chapter 3, Page 47, Paragraph 5
Error Type: Location
Current Text: "The hearing took place at the Franklin County Courthouse"
Issue: Case was in Knox County, not Franklin County (per court records)
Proposed Fix: Change to "Knox County Courthouse"
Verification: Court docket #98-CR-0234 filed in Knox County Circuit Court
```

**Good Error Report (MODERATE):**
```
Severity: MODERATE
Location: Chapter 12, Page 203, Paragraph 1
Error Type: Grammar
Current Text: "The jury was comprised of twelve members"
Issue: "Comprised of" is considered incorrect usage; "composed of" or "comprises" preferred
Proposed Fix: Change to "The jury was composed of twelve members" OR "The jury comprised twelve members"
Verification: Grammar style guide (AP/Chicago)
```

---

## 🎯 AUDIT COMPLETION CHECKLIST

Before submitting audit results:

- [ ] Reviewed entire manuscript start to finish
- [ ] Created and verified master timeline
- [ ] Cross-referenced all names against research doc
- [ ] Verified all location spellings
- [ ] Checked timeline math at least twice
- [ ] Categorized errors by severity
- [ ] Provided specific fixes for all errors
- [ ] Included verification sources
- [ ] Formatted report in standardized table
- [ ] Noted any unresolvable questions for author

---

## 📤 DELIVERABLE

Provide:
1. **Summary** (total errors by severity + category)
2. **Error table** (all findings in standardized format)
3. **Timeline verification document** (if timeline errors found)
4. **Questions for author** (any unverifiable claims or contradictions in source material)
5. **Clean-file confidence level** (Low/Medium/High - based on error density)

---

**Remember:** Your job is to catch EVERYTHING. Be ruthlessly thorough. A reader finding an error the auditor missed is a failure. Protect the author's credibility.