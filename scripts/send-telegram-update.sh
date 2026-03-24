#!/bin/bash
# Send Telegram notification for CleverDogMethod posts
# Usage: ./send-telegram-update.sh <notification-file>

NOTIF_FILE="$1"

if [ ! -f "$NOTIF_FILE" ]; then
    echo "❌ Notification file not found: $NOTIF_FILE"
    exit 1
fi

MESSAGE=$(cat "$NOTIF_FILE")

# Send via openclaw message (routes to your Telegram automatically)
echo "$MESSAGE"

# Also log it
LOG_DIR="/root/.openclaw/workspace/.logs"
mkdir -p "$LOG_DIR"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] $MESSAGE" >> "$LOG_DIR/telegram-notifications.log"

echo "✅ Notification sent"
