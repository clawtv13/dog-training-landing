# RESEARCH PROMPT: True Crime Case Investigation

## ROLE & CONTEXT
You are a true crime researcher compiling a comprehensive case document for a narrative non-fiction book. Your research will be read by a writer who needs factual accuracy, narrative structure, and psychological depth. This document must be publication-ready and fact-checkable.

---

## TARGET CASE
**Case Name:** [INSERT FULL CASE NAME]  
**Also Known As:** [Any alternate names/media names]

---

## OUTPUT REQUIREMENTS

### File Format
- **Path:** `/root/.openclaw/workspace/[case-name-slug].md`
- **Encoding:** UTF-8
- **Line length:** Max 120 characters (for readability)
- **Headers:** Use consistent markdown hierarchy (H1 for title, H2 for sections, H3 for subsections)

### Document Structure (MANDATORY SECTIONS)

#### 1. CASE SUMMARY (200-300 words)
A high-level overview written for someone unfamiliar with the case. Include:
- Who was killed/victimized
- Who committed the crime
- When and where it occurred
- How the perpetrator was caught
- Final legal outcome

**Success criteria:**
- ✅ A reader should understand the entire case arc in 2 minutes
- ✅ Include NO speculation—only confirmed facts
- ✅ Write in past tense

**Example (Good):**
> "On March 15, 2004, Laci Peterson (27) disappeared from her Modesto, California home while eight months pregnant. Her husband, Scott Peterson (31), reported her missing on December 24, 2002. On April 13, 2003, the decomposed remains of Laci and her unborn son Conner washed ashore in San Francisco Bay. Scott Peterson was arrested on April 18, 2003, near the Mexican border with $15,000 cash, survival gear, and bleached hair. He was convicted of first-degree murder (Laci) and second-degree murder (Conner) on November 12, 2004, and sentenced to death. In 2021, his sentence was commuted to life without parole."

**Example (Bad):**
> "Laci Peterson was probably killed by her husband Scott Peterson in a shocking crime that captivated America..."
> ❌ Uses "probably" (speculative)  
> ❌ Includes subjective language ("shocking," "captivated")  
> ❌ Missing key facts (dates, location, evidence)

---

#### 2. COMPLETE TIMELINE (Strict Chronological Order)
Every significant event with **exact dates** (or best available). Use ISO format (YYYY-MM-DD) when possible.

**Format:**
```
- **YYYY-MM-DD** - Event description (source if contested/critical)
```

**Minimum required entries:**
- Victim's birth
- Perpetrator's birth (if known)
- First meeting between victim/perpetrator (if applicable)
- Warning signs or prior incidents (if applicable)
- Crime date(s)
- Discovery of crime/body
- Arrest date
- Key investigation milestones
- Trial dates (start, verdict, sentencing)
- Appeals (if any)
- Current status

**Success criteria:**
- ✅ 20-50 timeline entries minimum
- ✅ NO "around," "approximately," or vague dates without notation
- ✅ Use "~YYYY-MM" or "[date unknown, estimated YYYY]" when exact date unavailable
- ✅ Include court transcripts/police reports as sources for contested dates

**Example (Good):**
```markdown
- **1975-05-05** - Scott Lee Peterson born in San Diego, California
- **1975-08-04** - Laci Denise Rocha born in Modesto, California
- **1994-Summer** - Scott and Laci meet at Pacific Café in Morro Bay
- **2002-11-15** - Scott Peterson begins affair with Amber Frey (per Frey's testimony)
- **2002-12-24** - Laci Peterson reported missing at 5:17 PM
```

**Example (Bad):**
```markdown
- Scott Peterson was born in 1975
- He met Laci in college
- The crime happened in late 2002
```
❌ No specific dates  
❌ Factually incorrect (they met at a restaurant, not college)  
❌ No sourcing

---

#### 3. VICTIM PROFILE (400-600 words)

**Required subsections:**
- **Early Life & Family Background** (100-150 words)
- **Education & Career** (50-100 words)
- **Personality & Interests** (100-150 words) - Use quotes from friends/family
- **Relationships** (100-150 words) - Focus on relationship with perpetrator
- **Life Before the Crime** (50-100 words) - State of mind, plans, recent events

**Success criteria:**
- ✅ Humanize the victim (avoid "perfect victim" clichés)
- ✅ Use direct quotes from 3+ sources (family, friends, colleagues)
- ✅ Avoid gratuitous trauma details—focus on who they were alive
- ✅ Cite sources for all biographical claims

**Source quality requirements:**
- Court testimony transcripts
- Documented interviews (TV, podcast, newspaper with date)
- Biographies or books
- Official obituaries
- Avoid: unsourced blogs, forums, Wikipedia

---

#### 4. PERPETRATOR PROFILE (500-800 words)

