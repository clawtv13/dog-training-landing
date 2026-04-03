# 📹 Book Trailer Generator - Complete Architecture

**Purpose:** Generate viral short-form video prompts for Mind Crimes book trailers  
**Platforms:** TikTok (60s), Instagram Reels (90s), YouTube Shorts (60s)  
**Goal:** Drive Amazon KDP sales via platform-native viral content  
**Status:** PLANNING ONLY - Architecture Document  
**Created:** 2026-04-03

---

## 🔍 Analysis: Existing Generator (Dog Training)

### What Works (Transfer to True Crime)
| Component | Dog Training | Transfer Value |
|-----------|-------------|----------------|
| Formula system | 6 formulas with retention % | ✅ Core pattern - adapt formulas |
| Auto-topic selection | Keywords file → cooldown | ✅ Adapt to books/cases |
| State tracking | JSON with timestamps | ✅ Direct reuse |
| OpenRouter integration | Claude Sonnet generation | ✅ Direct reuse |
| Telegram delivery | Bot + chat ID | ✅ Direct reuse |
| CLI interface | argparse, flags | ✅ Direct reuse |

### What Must Change
| Component | Dog Training | True Crime Need |
|-----------|-------------|-----------------|
| Formulas | Educational/training | Narrative/suspense/crime |
| Content source | KEYWORDS-V2-EXPANSION.md | Book metadata + research.md |
| Topic matching | Keyword → formula | Case type → best formula |
| Compliance | Minimal | Heavy (victim respect, no gore) |
| Platform variation | Single format (Shorts) | TikTok/IG/YouTube distinct |
| CTA | "Follow for tips" | "Link in bio → Amazon" |
| Hashtags | Dog training niche | True crime ecosystem |

---

## 🎬 6 True Crime Formulas

### Formula 1: NEWS_HOOK
**Best For:** Recently solved cold cases, current arrests, DNA breakthroughs  
**Retention Target:** 88%  
**Use When:** Book features recent news (2020+ arrest/resolution)

```yaml
name: "News Hook"
retention: 88
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-3s):
    hook_type: "Breaking news pattern interrupt"
    text: "🚨 After [X] YEARS, police finally arrested..."
    visual: "Urgent graphic, red/black color scheme, news ticker aesthetic"
    audio: "News sting sound, then silence"
    
  SCENE_2 (3-15s):
    purpose: "The original crime"
    text: "In [YEAR], [victim] was found [grim detail - tasteful]"
    visual: "Aged photo texture, newspaper clippings, slow zoom"
    pacing: "Slow, ominous"
    
  SCENE_3 (15-35s):
    purpose: "Years of mystery"
    text: "For [X] years, the killer walked free..."
    visual: "Timeline montage, calendar pages, seasons changing"
    build: "Frustration, injustice"
    
  SCENE_4 (35-52s):
    purpose: "The breakthrough"
    text: "Until [breakthrough method] revealed..."
    visual: "DNA helix, evidence closeup, courtroom"
    pacing: "Accelerating, revelation"
    
  SCENE_5 (52-60s):
    purpose: "CTA"
    text: "The full story 👆 link in bio"
    visual: "Book cover reveal, Amazon branding"
    audio: "Suspenseful resolve"

best_cases:
  - "The Killer Clown (2017 arrest after 27 years)"
  - Any case with DNA genealogy breakthrough
  - Cases with recent media coverage
```

### Formula 2: EVIDENCE_REVEAL
**Best For:** Unique forensic methods, unusual evidence, scientific angles  
**Retention Target:** 85%  
**Use When:** Case has fascinating forensic element

```yaml
name: "Evidence Reveal"
retention: 85
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-3s):
    hook_type: "Mystery object"
    text: "This [evidence item] solved a murder 20 years later"
    visual: "Closeup of mysterious evidence (wig, fiber, stamp)"
    audio: "Suspense sting"
    
  SCENE_2 (3-12s):
    purpose: "The crime"
    text: "[Year]. [Location]. A brutal murder with no witnesses."
    visual: "Crime scene tape, forensic photography aesthetic"
    pacing: "Slow, procedural"
    
  SCENE_3 (12-25s):
    purpose: "Why it went cold"
    text: "Detectives found [evidence] but couldn't connect it to anyone."
    visual: "Evidence bag, frustrated detective trope, cold case files"
    
  SCENE_4 (25-50s):
    purpose: "The science"
    text: "Then [forensic technique] did what detectives couldn't..."
    visual: "Lab equipment, DNA visualization, computer analysis"
    pacing: "Educational but fast"
    reveal: "Show connection being made"
    
  SCENE_5 (50-60s):
    purpose: "CTA"
    text: "The full investigation 👆"
    visual: "Book cover, forensic overlay"

best_cases:
  - Cases with DNA genealogy
  - Fiber evidence (Killer Clown orange wig)
  - Digital forensics breakthroughs
  - Bite mark/tool mark analysis
```

