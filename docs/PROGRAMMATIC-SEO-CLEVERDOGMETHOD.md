# Programmatic SEO Strategy: CleverDogMethod

**Site:** https://cleverdogmethod.com  
**Playbook:** Breed × Behavior Problem (Persona + Problem pattern)  
**Target Pages:** 500+ (50 breeds × 10+ problems)  
**Phase 1 Pilot:** 20 pages (test batch)

---

## Playbook Selection

**Pattern:** `[Dog Breed] [Behavior Problem]`

**Why this works:**
- High search intent (people searching for breed-specific solutions)
- Low competition (most content is generic "how to stop barking")
- Natural internal linking to existing behavior problem posts
- Builds topical authority in breed-specific training

**Search Volume Examples:**
- "golden retriever barking" → 880/month
- "german shepherd separation anxiety" → 590/month
- "labrador jumping" → 720/month
- "beagle pulling on leash" → 320/month

**Total Opportunity:** 15K-25K organic visits/month (aggregate)

---

## Data Sources

### Breed List (Top 50 AKC Popular Breeds)
```json
[
  "Golden Retriever",
  "Labrador Retriever", 
  "German Shepherd",
  "French Bulldog",
  "Bulldog",
  "Beagle",
  "Poodle",
  "Rottweiler",
  "Dachshund",
  "Pembroke Welsh Corgi",
  "Australian Shepherd",
  "Yorkshire Terrier",
  "Boxer",
  "Cavalier King Charles Spaniel",
  "Doberman Pinscher",
  "Miniature Schnauzer",
  "Shih Tzu",
  "Boston Terrier",
  "Bernese Mountain Dog",
  "Pomeranian",
  "Havanese",
  "English Springer Spaniel",
  "Shetland Sheepdog",
  "Brittany",
  "Cocker Spaniel",
  "Miniature American Shepherd",
  "Border Collie",
  "Siberian Husky",
  "Great Dane",
  "Mastiff",
  "Chihuahua",
  "Cane Corso",
  "Vizsla",
  "Newfoundland",
  "Rhodesian Ridgeback",
  "Shiba Inu",
  "Belgian Malinois",
  "Basset Hound",
  "Weimaraner",
  "Collie",
  "West Highland White Terrier",
  "Bichon Frise",
  "Akita",
  "Bloodhound",
  "Bull Terrier",
  "Dalmatian",
  "Maltese",
  "Samoyed",
  "Saint Bernard",
  "Pug"
]
```

### Behavior Problems List
```json
[
  {
    "problem": "barking",
    "slug": "barking-problems",
    "title": "Barking Problems",
    "description": "excessive barking, nuisance barking, alert barking"
  },
  {
    "problem": "separation anxiety",
    "slug": "separation-anxiety",
    "title": "Separation Anxiety",
    "description": "destructive behavior when alone, excessive whining, house soiling"
  },
  {
    "problem": "jumping on people",
    "slug": "jumping-on-people",
    "title": "Jumping on People",
    "description": "jumping on guests, jumping on owner, over-excited greetings"
  },
  {
    "problem": "pulling on leash",
    "slug": "pulling-on-leash",
    "title": "Leash Pulling",
    "description": "leash reactivity, strong pulling, dragging on walks"
  },
  {
    "problem": "chewing furniture",
    "slug": "destructive-chewing",
    "title": "Destructive Chewing",
    "description": "chewing furniture, destroying belongings, teething problems"
  },
  {
    "problem": "aggression",
    "slug": "aggression-issues",
    "title": "Aggression Issues",
    "description": "dog aggression, stranger aggression, resource guarding"
  },
  {
    "problem": "digging",
    "slug": "digging-problems",
    "title": "Digging Problems",
    "description": "yard digging, escape attempts, destructive digging"
  },
  {
    "problem": "house training accidents",
    "slug": "potty-training",
    "title": "House Training Issues",
    "description": "accidents indoors, not fully potty trained, regression"
  },
  {
    "problem": "fearfulness",
    "slug": "fear-anxiety",
    "title": "Fear & Anxiety",
    "description": "noise phobia, stranger fear, general anxiety"
  },
  {
    "problem": "food stealing",
    "slug": "counter-surfing",
    "title": "Counter Surfing & Food Stealing",
    "description": "stealing food from counter, begging, scavenging"
  }
]
```