**Required subsections:**
- **Early Life & Family Background** (150-200 words) - childhood, family dynamics, trauma
- **Education & Career Path** (100-150 words)
- **Psychological Profile** (200-300 words)
  - Diagnosed conditions (if any)
  - Behavioral patterns noted by experts
  - Prior criminal history (if any)
  - Red flags observed by others
- **Relationship with Victim** (100-150 words)
  - How they met
  - Relationship dynamics
  - Warning signs or abuse patterns

**Success criteria:**
- ✅ Distinguish between clinical diagnosis and armchair psychology
- ✅ Cite forensic psychologists, court-appointed experts, or trial testimony
- ✅ Avoid sensationalism—focus on documented behavior
- ✅ Include conflicting accounts if they exist (e.g., "Defense experts argued X, but prosecution experts testified Y")

---

#### 5. THE CRIME (600-1000 words)

**Required subsections:**
- **Date, Time & Location** (50-100 words) - Be specific
- **Method & Manner** (200-300 words) - How it happened (based on evidence, not speculation)
- **Physical Evidence** (200-400 words)
  - Forensic findings
  - Weapons/tools
  - DNA, fingerprints, fibers
  - Digital evidence (texts, emails, search history)
- **The Scene** (100-200 words) - Where the body/evidence was found
- **Cause of Death** (50-100 words) - Official medical examiner findings

**Success criteria:**
- ✅ Separate confirmed facts from prosecution theory from defense theory
- ✅ Use medical examiner language, not lay terms (e.g., "asphyxiation" not "strangled")
- ✅ Avoid graphic gratuitous detail—clinical language only
- ✅ Cite autopsy reports, forensic testimony, police reports

**Format for conflicting accounts:**
```markdown
**Prosecution Theory:** [detail] (Source: [testimony/report])
**Defense Theory:** [detail] (Source: [testimony/report])
**Evidence:** [what physical evidence shows]
```

---

#### 6. THE INVESTIGATION (500-800 words)

**Required subsections:**
- **Initial Response** (100-150 words) - Who responded, when, initial actions
- **Key Investigators** (50-100 words) - Lead detectives, agencies involved
- **Breakthrough Moment** (150-250 words) - What cracked the case
- **Evidence Collection** (200-300 words) - Search warrants, forensics, interviews
- **Mistakes or Controversies** (100-150 words) - If applicable

**Success criteria:**
- ✅ Include investigator names and titles
- ✅ Document chain of custody issues (if any)
- ✅ Note any excluded evidence or legal challenges
- ✅ Timeline of investigation milestones

---

#### 7. LEGAL PROCEEDINGS (400-700 words)

**Required subsections:**
- **Arrest** (50-100 words) - Date, location, circumstances
- **Charges Filed** (50-100 words) - Specific charges, jurisdiction
- **Trial** (200-400 words)
  - Dates (start, end)
  - Prosecution strategy & key witnesses
  - Defense strategy & key witnesses
  - Jury selection notes (if notable)
  - Verdict date & outcome
- **Sentencing** (50-100 words) - Date, sentence, judge's statement
- **Appeals** (50-100 words) - Current status, pending appeals

**Success criteria:**
- ✅ Use exact legal charge names (e.g., "Murder in the First Degree," not "murder")
- ✅ Include jury deliberation time
- ✅ Note any hung juries, mistrials, or procedural issues
- ✅ Cite court dockets, verdicts, sentencing transcripts

---

#### 8. PSYCHOLOGY & MOTIVE ANALYSIS (400-600 words)

**Required subsections:**
- **Established Motive** (150-250 words) - What prosecution/evidence showed
- **Psychological Factors** (150-250 words) - Expert analysis from trial or studies
- **Alternative Theories** (100-150 words) - If credible alternatives exist

**Success criteria:**
- ✅ Separate expert opinion from speculation
- ✅ Cite forensic psychologists, criminal profilers, or academic sources
- ✅ Avoid pop psychology—use clinical terms correctly
- ✅ If motive is unclear, state that explicitly

**Example (Good):**
> "Forensic psychologist Dr. [Name], testifying for the prosecution, stated Peterson exhibited traits consistent with narcissistic personality disorder, including lack of empathy and grandiosity. However, no formal diagnosis was made prior to the crime." (Source: Trial transcript, Day 34, p. 2847)

**Example (Bad):**
> "Scott Peterson was clearly a narcissistic sociopath who killed Laci because he wanted freedom."
> ❌ No clinical sourcing  
> ❌ Diagnosed by writer, not expert  
> ❌ Oversimplified motive

---

#### 9. AFTERMATH & CULTURAL IMPACT (200-400 words)
- Media coverage and public reaction
- Changes to law or policy (if any)
- Victim's family advocacy (if applicable)
- Documentaries, books, or media about the case

---

#### 10. SOURCES (Minimum 15)