### Formula 3: VILLAIN_REVEAL
**Best For:** Betrayal cases, partner murders, "hiding in plain sight"  
**Retention Target:** 90% (highest - betrayal is compelling)  
**Use When:** Killer was spouse, family member, or trusted person

```yaml
name: "Villain Reveal"
retention: 90
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-4s):
    hook_type: "Shocking reveal teaser"
    text: "The killer attended the victim's funeral... and married their spouse."
    visual: "Dark silhouette, wedding photo overlay"
    audio: "Dark ambient, heartbeat"
    
  SCENE_2 (4-15s):
    purpose: "Happy before"
    text: "[Victim] thought they had the perfect life..."
    visual: "Family photos, warm lighting (will contrast later)"
    tone: "Nostalgic, warm - creates contrast"
    
  SCENE_3 (15-30s):
    purpose: "The murder"
    text: "Then on [date], a clown knocked on her door."
    visual: "Door opening, shadow, balloons"
    pacing: "Sudden shift to dark"
    
  SCENE_4 (30-50s):
    purpose: "The betrayal"
    text: "While police searched for a stranger... the killer was [relationship]."
    visual: "Split screen: investigation vs. killer's normal life"
    reveal: "Gradual unmasking"
    
  SCENE_5 (50-60s):
    purpose: "CTA + hook"
    text: "How did they hide for 27 years? 👆"
    visual: "Book cover, question overlay"

best_cases:
  - Killer Clown (affair, married victim's husband)
  - Family annihilators
  - Partner poison cases
  - Insurance murder schemes
```

### Formula 4: VICTIM_STORY
**Best For:** Emotional impact, humanizing victims, justice angle  
**Retention Target:** 78%  
**Use When:** Victim story is compelling, audience needs emotional investment

```yaml
name: "Victim Story"
retention: 78
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-5s):
    hook_type: "Humanizing moment"
    text: "[Victim name] had just [normal human moment] when..."
    visual: "Warm photo of victim in happier times"
    audio: "Soft piano, then shift"
    
  SCENE_2 (5-20s):
    purpose: "Who they were"
    text: "She was a mother, a friend, a dreamer who..."
    visual: "Photo montage, quotes from family"
    tone: "Respectful, humanizing"
    
  SCENE_3 (20-35s):
    purpose: "The crime (tasteful)"
    text: "On [date], someone took her future."
    visual: "Candles, memorial imagery, NOT crime scene"
    pacing: "Slow, reverent"
    
  SCENE_4 (35-52s):
    purpose: "The fight for justice"
    text: "Her family never stopped fighting..."
    visual: "Advocacy, court proceedings, persistence"
    
  SCENE_5 (52-60s):
    purpose: "CTA"
    text: "Her story deserves to be told 👆"
    visual: "Book cover, victim-centered framing"

best_cases:
  - Cases where victim had strong community
  - Cases where family fought for justice
  - Lesser-known victims of famous cases

compliance_notes:
  - CRITICAL: No victim photos without implicit consent context
  - Focus on life, not death
  - No graphic crime details
  - Family would approve this framing
```

### Formula 5: SCIENCE_ANGLE
**Best For:** DNA genealogy, forensic technology, "how science caught them"  
**Retention Target:** 82%  
**Use When:** Book features heavy forensic/scientific elements

```yaml
name: "Science Angle"
retention: 82
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-3s):
    hook_type: "Science fact"
    text: "DNA from a family tree website caught a killer."
    visual: "DNA helix, ancestry interface"
    audio: "Tech/science sound design"
    
  SCENE_2 (3-15s):
    purpose: "The unsolvable case"
    text: "[Year]: A perfect crime. No witnesses. No DNA match."
    visual: "Cold case file aesthetic, frustrated investigators"
    
  SCENE_3 (15-30s):
    purpose: "The technology gap"
    text: "For [X] years, science couldn't help."
    visual: "Old lab equipment → modern lab transition"
    
  SCENE_4 (30-50s):
    purpose: "The breakthrough"
    text: "Then [technology] did what humans couldn't..."
    visual: "Computer screens, family tree visualization, match highlight"
    pacing: "Educational but exciting"
    key_info: "Explain the science simply"
    
  SCENE_5 (50-60s):
    purpose: "CTA"
    text: "The science that solved it 👆"
    visual: "Book cover with DNA/science overlay"

best_cases:
  - Golden State Killer (genealogy)
  - Killer Clown (DNA from wig)
  - Any case with forensic breakthrough
```

### Formula 6: COMPARISON_HOOK
**Best For:** Lesser-known cases with famous parallels  
**Retention Target:** 86%  
**Use When:** Case resembles famous case but is less known