---

## Page Template Structure

### URL Pattern
```
https://cleverdogmethod.com/blog/breed-guides/[breed-slug]/[problem-slug]/
```

**Examples:**
- `/blog/breed-guides/golden-retriever/barking-problems/`
- `/blog/breed-guides/german-shepherd/separation-anxiety/`
- `/blog/breed-guides/labrador/jumping-on-people/`

### Title Template
```
[Breed] [Problem]: Why It Happens & How to Stop It | Clever Dog Method
```

**Examples:**
- "Golden Retriever Barking: Why It Happens & How to Stop It"
- "German Shepherd Separation Anxiety: Why It Happens & How to Stop It"
- "Labrador Jumping on People: Why It Happens & How to Stop It"

**Length:** 55-65 characters (optimal for SERPs)

### Meta Description Template
```
Is your [breed] [problem]? Learn why [breed]s [problem] and proven training techniques to stop [problem] behavior. Step-by-step guide from certified trainers.
```

**Example:**
> "Is your Golden Retriever barking excessively? Learn why Golden Retrievers bark and proven training techniques to stop barking behavior. Step-by-step guide from certified trainers."

### Content Structure

#### **1. Hero Section**
```html
<h1>[Breed] [Problem]: Why It Happens & How to Stop It</h1>
<p class="lead">Is your [breed] [problem description]? You're not alone. [Breed]s are known for [breed trait], which can lead to [problem]. Here's what you need to know.</p>
```

#### **2. Why [Breed]s [Problem] (200-300 words)**
- Breed-specific characteristics (energy level, history, instincts)
- Common triggers for this breed
- Age-related factors

**Data Requirements:**
- Breed temperament data
- Energy level (1-5 scale)
- Original purpose (herding, hunting, guarding, etc.)
- Common traits

#### **3. Common Causes (150-200 words)**
- List 3-5 specific causes
- Link to generic behavior problem post for details

#### **4. How to Stop [Breed] [Problem] (400-500 words)**
- Step-by-step training plan
- Breed-specific tips
- Timeline expectations
- Equipment recommendations

#### **5. Prevention Tips (150-200 words)**
- Breed-specific prevention
- Exercise needs
- Mental stimulation ideas

#### **6. When to Seek Professional Help (100-150 words)**
- Signs you need a trainer
- CTA to email list or consultation

#### **7. Related Articles (Internal Links)**
- Link to parent behavior problem post
- Link to 2-3 related breed×problem pages
- Link to breed-specific training basics

#### **8. FAQ Section (Schema Markup)**
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Why do [breed]s [problem] so much?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Breed-specific answer]"
      }
    },
    {
      "@type": "Question", 
      "name": "At what age does [breed] [problem] start?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Age-specific answer]"
      }
    },
    {
      "@type": "Question",
      "name": "Can you train [breed] to stop [problem]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, with consistent training..."
      }
    }
  ]
}
```

---

## Breed Data Schema

**Required data per breed:**
```json
{
  "breed": "Golden Retriever",
  "slug": "golden-retriever",
  "traits": {
    "energyLevel": 4,
    "trainability": 5,
    "barkingTendency": 3,
    "exerciseNeeds": "high",
    "size": "large",
    "temperament": ["friendly", "intelligent", "devoted"],
    "originalPurpose": "hunting companion",
    "commonBehaviorIssues": ["separation anxiety", "jumping", "chewing"]
  },
  "breedSpecificAdvice": {
    "barking": "Golden Retrievers bark to alert or when bored. Their hunting background means they're vocal when excited. Provide outlet through fetch games.",
    "separationAnxiety": "Goldens are people-oriented dogs bred to work alongside humans. They struggle more than independent breeds when left alone.",
    "jumping": "Goldens are enthusiastic greeters. Their size makes jumping dangerous. Start training early with 'four on the floor' rule."
  }
}
```

---

## Phase 1 Pilot: 20 Test Pages

**High-volume combinations (launch first):**

1. Golden Retriever + Barking
2. Golden Retriever + Separation Anxiety
3. Golden Retriever + Jumping
4. Labrador + Barking
5. Labrador + Jumping
6. Labrador + Pulling on Leash
7. German Shepherd + Barking
8. German Shepherd + Separation Anxiety
9. German Shepherd + Aggression
10. Beagle + Barking
11. Beagle + Pulling on Leash
12. French Bulldog + Separation Anxiety
13. Siberian Husky + Pulling on Leash
14. Siberian Husky + Digging
15. Border Collie + Barking
16. Border Collie + Herding Behavior
17. Australian Shepherd + Separation Anxiety
18. Rottweiler + Aggression
19. Dachshund + Barking
20. Poodle + Separation Anxiety

**Success Metrics (30 days):**
- 15+ pages indexed
- 3+ pages ranking top 20
- 50+ organic visits from these pages
- If successful → expand to 100 pages
- If not → refine template before scaling

---

## Technical Implementation

### Generator Script Requirements
```python
# generate-breed-problem-pages.py