**Required format:**
```markdown
## SOURCES

### Primary Sources
1. [Court document/transcript] - [Court name, Case #, Date, Page/Section]
2. [Police report] - [Agency, Report #, Date]

### Expert Testimony
3. [Expert name, credentials] - [Trial transcript, Date, Page]

### News & Journalism
4. [Article title] - [Author, Publication, Date, URL]

### Books & Documentaries
5. [Title] - [Author/Director, Year, Publisher/Platform]
```

**Source quality hierarchy (use in order of preference):**
1. **Tier 1:** Court transcripts, police reports, autopsy reports, sworn testimony
2. **Tier 2:** Investigative journalism from major outlets (NYT, WaPo, AP, Reuters, local news with named reporters)
3. **Tier 3:** True crime books by investigative journalists (not "ripped from headlines" pulp)
4. **Tier 4:** Documentaries with producer credits (Dateline, 48 Hours, Netflix Original)
5. **Avoid:** Wikipedia (use its sources instead), forums, true crime blogs, unsourced content

**Success criteria:**
- ✅ Minimum 15 sources cited
- ✅ At least 5 must be Tier 1 (primary sources)
- ✅ Every factual claim in sections 1-8 must have a findable source here
- ✅ Include archived URLs or DOI when available (for link longevity)

---

## QUALITY ASSURANCE CHECKLIST

Before submitting, verify:

- [ ] **Word count:** 3,500-5,500 words total
- [ ] **All 10 sections present** with specified sub-sections
- [ ] **Timeline has 20+ entries** with dates in YYYY-MM-DD format
- [ ] **15+ sources cited** with at least 5 primary sources
- [ ] **No speculation** without labeling it as prosecution/defense theory
- [ ] **No gratuitous violence**—clinical language only
- [ ] **3+ victim quotes** from family/friends
- [ ] **Expert citations** in psychology section
- [ ] **Legal terms accurate** (checked against court documents)
- [ ] **Markdown formatted correctly** (headers, lists, bold/italic)
- [ ] **No broken claims** (if you state a fact, there's a source)

---

## VERIFICATION STEPS

1. **Date Cross-Check:** Run all dates through 2+ sources. Flag conflicts in [brackets].
2. **Legal Accuracy:** Verify charge names, verdict, sentence against official court records.
3. **Expert Credentials:** Confirm all expert witnesses' names, titles, specializations.
4. **Source Accessibility:** Ensure at least 70% of sources are publicly accessible (not paywalled).
5. **Fact Conflicts:** When sources disagree, document both versions with sources cited.

---

## WRITING TONE & STYLE

- **Tense:** Past tense (the case is historical)
- **Voice:** Third-person, objective
- **Tone:** Respectful, clinical, non-sensational
- **Avoid:** 
  - Clichés ("cold-blooded killer," "brutal murder," "shocked the nation")
  - Victim-blaming language
  - Speculation without clear labeling
  - Present tense ("the jury finds him guilty" → "the jury found him guilty")

---

## EDGE CASES

**If information is missing:**
- State explicitly: "[Information not available in public records]"
- Try FOIA requests, court clerk records, news archives
- Do NOT fill gaps with assumptions

**If case is unsolved:**
- Clearly mark "Status: Unsolved" in summary
- Document leading theories with equal weight
- Focus on evidence, not speculation

**If victim is a child:**
- Use extra sensitivity in profile section
- Avoid any details that could re-traumatize family
- Focus on life, not death

**If perpetrator maintains innocence:**
- Present both sides fairly
- Note "convicted of" vs "admitted to"
- Include defense arguments alongside prosecution

---

## EXAMPLE OUTPUT SKELETON

```markdown
# [Case Name]: [Victim Name] Murder

## CASE SUMMARY
[200-300 words]

## TIMELINE
- **YYYY-MM-DD** - [event]
[20-50 entries]

## VICTIM PROFILE
### Early Life & Family Background
[content]
### Education & Career
[content]
[etc.]

## PERPETRATOR PROFILE
[sections]

## THE CRIME
[sections]

## THE INVESTIGATION
[sections]

## LEGAL PROCEEDINGS
[sections]

## PSYCHOLOGY & MOTIVE ANALYSIS
[sections]

## AFTERMATH & CULTURAL IMPACT
[content]

## SOURCES
[15+ sources, formatted]
```

---

## SUCCESS CRITERIA SUMMARY

✅ **Comprehensive:** Answers all questions a reader might have  
✅ **Accurate:** Every fact is sourced and verifiable  
✅ **Balanced:** Presents all perspectives fairly  
✅ **Readable:** Flows narratively while maintaining objectivity  
✅ **Respectful:** Honors victim's humanity, avoids sensationalism  
✅ **Complete:** 3,500-5,500 words with all 10 sections  
✅ **Publication-ready:** A writer can use this to draft a book chapter  

---

*This document will serve as the foundation for Books 2-10. Consistency is critical.*
