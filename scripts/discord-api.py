#!/usr/bin/env python3
"""
Simpler Discord API wrapper using requests
No bot session needed
"""

import requests
import json

credentials = json.load(open('/root/.openclaw/workspace/.credentials/discord-tokens.json'))
TOKEN = credentials['clawtv']['bot_token']
GUILD_ID = "1484937580339400784"

BASE_URL = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

def get_channels():
    """Get all channels in guild"""
    url = f"{BASE_URL}/guilds/{GUILD_ID}/channels"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def post_message(channel_id: str, content: str = None, embed: dict = None):
    """Post message to channel"""
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    
    payload = {}
    if content:
        payload['content'] = content
    if embed:
        payload['embeds'] = [embed]
    
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

def get_channel_id(channel_name: str):
    """Get channel ID by name"""
    channels = get_channels()
    for channel in channels:
        if channel.get('name') == channel_name:
            return channel['id']
    return None

# Test
if __name__ == '__main__':
    print("📊 Getting channels...")
    channels = get_channels()
    
    print(f"\n✅ Found {len(channels)} channels:")
    for ch in channels[:10]:
        print(f"  #{ch.get('name', 'N/A')} (ID: {ch['id']})")
    
    # Post test message
    general_id = get_channel_id('general-chat')
    if general_id:
        print(f"\n📤 Posting to #general-chat...")
        
        embed = {
            "title": "🦞 Test from OpenClaw",
            "description": "This message was posted directly from the server.",
            "color": 4886754  # Blue
        }
        
        result = post_message(general_id, content="Testing direct control...", embed=embed)
        print(f"✅ Posted: {result.get('id')}")
    else:
        print("❌ #general-chat not found")
