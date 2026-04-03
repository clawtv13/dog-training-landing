# How I Run 3 Businesses Solo: Complete Operations Breakdown

**Meta Description:** Running 3 businesses alone in 15 hours/week for $280/month. Real operations breakdown: workless.build (6 posts/day), CleverDogMethod, and Mind Crimes documentary channel. No employees. Full automation stack revealed.

---

## The Setup

I run 3 businesses: workless.build (AI automation blog), CleverDogMethod (solopreneur automation), and Mind Crimes (documentary channel). Total time: 15 hours/week. Total cost: $280/month in tools. Revenue: $8K-12K/month across all three. Zero employees. Zero VAs. Here's exactly how I do it.

Most people think running multiple businesses means 80-hour weeks. Wrong. The trick isn't hustle—it's automation and knowing what to ignore.

---

## The 3 Businesses Overview

### workless.build: The AI Automation Blog

This is the flagship. Six posts per day, every day. All automated. Content covers AI automation, solopreneur operations, and working less while earning more.

**The numbers:**
- 6 posts/day = 180 posts/month
- SEO traffic: 35K-50K visitors/month
- Revenue: $4K-6K/month (digital products, affiliate)
- Time investment: 3 hours/week

Everything runs on GitHub Actions with OpenClaw agents. Posts generate at 08:00 and 20:00 UTC. I review batches weekly, approve or reject, and the system publishes, handles SEO metadata, and distributes.

### CleverDogMethod: Same Engine, Different Niche

This is workless.build's clone with a different domain and positioning. Same automation. Same content generation. Different audience: solopreneurs who care about business automation more than AI specifically.

**The numbers:**
- Same 6 posts/day cadence
- SEO traffic: 15K-25K visitors/month
- Revenue: $2K-3K/month
- Time investment: 2 hours/week
- Marginal cost: $10/month (domain only)

Why run two identical sites? Risk. If Google slaps one, the other survives. Different audiences find different angles. And since the infrastructure exists, the marginal cost is nearly zero.

### Mind Crimes: Documentary Production

The outlier. Mind Crimes produces true crime and mystery documentaries. One video per day, Monday through Friday. This is the highest-touch of the three.

**The numbers:**
- 5 videos/week
- Delivery: Telegram channel
- Revenue: $2K-3K/month (subscriptions)
- Time investment: 8 hours/week
- Cost: $120/month (API credits, storage)

This one needs more manual work because video quality standards are higher and audiences are brutal about mistakes. But even here, 60% is automated: script generation, voice synthesis, video assembly, delivery.

### Why Multiple Businesses vs Scaling One?

Two reasons: ceiling and risk.

Each business hits a natural ceiling. workless.build maxes out around $10K/month in its current form. Scaling past that means:
- Launching paid products (different business model)
- Building a community (different time commitment)
- Going the VC route (different game)

So I replicated the playbook. CleverDogMethod took 4 days to launch because the infrastructure existed. Mind Crimes took 3 weeks because video is harder than text.

**Revenue diversification:**
- Google tanks one site → still have two
- Telegram changes TOS → still have blogs
- Automation breaks → problems stay contained

Multiple small bets beat one big bet when you're solo.

---

## The Operations Framework

### Time Allocation: 15 Hours/Week Breakdown

Here's where every hour goes:

**Monday (3h):**
- 1h: Review weekend automation logs
- 1h: Content strategy for workless + CleverDog
- 1h: Mind Crimes production planning

**Tuesday-Thursday (2h each = 6h):**
- 30min/day: Approve/reject generated posts
- 30min/day: Mind Crimes script review + editing
- 1h/day: Production work (video assembly, voice selection)

**Friday (3h):**
- 1h: Week review, analytics check
- 1h: System maintenance (update prompts, fix breaks)
- 1h: Community management (Telegram, emails)

**Saturday-Sunday (3h total):**
- Strategic work only
- Planning next month
- Testing new automation
- Learning new tools

**What's NOT on the schedule:**
- Customer support (automated via FAQs + canned responses)
- Social media (not doing it—SEO only)
- Meetings (zero standing meetings)
- Admin busywork (automated or deleted)

### Decision Framework: Automate, Delegate, Delete

