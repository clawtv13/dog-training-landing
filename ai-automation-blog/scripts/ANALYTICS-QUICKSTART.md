# 🚀 Analytics Dashboard - Quick Start

## Run Now

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/analytics-dashboard.py
```

## What You Get

📊 **Weekly Report** with:
- Summary stats (posts, quality scores, trends)
- Top 5 performing posts
- Topic distribution pie chart
- A/B test results (if active)
- Actionable recommendations

📤 **Delivered via**:
- Telegram message (text summary)
- Telegram photo (pie chart)
- Markdown file (`reports/YYYY-MM-DD.md`)

## Enable Telegram

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
export TELEGRAM_CHAT_ID="8116230130"  # Already set as default
python3 scripts/analytics-dashboard.py
```

Or use the wrapper:

```bash
bash scripts/run-analytics.sh  # Auto-detects token from OpenClaw
```

## Schedule Weekly

```bash
# Every Monday at 9 AM
crontab -e
# Add this line:
0 9 * * 1 cd /root/.openclaw/workspace/ai-automation-blog && bash scripts/run-analytics.sh
```

## Output Location

- 📊 Charts: `reports/topic-distribution-YYYY-MM-DD.png`
- 📄 Reports: `reports/YYYY-MM-DD.md`

## Full Docs

See `scripts/ANALYTICS-README.md` for complete documentation.
