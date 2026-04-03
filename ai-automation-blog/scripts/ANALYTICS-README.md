# Analytics Dashboard

Weekly Telegram report with charts and insights for the AI Automation Blog.

## Features

### 📊 Report Sections

1. **Summary Stats**
   - Posts this week / month
   - Avg quality score (current week vs last week)
   - Trend indicator: ↗️ improving / ↘️ declining / → stable

2. **Top Performers** (this week)
   - Top 5 posts by quality_score
   - Shows: title, score, topic classification

3. **Topic Distribution** (pie chart)
   - Automatically classifies posts into topics:
     - AI Tools
     - Development
     - Business
     - Security/Privacy
     - Systems
     - Other
   - Generates matplotlib pie chart → saves PNG

4. **A/B Test Results** (if active)
   - Reads `prompts/ab-test.json`
   - Compares variant A vs B performance
   - Declares winner if statistically significant (>10% difference, 5+ samples)

5. **Recommendations**
   - "Post more about {top_topic}"
   - "Quality improved by {X}% this week"
   - "Consider promoting prompt variant {X}"
   - Volume recommendations

### 📤 Delivery

- **Telegram**: Sends text summary + chart as photo
- **Markdown**: Saves full report to `reports/YYYY-MM-DD.md`
- **Chart**: Saves pie chart to `reports/topic-distribution-YYYY-MM-DD.png`

## Usage

### Manual Run

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/analytics-dashboard.py
```

### With Wrapper (recommended)

```bash
cd /root/.openclaw/workspace/ai-automation-blog
bash scripts/run-analytics.sh
```

### Scheduled (Cron)

Run weekly on Monday mornings:

```bash
0 9 * * 1 cd /root/.openclaw/workspace/ai-automation-blog && bash scripts/run-analytics.sh
```

## Configuration

### Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="8116230130"  # Default is already set
```

The wrapper script (`run-analytics.sh`) attempts to extract the token from OpenClaw config automatically.

### A/B Testing

Edit `prompts/ab-test.json`:

```json
{
  "active": true,
  "variants": {
    "A": { "name": "Control", "description": "Baseline" },
    "B": { "name": "Enhanced", "description": "Quality focused" }
  }
}
```

Then tag posts with `"prompt_variant": "A"` or `"B"` in analytics data.

## Data Sources

### Primary

- `.state/analytics.json` - Post metrics and performance data
- `.state/published-posts.json` - Published post metadata

### Optional

- `prompts/ab-test.json` - A/B test configuration
- `../newsletter-ai-automation/database/newsletter.db` - Source content quality scores

## Output

### Report Structure

```
📊 Weekly Analytics Report
_2026-04-02_

📝 Summary Stats
• Posts this week: 20
• Avg quality score: 39.0 (prev: 39.0)
• Trend: → stable

🏆 Top Performers (this week)
1. Post Title (Score: 39 | Topic: AI Tools)
...

📊 Topic Distribution
• AI Tools: 19 posts (95.0%)
• Systems: 1 posts (5.0%)

💡 Recommendations
• 📈 Post more about AI Tools
```

## Dependencies

```bash
pip3 install matplotlib requests
```

Or with system packages flag:

```bash
pip3 install matplotlib requests --break-system-packages
```

## Troubleshooting

### "No analytics data found"

Check that `.state/analytics.json` exists and has post data:

```bash
cat .state/analytics.json | jq '.posts | length'
```

### "Telegram credentials not configured"

The script will still generate reports locally. To enable Telegram:

1. Export `TELEGRAM_BOT_TOKEN` environment variable
2. Or configure OpenClaw Telegram integration
3. Or use the wrapper script which attempts to auto-detect

### Charts not generating

Ensure matplotlib is installed and you have write permissions:

```bash
python3 -c "import matplotlib; print('✅ OK')"
ls -ld reports/
```

## Testing

Run once to verify:

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/analytics-dashboard.py

# Check outputs
ls -lh reports/
cat reports/2026-04-02.md
```

## Performance

- **Runtime**: ~2-3 seconds for 20 posts
- **Memory**: <100MB
- **Output size**: ~50KB (chart + markdown)

## Future Enhancements

- [ ] Multi-week trend charts
- [ ] Email report option
- [ ] Engagement tracking from external analytics
- [ ] Custom topic classifiers
- [ ] HTML report generation
- [ ] Slack integration
- [ ] Comparative analysis vs competitors
