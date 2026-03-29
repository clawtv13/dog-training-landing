# Cron Configuration for Master Content Agent V3

## 📅 Recommended Schedule

### Production Schedule (2 posts/day)

```cron
# Master Content Agent V3 - Blog Auto-Posting
0 9 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Times:**
- 9:00 AM UTC (Morning post)
- 5:00 PM UTC (Afternoon post)

**Why these times:**
- Spread out throughout day
- Allows monitoring between runs
- Aligns with peak reader times (US/EU timezones)

---

## 🔧 Installation

### 1. Edit Crontab

```bash
crontab -e
```

### 2. Add Master Agent Lines

Paste:
```cron
# AI Automation Blog - Master Content Agent V3
OPENROUTER_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

0 9 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 17 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

### 3. Verify

```bash
crontab -l | grep master-content-agent
```

Should show 2 lines (9:00 and 17:00).

---

## 📊 Alternative Schedules

### Aggressive (3 posts/day)

```cron
0 8 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 14 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 20 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Cost:** ~$4.50-$5.40/month

### Conservative (1 post/day)

```cron
0 10 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Cost:** ~$1.50-$1.80/month

### Weekdays Only

```cron
0 9 * * 1-5 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
0 17 * * 1-5 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

**Posts:** 10/week (~43/month)

---

## 🔍 Monitoring

### Check Last Run

```bash
tail -50 logs/cron.log
```

### Check Today's Posts

```bash
ls -lh blog/posts/*$(date +%Y-%m-%d)*.html
```

### View Quality Scores

```bash
jq -r '.[] | select(.published_at | startswith("'$(date +%Y-%m-%d)'")) | "\(.title): \(.quality_score)/100"' .state/published-posts.json
```

### Cron Email Notifications

Add to crontab for email alerts on errors:

```cron
MAILTO=your-email@example.com

0 9 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

---

## 🚨 Error Handling

### Cron Doesn't Run

**Check cron service:**
```bash
systemctl status cron
```

**Check cron logs:**
```bash
grep CRON /var/log/syslog | tail -20
```

### Script Fails Silently

**Check permissions:**
```bash
chmod +x scripts/master-content-agent.py
```

**Check Python path:**
```bash
which python3
```

**Update cron with full path:**
```cron
0 9 * * * cd /root/.openclaw/workspace/ai-automation-blog && /usr/bin/python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

### API Key Not Found

**Set in crontab header:**
```cron
OPENROUTER_API_KEY=sk-...
```

Or use systemd environment file (more secure).

---

## 📈 Health Check Cron

**Optional:** Add daily health check

```cron
0 8 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/health-check.py >> logs/health.log 2>&1
```

Checks:
- API key valid
- Newsletter DB accessible
- Git repo healthy
- Recent posts exist
- Quality scores in range

---

## 🧪 Test Run

Before enabling cron, test manually:

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/master-content-agent.py
```

Should complete in 3-5 minutes with:
```
✅ MASTER CONTENT AGENT COMPLETE
```

---

## 📝 Log Rotation

Prevent log files from growing too large:

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/master-content-agent
```

Add:
```
/root/.openclaw/workspace/ai-automation-blog/logs/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 🔐 Security Best Practices

### 1. Don't store API keys in crontab

**Use environment file:**
```bash
# Create secure env file
echo "export OPENROUTER_API_KEY='sk-...'" > ~/.master-agent-env
chmod 600 ~/.master-agent-env
```

**Update cron:**
```cron
0 9 * * * source ~/.master-agent-env && cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/master-content-agent.py >> logs/cron.log 2>&1
```

### 2. Restrict log file permissions

```bash
chmod 600 logs/*.log
```

### 3. Use systemd timer (alternative to cron)

More robust, better logging:

```bash
# Create systemd service
sudo nano /etc/systemd/system/master-content-agent.service
```

```ini
[Unit]
Description=Master Content Agent V3
After=network.target

[Service]
Type=oneshot
User=root
WorkingDirectory=/root/.openclaw/workspace/ai-automation-blog
EnvironmentFile=/root/.master-agent-env
ExecStart=/usr/bin/python3 scripts/master-content-agent.py
StandardOutput=append:/root/.openclaw/workspace/ai-automation-blog/logs/cron.log
StandardError=append:/root/.openclaw/workspace/ai-automation-blog/logs/cron.log

[Install]
WantedBy=multi-user.target
```

Create timer:
```bash
sudo nano /etc/systemd/system/master-content-agent.timer
```

```ini
[Unit]
Description=Run Master Content Agent twice daily

[Timer]
OnCalendar=09:00
OnCalendar=17:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl enable master-content-agent.timer
sudo systemctl start master-content-agent.timer
sudo systemctl status master-content-agent.timer
```

---

## 📊 Cron Monitoring Dashboard

**Create simple status page:**

```bash
# Add to crontab for daily summary
0 22 * * * cd /root/.openclaw/workspace/ai-automation-blog && python3 -c "
import json
from datetime import datetime

# Load today's posts
with open('.state/published-posts.json') as f:
    posts = json.load(f)

today = datetime.now().date().isoformat()
today_posts = [p for p in posts if p['published_at'].startswith(today)]

print(f'📊 Daily Summary - {today}')
print(f'Posts: {len(today_posts)}')
if today_posts:
    avg_score = sum(p['quality_score'] for p in today_posts) / len(today_posts)
    print(f'Avg Quality: {avg_score:.1f}/100')
    for p in today_posts:
        print(f'  • {p[\"title\"][:60]}... ({p[\"quality_score\"]}/100)')
" >> logs/daily-summary.log
```

---

## ✅ Cron Checklist

Before going live:

- [ ] Cron entries added
- [ ] API keys set (secure method)
- [ ] Test run completes successfully
- [ ] Logs directory writable
- [ ] Git credentials configured
- [ ] Telegram notifications work (if enabled)
- [ ] Logrotate configured
- [ ] Monitoring set up

---

## 📞 Quick Reference

**View crontab:**
```bash
crontab -l
```

**Edit crontab:**
```bash
crontab -e
```

**Disable cron temporarily:**
```bash
crontab -l > /tmp/crontab.backup
crontab -r  # Remove all cron jobs
```

**Re-enable:**
```bash
crontab /tmp/crontab.backup
```

**Check if cron ran today:**
```bash
ls -lh blog/posts/*$(date +%Y-%m-%d)*.html
```

---

**Status:** Production-ready  
**Recommended:** 2 posts/day (9:00, 17:00 UTC)  
**Cost:** ~$3.00-$3.60/month
