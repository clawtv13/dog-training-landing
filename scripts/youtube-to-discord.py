#!/usr/bin/env python3
"""
Auto-post new YouTube videos to Discord
Checks RSS feed every 15 minutes, posts new videos to #tutorials
"""

import requests
import feedparser
import json
import time
from datetime import datetime

# Config
CHANNEL_CONFIGS = {
    "clawtv": {
        "youtube_id": "UChBdWwiR29C7nT8nIXJuAfA",  # @ClawTV_YT channel ID
        "discord_channel": "1484939224372215921",  # #tutorials channel ID
        "last_video_file": "/root/.openclaw/workspace/.state/clawtv-last-video.txt"
    }
}

DISCORD_BOT_TOKEN_FILE = "/root/.openclaw/workspace/.credentials/discord-tokens.json"

def get_bot_token():
    """Load Discord bot token"""
    with open(DISCORD_BOT_TOKEN_FILE) as f:
        data = json.load(f)
        return data['clawtv']['bot_token']

def get_latest_video(youtube_channel_id):
    """Fetch latest video from YouTube RSS feed"""
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={youtube_channel_id}"
    
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            latest = feed.entries[0]
            return {
                "video_id": latest.yt_videoid,
                "title": latest.title,
                "url": latest.link,
                "published": latest.published,
                "author": latest.author
            }
    except Exception as e:
        print(f"❌ Error fetching RSS: {e}")
    
    return None

def get_last_posted_video_id(last_video_file):
    """Read last posted video ID from file"""
    try:
        with open(last_video_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_posted_video_id(last_video_file, video_id):
    """Save last posted video ID to file"""
    import os
    os.makedirs(os.path.dirname(last_video_file), exist_ok=True)
    with open(last_video_file, 'w') as f:
        f.write(video_id)

def post_to_discord(bot_token, channel_id, video):
    """Post video to Discord channel with embed"""
    
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    
    # Create rich embed
    embed = {
        "title": f"🎥 New Video: {video['title']}",
        "description": f"New tutorial just dropped! Check it out 👇",
        "url": video['url'],
        "color": 0xFF0000,  # YouTube red
        "fields": [
            {
                "name": "📺 Channel",
                "value": video['author'],
                "inline": True
            },
            {
                "name": "🕐 Published",
                "value": video['published'],
                "inline": True
            }
        ],
        "thumbnail": {
            "url": f"https://i.ytimg.com/vi/{video['video_id']}/maxresdefault.jpg"
        },
        "footer": {
            "text": "ClawTV • OpenClaw Automation"
        }
    }
    
    message = {
        "content": f"@everyone **New video is live!** 🔥",
        "embeds": [embed]
    }
    
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    response = requests.post(url, headers=headers, json=message)
    
    if response.status_code == 200:
        print(f"✅ Posted to Discord: {video['title']}")
        return True
    else:
        print(f"❌ Discord error {response.status_code}: {response.text}")
        return False

def check_and_post(config_name):
    """Check for new video and post if found"""
    config = CHANNEL_CONFIGS[config_name]
    bot_token = get_bot_token()
    
    # Get latest video
    latest_video = get_latest_video(config['youtube_id'])
    if not latest_video:
        print(f"⚠️ No videos found for {config_name}")
        return
    
    # Check if already posted
    last_posted = get_last_posted_video_id(config['last_video_file'])
    
    if latest_video['video_id'] == last_posted:
        print(f"✓ No new videos for {config_name}")
        return
    
    # New video detected!
    print(f"🆕 New video detected: {latest_video['title']}")
    
    # Post to Discord
    if post_to_discord(bot_token, config['discord_channel'], latest_video):
        save_last_posted_video_id(config['last_video_file'], latest_video['video_id'])
        print(f"💾 Saved video ID: {latest_video['video_id']}")

def run_once():
    """Run check once for all channels"""
    print(f"\n{'='*60}")
    print(f"🔍 Checking for new videos... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    for config_name in CHANNEL_CONFIGS:
        check_and_post(config_name)

def run_daemon(interval_minutes=15):
    """Run continuously, checking every N minutes"""
    print(f"🤖 YouTube → Discord bot started")
    print(f"📡 Checking every {interval_minutes} minutes")
    print(f"🛑 Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            run_once()
            print(f"\n💤 Sleeping {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print(f"🔄 Retrying in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        # Run as background daemon
        run_daemon(interval_minutes=15)
    else:
        # Run once (for testing or cron)
        run_once()