```yaml
name: "Comparison Hook"
retention: 86
scene_count: 5
duration: 60s

structure:
  SCENE_1 (0-3s):
    hook_type: "Famous comparison"
    text: "Everyone knows Ted Bundy. Nobody knows [killer name]."
    visual: "Split screen: famous killer → lesser known"
    audio: "Dramatic sting"
    
  SCENE_2 (3-15s):
    purpose: "The famous case (brief)"
    text: "[Famous killer] killed [X] people and became infamous."
    visual: "News clips, documentary aesthetic"
    pacing: "Fast, familiar territory"
    
  SCENE_3 (15-35s):
    purpose: "The unknown case"
    text: "But in [location], someone else used the SAME methods..."
    visual: "Map transition, new location, parallels shown"
    
  SCENE_4 (35-52s):
    purpose: "Why this case matters"
    text: "And nobody talks about it."
    visual: "Victim photos, case details, urgency"
    
  SCENE_5 (52-60s):
    purpose: "CTA"
    text: "The case you've never heard 👆"
    visual: "Book cover, comparison overlay"

best_cases:
  - Regional serial killers
  - Cases similar to Netflix documentaries
  - "Florida's [Famous Killer]" angles

compliance_notes:
  - Don't glorify either killer
  - Frame as "understanding evil" not "celebrating evil"
  - Victim-centered comparison when possible
```

---

## 📱 Platform-Specific Optimization

### TikTok (Primary)
```yaml
platform: "tiktok"
max_duration: 60s
optimal_duration: 45-55s
aspect_ratio: "9:16"

hooks:
  mandatory: true
  timing: "0-3s CRITICAL"
  style: "Pattern interrupt, shocking fact, or question"
  
audio:
  mandatory: "trending sound"
  strategy: "Use sound EARLY (first 2s) for For You Page boost"
  fallback: "Original audio with text-to-speech"
  
pacing:
  cuts_per_second: 2-3
  scene_avg: "8-12s max"
  style: "Fast, punchy, no dead air"
  
text_overlays:
  font: "Bold, high contrast"
  position: "Center or top-third"
  max_words_per_screen: 8
  
hashtags:
  total: 5-7
  viral: 2  # e.g., #foryou #fyp
  niche: 3  # e.g., #truecrime #coldcase #crimestories
  book: 1  # #mindcrimes
  trending: 1  # Check current trends
  
cta:
  style: "Link in bio → Amazon"
  placement: "Final 3 seconds + pinned comment"
  
compliance:
  - No graphic violence
  - No real crime scene photos
  - No killer glorification
  - Age-restrict if borderline
```

### Instagram Reels
```yaml
platform: "instagram"
max_duration: 90s
optimal_duration: 60-75s
aspect_ratio: "9:16"

hooks:
  mandatory: true
  timing: "0-3s"
  style: "Polished, cinematic opening"
  
audio:
  trending: "Use IG's trending audio tab"
  original: "More accepted than TikTok"
  voiceover: "Higher quality expected"
  
pacing:
  cuts_per_second: 1-2
  scene_avg: "10-15s"
  style: "More polished, less chaotic"
  
aesthetic:
  filter: "Consistent color grade"
  graphics: "Clean, minimalist"
  text: "Sans-serif, elegant"
  
hashtags:
  total: 10-15
  placement: "First comment, not caption"
  viral: 3  # #reels #explore
  niche: 7  # #truecrimecommunity #truecrimejunkie
  book: 2  # #mindcrimes #truecrimebooks
  trending: 3
  
cta:
  style: "Link in bio"
  pinned_comment: "📚 Full story → Amazon link in bio"
  
carousel_option:
  use_when: "Evidence-heavy stories"
  slides: 5-7
  final_slide: "Book CTA"
```

### YouTube Shorts
```yaml
platform: "youtube"
max_duration: 60s
optimal_duration: 50-58s
aspect_ratio: "9:16"

hooks:
  mandatory: true
  timing: "0-3s"
  style: "Question or dramatic statement"
  
audio:
  original: "Preferred (copyright safe)"
  voiceover: "High quality TTS or real voice"
  music: "Royalty-free only"
  
pacing:
  cuts_per_second: 1-2
  scene_avg: "10-15s"
  style: "Can breathe more, YouTube audience tolerates"
  
description:
  seo_optimized: true
  structure: |
    [HOOK - First line visible in mobile]
    
    The full story of [case] is available now on Amazon.
    
    🔗 Get the book: [Amazon link]
    
    #truecrime #coldcase #murdermystery #forensics
    
    CHAPTERS:
    0:00 - Hook
    0:05 - The crime
    0:20 - The investigation
    0:45 - The breakthrough
    
title:
  max_length: 70
  structure: "[HOOK] | [Case Name] #shorts"
  example: "The Killer Wore a Clown Costume... | True Crime #shorts"
  
hashtags:
  in_description: true
  total: 5
  mandatory: "#shorts"
  niche: 3  # #truecrime #coldcase
  
cta:
  end_screen: false  # Not available for Shorts
  pinned_comment: "📚 Full book available on Amazon: [link]"
  description: "Link in description"
```

