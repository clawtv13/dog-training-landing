# 🚀 Getting Started with AI Automation Builder

Quick setup guide to get your newsletter running.

---

## Prerequisites

- Python 3.10+
- Beehiiv account (free tier OK for <2.5K subs)
- OpenRouter account (for Claude API access)

---

## Step 1: Install Dependencies

```bash
cd /root/.openclaw/workspace/newsletter-ai-automation

# Install required packages
pip3 install -r requirements.txt
```

---

## Step 2: Configure API Keys

```bash
# Copy example env file
cp .env.example .env

# Edit with your keys
nano .env
```

**Minimum required:**
- `OPENROUTER_API_KEY` - For Claude content generation
- `BEEHIIV_API_KEY` - For newsletter publishing
- `BEEHIIV_PUBLICATION_ID` - Your publication ID

**Optional (but recommended):**
- `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` - For Reddit monitoring
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` - For notifications

---

## Step 3: Test the System

### Test Daily Research

```bash
python3 scripts/daily-research.py
```

This will:
- ✅ Fetch content from RSS feeds, Reddit, etc
- ✅ Score items with Claude
- ✅ Save to database

**Expected output:** 20-50 high-quality items collected

### Test Weekly Generation

```bash
python3 scripts/weekly-generate.py
```

This will:
- ✅ Pull top content from database
- ✅ Generate newsletter with Claude
- ✅ Create draft in Beehiiv
- ✅ Notify via Telegram

**Expected output:** Draft edition ready for review

---

## Step 4: Setup Automation

### Option A: Cron (Recommended)

```bash
# Edit crontab
crontab -e

# Add these lines:

# Daily research at 09:00 UTC
0 9 * * * cd /root/.openclaw/workspace/newsletter-ai-automation && python3 scripts/daily-research.py >> logs/research.log 2>&1

# Weekly generation Wednesday 10:00 UTC
0 10 * * 3 cd /root/.openclaw/workspace/newsletter-ai-automation && python3 scripts/weekly-generate.py >> logs/generate.log 2>&1
```

### Option B: Manual Execution

Run scripts manually when needed:
```bash
# Research
./scripts/daily-research.py

# Generate edition
./scripts/weekly-generate.py
```

---

## Step 5: Review & Publish Workflow

### Wednesday (Generation Day)

1. ✅ Script runs at 10:00 UTC automatically
2. ✅ Draft created in Beehiiv
3. ✅ Telegram notification sent

### Thursday (Review Day)

1. 📧 Open Beehiiv dashboard
2. 📝 Review draft edition
3. ✏️ Edit if needed (grammar, links, etc)
4. ⏰ Schedule for Friday 08:00 UTC

### Friday (Publish Day)

1. 📤 Beehiiv auto-sends to subscribers
2. 📊 Monitor open/click rates
3. 💬 Respond to replies

---

## Typical Week Schedule

| Day | Time (UTC) | Action | Who |
|-----|-----------|--------|-----|
| Mon | 09:00 | Daily research | Automated |
| Tue | 09:00 | Daily research | Automated |
| **Wed** | 09:00 | Daily research | Automated |
| **Wed** | 10:00 | **Generate edition** | **Automated** |
| **Thu** | Anytime | **Review draft** | **Manual** |
| **Thu** | EOD | **Schedule send** | **Manual** |
| **Fri** | 08:00 | **Publish** | **Automated** |
| Fri | 09:00 | Daily research | Automated |
| Sat | 09:00 | Daily research | Automated |
| Sun | 09:00 | Daily research | Automated |

**Total manual time:** ~30 min/week (Thursday review)

---

## Troubleshooting

### "No content items in database"

Run research script first:
```bash
python3 scripts/daily-research.py
```

Need at least 5 items for generation.

### "OpenRouter API error"

Check your API key:
```bash
echo $OPENROUTER_API_KEY
```

Verify credits: https://openrouter.ai/credits

### "Beehiiv API 401"

Your API key might be invalid. Regenerate at:
https://app.beehiiv.com/settings/integrations/api

### Database locked

Another process might be accessing it:
```bash
# Check running processes
ps aux | grep daily-research

# Kill if stuck
pkill -f daily-research
```

---

## Monitoring

### Check Database Stats

```bash
# Open database
sqlite3 database/newsletter.db

# Count content items
SELECT COUNT(*) FROM content_items;

# See recent items
SELECT title, total_score FROM content_items 
ORDER BY created_at DESC LIMIT 10;

# Exit
.quit
```

### View Logs

```bash
# Research logs
tail -f logs/research.log

# Generation logs
tail -f logs/generate.log
```

### Check State Files

```bash
# Last research run
cat .state/daily-research-state.json

# Last generation
cat .state/weekly-generate-state.json
```

---

## Growing Your Newsletter

See [GROWTH-TACTICS.md](./GROWTH-TACTICS.md) for detailed strategies on:
- Reddit posting
- Twitter threads
- Referral programs
- Paid ads
- Partnership swaps

---

## Support

- **Documentation:** `/docs/` folder
- **Issues:** Check logs in `/logs/`
- **Questions:** Review FAQ.md

---

**Next:** Read [CONTENT-GUIDELINES.md](./CONTENT-GUIDELINES.md) for editorial standards.