Every task faces this filter:

**1. Can I automate it?**
If yes → build the automation (even if it takes 4 hours to save 30 minutes/week).

Examples:
- Post scheduling → Automated via cron
- SEO metadata → AI-generated on publish
- Image creation → Stable Diffusion + templates
- Email responses → GPT-4 with approval queue

**2. Can I delegate it?**
If automation isn't possible AND it's high-value → delegate.

My current delegation: Zero. Everything is either automated or deleted. The only "delegation" is to AI systems.

**3. Can I delete it?**
If it's not automated or delegated → it probably doesn't need doing.

Examples I deleted:
- Social media promotion (SEO replaced it)
- Newsletter (blog RSS is enough)
- A/B testing thumbnails (waste of time at my scale)
- Customer phone calls (email/text only)

**The Rule:** If a task shows up 3 times and isn't automated by the third time, I'm doing something wrong.

### Weekly Schedule: What Happens When

My automation runs on a strict schedule:

**Daily (08:00 UTC):**
```cron
0 8 * * * /root/scripts/generate-posts.sh workless
5 8 * * * /root/scripts/generate-posts.sh cleverdog
10 8 * * * /root/scripts/publish-queue.sh
```

**Daily (20:00 UTC):**
```cron
0 20 * * * /root/scripts/generate-posts.sh workless
5 20 * * * /root/scripts/generate-posts.sh cleverdog
10 20 * * * /root/scripts/publish-queue.sh
```

**Monday-Friday (10:00 UTC):**
```cron
0 10 * * 1-5 /root/scripts/mindcrimes-deliver.sh
```

**Weekly (Sunday 22:00 UTC):**
```cron
0 22 * * 0 /root/scripts/analytics-report.sh
0 22 * * 0 /root/scripts/health-check.sh
```

### How I Prioritize Across 3 Businesses

Priority ranking:
1. Mind Crimes (highest revenue per hour)
2. workless.build (largest audience, brand asset)
3. CleverDogMethod (lowest maintenance, pure profit)

When I have only 1 hour:
- Mind Crimes gets it (production work)

When I have 3 hours:
- 2h Mind Crimes
- 1h workless/CleverDog review

When I have 10 hours:
- Strategic work across all three

### Crisis Management: When Things Break

Things break weekly. Here's the protocol:

**Break severity levels:**

**P0 (Drop everything):**
- Site completely down
- Payment processing broken
- Data loss/security breach

**P1 (Fix within 24h):**
- Automation stopped generating content
- Delivery system down
- Revenue impact >$50/day

**P2 (Fix within week):**
- Analytics broken
- Non-critical features down
- Quality issues in automation

**P3 (Fix when convenient):**
- Minor UI bugs
- Optimization opportunities
- Nice-to-have features

**Actual P0 incidents in last 90 days:** 2
1. Vercel deployment failed (fixed in 20 minutes)
2. OpenAI API key expired (10 minutes)

Most "crises" are P2 or P3. I don't check systems hourly on purpose. Daily reviews catch 95% of issues before they matter.

---

## Business #1: workless.build Operations

### Content System: 6 Posts/Day Automation

The whole content engine runs on OpenClaw + GPT-4. Here's the flow:

**1. Topic Generation (Automated)**
Daily at 07:00 UTC, a script:
- Pulls trending keywords from Google Trends API
- Analyzes Search Console for rising queries
- Cross-references with content gaps
- Generates 12 topic suggestions (6 for each run)

**2. Content Creation (Automated)**
At 08:00 and 20:00 UTC:
- OpenClaw agents receive topic queue
- Generate full posts (1,500-2,500 words each)
- Include SEO metadata, images, internal links
- Push to GitHub as markdown files

**3. Review Queue (Manual)**
I review posts in batches:
- Tuesday: Review Monday + weekend generation
- Thursday: Review Tuesday + Wednesday generation

Review criteria (takes 2-3 minutes per post):
- Factual accuracy
- Tone matches brand
- SEO elements present
- No obvious AI patterns

**Approval rate: 85%**
Rejected posts go back for regeneration with specific feedback.

