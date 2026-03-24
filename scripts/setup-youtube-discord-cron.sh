#!/bin/bash
# Setup cron job to check YouTube → Discord every 15 minutes

SCRIPT="/root/.openclaw/workspace/scripts/youtube-to-discord.py"

# Add cron job (runs every 15 minutes)
(crontab -l 2>/dev/null; echo "*/15 * * * * /usr/bin/python3 $SCRIPT >> /root/.openclaw/workspace/logs/youtube-discord.log 2>&1") | crontab -

echo "✅ Cron job added:"
echo "   Checks every 15 minutes"
echo "   Logs: ~/.openclaw/workspace/logs/youtube-discord.log"
echo ""
echo "To remove: crontab -e (delete the line)"

# Create logs dir
mkdir -p /root/.openclaw/workspace/logs

# Test run
echo ""
echo "🧪 Testing now..."
python3 $SCRIPT