---

## 🎯 Book-Formula Auto-Matching Algorithm

```python
def match_book_to_formula(book_metadata: dict) -> str:
    """
    Match book metadata to optimal formula.
    
    Priority order based on viral potential:
    1. VILLAIN_REVEAL (90% retention) - betrayal stories
    2. NEWS_HOOK (88%) - recent arrests
    3. COMPARISON_HOOK (86%) - famous parallels
    4. EVIDENCE_REVEAL (85%) - unique forensics
    5. SCIENCE_ANGLE (82%) - DNA/tech heavy
    6. VICTIM_STORY (78%) - emotional focus
    """
    
    # Extract signals from metadata
    case_type = book_metadata.get('case_type', '')
    killer_relationship = book_metadata.get('killer_relationship', '')
    resolution_year = book_metadata.get('resolution_year', 0)
    forensic_method = book_metadata.get('forensic_method', '')
    famous_comparison = book_metadata.get('famous_comparison', '')
    years_unsolved = book_metadata.get('years_unsolved', 0)
    
    # Decision tree (ordered by viral potential)
    
    # 1. VILLAIN_REVEAL - Betrayal cases (highest retention)
    betrayal_keywords = ['spouse', 'partner', 'affair', 'husband', 'wife', 
                         'family', 'friend', 'trusted', 'neighbor']
    if any(kw in killer_relationship.lower() for kw in betrayal_keywords):
        return 'villain_reveal'
    
    # 2. NEWS_HOOK - Recent arrests (news cycle leverage)
    if resolution_year and resolution_year >= 2015:
        if years_unsolved and years_unsolved >= 10:
            return 'news_hook'
    
    # 3. COMPARISON_HOOK - Famous parallels (algorithm boost)
    if famous_comparison:
        return 'comparison_hook'
    
    # 4. EVIDENCE_REVEAL - Unique forensics
    unique_evidence = ['wig', 'fiber', 'bite mark', 'digital', 'phone',
                       'surveillance', 'dna', 'genealogy', 'fingerprint']
    if any(ev in forensic_method.lower() for ev in unique_evidence):
        return 'evidence_reveal'
    
    # 5. SCIENCE_ANGLE - DNA/genealogy heavy
    science_keywords = ['dna genealogy', 'familial dna', 'genetic', 
                        'gedmatch', '23andme', 'ancestry']
    if any(kw in forensic_method.lower() for kw in science_keywords):
        return 'science_angle'
    
    # 6. VICTIM_STORY - Default for emotional cases
    return 'victim_story'


def extract_book_metadata(research_file: str) -> dict:
    """
    Parse research.md file to extract metadata for formula matching.
    
    Extracts:
    - case_type: murder, serial, cold_case, etc.
    - killer_relationship: spouse, stranger, family, etc.
    - resolution_year: year case was solved
    - forensic_method: DNA, fingerprint, witness, etc.
    - famous_comparison: similar famous case if any
    - years_unsolved: time between crime and resolution
    - victim_name: for humanizing
    - location: for regional interest
    """
    
    # Read research file
    with open(research_file) as f:
        content = f.read().lower()
    
    metadata = {
        'case_type': 'cold_case',  # default
        'killer_relationship': 'unknown',
        'resolution_year': None,
        'forensic_method': '',
        'famous_comparison': '',
        'years_unsolved': 0,
        'victim_name': '',
        'location': ''
    }
    
    # Extract relationship (look for patterns)
    relationship_patterns = [
        (r'affair|mistress|lover', 'affair'),
        (r'husband|wife|spouse', 'spouse'),
        (r'neighbor', 'neighbor'),
        (r'family|brother|sister|parent', 'family'),
        (r'friend|roommate', 'friend'),
        (r'stranger|unknown', 'stranger')
    ]
    for pattern, rel in relationship_patterns:
        if re.search(pattern, content):
            metadata['killer_relationship'] = rel
            break
    
    # Extract years (look for timeline)
    crime_year = re.search(r'(\d{4}).*(?:murder|crime|death)', content)
    solve_year = re.search(r'(?:arrest|solve|convict).*(\d{4})', content)
    
    if solve_year:
        metadata['resolution_year'] = int(solve_year.group(1))
    if crime_year and solve_year:
        metadata['years_unsolved'] = int(solve_year.group(1)) - int(crime_year.group(1))
    
    # Extract forensic method
    forensic_patterns = ['dna genealogy', 'familial dna', 'dna', 'fingerprint',
                         'fiber', 'hair', 'surveillance', 'phone records']
    for pattern in forensic_patterns:
        if pattern in content:
            metadata['forensic_method'] = pattern
            break
    
    return metadata
```

---

## ⚠️ Compliance & Safety Filters