**4. Publishing (Automated)**
Approved posts deploy via:
```bash
# publish-queue.sh
#!/bin/bash
cd /root/workless-build
git pull origin main
approved_posts=$(ls content/approved/*.md)
for post in $approved_posts; do
  mv $post content/posts/
  git add .
  git commit -m "Publish: $(basename $post)"
  git push origin main
done
```

Vercel picks up the push and deploys in 90 seconds.

### Tech Stack Specifics

**Content Generation:**
- OpenClaw agents (custom prompts tuned over 60 days)
- GPT-4 API ($30/month in usage)
- GitHub for version control + collaboration

**Hosting:**
- Vercel (free tier, somehow)
- Custom domain ($12/year)

**SEO & Analytics:**
- Google Search Console (free)
- Google Analytics 4 (free)
- Ahrefs ($99/month, split across all businesses)

**Automation:**
- Cron (free, runs on my VPS)
- GitHub Actions (free tier covers it)

**Total cost for workless.build: $50/month**

### Time Breakdown: 3 Hours/Week

**Content review:** 90 minutes
- 30 posts/week reviewed
- 3 minutes each

**Strategy:** 60 minutes
- Keyword research
- Competitor analysis
- Content gap identification

**Maintenance:** 30 minutes
- Check automation logs
- Update prompts if needed
- Fix any breaks

### Revenue: $4K-6K/Month

**Revenue sources:**
1. **Digital products (60%):** Playbooks, templates, automation blueprints
2. **Affiliate (30%):** Tool recommendations (OpenClaw, Vercel, AI APIs)
3. **Sponsorships (10%):** Occasional tool sponsorships

**Why it works:**
Traffic is targeted. People searching "how to automate your business" are ready to buy solutions. Conversion rate: 2-3% on product pages.

### What's Automated vs Manual

**100% automated:**
- Topic research
- Content generation
- Publishing
- SEO metadata
- Image creation
- Internal linking
- Social sharing (minimal)

**Manual:**
- Post review and approval (85% pass rate)
- Product creation (quarterly)
- Email responses (weekly batch)
- Strategic planning (weekly)

**The 80/20:** Automation handles 80% of operations. I spend time on the 20% that moves revenue: strategy and quality control.

---

## Business #2: CleverDogMethod Operations

### Same Infrastructure, Different Positioning

CleverDogMethod is workless.build's twin. Same GitHub repo structure. Same OpenClaw agents. Same Vercel deployment. Different domain, different brand, different content angle.

**Why this works:**

Once I built workless.build's automation, replicating it took 4 days:
1. **Day 1:** Clone repo, update config, new domain
2. **Day 2:** Modify content prompts for solopreneur angle
3. **Day 3:** Generate initial 20 posts for SEO foundation
4. **Day 4:** Set up analytics, test automation

**Marginal cost: $10/month**
- Domain registration only
- Everything else shares workless infrastructure

### Different Positioning

**workless.build focuses on:**
- AI automation
- Technical implementations
- Developer-friendly content

**CleverDogMethod focuses on:**
- Business automation
- Non-technical solopreneurs
- Productivity and systems

**Same automation, different voice.**

The content prompts emphasize different angles:
- workless: "Here's the code to automate..."
- CleverDog: "Here's the system to automate..."

Both serve the same reader at different stages. Someone Googling "how to run a business alone" finds CleverDog. Same person later Googling "automate blog with ChatGPT API" finds workless.

### Time Investment: 2 Hours/Week

**Content review:** 60 minutes
- Same batch review process as workless
- Approve/reject generated posts
- Quality threshold slightly lower (audience less technical)

**Strategy alignment:** 30 minutes
- Make sure CleverDog isn't stealing workless keywords
- Identify unique angles for solopreneur audience

**Maintenance:** 30 minutes
- Automation health check
- Prompt adjustments if quality dips

### Cross-Promotion Strategy

**Internal linking:**
- workless posts link to CleverDog for "non-technical" approaches
- CleverDog posts link to workless for "technical deep dives"

**Product bundling:**
- Playbooks sold on both sites
- Different pricing (CleverDog audience pays more)
- Bundle discount for both audiences

**Email list sharing:**
- Separate lists
- Occasional cross-email: "If you like this, check out..."
- Conversion rate: 8-12% click-through