import json
from string import Template

def generate_page(breed, problem, breed_data, problem_data):
    """Generate programmatic breed×problem page"""
    
    # URL structure
    url = f"/blog/breed-guides/{breed['slug']}/{problem['slug']}/"
    
    # Title
    title = f"{breed['breed']} {problem['title']}: Why It Happens & How to Stop It"
    
    # Meta description
    meta_desc = f"Is your {breed['breed']} {problem['problem']}? Learn why {breed['breed']}s {problem['problem']} and proven training techniques. Step-by-step guide."
    
    # Breed-specific intro
    intro = generate_intro(breed, problem, breed_data)
    
    # Why [Breed] [Problem]
    why_section = generate_why_section(breed, problem, breed_data)
    
    # Training steps
    training_section = generate_training_section(breed, problem)
    
    # Related links
    related = generate_related_links(breed, problem)
    
    # FAQ
    faq = generate_faq(breed, problem)
    
    # Schema
    schema = generate_schema(breed, problem, url, title, meta_desc)
    
    return {
        'url': url,
        'title': title,
        'meta_desc': meta_desc,
        'content': {
            'intro': intro,
            'why': why_section,
            'training': training_section,
            'related': related,
            'faq': faq
        },
        'schema': schema
    }
```

### Data Files Needed
- `data/breeds.json` - Breed characteristics
- `data/behavior-problems.json` - Problem definitions
- `data/breed-problem-advice.json` - Breed-specific advice per problem
- `data/related-posts-map.json` - Internal linking logic

---

## Quality Assurance Checklist

Before launching 20 pages:

- [ ] Each page 1000+ words
- [ ] Unique content (not just find/replace)
- [ ] Breed-specific advice in every section
- [ ] 3-5 internal links per page
- [ ] FAQ section with 3+ questions
- [ ] Schema markup (Article + FAQ + Breadcrumb)
- [ ] Breadcrumbs visible in UI
- [ ] Related articles section
- [ ] CTA for email signup
- [ ] Images (breed photo + training illustration)

**Manual Review:** Check 3-5 pages for quality before generating all 20

---

## Expansion Plan (Post-Pilot)

**If pilot succeeds:**

### Phase 2: 50 more pages (Top 10 breeds × 5 problems)
### Phase 3: 100 more pages (Top 25 breeds × 6 problems)
### Phase 4: 350 more pages (All 50 breeds × 10 problems)

**Total potential:** 500 pages

**Timeline:** 3-6 months (50 pages/month max to avoid thin content flags)

---

## Monitoring & Optimization

**Track per page:**
- Indexation status
- Keyword rankings (1-50)
- Organic traffic
- Bounce rate
- Time on page

**Red flags:**
- Not indexed after 30 days
- High bounce rate (>80%)
- Avg time on page <1 min
- No rankings after 60 days

**Action:** Improve content, add more breed-specific info, better internal linking

---

**Next Steps:**
1. Create breed data file (`data/breeds.json`)
2. Create breed-problem advice file
3. Build generator script
4. Generate 3 test pages manually
5. Review quality
6. Generate remaining 17 pages
7. Deploy + monitor

---

**Strategy Owner:** n0body  
**Date Created:** 2026-04-03
