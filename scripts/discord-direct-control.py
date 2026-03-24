#!/usr/bin/env python3
"""
Direct Discord control - No user commands needed
Execute actions directly from OpenClaw
"""

import discord
import json
import asyncio

# Load credentials
credentials = json.load(open('/root/.openclaw/workspace/.credentials/discord-tokens.json'))
TOKEN = credentials['clawtv']['bot_token']
GUILD_ID = 1484937580339400784

class DiscordController:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.all())
        self.guild = None
        
    async def connect(self):
        """Connect and get guild"""
        await self.client.login(TOKEN)
        await self.client.connect()
        self.guild = self.client.get_guild(GUILD_ID)
        if not self.guild:
            # Wait and retry
            await asyncio.sleep(2)
            self.guild = self.client.get_guild(GUILD_ID)
        return self.guild
    
    async def post_to_channel(self, channel_name: str, content: str = None, embed: discord.Embed = None):
        """Post message to channel"""
        channel = discord.utils.get(self.guild.channels, name=channel_name)
        if channel:
            if embed:
                msg = await channel.send(content=content, embed=embed)
            else:
                msg = await channel.send(content)
            print(f"✅ Posted to #{channel_name}")
            return msg
        else:
            print(f"❌ Channel #{channel_name} not found")
            return None
    
    async def pin_message(self, channel_name: str, message_id: int):
        """Pin a message"""
        channel = discord.utils.get(self.guild.channels, name=channel_name)
        if channel:
            msg = await channel.fetch_message(message_id)
            await msg.pin()
            print(f"✅ Pinned message in #{channel_name}")
    
    async def create_role(self, name: str, color: discord.Color, permissions=None):
        """Create role"""
        role = await self.guild.create_role(name=name, color=color, permissions=permissions)
        print(f"✅ Created role: {name}")
        return role
    
    async def send_dm(self, user_id: int, content: str):
        """Send DM to user"""
        user = await self.client.fetch_user(user_id)
        await user.send(content)
        print(f"✅ DM sent to {user.name}")
    
    async def get_channel_history(self, channel_name: str, limit=10):
        """Get recent messages from channel"""
        channel = discord.utils.get(self.guild.channels, name=channel_name)
        if channel:
            messages = []
            async for msg in channel.history(limit=limit):
                messages.append({
                    'author': msg.author.name,
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                })
            return messages
        return []
    
    async def close(self):
        """Close connection"""
        await self.client.close()


async def example_usage():
    """Example: Post welcome message to general-chat"""
    
    controller = DiscordController()
    
    try:
        await controller.connect()
        print(f"✅ Connected to: {controller.guild.name}")
        
        # Example: Post to general-chat
        embed = discord.Embed(
            title="🦞 ClawTV is Live!",
            description="Welcome to the automation community.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="What we're about:",
            value="Building businesses with OpenClaw. No fluff. Just results.",
            inline=False
        )
        
        await controller.post_to_channel('general-chat', embed=embed)
        
        # Get recent messages
        history = await controller.get_channel_history('general-chat', limit=5)
        print(f"\n📜 Recent messages in #general-chat:")
        for msg in history:
            print(f"  [{msg['timestamp']}] {msg['author']}: {msg['content'][:50]}...")
        
    finally:
        await controller.close()


if __name__ == '__main__':
    asyncio.run(example_usage())
