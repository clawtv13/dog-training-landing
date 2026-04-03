#!/bin/bash
# Wrapper script to run analytics dashboard with proper environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Try to extract Telegram credentials from openclaw config
# If not available, the script will still run but won't send messages
if command -v openclaw &> /dev/null; then
    # Extract token - this may fail if not configured, that's OK
    TOKEN=$(openclaw config 2>/dev/null | grep -A5 "telegram:" | grep "token:" | cut -d':' -f2- | xargs || echo "")
    
    if [ -n "$TOKEN" ]; then
        export TELEGRAM_BOT_TOKEN="$TOKEN"
    fi
fi

# Chat ID is hardcoded as per task spec
export TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-8116230130}"

# Run the analytics dashboard
python3 "$SCRIPT_DIR/analytics-dashboard.py" "$@"
