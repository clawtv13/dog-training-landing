#!/usr/bin/env python3
"""
Mind Crimes - Daily Content Generator V2
Uses large topics database with smart rotation
"""

import requests
import json
import os
import random
from datetime import datetime
from pathlib import Path

# Config
OPENROUTER_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU"
TELEGRAM_CHAT_ID = "8116230130"
WORKSPACE = "/root/.openclaw/workspace"
OUTPUT_DIR = Path(f"{WORKSPACE}/content/mind-crimes")
LOG_FILE = Path(f"{WORKSPACE}/.logs/mind-crimes-daily.log")

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + "\n")

# 50 TOPICS DATABASE
TOPICS_DB = [
    # REALISTIC (25 topics)
    {"title": "The Crypto Queen: How OneCoin Scammed $4 Billion", "type": "realistic"},
    {"title": "Family Annihilators: The Dark Psychology Behind Mass Murder", "type": "realistic"},
    {"title": "The TikTok Cult Leader Who Convinced 50 People to Disappear", "type": "realistic"},
    {"title": "When Good Neighbors Turn Serial Killers: The BTK Story", "type": "realistic"},
    {"title": "The Instagram Influencer Who Faked Her Own Death for Likes", "type": "realistic"},
    {"title": "Corporate Psychopaths: How CEOs Destroy Lives Without Guilt", "type": "realistic"},
    {"title": "The Roommate Who Slowly Poisoned Her Best Friend", "type": "realistic"},
    {"title": "MLM Cult Leaders: How Multi-Level Marketing Became a Religion", "type": "realistic"},
    {"title": "The Airbnb Murder Nobody Saw Coming", "type": "realistic"},
    {"title": "Catfishing Gone Fatal: When Online Love Turns Deadly", "type": "realistic"},
    {"title": "Swatting Deaths: Anonymous Gaming Revenge Kills Innocent People", "type": "realistic"},
    {"title": "Dark Web Hitmen: Do They Actually Exist? (Spoiler: Mostly Scams)", "type": "realistic"},
    {"title": "The Rise of Female Serial Killers in the Tech Industry", "type": "realistic"},
    {"title": "Cryptocurrency Murders: Killing for Bitcoin in 2024", "type": "realistic"},
    {"title": "When Innocent People Confess to Murder (False Confession Psychology)", "type": "realistic"},
    {"title": "The Satanic Panic: False Memories That Destroyed Lives", "type": "realistic"},
    {"title": "Why Juries Get It Wrong 25% of the Time", "type": "realistic"},
    {"title": "Forensic Science Lies That Sent Innocent People to Prison", "type": "realistic"},
    {"title": "The Innocence Project: 400+ Murder Exonerations Exposed Police Corruption", "type": "realistic"},
    {"title": "Cartel Brutality: Why Mexican Crime Is Psychologically Different", "type": "realistic"},
    {"title": "Yakuza Psychology: The Honor Code Behind Japanese Organized Crime", "type": "realistic"},
    {"title": "The Italian Mafia's Strangest Murder Rituals", "type": "realistic"},
    {"title": "North Korean Assassinations: State-Sponsored Murder Gone Global", "type": "realistic"},
    {"title": "Human Trafficking Routes the Police Won't Touch", "type": "realistic"},
    {"title": "The Vanishing Hitchhiker: America's Most Famous Urban Legend Based on Real Murders", "type": "realistic"},
    
    # LOVECRAFTIAN (25 topics)
    {"title": "The Forer Effect: Why Horoscopes Hijack Your Brain", "type": "lovecraft"},
    {"title": "Folie à Deux: When Madness Becomes Contagious Between Two People", "type": "lovecraft"},
    {"title": "The Milgram Experiment: You'd Electrocute Someone to Death If Told To", "type": "lovecraft"},
    {"title": "Stanford Prison Experiment: Proof We're All Monsters Inside", "type": "lovecraft"},
    {"title": "MK-Ultra: The CIA's Real Mind Control Experiments on Americans", "type": "lovecraft"},
    {"title": "The Dark Tetrad: The Personality Trait Worse Than Psychopathy", "type": "lovecraft"},
    {"title": "Malignant Narcissism: When NPD Becomes a Serial Killer", "type": "lovecraft"},
    {"title": "The Sadistic Personality: People Who Literally Enjoy Your Pain", "type": "lovecraft"},
    {"title": "Machiavellianism: The Art of Manipulation Without Empathy", "type": "lovecraft"},
    {"title": "Subclinical Psychopathy: Your Boss Probably Has It", "type": "lovecraft"},
    {"title": "The Mandela Effect: Collective False Memories Across Millions", "type": "lovecraft"},
    {"title": "Derealization: When Reality Stops Feeling Real (And Never Comes Back)", "type": "lovecraft"},
    {"title": "Cotard's Syndrome: The Walking Corpse Delusion", "type": "lovecraft"},
    {"title": "Capgras Syndrome: Everyone You Love Is an Impostor", "type": "lovecraft"},
    {"title": "Sleep Paralysis Demons: Hallucinations or Something Worse?", "type": "lovecraft"},
    {"title": "The Bystander Effect: Why Nobody Helps When You're Dying", "type": "lovecraft"},
    {"title": "Groupthink: How Cults Turn Intelligent People Into Zombies", "type": "lovecraft"},
    {"title": "Deindividuation: Why Mobs Turn Into Murderers", "type": "lovecraft"},
    {"title": "The Halo Effect: Beautiful People Literally Get Away With Murder", "type": "lovecraft"},
    {"title": "Confirmation Bias: Your Brain Is Constantly Lying to You", "type": "lovecraft"},
    {"title": "The Monster Study: Scientists Made Kids Stutter on Purpose", "type": "lovecraft"},
    {"title": "Little Albert Experiment: Torturing a Baby for Science", "type": "lovecraft"},
    {"title": "Harlow's Monkeys: The Cruelest Psychology Experiment Ever", "type": "lovecraft"},
    {"title": "The Third Wave: How a Teacher Created Nazis in 5 Days", "type": "lovecraft"},
    {"title": "The Asch Conformity Experiment: You'd Lie to Fit In (Even When Obviously Wrong)", "type": "lovecraft"},
]
    
    # Load usage history
    usage_file = OUTPUT_DIR / "topics-used.json"
    used_ids = []
    if usage_file.exists():
        with open(usage_file, 'r') as f:
            history = json.load(f)
            # Get IDs used in last 15 days
            used_ids = [item for day in history[-15:] for item in day.get('topics', [])]
    
    # Filter out recently used
    available_realistic = [t for t in TOPICS_DB if t['type'] == 'realistic' and t['id'] not in used_ids]
    available_lovecraft = [t for t in TOPICS_DB if t['type'] == 'lovecraft' and t['id'] not in used_ids]
    
    # Fallback to all if too many used
    if len(available_realistic) < 3:
        available_realistic = [t for t in TOPICS_DB if t['type'] == 'realistic']
    if len(available_lovecraft) < 3:
        available_lovecraft = [t for t in TOPICS_DB if t['type'] == 'lovecraft']
    
    # Random selection
    selected = [
        random.choice(available_realistic),
        random.choice(available_lovecraft)
    ]
    
    # Update usage history
    history_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "topics": [t['id'] for t in selected]
    }
    
    if usage_file.exists():
        with open(usage_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    history.append(history_entry)
    with open(usage_file, 'w') as f:
        json.dump(history[-30:], f, indent=2)  # Keep last 30 days
    
    log(f"Selected from database (avoiding {len(used_ids)} recent topics)")
    return selected
'''

print(f"✅ Created mind-crimes-daily-v2.py with 50-topic database")
print(f"\nReplace in cron:")
print(f"  OLD: /scripts/mind-crimes-daily.py")
print(f"  NEW: /scripts/mind-crimes-daily-v2.py")
PYUPDATE
*Hashtags:*
`{video1['metadata']['hashtags']}`

━━━━━━━━━━━━━━━━━"""
        
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": desc1, "parse_mode": "Markdown"},
            timeout=10
        )
        
        # VIDEO 2 - Full details
        video2 = topics_with_prompts[1]
        
        prompt2_text = f"""📹 *VIDEO 2 - {video2['topic']['type'].upper()}*

*Title:*
`{video2['metadata']['title']}`

*CapCut AI Prompt:*
```
{video2['prompt']}
```"""
        
        if len(prompt2_text) > 4000:
            part1 = f"""📹 *VIDEO 2 - {video2['topic']['type'].upper()}*

*Title:*
`{video2['metadata']['title']}`

*CapCut Prompt (Part 1):*
```
{video2['prompt'][:1800]}
```"""
            
            part2 = f"""*CapCut Prompt (Part 2):*
```
{video2['prompt'][1800:]}
```"""
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": part1, "parse_mode": "Markdown"},
                timeout=10
            )
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": part2, "parse_mode": "Markdown"},
                timeout=10
            )
        else:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": prompt2_text, "parse_mode": "Markdown"},
                timeout=10
            )
        
        # YouTube metadata for Video 2
        desc2 = f"""*YouTube Description:*
```
{video2['metadata']['description']}
```

*Hashtags:*
`{video2['metadata']['hashtags']}`

✅ *Ready to produce!* 🎬"""
        
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": desc2, "parse_mode": "Markdown"},
            timeout=10
        )
        
        return True
    except Exception as e:
        print(f"Telegram notification failed: {e}")
        return False

# ==================== LOGGING ====================

def log(message):
    """Write to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    print(log_message.strip())
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_message)

# ==================== MAIN ====================

def main():
    """Main execution"""
    
    log("=== Mind Crimes Daily Generator Started ===")
    
    try:
        # Step 1: Research