### Content Filters
```yaml
prohibited_content:
  - graphic_violence: "No blood, wounds, or crime scene gore"
  - crime_scene_photos: "Never use actual crime scene images"
  - victim_autopsy: "No medical examiner content"
  - killer_celebration: "No 'cool killer' framing"
  - victim_mockery: "Respectful at all times"
  - minor_victims: "Extra caution, parental framing only"
  - ongoing_cases: "No speculation on active investigations"

required_filters:
  victim_respect:
    - "Always use victim's name respectfully"
    - "Frame as 'life cut short' not 'interesting murder'"
    - "Show victims in life, not death"
    - "Family-approved framing test: would family object?"
    
  killer_framing:
    - "Villain, not antihero"
    - "Focus on justice, not infamy"
    - "No nicknames that glamorize (unless widely known)"
    - "Show consequences: prison, conviction"
    
  age_gating:
    tiktok: "If borderline, add age restriction"
    youtube: "Mature content flag if needed"
    instagram: "Avoid graphic text overlays"

platform_guidelines:
  tiktok:
    - "No detailed crime methods"
    - "No celebration of violence"
    - "No harassment of families"
    - "Age-restrict true crime content"
    
  instagram:
    - "No graphic violence imagery"
    - "No self-harm/suicide detail"
    - "Sensitive content warnings"
    
  youtube:
    - "No monetization on graphic content"
    - "Age-restrict appropriately"
    - "No misleading thumbnails"
```

### Compliance Validation Function
```python
def validate_prompt_compliance(prompt: str) -> tuple[bool, list]:
    """
    Check prompt for compliance issues before generation.
    Returns (is_compliant, issues_list)
    """
    issues = []
    
    # Prohibited phrases
    prohibited = [
        'blood', 'gore', 'graphic', 'autopsy', 'mutilat',
        'torture detail', 'sexual assault detail',
        'celebrate', 'iconic killer', 'legend'
    ]
    
    for term in prohibited:
        if term in prompt.lower():
            issues.append(f"Prohibited term: {term}")
    
    # Required elements
    required = ['victim', 'justice']
    for term in required:
        if term not in prompt.lower():
            issues.append(f"Missing required framing: {term}")
    
    # Killer glorification check
    glorifying = ['genius', 'mastermind', 'brilliant', 'legend', 'icon']
    for term in glorifying:
        if term in prompt.lower() and 'not' not in prompt.lower():
            issues.append(f"Potential glorification: {term}")
    
    return (len(issues) == 0, issues)
```

---

## 🧠 Intelligence Features

### 1. Hashtag Optimizer
```python
def optimize_hashtags(platform: str, case_type: str, book_title: str) -> list:
    """
    Generate optimal hashtag mix per platform.
    Strategy: 30% viral + 50% niche + 20% branded
    """
    
    # Platform-specific viral tags
    viral_tags = {
        'tiktok': ['#fyp', '#foryou', '#viral', '#storytime'],
        'instagram': ['#reels', '#explore', '#trending'],
        'youtube': ['#shorts']
    }
    
    # True crime niche tags (high engagement communities)
    niche_tags = {
        'general': ['#truecrime', '#truecrimecommunity', '#crimejunkie',
                    '#murderino', '#truecrimepodcast', '#crimetok'],
        'cold_case': ['#coldcase', '#unsolvedmysteries', '#coldcasefiles'],
        'dna': ['#dna', '#forensics', '#geneticgenealogy', '#coldcasesolved'],
        'serial': ['#serialkiller', '#serialkillers', '#criminalminds']
    }
    
    # Branded tags
    brand_tags = ['#mindcrimes', '#mindcrimesbooks']
    
    # Build hashtag set
    result = []
    result.extend(random.sample(viral_tags.get(platform, []), 2))
    result.extend(random.sample(niche_tags['general'], 3))
    result.extend(random.sample(niche_tags.get(case_type, niche_tags['general']), 2))
    result.extend(brand_tags[:1])
    
    # Platform limits
    limits = {'tiktok': 7, 'instagram': 15, 'youtube': 5}
    return result[:limits.get(platform, 7)]
```

### 2. Title Generator
```python
def generate_titles(book_metadata: dict, platform: str) -> list:
    """
    Generate 5 title variations per platform.
    """
    
    templates = {
        'tiktok': [
            "The {detail} that solved a {years}-year-old murder",
            "Nobody believed her until the DNA came back...",
            "This {relationship} killed {victim}. Here's how they caught them.",
            "🚨 SOLVED: {case_name} after {years} years",
            "The killer was at the funeral..."
        ],
        'instagram': [
            "After {years} years, justice finally came.",
            "The {case_name}: A story of betrayal and justice.",
            "How {forensic_method} solved the unsolvable.",
            "{victim}'s story needed to be told. 📚",
            "They thought they got away with it..."
        ],
        'youtube': [
            "The {case_name} Murder Explained | True Crime #shorts",
            "How They Finally Caught the {killer_type} | #shorts",
            "{years} Years Later: The {case_name} Solved #shorts",
            "The Evidence That Changed Everything | #shorts",
            "True Crime: {victim}'s Story #shorts"
        ]
    }
    
    return [t.format(**book_metadata) for t in templates.get(platform, templates['tiktok'])]
```

