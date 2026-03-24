#!/usr/bin/env python3
"""
Post content to ClawTV Discord channels
"""

import discord
from discord.ext import commands
import json
import asyncio

# Load token
credentials = json.load(open('/root/.openclaw/workspace/.credentials/discord-tokens.json'))
TOKEN = credentials['clawtv']['bot_token']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Content bot ready: {bot.user.name}')

@bot.command(name='populate')
async def populate_content(ctx):
    """Populate all channels with content (admin only)"""
    
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Admin only command")
        return
    
    guild = ctx.guild
    await ctx.send("📝 Populating ClawTV content...")
    
    # Find channels
    rules_channel = discord.utils.get(guild.channels, name='rules')
    start_channel = discord.utils.get(guild.channels, name='start-here')
    downloads_channel = discord.utils.get(guild.channels, name='free-downloads')
    
    # 1. RULES
    if rules_channel:
        rules_embed = discord.Embed(
            title="🦞 ClawTV Community Rules",
            description="Keep it real, keep it helpful.",
            color=discord.Color.blue()
        )
        
        rules_embed.add_field(
            name="1️⃣ Be helpful, not spammy",
            value="Share knowledge. No self-promo without adding value.",
            inline=False
        )
        
        rules_embed.add_field(
            name="2️⃣ No gatekeeping",
            value="Help beginners. We all started somewhere.",
            inline=False
        )
        
        rules_embed.add_field(
            name="3️⃣ Show your work",
            value="Results > theory. Share what's working.",
            inline=False
        )
        
        rules_embed.add_field(
            name="4️⃣ Respect the vibe",
            value="We're nerds building cool shit. Keep it real.",
            inline=False
        )
        
        rules_embed.add_field(
            name="5️⃣ No piracy",
            value="Don't share paid content from other creators.",
            inline=False
        )
        
        rules_embed.add_field(
            name="💎 Want deeper access?",
            value="Check <#whop-community> for premium tier.",
            inline=False
        )
        
        rules_embed.set_footer(text="Break rules = kick. Simple.")
        
        msg = await rules_channel.send(embed=rules_embed)
        await msg.pin()
        print("✅ Rules posted")
    
    # 2. START HERE
    if start_channel:
        start_embed = discord.Embed(
            title="👋 Welcome to ClawTV Community",
            description="Your roadmap to AI automation mastery.",
            color=discord.Color.green()
        )
        
        start_embed.add_field(
            name="🎯 What is ClawTV?",
            value="We build businesses with OpenClaw automation. No fluff. Just results.",
            inline=False
        )
        
        start_embed.add_field(
            name="📚 Start Here:",
            value="""
**New to OpenClaw?**
→ Check <#free-downloads> for setup guide
→ Ask questions in <#questions>
→ See real results in <#show-your-results>

**Ready to build?**
→ Browse <#configs-and-templates>
→ Share in <#agent-workflows>
→ Monetize in <#monetization>

**Want premium access?**
→ Weekly calls, private templates, job board
→ Check <#whop-community> (50% off first month)
            """,
            inline=False
        )
        
        start_embed.add_field(
            name="🦞 Our channels:",
            value="""
YouTube: @ClawTV
TikTok: @clawtv
Instagram: @clawtv
            """,
            inline=False
        )
        
        start_embed.set_footer(text="Questions? Ask in #questions")
        
        msg = await start_channel.send(embed=start_embed)
        await msg.pin()
        print("✅ Start guide posted")
    
    # 3. FREE DOWNLOADS
    if downloads_channel:
        downloads_embed = discord.Embed(
            title="🎁 Free OpenClaw Resources",
            description="Everything you need to get started.",
            color=discord.Color.gold()
        )
        
        downloads_embed.add_field(
            name="📄 OpenClaw Setup Checklist",
            value="Step-by-step guide to your first automation.\n[Download PDF] → Coming soon",
            inline=False
        )
        
        downloads_embed.add_field(
            name="📊 Model Cost Comparison",
            value="Compare Opus, Sonnet, Gemini, Deepseek pricing.\n[Spreadsheet] → Coming soon",
            inline=False
        )
        
        downloads_embed.add_field(
            name="⚙️ First Automation Template",
            value="Pre-built config for content generation.\n[Config file] → Coming soon",
            inline=False
        )
        
        downloads_embed.add_field(
            name="💡 10 Proven Prompts",
            value="Copy-paste prompts that work.\n[Doc] → Coming soon",
            inline=False
        )
        
        downloads_embed.add_field(
            name="🔥 More resources added weekly",
            value="Check <#feature-requests> to suggest what you need.",
            inline=False
        )
        
        msg = await downloads_channel.send(embed=downloads_embed)
        await msg.pin()
        print("✅ Free downloads posted")
    
    await ctx.send("✅ All content populated! Check pinned messages in each channel.")

@bot.command(name='welcome_test')
async def test_welcome(ctx):
    """Test welcome message"""
    
    welcome_embed = discord.Embed(
        title="👋 Welcome to ClawTV Community!",
        description=f"Hey {ctx.author.mention}, glad you're here.",
        color=discord.Color.blue()
    )
    
    welcome_embed.add_field(
        name="🎁 Your Free Starter Pack:",
        value="""
→ Setup Checklist (pinned in <#free-downloads>)
→ First Automation Template
→ Quick Start Guide
        """,
        inline=False
    )
    
    welcome_embed.add_field(
        name="📌 Next steps:",
        value="""
1. Check <#start-here> for the roadmap
2. Introduce yourself in <#general-chat>
3. Ask questions in <#questions>
        """,
        inline=False
    )
    
    welcome_embed.add_field(
        name="🔥 Want advanced training?",
        value="Check <#whop-community> (paid tier)",
        inline=False
    )
    
    welcome_embed.set_footer(text="See you inside! — ClawTV Team 🦞")
    
    await ctx.send(embed=welcome_embed)

if __name__ == '__main__':
    print("🦞 Starting content bot...")
    bot.run(TOKEN)
