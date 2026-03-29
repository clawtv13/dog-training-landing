# Email Sequence Automation System

**Automated email funnels that convert free subscribers into paying customers.**

Built for: **AI Automation Builder Newsletter**  
Platform: **Beehiiv**  
Target: **2-5% conversion rate, $50-500 LTV**

---

## 🎯 What This Does

Complete email marketing automation system:
- ✅ 5 pre-built email sequences (welcome, upsell, abandoned cart, re-engagement, product launch)
- ✅ Behavioral trigger system (clicks, downloads, purchases)
- ✅ Auto-segmentation (active, warm, cold, customer)
- ✅ A/B testing framework
- ✅ Performance analytics & optimization
- ✅ SQLite database for tracking
- ✅ Beehiiv API integration

---

## 📂 Project Structure

```
newsletter-ai-automation/
├── scripts/
│   ├── email-sequence-manager.py    # Core automation engine
│   ├── engagement-tracker.py        # Behavioral tracking
│   └── conversion-optimizer.py      # A/B testing & analytics
├── sequences/
│   ├── welcome.json                 # 5-email welcome sequence
│   ├── upsell.json                  # 4-email upsell sequence
│   ├── abandoned-cart.json          # 3-email recovery sequence
│   ├── re-engagement.json           # 3-email win-back sequence
│   └── product-launch.json          # 7-email launch sequence
├── docs/
│   ├── EMAIL-STRATEGY.md            # Complete playbook
│   └── BEEHIIV-INTEGRATION.md       # API setup guide
└── README.md                         # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Set Environment Variables

```bash
export BEEHIIV_API_KEY="your_api_key_here"
```

### 3. Initialize Database

```bash
cd scripts/
python3 email-sequence-manager.py
```

This creates `email_sequences.db` with all required tables.

### 4. Set Up Beehiiv Automations

Follow [BEEHIIV-INTEGRATION.md](docs/BEEHIIV-INTEGRATION.md) to:
- Create automation sequences in Beehiiv UI
- Enable "Add by API" triggers
- Get automation IDs
- Configure custom fields

### 5. Enroll Your First Subscriber

```bash
python3 email-sequence-manager.py enroll user@example.com welcome A
```

### 6. Process Sequences (Daily Cron)

```bash
python3 email-sequence-manager.py process
```

---

## 📧 Email Sequences

### Welcome Sequence (5 Emails)
**Goal:** Deliver value, build trust, convert to first product

- **Day 0:** Welcome + AI Automation Starter Kit
- **Day 2:** Quick win (15-min automation tutorial)
- **Day 5:** Case study (Sarah's $5K/month story)
- **Day 7:** First offer (Masterclass at $97, 67% off)
- **Day 10:** Urgency (Last chance, expires tonight)

**Expected Performance:**
- Open Rate: 40%+
- Click Rate: 10%+
- Conversion Rate: 2-5%

### Upsell Sequence (4 Emails)
**Trigger:** Downloaded starter kit  
**Goal:** Convert free users to paid customers

- **Day 1:** Check-in (How's the starter kit?)
- **Day 3:** Deep value (The one automation that changed everything)
- **Day 5:** ROI calculation (Your automation potential)
- **Day 7:** Philosophy (Automation vs. hustle)

### Abandoned Cart (3 Emails)
**Trigger:** Clicked pricing but didn't buy  
**Goal:** Recover lost conversions

- **Day 0:** Q&A (Address objections)
- **Day 1:** Bonus offer (Free 1-on-1 setup call)
- **Day 2:** Honest feedback (What's holding you back?)

### Re-Engagement (3 Emails)
**Trigger:** No opens in 30+ days  
**Goal:** Win back or clean list

- **Day 0:** Check-in (Did I lose you?)
- **Day 3:** Final gift (Free playbook download)
- **Day 7:** Goodbye (Auto-unsubscribe warning)

### Product Launch (7 Emails)
**Trigger:** Manual (new product)  
**Goal:** Build excitement and sales

- **Day 0:** Teaser
- **Day 2:** Reveal
- **Day 3:** Behind-the-scenes
- **Day 5:** Early access (50% off)
- **Day 6:** Urgency (12 hours left)
- **Day 7:** Public launch

---

## 🔧 Usage

### Enroll Subscriber in Sequence

```bash
python3 email-sequence-manager.py enroll EMAIL SEQUENCE VARIANT

