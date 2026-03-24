#!/bin/bash
# Watch for CleverDogMethod notifications and send to Telegram
# Run via cron every 5 minutes

NOTIF_DIR="/root/.openclaw/workspace/.notifications"
SENT_LOG="/root/.openclaw/workspace/.logs/notifications-sent.log"

mkdir -p "$NOTIF_DIR"
mkdir -p "$(dirname "$SENT_LOG")"

# Check for new notifications
for notif_file in "$NOTIF_DIR"/cleverdogmethod-*.txt; do
    [ -f "$notif_file" ] || continue
    
    # Check if already sent
    basename=$(basename "$notif_file")
    if grep -q "$basename" "$SENT_LOG" 2>/dev/null; then
        continue
    fi
    
    # Read message
    message=$(cat "$notif_file")
    
    # Log as sent
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $basename" >> "$SENT_LOG"
    
    # Output message (will be captured by cron and sent to session)
    echo "$message"
    
    # Archive notification
    mv "$notif_file" "$NOTIF_DIR/sent-$(basename "$notif_file")"
done
