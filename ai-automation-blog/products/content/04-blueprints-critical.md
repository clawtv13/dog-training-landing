# 3 Critical Automation Blueprints

These are the highest-ROI automations from testing with 50+ solo founders. Invoice processing alone saved Mike $800/month in VA costs.

---

## Blueprint 1: Invoice Processing Automation

**The Problem**

You spend 4 hours every week: opening invoice emails, copying data to spreadsheets, updating QuickBooks, chasing late payments. That's 16 hours/month doing data entry a robot could handle.

**ROI: $640/month saved** (16h × $40/hour)

**What You Need**
- Gmail account (free)
- Google Sheets (free)
- Zapier (free tier: 100 tasks/month)
- ChatGPT API access ($0.50/month typical)
- QuickBooks (optional, if you use it)

**The 30-Minute Setup**

### Step 1: Create Your Google Sheet Template (5 minutes)

Create new spreadsheet: "Invoice Tracker 2026"

Columns needed:
- A: Date Received
- B: Invoice Number  
- C: Client Name
- D: Amount
- E: Due Date
- F: Status (Pending/Paid)
- G: Notes

Share with your Zapier email (Settings → Share → zapier@zapier.com)

### Step 2: Setup Gmail Label + Filter (3 minutes)

Create label: "Invoices/Auto-Process"

Create filter:
- From: your invoice software OR subject contains "invoice"
- Apply label: Invoices/Auto-Process
- Skip inbox (optional - keeps main inbox clean)

### Step 3: Connect Zapier Trigger (5 minutes)

New Zap:
- Trigger: Gmail → New Email Matching Search
- Search string: `label:invoices-auto-process`
- Test trigger (send yourself sample invoice)

### Step 4: Add ChatGPT Data Extraction (10 minutes)

Action: OpenAI → Conversation (ChatGPT)
- Model: GPT-4 (more accurate) or GPT-3.5-turbo (cheaper)
- Message:
```
Extract from this email:
- Invoice number
- Client/company name  
- Total amount (numbers only, no currency symbol)
- Due date (format: YYYY-MM-DD)

Email content:
{{Email Body}}

Return ONLY as JSON:
{"invoice_number": "...", "client": "...", "amount": "...", "due_date": "..."}
```

Test with your sample email. Verify JSON format.

### Step 5: Update Google Sheet (5 minutes)

Action: Google Sheets → Create Spreadsheet Row
- Spreadsheet: Invoice Tracker 2026
- Worksheet: Sheet1
- Date Received: {{Trigger Date}}
- Invoice Number: {{ChatGPT invoice_number}}
- Client Name: {{ChatGPT client}}
- Amount: {{ChatGPT amount}}
- Due Date: {{ChatGPT due_date}}
- Status: "Pending"

### Step 6: QuickBooks Integration (Optional, 5 minutes)

Action: QuickBooks → Create Invoice
- Customer: {{ChatGPT client}}
- Amount: {{ChatGPT amount}}
- Due Date: {{ChatGPT due_date}}

**Testing Checklist**

Send 3 test invoices to yourself:
- [ ] Different formats (PDF attachment, email body, forwarded)
- [ ] Various invoice software (Stripe, PayPal, manual)
- [ ] Edge case: multi-line items, taxes included

Check:
- [ ] Google Sheet populated correctly
- [ ] All fields extracted (100% accuracy expected)
- [ ] QuickBooks invoice created (if enabled)
- [ ] No duplicate entries

**Troubleshooting**

**Issue:** ChatGPT returns incomplete data
- Fix: Add example JSON to prompt: `Example: {"invoice_number": "INV-001", ...}`

**Issue:** Date format wrong (03/29/2026 instead of 2026-03-29)
- Fix: Add to prompt: "Use ISO format YYYY-MM-DD for dates"

**Issue:** Amount includes currency symbol ($1,234.56)
- Fix: Add to prompt: "Amount as number only, no $ or commas"

**Issue:** Zap triggers for non-invoice emails
- Fix: Tighten Gmail filter - require both sender AND keyword