**The result:** CleverDog got to $2K/month in 60 days by using workless's existing systems and audience.

---

## Business #3: Mind Crimes Operations

### Documentary Production Workflow

Mind Crimes is different. Video demands higher quality and audiences are brutal. A typo in a blog post? No one notices. Audio glitch in a documentary? Comments explode.

**The production pipeline:**

**1. Topic Selection (Manual)**
Monday morning, 1 hour:
- Browse r/UnresolvedMysteries, r/TrueCrime
- Check trending crime stories
- Select 5 topics for the week
- Outline each episode

**2. Script Generation (Automated)**
Python script + GPT-4:
```python
# mindcrimes-script-gen.py
import openai

def generate_script(topic, outline):
    prompt = f"""
    Write a 10-minute documentary script about: {topic}
    
    Structure: {outline}
    
    Style: True crime documentary, neutral tone, suspenseful pacing.
    Include: Timeline, key facts, open questions.
    Exclude: Speculation, conspiracy theories.
    
    Target length: 2,000 words.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response['choices'][0]['message']['content']
```

**Output:** First draft script in 30 seconds.

**3. Script Editing (Manual)**
Tuesday-Thursday, 30 minutes/day:
- Review generated script
- Fact-check key points
- Adjust pacing and tone
- Add specific details AI missed

**Approval rate: 70%**
Higher rejection rate than blog content because quality bar is higher.

**4. Voice Synthesis (Automated)**
ElevenLabs API:
- Professional narrator voice
- Voice cloning for consistency
- Batch synthesis for approved scripts

**Cost:** $40/month for voice credits.

**5. Video Assembly (Semi-Automated)**
Python script + FFmpeg:
- Pull stock footage from Pexels API
- Sync to audio timestamps
- Add title cards and transitions
- Render final video

**Manual intervention:** 20% of videos need custom adjustments.

**6. Delivery (Automated)**
Telegram Bot API:
- Post video to private channel
- Schedule for 10:00 UTC Mon-Fri
- Include episode description
- Track views and engagement

### Time Breakdown: 8 Hours/Week

**Topic research + outlining:** 2 hours (Monday)
**Script review + editing:** 3 hours (Tue-Thu, 1h each)
**Production supervision:** 2 hours (fixing issues, custom edits)
**Community management:** 1 hour (Telegram replies, feedback)

### Why This One Is Less Automated

Three reasons:

**1. Quality threshold is higher**
Blog readers forgive minor issues. Video viewers don't. One audio glitch or factual error tanks credibility.

**2. Medium complexity is higher**
Text is easy to automate. Video involves:
- Script
- Voice
- Footage selection
- Timing and editing
- Rendering

Each layer adds failure points.

**3. Audience expectations differ**
Blog readers want information. Documentary viewers want entertainment. Entertainment needs human judgment in pacing, tone, and emotional beats.

**Could I automate more?** Yes. But returns shrink. Getting from 60% to 80% automation would take 40 hours of dev work to save 1-2 hours/week. Not worth it at this scale.

---

## The Complete Tech Stack

Here's every tool I use across all three businesses.

### Content Creation
- **OpenClaw:** Agent orchestration, automation workflows ($0, open source)
- **GPT-4 API:** Content + script generation ($70/month across all)
- **ElevenLabs:** Voice synthesis for Mind Crimes ($40/month)
- **Stable Diffusion:** Blog post images (self-hosted, $0)

### Code & Deployment
- **GitHub:** Version control, content storage ($0, free tier)
- **Vercel:** Hosting for workless + CleverDog ($0, free tier)
- **Python:** Automation scripts (free)
- **FFmpeg:** Video rendering (free)

### Commerce
- **Gumroad:** Digital product sales ($0 base + 10% transaction fee)
- **Etsy:** Template sales ($3/month listing fees)

### Communication
- **Telegram Bot API:** Mind Crimes delivery ($0)
- **Email:** FastMail ($5/month)

### Analytics & SEO
- **Google Search Console:** Free
- **Google Analytics 4:** Free
- **Ahrefs:** $99/month (keyword research, competitor analysis)

### Infrastructure
- **VPS (Hetzner):** Runs cron jobs, hosts scripts ($5/month)
- **Domains:** $36/year total for 3 domains

