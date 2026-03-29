#!/bin/bash
#
# Growth Engine - Master automation orchestrator
#
# Runs all growth systems in sequence:
# 1. Publish new blog posts (2/day)
# 2. Add viral mechanisms to new posts
# 3. Crosspost to Medium/Dev.to
# 4. Distribute to Reddit/social
# 5. Track metrics
# 6. Generate reports
#
# Run via cron: 0 10,16 * * * (10am & 4pm UTC)
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOG_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$BLOG_DIR/logs"
LOG_FILE="$LOG_DIR/growth-engine-$(date +%Y-%m-%d).log"

mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "============================================================"
log "🚀 GROWTH ENGINE STARTED"
log "============================================================"

# ============================================================================
# 1. PUBLISH NEW BLOG POSTS
# ============================================================================

log ""
log "📝 Step 1: Publishing new blog posts..."

cd "$BLOG_DIR"

if python3 "$SCRIPT_DIR/blog-auto-post.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Blog posts published"
else
    log "⚠️  Blog publishing failed (check logs)"
fi

# ============================================================================
# 2. ADD VIRAL MECHANISMS
# ============================================================================

log ""
log "🔥 Step 2: Adding viral mechanisms to new posts..."

if python3 "$SCRIPT_DIR/add-viral-mechanisms.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Viral mechanisms added"
else
    log "⚠️  Viral mechanisms failed (check logs)"
fi

# ============================================================================
# 3. CROSSPOST TO PLATFORMS
# ============================================================================

log ""
log "📢 Step 3: Crossposting to Medium/Dev.to..."

if python3 "$SCRIPT_DIR/crosspost-platforms.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Crossposting complete"
else
    log "⚠️  Crossposting failed (check logs)"
fi

# ============================================================================
# 4. SOCIAL MEDIA DISTRIBUTION
# ============================================================================

log ""
log "📱 Step 4: Distributing to social media..."

# Reddit (smart distribution)
if python3 "$SCRIPT_DIR/smart-reddit-distribute.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Reddit distribution complete"
else
    log "⚠️  Reddit distribution failed (check logs)"
fi

# Twitter/LinkedIn (via newsletter auto-distribute if newsletter published)
# This runs separately after newsletter is sent

# ============================================================================
# 5. TRACK METRICS
# ============================================================================

log ""
log "📊 Step 5: Tracking growth metrics..."

if python3 "$SCRIPT_DIR/growth-tracker.py" >> "$LOG_FILE" 2>&1; then
    log "✅ Metrics tracked"
else
    log "⚠️  Metrics tracking failed (check logs)"
fi

# ============================================================================
# 6. CLEANUP & DEPLOY
# ============================================================================

log ""
log "🚀 Step 6: Deploying to GitHub Pages..."

cd "$BLOG_DIR/blog"

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Auto-update: $(date +'%Y-%m-%d %H:%M UTC')" >> "$LOG_FILE" 2>&1 || true
    
    # Push to GitHub
    if git push origin main >> "$LOG_FILE" 2>&1; then
        log "✅ Deployed to GitHub Pages"
    else
        log "⚠️  Deployment failed (check logs)"
    fi
else
    log "✓ No changes to deploy"
fi

# ============================================================================
# SUMMARY
# ============================================================================

log ""
log "============================================================"
log "✅ GROWTH ENGINE COMPLETED"
log "============================================================"

# Count actions
POSTS_TODAY=$(find "$BLOG_DIR/blog/posts" -name "*.html" -mtime -1 | wc -l)
log "Posts published today: $POSTS_TODAY"

# Send Telegram notification (if configured)
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    MESSAGE="🤖 *Growth Engine Report*

✅ Growth cycle complete
📝 Posts published: $POSTS_TODAY
🚀 Deployed to GitHub Pages
⏰ $(date +'%Y-%m-%d %H:%M UTC')

View blog: https://aiautomationbuilder.com"

    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$TELEGRAM_CHAT_ID" \
        -d "text=$MESSAGE" \
        -d "parse_mode=Markdown" \
        > /dev/null 2>&1 || true
    
    log "✅ Telegram notification sent"
fi

log ""
log "📋 Full log: $LOG_FILE"
log ""

# Exit successfully
exit 0