**Issue:** Hitting 100 task/month limit on Zapier free
- Solution A: Upgrade to Zapier Starter ($20/month, 750 tasks)
- Solution B: Switch to Make.com (1,000 ops/month free)
- Solution C: Process in batches weekly instead of real-time

**Level Up: Optimization Tips**

After 30 days running:
1. Add automatic payment reminders (7 days before due date)
2. Flag overdue invoices (Status → "OVERDUE" if past due date)
3. Categorize by client (consulting vs product revenue)
4. Monthly summary report (total invoiced, total paid)
5. Integrate with Slack (notify when invoice >$5,000)

**Real Results**

Mike (SaaS founder, $400K revenue):
- Before: 4h/week processing 60 invoices/month = 16h/month
- After: 0h manual (100% automated) + 30min/month monitoring
- Savings: 15.5h/month × $120/hour = **$1,860/month**
- Setup: 35 minutes
- Break-even: 1 invoice processed

Sarah (consultant, $180K revenue):
- Before: 2h/week on 15 invoices/month = 8h/month
- After: 5 min/week spot-checking = 0.3h/month  
- Savings: 7.7h/month × $80/hour = **$616/month**
- Setup: 25 minutes
- Break-even: Day 1

**Prompt Reference**

The email extraction prompt used above is **Prompt #9: Email Summarizer** (Part 2 of this kit).

---

## Blueprint 2: Lead Qualification System

**The Problem**

You get 20-30 leads/week. Spend 6 hours qualifying them manually: checking LinkedIn, reviewing their website, deciding if they're a fit. 70% aren't qualified. You're wasting time on tire-kickers.

**ROI: $960/month saved** (24h × $40/hour)

**What You Need**
- Lead form (Google Forms/Typeform - free)
- Airtable or Notion (free tier)
- ChatGPT API ($1-2/month)
- Calendly (free tier) or similar
- Zapier/Make.com (free tier works)

**The 40-Minute Setup**

### Step 1: Create Qualification Criteria (10 minutes)

Define YOUR ideal customer. Example for B2B SaaS consultant:

