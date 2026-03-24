#!/usr/bin/env python3
"""
Fetch latest ClawTV video and post to Discord
Usage: Just run it when user says "subí video en clawtv"
"""

import requests
import feedparser
import json

YOUTUBE_CHANNEL_ID = "UChBdWwiR29C7nT8nIXJuAfA"  # @ClawTV_YT
DISCORD_CHANNEL_ID = "1484992372680032308"  # #new-videos
DISCORD_BOT_TOKEN_FILE = "/root/.openclaw/workspace/.credentials/discord-tokens.json"

def get_bot_token():
    with open(DISCORD_BOT_TOKEN_FILE) as f:
        data = json.load(f)
        return data['clawtv']['bot_token']

def get_latest_video():
    """Fetch latest video from YouTube RSS"""
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
    
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            latest = feed.entries[0]
            return {
                "video_id": latest.yt_videoid,
                "title": latest.title,
                "url": latest.link,
                "published": latest.published
            }
    except Exception as e:
        print(f"❌ Error fetching video: {e}")
    
    return None

def post_to_discord(video):
    """Post video to Discord"""
    bot_token = get_bot_token()
    
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    
    embed = {
        "title": f"🎥 {video['title']}",
        "description": "New video just dropped! Check it out 👇",
        "url": video['url'],
        "color": 0xFF0000,
        "thumbnail": {
            "url": f"https://i.ytimg.com/vi/{video['video_id']}/maxresdefault.jpg"
        },
        "footer": {
            "text": "ClawTV • OpenClaw Automation"
        }
    }
    
    message = {
        "content": "@everyone **New video is live!** 🔥",
        "embeds": [embed]
    }
    
    url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages"
    response = requests.post(url, headers=headers, json=message)
    
    if response.status_code == 200:
        print(f"✅ Posted to Discord: {video['title']}")
        print(f"📺 {video['url']}")
        return True
    else:
        print(f"❌ Discord error {response.status_code}: {response.text}")
        return False

if __name__ == '__main__':
    print("🔍 Fetching latest ClawTV video...")
    
    video = get_latest_video()
    
    if not video:
        print("❌ No video found")
    else:
        print(f"📹 Found: {video['title']}")
        print(f"📺 {video['url']}")
        print()
        post_to_discord(video)
