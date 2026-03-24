# 5 OpenClaw Mistakes Costing You $1K+/Month

**Quick audit: Check all that apply, then fix them**

---

## ❌ MISTAKE #1: Using Opus for Everything

### **The Problem:**

Most people set Opus as default and forget about it.

**Result:** $60 per 1M tokens for tasks that could use $3 models.

**20x more expensive than necessary.**

### **Why It Happens:**

- Opus = best model → "I should use the best always"
- Never learned about model tiering
- Afraid cheaper models = worse quality

### **The Truth:**

Sonnet 4.5 is 95% as good as Opus for 95% of tasks.

**Only use Opus for:**
- Strategic decisions (once per week, not daily)
- Complex analysis requiring max reasoning
- High-stakes content (major launches, legal docs)

**Everything else:** Sonnet or cheaper.

### **The Fix:**

```json
// In openclaw.json
"model": "openrouter/anthropic/claude-sonnet-4.5"
```

**Savings:** $1,000-1,500/month (if you were Opus-only before)

---

## ❌ MISTAKE #2: No Heartbeat Optimization

### **The Problem:**

Heartbeats = regular health checks (every 15-30 min).

If your heartbeat model is Sonnet or Opus:
- 96 heartbeats/day × $0.03 = $2.88/day
- **$86/month just for pings**

### **Why It Happens:**

- Default heartbeat = same as main model
- Never configured heartbeatModel separately
- Don't realize how often heartbeats run

### **The Truth:**

Heartbeats are SIMPLE tasks:
- "Check memory, reply HEARTBEAT_OK"
- No creativity, no reasoning needed
- Flash-Lite handles it perfectly

### **The Fix:**

```json
// In openclaw.json
"heartbeatModel": "google/gemini-2.5-flash-lite"
```

**Cost:**
- Flash-Lite: $0.075 per 1M tokens
- 96 heartbeats/day = ~$0.03/month (vs $86)

**Savings:** $85/month = $1,020/year

---

## ❌ MISTAKE #3: Context Bloat (Old Messages Never Die)

### **The Problem:**

Every message stays in context FOREVER.

**Result:**
- Week 1: 500 tokens context
- Week 4: 50,000 tokens context
- **Costs 100x more per request**

### **Why It Happens:**

- Never configured message retention (TTL)
- Think "more context = better AI"
- Don't realize old messages cost money EVERY request

### **The Truth:**

AI doesn't need 3-week-old messages.

**2-hour TTL** is perfect for most use cases:
- Recent context = relevant
- Old messages = auto-deleted
- Cost = 90% lower

### **The Fix:**

```json
// In openclaw.json
"messageRetentionHours": 2
```

**Exception:** Use MEMORY.md for long-term info (not raw messages)

**Savings:** $300-600/month (depending on usage)

---

## ❌ MISTAKE #4: No Subagent Model Routing

### **The Problem:**

Subagents = background workers (research, automation tasks).

If subagents use your default model (Sonnet):
- 100 subagent tasks/day × $0.03 = $3/day
- **$90/month for background work**

### **Why It Happens:**

- Never configured subAgentModel
- Didn't know subagents could use different models
- Assumed they NEED good models

### **The Truth:**

Subagents are background tasks:
- Web search
- File organization
- Data gathering
- Simple automation

**Deepseek R1** handles these perfectly for 90% less.

### **The Fix:**

```json
// In openclaw.json
"subAgentModel": "deepseek/deepseek-reasoner"
```

**Cost:**
- Deepseek: $0.27 per 1M tokens
- Sonnet: $3 per 1M tokens
- **11x cheaper**

**Savings:** $80/month = $960/year

---

## ❌ MISTAKE #5: No Cost Monitoring

### **The Problem:**

You don't track spending until bill shock.

**Result:**
- Month 1: $200 (seems fine)
- Month 2: $800 (huh?)
- Month 3: $2,100 (WTF?!)

### **Why It Happens:**

- OpenRouter doesn't alert you
- No budget tracking
- Don't review usage regularly

### **The Truth:**

Costs compound FAST:
- More messages = bigger context
- Bigger context = higher costs
- Higher costs = exponential growth

**Without monitoring, costs spiral out of control.**

### **The Fix (Manual):**

Check OpenRouter dashboard weekly:
- openrouter.ai/activity
- Set calendar reminder
- Track model usage

### **The Fix (Automated — VIP):**

My cost monitoring skill:
- Alerts when spend >$X/day
- Weekly usage reports
- Model breakdown
- Optimization recommendations

**Savings:** Catch waste BEFORE it costs $1K

---

## 📊 TOTAL SAVINGS POTENTIAL

**If you're making all 5 mistakes:**

| Mistake | Monthly Waste | Annual Waste |
|---------|---------------|--------------|
| #1 Opus everywhere | $1,000 | $12,000 |
| #2 No heartbeat opt | $85 | $1,020 |
| #3 Context bloat | $400 | $4,800 |
| #4 No subagent routing | $80 | $960 |
| #5 No monitoring | $200 | $2,400 |
| **TOTAL** | **$1,765** | **$21,180** |

**Fix all 5 → Save $21K/year.**

---

## ✅ ACTION CHECKLIST

**Right now (5 minutes):**

- [ ] Change default model to Sonnet
- [ ] Set heartbeat model to Flash-Lite
- [ ] Configure message TTL (2 hours)
- [ ] Set subagent model to Deepseek
- [ ] Check OpenRouter dashboard

**This week:**

- [ ] Track savings for 7 days
- [ ] Compare before/after costs
- [ ] Join #questions if stuck

**This month:**

- [ ] Join VIP for full optimization
- [ ] Get my exact config (done-for-you)
- [ ] Access cost monitoring skill

---

## 💎 WANT IT DONE FOR YOU?

This checklist shows you WHAT to fix.

**VIP members get:**
✅ My exact openclaw.json (all fixes pre-configured)
✅ Cost monitoring skill (auto-alerts)
✅ Advanced routing logic (conditional models)
✅ Direct support (I fix your config)
✅ Ongoing optimization (new cost hacks)

**Result:** Most save 60-80% in Week 1

**Investment:** $49/month  
**ROI:** Save $500-2K/month

[Join VIP Here](https://whop.com/clawtv-community)

---

## 📝 NEED HELP?

**Free support:** #questions (Discord)  
**Priority support:** VIP members (24h response)

---

**Stop wasting money. Fix these 5 mistakes today.**

— n0body ◼️
