# Quick Reference Card - Email Sequence System

**Location:** `/root/.openclaw/workspace/newsletter-ai-automation/`

---

## 🚀 Quick Start (5 Minutes)

```bash
cd /root/.openclaw/workspace/newsletter-ai-automation

# 1. Set API key
export BEEHIIV_API_KEY="your_key_here"

# 2. Initialize (creates database)
python3 scripts/email-sequence-manager.py

# 3. Enroll first subscriber
python3 scripts/email-sequence-manager.py enroll user@example.com welcome A

# 4. Process sequences (run daily)
python3 scripts/email-sequence-manager.py process
```

---

## 📧 Sequences Available

| Sequence | Emails | Trigger | Goal |
|----------|--------|---------|------|
| **welcome** | 5 | New subscriber | Convert to $97 product |
| **upsell** | 4 | Downloaded lead magnet | Free → Paid |
| **abandoned-cart** | 3 | Clicked pricing | Recover conversion |
| **re-engagement** | 3 | No opens 30 days | Win back or clean |
| **product-launch** | 7 | Manual | Launch excitement |

---

## 🔧 Common Commands

### Enrollment
```bash
# Enroll in welcome (variant A)
python3 scripts/email-sequence-manager.py enroll EMAIL welcome A

# Enroll in upsell (variant B)
python3 scripts/email-sequence-manager.py enroll EMAIL upsell B
```

### Processing
```bash
# Process all due emails (run daily)
python3 scripts/email-sequence-manager.py process

# Get performance report
python3 scripts/email-sequence-manager.py report welcome
```

### Tracking
```bash
# Track open
python3 scripts/engagement-tracker.py open EMAIL welcome 0

# Track click
python3 scripts/engagement-tracker.py click EMAIL welcome 0 "https://url.com"

# Track conversion
python3 scripts/engagement-tracker.py conversion EMAIL "Product" 97.00

# Auto-segment all subscribers
python3 scripts/engagement-tracker.py segment

# Get engagement report
python3 scripts/engagement-tracker.py report
```

### Analytics
```bash
# Analyze sequence performance
python3 scripts/conversion-optimizer.py analyze welcome

# Compare A/B variants
python3 scripts/conversion-optimizer.py compare welcome 0

# Best send times
python3 scripts/conversion-optimizer.py sendtime

# ROI calculation
python3 scripts/conversion-optimizer.py roi

# Subject line insights
python3 scripts/conversion-optimizer.py subjects

# Get recommendations
python3 scripts/conversion-optimizer.py recommend
```

---

## 🎯 Segments

| Segment | Criteria | Strategy |
|---------|----------|----------|
| **active** | Score ≥10, opened <7d | Upsells, premium |
| **warm** | Score 5-10, opened <30d | Value content |
| **cold** | Score <5 or no opens 30d+ | Re-engage |
| **customer** | Made purchase | Retention, upsell |

**Engagement Scoring:**
- Open: +1
- Click: +3
- Reply: +5
- Purchase: +20

---

## 🔀 Behavioral Triggers

| Action | → | Sequence |
|--------|---|----------|
| New subscriber | → | Welcome |
| Downloaded lead magnet | → | Upsell |
| Clicked pricing | → | Abandoned cart |
| No opens 30 days | → | Re-engagement |
| Made purchase | → | Customer onboard |

---

## 📊 Target Metrics

| Metric | Target | Industry |
|--------|--------|----------|
| Open Rate | 40%+ | 20-25% |
| Click Rate | 10%+ | 2-5% |
| Conversion | 2-5% | 1-2% |
| Unsubscribe | <1% | 0.5-1% |

---

## 🔄 Daily Automation

```bash
# Add to crontab: crontab -e

# 9 AM: Process due emails
0 9 * * * cd /path/to/newsletter-ai-automation && python3 scripts/email-sequence-manager.py process

# 10 AM: Auto-segment
0 10 * * * cd /path/to/newsletter-ai-automation && python3 scripts/engagement-tracker.py segment

# 2 AM: Churn detection
0 2 * * * cd /path/to/newsletter-ai-automation && python3 scripts/engagement-tracker.py churn
```

---

## 📁 Key Files

### Scripts
- `email-sequence-manager.py` - Core automation
- `engagement-tracker.py` - Behavioral tracking
- `conversion-optimizer.py` - Analytics

### Sequences
- `welcome.json` - 5-email welcome
- `upsell.json` - 4-email upsell
- `abandoned-cart.json` - 3-email recovery
- `re-engagement.json` - 3-email win-back
- `product-launch.json` - 7-email launch

### Docs
- `README.md` - Quick start
- `EMAIL-STRATEGY.md` - Complete playbook
- `BEEHIIV-INTEGRATION.md` - API guide
- `DELIVERABLES-SUMMARY.md` - Full inventory

---

## 🐛 Troubleshooting

### Low Open Rates
```bash
python3 scripts/conversion-optimizer.py subjects
python3 scripts/conversion-optimizer.py sendtime
```

### Low Conversions
```bash
python3 scripts/conversion-optimizer.py recommend
python3 scripts/conversion-optimizer.py dropoff welcome
```

### Database Issues
```bash
# Check database exists
ls -lh email_sequences.db

# Re-initialize if needed
rm email_sequences.db
python3 scripts/email-sequence-manager.py
```

---

## 💰 Pricing Strategy

| Product | Regular | Discount | When |
|---------|---------|----------|------|
| Starter Kit | FREE | - | Lead magnet |
| Masterclass | $297 | $97 (67%) | Welcome seq |
| Advanced | $497 | $297 | Upsell |
| Consulting | $2000 | $500/hr | VIP only |

**Target LTV:** $50-500 per customer

---

## 🎯 Expected Results

### Phase 1: 0-1K subs (Month 1-2)
- Conv: 2-3%
- Revenue: $500-1,500/mo

### Phase 2: 1K-10K subs (Month 3-6)
- Conv: 3-5%
- Revenue: $5K-15K/mo

### Phase 3: 10K+ subs (Month 6+)
- Conv: 5%+
- Revenue: $50K+/mo

---

## 📞 Need Help?

1. Read `README.md`
2. Check `EMAIL-STRATEGY.md`
3. Review `BEEHIIV-INTEGRATION.md`
4. Check code comments in scripts

---

**Quick Tip:** Start with welcome sequence only. Get it working. Add others later.

**Remember:** Ship > Perfect. Test. Iterate. Scale.

---

*Last Updated: 2026-03-29*