# Examples:
python3 email-sequence-manager.py enroll john@example.com welcome A
python3 email-sequence-manager.py enroll jane@example.com upsell B
```

### Process Due Emails (Run Daily)

```bash
python3 email-sequence-manager.py process
```

Returns JSON with emails ready to send:
```json
[
  {
    "status": "ready_to_send",
    "email": "user@example.com",
    "subject": "Welcome! Here's Your AI Automation Toolkit",
    "body": "Hey John! 👋\n\n...",
    "sequence": "welcome",
    "step": 0
  }
]
```

### Track Engagement

```bash
# Track email open
python3 engagement-tracker.py open user@example.com welcome 0

# Track link click
python3 engagement-tracker.py click user@example.com welcome 0 "https://site.com/pricing"

# Track conversion
python3 engagement-tracker.py conversion user@example.com "Masterclass" 97.00
```

### Auto-Segment Subscribers

```bash
python3 engagement-tracker.py segment
```

Output:
```json
{
  "active": 150,
  "warm": 320,
  "cold": 180,
  "customer": 45
}
```

### Performance Reports

```bash
# Sequence performance
python3 conversion-optimizer.py analyze welcome

# A/B test comparison
python3 conversion-optimizer.py compare welcome 0

# Best send times
python3 conversion-optimizer.py sendtime

# ROI calculation
python3 conversion-optimizer.py roi

# Subject line insights
python3 conversion-optimizer.py subjects

# Optimization recommendations
python3 conversion-optimizer.py recommend
```

---

## 🎯 Segmentation

Subscribers are automatically segmented based on behavior:

| Segment   | Criteria                                        | Strategy          |
|-----------|-------------------------------------------------|-------------------|
| **Active**| Engagement score ≥10, opened in last 7 days     | Upsells, premium  |
| **Warm**  | Engagement score 5-10, opened in last 30 days   | Value content     |
| **Cold**  | Engagement score <5 or no opens in 30+ days     | Re-engagement     |
| **Customer** | Made a purchase                              | Retention, upsells|

**Engagement Scoring:**
- Open: +1 point
- Click: +3 points
- Reply: +5 points
- Purchase: +20 points

---

## 🔀 Behavioral Triggers

Automatic sequence enrollment based on actions:

| Trigger                     | Enrolls In        | Delay      |
|-----------------------------|-------------------|------------|
| New subscriber              | Welcome           | Immediate  |
| Downloaded starter kit      | Upsell            | 24 hours   |
| Clicked pricing link        | Abandoned Cart    | Same day   |
| No opens in 30 days         | Re-Engagement     | Immediate  |
| Made purchase               | Customer Onboard  | Immediate  |

---

## 📊 Key Metrics

### Email-Level
- **Open Rate:** Opens / Sent
- **Click Rate:** Clicks / Sent
- **Click-to-Open:** Clicks / Opens
- **Conversion Rate:** Conversions / Sent

### Sequence-Level
- **Completion Rate:** % who reach last email
- **Drop-Off Points:** Where subscribers disengage
- **Time to Convert:** Days from enrollment to purchase
- **Revenue per Recipient:** Total revenue / Unique recipients

### Subscriber-Level
- **Engagement Score:** Weighted activity
- **Lifetime Value (LTV):** Total revenue
- **Segment:** Current classification

---

## 🧪 A/B Testing

### Test Variants

Each email sequence supports A/B testing:

```json
{
  "subject_A": "🎁 Your AI Automation Starter Kit is Here",
  "subject_B": "Welcome! Here's Your AI Automation Toolkit"
}
```

Enroll subscribers with variant:
```bash
python3 email-sequence-manager.py enroll user@example.com welcome A
python3 email-sequence-manager.py enroll user2@example.com welcome B
```

Compare results:
```bash
python3 conversion-optimizer.py compare welcome 0
```

Output:
```json
{
  "winner": "A",
  "winning_subject": "🎁 Your AI Automation Starter Kit is Here",
  "improvement": 8.5
}
```

---

## 🔄 Automation Workflow

### Daily Cron Job

```bash
# crontab -e
0 9 * * * cd /path/to/scripts && python3 email-sequence-manager.py process
0 10 * * * cd /path/to/scripts && python3 engagement-tracker.py segment
0 2 * * * cd /path/to/scripts && python3 engagement-tracker.py churn
```

### Webhook Handler (Real-Time Tracking)

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhooks/beehiiv', methods=['POST'])
def beehiiv_webhook():
    data = request.json
    
    if data['event'] == 'email.opened':
        tracker.record_open(data['email'], data['sequence'], data['step'])
    
    elif data['event'] == 'email.clicked':
        tracker.record_click(data['email'], data['sequence'], data['step'], data['url'])
    
    return {"status": "ok"}, 200
```