### 3. Description Generator
```python
def generate_description(book_metadata: dict, platform: str) -> str:
    """
    Generate SEO-optimized, engagement-focused descriptions.
    """
    
    if platform == 'youtube':
        return f"""
{book_metadata['hook_line']}

The full story of {book_metadata['case_name']} is now available on Amazon.

🔗 Get the book: {book_metadata['amazon_link']}

This case was unsolved for {book_metadata['years_unsolved']} years until {book_metadata['forensic_method']} changed everything.

#truecrime #coldcase #murdermystery #shorts

CHAPTERS:
0:00 - The hook
0:05 - The crime  
0:20 - The investigation
0:45 - The breakthrough
"""
    
    elif platform == 'instagram':
        return f"""
{book_metadata['hook_line']}

📚 Full story → link in bio

{book_metadata['one_sentence_summary']}
"""
    
    else:  # tiktok
        return f"""
{book_metadata['hook_line']} 📚 Full story on Amazon (link in bio) #truecrime #coldcase
"""
```

### 4. Book Context Extractor
```python
def extract_book_context(research_file: str) -> dict:
    """
    Extract key storytelling elements from research.md files.
    
    Returns structured context for prompt generation.
    """
    
    context = {
        'victim_name': '',
        'killer_name': '',
        'location': '',
        'date': '',
        'years_unsolved': 0,
        'hook_detail': '',  # Most compelling single detail
        'relationship': '',
        'forensic_breakthrough': '',
        'one_sentence': '',  # Elevator pitch
        'emotional_angle': '',
        'key_scenes': []  # For scene-by-scene prompts
    }
    
    # Parse research file
    with open(research_file) as f:
        content = f.read()
    
    # Extract structured data (regex patterns)
    # ... implementation details
    
    # Build one-sentence hook
    context['one_sentence'] = (
        f"{context['victim_name']} was murdered in {context['location']} "
        f"in {context['date']}. {context['years_unsolved']} years later, "
        f"{context['forensic_breakthrough']} finally revealed the truth."
    )
    
    return context
```

---

## 📁 File Structure

```
/root/.openclaw/workspace/
├── scripts/
│   └── book-trailer-generator.py          # Main generator script
│
├── data/
│   ├── formulas.yaml                       # 6 true crime formulas
│   ├── scenes.yaml                         # Scene templates per formula
│   ├── hashtags.yaml                       # Platform hashtag strategies
│   ├── book-formula-mapping.yaml           # Book → formula matching rules
│   └── compliance-filters.yaml             # Prohibited content list
│
├── .state/
│   └── trailers-generated.json             # Tracking: which books, which formulas
│
├── content/mind-crimes/
│   ├── TOPICS-DATABASE.md                  # Case ideas
│   ├── [book-name]-RESEARCH.md             # Research files per book
│   └── topics-used.json                    # Rotation tracking
│
└── kdp-launch/
    └── BOOK-*-DESCRIPTION.md               # Book metadata source
```

---

## 🔧 Code Structure Outline

