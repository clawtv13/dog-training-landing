#!/usr/bin/env python3
"""
Manual post video to Discord
Usage: python3 post-video-discord.py https://youtu.be/VIDEO_ID
"""

import requests
import json
import sys
import re

DISCORD_CHANNEL_ID = "1484992372680032308"  # #new-videos
DISCORD_BOT_TOKEN_FILE = "/root/.openclaw/workspace/.credentials/discord-tokens.json"

def get_bot_token():
    with open(DISCORD_BOT_TOKEN_FILE) as f:
        data = json.load(f)
        return data['clawtv']['bot_token']

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'youtu\.be/([^?&]+)',
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtube\.com/shorts/([^?&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    """Fetch video title from oembed API (no auth needed)"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()['title']
    except:
        pass
    return None

def post_video(video_url, video_id, title):
    """Post video to Discord"""
    bot_token = get_bot_token()
    
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    
    embed = {
        "title": f"🎥 {title}",
        "description": "New video just dropped! Check it out 👇",
        "url": video_url,
        "color": 0xFF0000,
        "thumbnail": {
            "url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
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
        print(f"✅ Posted to Discord: {title}")
        return True
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 post-video-discord.py https://youtu.be/VIDEO_ID")
        sys.exit(1)
    
    video_url = sys.argv[1]
    
    # Extract video ID
    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ Invalid YouTube URL")
        sys.exit(1)
    
    print(f"📹 Video ID: {video_id}")
    
    # Get title
    title = get_video_title(video_id)
    if not title:
        title = "New ClawTV Video"
    
    print(f"📝 Title: {title}")
    print()
    
    # Post to Discord
    post_video(video_url, video_id, title)