---

## 💰 Revenue Tracking

### Track Conversions

```python
from scripts.engagement_tracker import EngagementTracker

tracker = EngagementTracker()

# When a purchase happens:
tracker.record_conversion(
    email="user@example.com",
    product="Masterclass",
    amount=97.00
)
```

### Calculate ROI

```bash
python3 conversion-optimizer.py roi
```

Output:
```json
{
  "total_revenue": 12450.00,
  "total_conversions": 128,
  "total_emails_sent": 5600,
  "estimated_cost": 5.60,
  "roi": 222321.43,
  "revenue_per_email": 2.22,
  "by_sequence": [
    {"sequence": "welcome", "revenue": 7280.00},
    {"sequence": "upsell", "revenue": 3200.00},
    {"sequence": "abandoned-cart", "revenue": 1970.00}
  ]
}
```

---

## 🚨 Troubleshooting

### Low Open Rates (<20%)

```bash
# Check subject line performance
python3 conversion-optimizer.py subjects

# Test different send times
python3 conversion-optimizer.py sendtime
```

### Low Conversion Rates (<1%)

```bash
# Get optimization recommendations
python3 conversion-optimizer.py recommend

# Analyze drop-off points
python3 conversion-optimizer.py dropoff welcome
```

### Database Locked Error

```bash
# If SQLite is locked, wait and retry
sleep 1 && python3 email-sequence-manager.py process
```

---

## 📋 Deployment Checklist

**Beehiiv Setup:**
- [ ] Create Beehiiv account (Scale plan recommended)
- [ ] Set up custom fields (engagement_score, segment, ltv)
- [ ] Create automation sequences in UI with "Add by API" trigger
- [ ] Get automation IDs from URLs
- [ ] Generate API key

**Scripts Setup:**
- [ ] Install Python dependencies
- [ ] Set environment variables (BEEHIIV_API_KEY)
- [ ] Initialize database
- [ ] Test API connection
- [ ] Test subscriber enrollment

**Automation:**
- [ ] Set up daily cron jobs (process, segment, churn)
- [ ] Configure webhook endpoint (optional but recommended)
- [ ] Test webhook with mock data

**Monitoring:**
- [ ] Run initial performance report
- [ ] Set up alerts for low open rates
- [ ] Schedule weekly ROI reviews

---

## 📚 Documentation

- **[EMAIL-STRATEGY.md](docs/EMAIL-STRATEGY.md)** - Complete email marketing playbook
- **[BEEHIIV-INTEGRATION.md](docs/BEEHIIV-INTEGRATION.md)** - API setup and integration guide

---

## 🎓 Expected Results

### Phase 1: 0-1,000 Subscribers (Month 1-2)
- Focus: List building + engagement
- Expected Conversion: 2-3%
- Revenue: $500-1,500/month

### Phase 2: 1,000-10,000 Subscribers (Month 3-6)
- Focus: Optimization + scale
- Expected Conversion: 3-5%
- Revenue: $5,000-15,000/month

### Phase 3: 10,000+ Subscribers (Month 6+)
- Focus: Advanced funnels
- Expected Conversion: 5%+
- Revenue: $50,000+/month

---

## 🔐 Compliance

- ✅ **CAN-SPAM:** Unsubscribe link in every email
- ✅ **GDPR:** Data access/deletion on request
- ✅ **Privacy:** No selling/sharing subscriber data
- ✅ **Deliverability:** SPF, DKIM, DMARC configured

---

## 🤝 Contributing

This is a complete, production-ready system. To extend:

1. Add new sequences: Create JSON in `sequences/` directory
2. Add new triggers: Edit `engagement-tracker.py` → `check_triggers()`
3. Add new metrics: Edit `conversion-optimizer.py` → new methods

---

## 📝 License

MIT License - Use freely, build your empire.

---

## 💡 Support

Questions? Issues? Improvements?

- Read the docs: [EMAIL-STRATEGY.md](docs/EMAIL-STRATEGY.md)
- Check Beehiiv API: https://developers.beehiiv.com
- Review code comments in scripts

---

**Built by:** n0mad (n0body AI)  
**For:** AI Automation Builder Newsletter  
**Date:** 2026-03-29  

**Remember:** Perfect is the enemy of done. Ship it, test it, improve it.

🚀 **Now go convert some subscribers.**