```python
#!/usr/bin/env python3
"""
Book Trailer Generator for Mind Crimes
Generates viral short-form video prompts for TikTok, IG Reels, YouTube Shorts
"""

# === IMPORTS ===
import requests
import json
import yaml
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# === CONFIG ===
WORKSPACE = Path("/root/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data"
STATE_FILE = WORKSPACE / ".state/trailers-generated.json"
BOOKS_DIR = WORKSPACE / "content/mind-crimes"
KDP_DIR = WORKSPACE / "kdp-launch"

OPENROUTER_KEY = "sk-or-v1-..."
TELEGRAM_BOT = "..."
TELEGRAM_CHAT = "..."

# === DATA LOADING ===
def load_formulas() -> Dict:
    """Load formula definitions from YAML"""
    with open(DATA_DIR / "formulas.yaml") as f:
        return yaml.safe_load(f)

def load_hashtags() -> Dict:
    """Load hashtag strategies"""
    with open(DATA_DIR / "hashtags.yaml") as f:
        return yaml.safe_load(f)

def load_compliance() -> Dict:
    """Load compliance filters"""
    with open(DATA_DIR / "compliance-filters.yaml") as f:
        return yaml.safe_load(f)

def load_state() -> List:
    """Load generation history"""
    if not STATE_FILE.exists():
        return []
    with open(STATE_FILE) as f:
        return json.load(f)

# === BOOK DISCOVERY ===
def discover_books() -> List[Dict]:
    """Find all available books with metadata"""
    books = []
    for research_file in BOOKS_DIR.glob("*-RESEARCH.md"):
        book_name = research_file.stem.replace("-RESEARCH", "")
        metadata = extract_book_metadata(research_file)
        
        # Try to find matching KDP description
        desc_file = KDP_DIR / f"BOOK-*-DESCRIPTION.md"
        
        books.append({
            'name': book_name,
            'research_file': research_file,
            'metadata': metadata
        })
    return books

def select_book(books: List[Dict], force_book: Optional[str] = None) -> Dict:
    """Select next book (respects cooldown, rotation)"""
    if force_book:
        return next(b for b in books if force_book in b['name'].lower())
    
    state = load_state()
    cooldown_date = datetime.now() - timedelta(days=7)
    
    used_recent = {
        entry['book'] for entry in state
        if datetime.fromisoformat(entry['generated_at']) > cooldown_date
    }
    
    available = [b for b in books if b['name'] not in used_recent]
    return available[0] if available else books[0]

# === FORMULA MATCHING ===
def extract_book_metadata(research_file: Path) -> Dict:
    """Parse research file for metadata"""
    # ... implementation per algorithm above
    pass

def match_book_to_formula(metadata: Dict) -> str:
    """Apply matching algorithm"""
    # ... implementation per algorithm above
    pass

# === PROMPT GENERATION ===
def generate_trailer_prompt(
    book: Dict, 
    formula_key: str, 
    platform: str
) -> str:
    """Generate video prompt via OpenRouter"""
    
    formula = load_formulas()[formula_key]
    platform_config = get_platform_config(platform)
    book_context = extract_book_context(book['research_file'])
    
    system_prompt = build_system_prompt(formula, platform_config, book_context)
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "anthropic/claude-sonnet-4.5",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate {platform} trailer for: {book['name']}"}
            ],
            "temperature": 0.8
        }
    )
    
    return response.json()['choices'][0]['message']['content']

def build_system_prompt(formula: Dict, platform: Dict, context: Dict) -> str:
    """Build comprehensive system prompt for generation"""
    
    return f"""You are a viral true crime short-form video expert.

FORMULA: {formula['name']}
PLATFORM: {platform['name']} ({platform['duration']}s max)
RETENTION TARGET: {formula['retention']}%

BOOK CONTEXT:
- Victim: {context['victim_name']}
- Location: {context['location']}
- Years unsolved: {context['years_unsolved']}
- Key detail: {context['hook_detail']}
- Forensic method: {context['forensic_breakthrough']}

FORMULA STRUCTURE:
{formula['structure']}

PLATFORM REQUIREMENTS:
{platform['requirements']}

COMPLIANCE (CRITICAL):
- NO graphic violence or gore
- Victim-respectful framing only
- No killer glorification
- Family-approval test: Would victim's family object?

OUTPUT FORMAT:
1. Hook (first line that appears in feed)
2. Scene-by-scene breakdown with exact timing
3. Text overlay suggestions per scene
4. Audio/music recommendations
5. Hashtags ({platform['hashtag_count']})
6. Title
7. Description
8. Pinned comment CTA

CTA: Always drive to "link in bio" for Amazon purchase."""

# === PLATFORM VARIATIONS ===
def generate_all_platforms(book: Dict, formula_key: str) -> Dict[str, str]:
    """Generate prompts for all 3 platforms"""
    platforms = ['tiktok', 'instagram', 'youtube']
    results = {}
    
    for platform in platforms:
        results[platform] = generate_trailer_prompt(book, formula_key, platform)
    
    return results

def get_platform_config(platform: str) -> Dict:
    """Get platform-specific settings"""
    configs = {
        'tiktok': {
            'name': 'TikTok',
            'duration': 60,
            'hashtag_count': 7,
            'requirements': """
- 60 seconds MAX (optimal: 45-55s)
- FAST cuts (2-3 per second)
- Trending audio MANDATORY
- Hook in first 3s CRITICAL
- Text: 8 words max per screen
- Hashtags: #fyp #truecrime #coldcase
"""
        },
        'instagram': {
            'name': 'Instagram Reels',
            'duration': 90,
            'hashtag_count': 15,
            'requirements': """
- 90 seconds MAX (optimal: 60-75s)
- Polished, cinematic aesthetic
- Can use original audio
- Hook in first 3s
- Clean text overlays (sans-serif)
- Hashtags in first comment
"""
        },
        'youtube': {
            'name': 'YouTube Shorts',
            'duration': 60,
            'hashtag_count': 5,
            'requirements': """
- 60 seconds MAX (optimal: 50-58s)
- Can breathe more (1-2 cuts/sec)
- Original audio preferred (copyright safe)
- SEO-optimized description with chapters
- #shorts MANDATORY
- Pinned comment with Amazon link
"""
        }
    }
    return configs[platform]

# === COMPLIANCE ===
def validate_compliance(prompt: str) -> Tuple[bool, List[str]]:
    """Check prompt against compliance filters"""
    # ... implementation per compliance section
    pass

# === INTELLIGENCE ===
def generate_hashtags(platform: str, metadata: Dict) -> List[str]:
    """Generate optimized hashtag mix"""
    # ... implementation per intelligence section
    pass

def generate_titles(metadata: Dict, platform: str) -> List[str]:
    """Generate 5 title options"""
    # ... implementation per intelligence section
    pass

def generate_description(metadata: Dict, platform: str) -> str:
    """Generate SEO description"""
    # ... implementation per intelligence section
    pass

# === STATE MANAGEMENT ===
def save_state(book_name: str, formula: str, platforms: List[str]):
    """Track generated trailers"""
    state = load_state()
    state.append({
        'book': book_name,
        'formula': formula,
        'platforms': platforms,
        'generated_at': datetime.now().isoformat()
    })
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# === OUTPUT ===
def send_telegram(message: str):
    """Deliver prompt via Telegram"""
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT,
            "text": message,
            "parse_mode": "Markdown"
        }
    )

def format_output(book: Dict, formula: str, results: Dict) -> str:
    """Format results for Telegram delivery"""
    output = f"""
📹 **BOOK TRAILER PROMPTS**

📚 **Book:** {book['name']}
🎯 **Formula:** {formula}
📊 **Est. Retention:** {load_formulas()[formula]['retention']}%

---

**TIKTOK (60s):**
{results['tiktok']}

---

**INSTAGRAM REELS (90s):**
{results['instagram']}

---

**YOUTUBE SHORTS (60s):**
{results['youtube']}

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
"""
    return output

# === CLI ===
def main():
    parser = argparse.ArgumentParser(description="Generate book trailer prompts")
    parser.add_argument("--book", help="Force specific book")
    parser.add_argument("--formula", choices=[
        'news_hook', 'evidence_reveal', 'villain_reveal',
        'victim_story', 'science_angle', 'comparison_hook'
    ], help="Force formula (default: auto-match)")
    parser.add_argument("--platform", choices=['tiktok', 'instagram', 'youtube', 'all'],
                        default='all', help="Target platform")
    parser.add_argument("--list-books", action="store_true")
    parser.add_argument("--list-formulas", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Don't save state")
    
    args = parser.parse_args()
    
    if args.list_formulas:
        formulas = load_formulas()
        for key, formula in formulas.items():
            print(f"{key}: {formula['name']} ({formula['retention']}%)")
        return
    
    if args.list_books:
        books = discover_books()
        for book in books:
            print(f"- {book['name']}")
        return
    
    # Main flow
    books = discover_books()
    book = select_book(books, args.book)
    
    formula = args.formula or match_book_to_formula(book['metadata'])
    
    if args.platform == 'all':
        results = generate_all_platforms(book, formula)
    else:
        results = {args.platform: generate_trailer_prompt(book, formula, args.platform)}
    
    output = format_output(book, formula, results)
    print(output)
    
    send_telegram(output)
    
    if not args.dry_run:
        save_state(book['name'], formula, list(results.keys()))

if __name__ == "__main__":
    main()
```