### Total Monthly Cost: $280

**Breakdown:**
- AI APIs (GPT-4, ElevenLabs): $110
- Ahrefs: $99
- VPS: $5
- Email: $5
- Domains: $3/month average
- Gumroad/Etsy transaction fees: $40-60/month (variable)

**What I'm NOT paying for:**
- Virtual assistants ($0)
- Employees ($0)
- Social media scheduling tools ($0)
- Email marketing platforms ($0)
- Project management software ($0)
- Most SaaS subscriptions ($0)

**The rule:** If a tool costs more than $20/month, it needs to directly generate revenue or save 5+ hours monthly.

---

## What I Learned

### Start With One, Automate, Then Add Next

**Mistake #1:** Trying to launch all three at once.

I originally planned to launch workless, CleverDog, and Mind Crimes together. "Efficiency," I thought. Wrong.

**What actually happened:**
- Built workless.build first
- Spent 60 days tuning automation
- Made every mistake on one business
- Then cloned it for CleverDog (took 4 days)
- Launched Mind Crimes after content system was proven

**Lesson:** Perfect the system on one, then copy it. Splitting attention across three untested businesses = 3× the problems, 0.3× the progress.

### 80% Automation, 20% Human Touch

**Mistake #2:** Trying to automate everything.

I tried to automate post approval. Built a scoring system, confidence thresholds, quality filters. Spent 20 hours on it.

**Result:** 60% approval accuracy. I spent more time fixing bad posts than just reviewing them manually.

**Lesson:** Some tasks are faster manual. For me:
- Content approval (pattern recognition humans excel at)
- Strategy decisions (needs context AI doesn't have)
- Customer empathy (AI voice sounds robotic)

The 20% I keep manual is where judgment matters more than speed.

### Systems > Hustle

**Mistake #3:** Working harder when growth slowed.

In month 2, workless traffic plateaued. My instinct: write more posts manually, work weekends, "hustle harder."

**What actually worked:**
- Stepped back
- Analyzed what WAS working
- Doubled down on those topics
- Improved automation prompts
- Let the system run

**Result:** Traffic 2× in 30 days without increasing hours.

**Lesson:** When things aren't growing, the answer is usually better systems, not more hours.

### When to NOT Automate

Not everything should be automated.

**Don't automate if:**
1. **Task occurs <3 times** - Building automation costs time. If it's one-off, just do it manually.
2. **Automation is fragile** - Some tasks change constantly. Automating creates more maintenance than it saves.
3. **Human judgment is the value** - Strategic decisions, creative direction, quality control—these are why people pay.

**Example I didn't automate:** Product creation.

I could generate playbooks with AI. But customers buy my thinking, not just information. That stays manual.

### Mistakes Made

**Big ones:**

1. **Launched Mind Crimes too early** - Should've waited until blog systems were more mature. Spent 3 weeks fighting fires across all businesses.

2. **Over-engineered analytics** - Built custom dashboards, data pipelines, automated reports. Then I checked them once a week and only cared about 3 metrics.

3. **Underpriced products at first** - Launched playbooks at $29. Should've been $79 from day one. Price anchoring matters.

4. **Ignored email lists too long** - Focused purely on SEO. Then I realized email lists give you leverage when algorithms change. Started building lists at month 5—should've been day 1.

5. **Tried to be everywhere** - Spread thin across Twitter, LinkedIn, Reddit. Cut everything except Reddit (where my audience actually is). 10× better results.

---

## Build This System Yourself

This framework took me 90 days to build through trial, error, and broken automation.

You can do it in 30 days with the **Solopreneur Operations Playbook:**

**What's inside:**
- Complete automation blueprints (OpenClaw + GPT-4 content systems)
- Decision frameworks (what to automate, delegate, delete)
- Tech stack templates (copy-paste configurations)
- Cron schedules and scripts (working code, not theory)
- Revenue models (what actually converts)
- Time allocation frameworks (15-hour workweek breakdown)

**Price: $79**

No fluff. No "mindset" filler. Just the systems I use to run 3 businesses in 15 hours/week.

**[Get the Playbook →](#)**

---

*Questions? I'm on Telegram: @n0mad_builds*
