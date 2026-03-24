# 🦞 OpenClaw Setup Checklist

**Get started with OpenClaw automation in 30 minutes**

---

## ✅ PHASE 1: Installation (10 min)

### Step 1: Install OpenClaw
```bash
npm install -g openclaw
```

**Verify:**
```bash
openclaw --version
```

### Step 2: Create Workspace
```bash
mkdir ~/openclaw-projects
cd ~/openclaw-projects
openclaw init
```

### Step 3: Configure API Keys
```bash
openclaw config set OPENROUTER_API_KEY your_key_here
```

**Get OpenRouter key:** https://openrouter.ai/keys

---

## ✅ PHASE 2: First Automation (15 min)

### Step 1: Create Simple Task
Create file: `tasks/daily-summary.md`

```markdown
# Daily Summary Task

Generate a summary of trending topics in AI automation.

Sources:
- Twitter #aiautomation
- Reddit r/OpenClaw
- Hacker News

Output: 
- 5 bullet points
- Save to summaries/YYYY-MM-DD.md
```

### Step 2: Run Task
```bash
openclaw run tasks/daily-summary.md
```

### Step 3: Verify Output
Check: `summaries/2026-03-21.md`

---

## ✅ PHASE 3: Optimization (5 min)

### Enable Model Tiering

Edit `openclaw.json`:
```json
{
  "defaultModel": "openrouter/anthropic/claude-sonnet-4.5",
  "models": {
    "fast": "openrouter/google/gemini-2.5-flash-lite",
    "reasoning": "openrouter/deepseek/deepseek-reasoner"
  }
}
```

### Set Context Limits
```json
{
  "context": {
    "messageTTL": 7200,
    "maxTokens": 100000
  }
}
```

---

## ✅ PHASE 4: Automation (Bonus)

### Schedule Daily Runs
```bash
# Cron: Run every morning at 9 AM
0 9 * * * cd ~/openclaw-projects && openclaw run tasks/daily-summary.md
```

### Setup Heartbeat Monitoring
Edit `HEARTBEAT.md`:
```markdown
# Heartbeat

Check for new tasks every hour.
If tasks found, execute automatically.
```

---

## 🎯 Next Steps

**Beginner:**
- [ ] Run 5 different tasks
- [ ] Explore skills library
- [ ] Join ClawTV Discord

**Intermediate:**
- [ ] Create custom agent workflow
- [ ] Implement model tiering
- [ ] Optimize costs below $100/mo

**Advanced:**
- [ ] Build multi-agent system
- [ ] Monetize automation service
- [ ] Join Whop premium community

---

## 💬 Need Help?

**Discord:** discord.gg/clawtv  
**Twitter:** @clawtv  
**Docs:** openclaw.ai/docs

---

**🦞 Made by ClawTV Community**  
_Automation That Works_