---

## 📦 Dependencies

```txt
# requirements.txt
requests>=2.31.0
pyyaml>=6.0.1
```

**No additional dependencies needed** - script uses stdlib + 2 common packages already in environment.

---

## 💻 Usage Examples

```bash
# Auto-select book and formula, generate for all platforms
python3 book-trailer-generator.py

# Specific book
python3 book-trailer-generator.py --book "killer-clown"

# Force formula
python3 book-trailer-generator.py --book "killer-clown" --formula villain_reveal

# Single platform
python3 book-trailer-generator.py --book "killer-clown" --platform tiktok

# Preview without saving state
python3 book-trailer-generator.py --dry-run

# List available
python3 book-trailer-generator.py --list-books
python3 book-trailer-generator.py --list-formulas
```

**Cron Example (daily prompt generation):**
```bash
# Generate trailer prompt every day at 10:00 UTC
0 10 * * * /usr/bin/python3 /root/.openclaw/workspace/scripts/book-trailer-generator.py >> /var/log/book-trailer.log 2>&1
```

---

## ⏱️ Build Phase Time Estimate

| Component | Time |
|-----------|------|
| Main script structure | 30 min |
| Formula YAML definitions | 45 min |
| Book metadata extraction | 30 min |
| Platform config + hashtags | 20 min |
| Compliance filters | 15 min |
| OpenRouter prompt engineering | 45 min |
| Telegram integration | 10 min |
| Testing with Killer Clown | 30 min |
| Documentation | 15 min |
| **TOTAL** | **~4 hours** |

**Fast-track option:** Reuse more from dog training generator = **2.5 hours**

---

## ✅ Next Steps (Build Phase)

1. Create `data/formulas.yaml` with all 6 formulas
2. Create `data/hashtags.yaml` with platform strategies
3. Create `data/compliance-filters.yaml`
4. Build `book-trailer-generator.py`
5. Test with "The Killer Clown" book
6. Verify Telegram delivery
7. Run first generation batch

---

**Architecture complete. Ready for build phase on approval.**
