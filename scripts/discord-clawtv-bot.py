#!/usr/bin/env python3
"""
ClawTV Discord Bot - Setup and Management
"""

import discord
from discord.ext import commands
import json
from pathlib import Path

# Load token
credentials = json.load(open('/root/.openclaw/workspace/.credentials/discord-tokens.json'))
TOKEN = credentials['clawtv']['bot_token']

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot connected: {bot.user.name}')
    print(f'📊 Guilds: {len(bot.guilds)}')
    
    for guild in bot.guilds:
        print(f'\n🏠 Server: {guild.name} (ID: {guild.id})')
        print(f'   Members: {guild.member_count}')
        print(f'   Channels: {len(guild.channels)}')

@bot.event
async def on_member_join(member):
    """Welcome new members with DM"""
    
    welcome_message = f"""👋 Welcome to ClawTV Community, {member.mention}!

🎁 Here's your free OpenClaw Starter Pack:
→ Setup Checklist (pinned in #free-downloads)
→ First Automation Template
→ Quick Start Guide

📌 Next steps:
1. Check <#start-here> for the roadmap
2. Introduce yourself in <#general-chat>
3. Ask questions in <#questions>

🔥 Want advanced training?
Check <#whop-community> (paid tier)

See you inside!
— ClawTV Team 🦞"""
    
    try:
        await member.send(welcome_message)
        print(f"✅ Welcome DM sent to {member.name}")
    except:
        print(f"⚠️  Couldn't DM {member.name} (DMs closed)")

@bot.command(name='setup')
async def setup_server(ctx):
    """Setup channel structure (admin only)"""
    
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Admin only command")
        return
    
    guild = ctx.guild
    
    await ctx.send("🔧 Setting up ClawTV Community structure...")
    
    # Category: WELCOME
    welcome_cat = await guild.create_category("📢 WELCOME")
    await guild.create_text_channel("rules", category=welcome_cat)
    await guild.create_text_channel("start-here", category=welcome_cat)
    await guild.create_text_channel("free-downloads", category=welcome_cat)
    
    # Category: LEARN
    learn_cat = await guild.create_category("🎓 LEARN")
    await guild.create_text_channel("quick-wins", category=learn_cat)
    await guild.create_text_channel("tutorials", category=learn_cat)
    await guild.create_text_channel("questions", category=learn_cat)
    
    # Category: OPENCLAW
    openclaw_cat = await guild.create_category("🦞 OPENCLAW")
    await guild.create_text_channel("general-chat", category=openclaw_cat)
    await guild.create_text_channel("troubleshooting", category=openclaw_cat)
    await guild.create_text_channel("configs-and-templates", category=openclaw_cat)
    await guild.create_text_channel("show-your-results", category=openclaw_cat)
    
    # Category: AUTOMATION
    auto_cat = await guild.create_category("🚀 AUTOMATION")
    await guild.create_text_channel("agent-workflows", category=auto_cat)
    await guild.create_text_channel("content-automation", category=auto_cat)
    await guild.create_text_channel("monetization", category=auto_cat)
    
    # Category: OPPORTUNITIES
    opp_cat = await guild.create_category("💼 OPPORTUNITIES")
    await guild.create_text_channel("jobs-and-gigs", category=opp_cat)
    await guild.create_text_channel("collaborations", category=opp_cat)
    
    # Category: COMMUNITY
    comm_cat = await guild.create_category("🎉 COMMUNITY")
    await guild.create_text_channel("off-topic", category=comm_cat)
    await guild.create_text_channel("wins-and-milestones", category=comm_cat)
    await guild.create_text_channel("feature-requests", category=comm_cat)
    
    # Category: VIP (private)
    vip_cat = await guild.create_category("🔐 VIP")
    vip_role = await guild.create_role(name="VIP Member", color=discord.Color.gold())
    
    vip_chat = await guild.create_text_channel("vip-chat", category=vip_cat)
    await vip_chat.set_permissions(guild.default_role, read_messages=False)
    await vip_chat.set_permissions(vip_role, read_messages=True)
    
    vip_calls = await guild.create_text_channel("call-recordings", category=vip_cat)
    await vip_calls.set_permissions(guild.default_role, read_messages=False)
    await vip_calls.set_permissions(vip_role, read_messages=True)
    
    vip_configs = await guild.create_text_channel("premium-configs", category=vip_cat)
    await vip_configs.set_permissions(guild.default_role, read_messages=False)
    await vip_configs.set_permissions(vip_role, read_messages=True)
    
    await ctx.send("✅ ClawTV Community structure created!")

@bot.command(name='stats')
async def stats(ctx):
    """Show server stats"""
    
    guild = ctx.guild
    
    embed = discord.Embed(
        title="📊 ClawTV Community Stats",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """Auto-responses to keywords"""
    
    # Ignore bot messages
    if message.author.bot:
        return
    
    content = message.content.lower()
    
    # Keyword responses
    if any(word in content for word in ['cost', 'expensive', 'price', 'how much']):
        if 'openclaw' in content or message.channel.name in ['questions', 'general-chat']:
            await message.add_reaction('💰')
            # Don't spam if recently answered
    
    if 'worth it' in content or 'should i' in content:
        await message.add_reaction('🤔')
    
    # Process commands
    await bot.process_commands(message)

# Run bot
if __name__ == '__main__':
    print("🦞 Starting ClawTV Bot...")
    bot.run(TOKEN)