**Must Have (Disqualify if missing):**
- Revenue: $100K-$2M/year (below = can't afford, above = enterprise)
- Decision maker or strong influence
- Specific problem we solve
- Timeline: <90 days to implement

**Scoring System (0-10):**
- Budget clarity (+3 if stated, +1 if range)
- Problem severity (+3 if urgent, +1 if exploring)
- Decision timeline (+2 if <30 days, +1 if <90 days)
- Referral source (+2 if customer referral, +1 if organic)

Score 7+ = Qualified (book call)
Score 4-6 = Nurture (email sequence)
Score 0-3 = Reject politely

### Step 2: Build Smart Lead Form (10 minutes)

Create form with these questions:
1. Company name + website URL
2. Your role/title
3. Annual revenue (dropdown: <$100K, $100K-$500K, $500K-$2M, $2M+)
4. What problem are you trying to solve? (open text, 2-3 sentences)
5. Timeline to implement (dropdown: This month, Next 90 days, Exploring, No rush)
6. How did you hear about us? (dropdown: includes "Referral from [name]")
7. Budget allocated (optional dropdown: <$5K, $5K-$20K, $20K+, Not sure yet)

Connect form to Airtable/Notion (Zapier/Make integration)

### Step 3: Automate ChatGPT Scoring (10 minutes)

Zapier Action: OpenAI → Conversation

Prompt:
```
Score this lead 0-10 for our B2B SaaS consulting firm.

Scoring rubric:
- Revenue $100K-$2M: +3 points (disqualify if outside range)
- Decision maker (CEO/Founder/VP): +2 points  
- Urgent timeline (<30 days): +2 points
- Specific problem mentioned: +2 points
- Budget stated: +1 point

Lead data:
Company: {{Form Company}}
Revenue: {{Form Revenue}}
Role: {{Form Role}}
Problem: {{Form Problem}}  
Timeline: {{Form Timeline}}
Source: {{Form Source}}

Return JSON:
{"score": [0-10], "qualified": [true/false], "reason": "[1 sentence]", "next_step": "[book_call/nurture/reject]"}
```

### Step 4: Route Based on Score (5 minutes)

Zapier Paths (if/then logic):

**Path A: Score 7+** (Qualified)
- Send to Calendly (auto-book discovery call)
- Email: "Great fit - here's my calendar [link]"
- Add to Airtable: Status = "Qualified - Call Scheduled"

**Path B: Score 4-6** (Nurture)
- Add to email sequence (Beehiiv/ConvertKit)
- Email: "Not ready yet? Here's [relevant resource]"
- Add to Airtable: Status = "Nurturing"

**Path C: Score 0-3** (Reject)
- Email: "Thanks for interest. Not a fit because [ChatGPT reason]. Here's [alternative resource]"
- Add to Airtable: Status = "Rejected - Not Fit"

### Step 5: Calendly Integration (5 minutes)

If qualified:
- Action: Calendly → Create Invitee
- Event type: Discovery Call (30 min)
- Pre-fill: Name, Email, Company
- Add note: ChatGPT qualification score + reason

**Testing Checklist**

Submit 10 test leads:
- [ ] 3 highly qualified (score 8-10)
- [ ] 4 maybe leads (score 4-6)  
- [ ] 3 unqualified (score 0-3)

Verify:
- [ ] Qualified leads get calendar link immediately
- [ ] Nurture leads get resource email
- [ ] Rejected leads get polite redirect
- [ ] All leads logged in Airtable correctly
- [ ] ChatGPT scoring matches your manual assessment (80%+ accuracy)

**Troubleshooting**

**Issue:** ChatGPT scores too generously (everyone 7+)
- Fix: Add negative points to prompt: "No stated budget: -1 point"

**Issue:** Form abandonment (people start, don't finish)
- Fix: Make questions optional except email + problem
- Score with incomplete data (penalize missing fields)

**Issue:** Spam submissions
- Fix: Add honeypot field (hidden input, disqualify if filled)
- Require email verification before triggering Zap

**Real Results**

Lisa (e-commerce consultant):
- Before: 6h/week qualifying 25 leads → 5 actually fit
- After: 0h manual qualification, system handles 100%
- Qualified leads: 5/25 (same hit rate, zero manual time)
- Savings: 6h/week × $80/hour × 4 weeks = **$1,920/month**
- Calendar booking rate: 80% (vs 40% when manual)

**Prompt Reference**

Lead scoring prompt above is custom for this blueprint. Adapt the rubric section to YOUR business criteria.

---

## Blueprint 3: Meeting Notes Automation

**The Problem**

8 meetings/week = 8 hours of notes + follow-up. You spend 20 minutes after each call typing action items, updating CRM, sending recaps. That's 2.7 hours/week on administrative work that could be automated.

**ROI: $480/month saved** (12h × $40/hour)

**What You Need**
- Otter.ai (free tier: 300 min/month)
- ChatGPT API ($0.50-1/month)
- Notion or Airtable (free tier)
- Zapier/Make.com (free tier)

**The 35-Minute Setup**

### Step 1: Connect Otter.ai to Calendar (5 minutes)

Settings → Integrations → Google Calendar/Outlook
- Auto-join all meetings (or specific calendar)
- Record audio + transcript
- Share link with attendees

Test: Schedule fake meeting, verify Otter joins

### Step 2: Create Notion Meeting Database (10 minutes)

New database: "Meeting Notes 2026"

Properties needed:
- Title (text)
- Date (date)
- Attendees (multi-select)
- Meeting Type (select: Sales, Client, Internal, Partner)
- Key Points (text)
- Action Items (text)
- Next Steps (text)
- Recording URL (URL)
- Transcript (text - long)

### Step 3: Setup Otter → Zapier Trigger (5 minutes)

New Zap:
- Trigger: Otter.ai → New Transcript
- Test: Pull your fake meeting transcript

### Step 4: ChatGPT Summarization (10 minutes)

Action: OpenAI → Conversation

Prompt:
```
Summarize this meeting transcript. Extract:

1. KEY POINTS (3-5 bullets, most important topics discussed)
2. ACTION ITEMS (who does what by when, format: "[@Person] [Action] [by Date]")
3. DECISIONS MADE (any commitments or choices)
4. NEXT STEPS (what happens next, timeline)

Transcript:
{{Otter Transcript}}

Return as structured markdown. Be specific - no vague actions like "follow up."
```

### Step 5: Save to Notion (5 minutes)

Action: Notion → Create Database Item
- Database: Meeting Notes 2026
- Title: {{Otter Meeting Name}}
- Date: {{Otter Meeting Date}}
- Key Points: {{ChatGPT Key Points}}
- Action Items: {{ChatGPT Action Items}}
- Next Steps: {{ChatGPT Next Steps}}
- Recording URL: {{Otter Recording Link}}

**Bonus: Auto-send Recap Email**

Action: Gmail → Send Email (optional)
- To: {{Otter Attendees}}
- Subject: "Recap: {{Meeting Name}}"
- Body:
```
Thanks for today's call!

Key points:
{{ChatGPT Key Points}}

Action items:
{{ChatGPT Action Items}}

Recording: {{Otter Link}}

Reply if I missed anything.
```

**Testing Checklist**

Record 3 test meetings:
- [ ] Sales call (prospect name, clear next steps)
- [ ] Client call (action items, timeline)
- [ ] Internal meeting (decisions, who owns what)

Verify:
- [ ] Transcript accurate (>90%)
- [ ] Key points relevant (not generic)
- [ ] Action items specific (name + task + date)
- [ ] Notion database populated
- [ ] Email sent (if enabled)

**Troubleshooting**

**Issue:** Otter doesn't join meeting
- Fix: Check calendar permission (view + edit required)
- Ensure meeting has video link (Zoom/Meet/Teams)

**Issue:** ChatGPT summaries too vague
- Fix: Add examples to prompt:
  ```
  Bad: "Follow up on proposal"
  Good: "[@Sarah] Send updated proposal with pricing by March 20"
  ```

**Issue:** Action items missing owner
- Fix: Add to prompt: "If no name mentioned, use role (e.g., [@Client] or [@Our team])"

**Issue:** Transcript quality poor (background noise)
- Fix A: Use headset with noise cancellation
- Fix B: Post-process in Otter app (edit before Zap triggers)
- Fix C: Add to prompt: "Ignore unclear audio artifacts"

**Level Up: Advanced Features**

After running 30 days:
1. CRM integration (Notion → HubSpot/Salesforce)
2. Task creation (action items → Asana/Todoist automatically)
3. Template-based summaries (different format for sales vs client calls)
4. Speaker identification (track who said what)
5. Sentiment analysis (flag if client seems frustrated)

**Real Results**

Mike (SaaS founder, 12 meetings/week):
- Before: 20 min/meeting notes + recap = 4h/week
- After: 0 min manual (just review AI summary) = 0.5h/week
- Savings: 3.5h/week × $120/hour × 4 weeks = **$1,680/month**
- Setup: 30 minutes
- Accuracy: 85% (reviewed first 20 meetings)

Sarah (marketing consultant, 6 meetings/week):
- Before: 25 min/meeting = 2.5h/week  
- After: 5 min/week review
- Savings: 2h/week × $80/hour × 4 weeks = **$640/month**

**Prompt Reference**

Meeting summarization prompt is custom for this blueprint.

---

## Combined ROI: All 3 Blueprints

If you implement all three:

**Time Saved:**
- Invoice automation: 16h/month
- Lead qualification: 24h/month
- Meeting notes: 12h/month
- **Total: 52 hours/month**

**Value Created:**
- 52h × $40/hour = **$2,080/month**
- Annual: **$24,960**

**Setup Investment:**
- Time: 1.75 hours (105 minutes)
- Cost: $39 (this kit) + $2-3/month (APIs)
- Break-even: Week 1
- ROI: 640x Year 1

These three blueprints alone justify the entire kit price. The remaining 7 blueprints (Part 5) + 50 prompts (Part 2) are pure upside.

---

**Ready to start?** Pick Blueprint 1 (invoice automation) - highest ROI, easiest setup, immediate results.
