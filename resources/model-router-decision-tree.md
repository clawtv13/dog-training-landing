# Model Router Decision Tree

**Which OpenClaw model to use when (flowchart guide)**

---

## 🎯 QUICK REFERENCE

**Copy this and put it on your desk:**

```
CREATIVE WORK → Sonnet 4.5
MONITORING → Flash-Lite
CODING → Flash-Thinking
BACKGROUND TASKS → Deepseek R1
CRITICAL THINKING → Opus (only 5% of time)
```

---

## 🌳 DECISION TREE (Follow This)

### **START HERE:**

**Is this task CRITICAL and requires BEST reasoning?**
- Examples: Strategic decisions, complex analysis, nuanced writing
- ✅ Yes → **Opus 4.5** ($60/1M tokens)
- ❌ No → Go to next question

---

**Is this CREATIVE work?**
- Examples: Writing, scripts, content generation, brainstorming
- ✅ Yes → **Sonnet 4.5** ($3/1M tokens)
- ❌ No → Go to next question

---

**Is this CODING or TECHNICAL?**
- Examples: Writing code, debugging, technical documentation
- ✅ Yes → **Flash-Thinking** ($1/1M tokens)
- ❌ No → Go to next question

---

**Is this MONITORING or STATUS CHECK?**
- Examples: Heartbeat pings, health checks, simple queries
- ✅ Yes → **Flash-Lite** ($0.075/1M tokens)
- ❌ No → Go to next question

---

**Is this BACKGROUND WORK or RESEARCH?**
- Examples: Web search, data gathering, subagent tasks
- ✅ Yes → **Deepseek R1** ($0.27/1M tokens)
- ❌ No → Default to **Sonnet 4.5**

---

## 📊 COST COMPARISON (Per 1M Tokens)

| Model | Cost | Use Case | Speed |
|-------|------|----------|-------|
| **Opus 4.5** | $60 | Critical thinking only | Medium |
| **Sonnet 4.5** | $3 | Creative work (80% of tasks) | Fast |
| **Flash-Thinking** | $1 | Coding & technical | Very Fast |
| **Deepseek R1** | $0.27 | Background & research | Fast |
| **Flash-Lite** | $0.075 | Monitoring only | Ultra Fast |

---

## 🎯 REAL EXAMPLES

### **Example 1: Writing YouTube Script**

**Task:** Generate 60-second video script

**Decision Tree:**
1. Critical? No (not strategic decision)
2. Creative? **YES** → Sonnet 4.5
3. Cost: $3 per 1M tokens

**Wrong choice:** Opus ($60) = 20x more expensive for same quality

---

### **Example 2: Monitoring Email Inbox**

**Task:** Check for urgent emails every 15 minutes

**Decision Tree:**
1. Critical? No
2. Creative? No
3. Coding? No
4. Monitoring? **YES** → Flash-Lite
5. Cost: $0.075 per 1M tokens

**Wrong choice:** Sonnet ($3) = 40x more expensive

---

### **Example 3: Strategic Business Decision**

**Task:** Evaluate pivoting business model (high stakes)

**Decision Tree:**
1. Critical? **YES** → Opus 4.5
2. Cost: $60 per 1M tokens

**Right choice:** This IS worth Opus (once per month, not daily)

---

### **Example 4: Web Research**

**Task:** Find trending topics for content

**Decision Tree:**
1. Critical? No
2. Creative? No
3. Coding? No
4. Monitoring? No
5. Background? **YES** → Deepseek R1
6. Cost: $0.27 per 1M tokens

**Wrong choice:** Sonnet ($3) = 11x more expensive

---

## 🔧 HOW TO IMPLEMENT

### **Option 1: Manual Routing (Free)**

Edit each session:
```
/model sonnet    (for creative work)
/model flash     (for monitoring)
/model deepseek  (for research)
```

**Pro:** Works immediately  
**Con:** You have to remember each time

---

### **Option 2: Config-Based (Recommended)**

Set up `openclaw.json`:
```json
{
  "model": "openrouter/anthropic/claude-sonnet-4.5",
  "heartbeatModel": "google/gemini-2.5-flash-lite",
  "subAgentModel": "deepseek/deepseek-reasoner"
}
```

**Pro:** Automatic routing  
**Con:** Requires config knowledge

---

### **Option 3: My Full Config (VIP)**

Pre-configured routing for:
- Default tasks → Sonnet
- Heartbeats → Flash-Lite
- Subagents → Deepseek
- Conditional logic (if X then Y)
- Cost monitors & alerts

**Pro:** Done-for-you, zero thinking  
**Con:** Requires VIP membership

---

## 💰 SAVINGS CALCULATOR

**Before optimization (using Opus for everything):**
- 1M tokens/month × $60 = **$60/month**

**After optimization (model tiering):**
- 800K tokens Sonnet × $3 = $2.40
- 150K tokens Deepseek × $0.27 = $0.04
- 50K tokens Flash-Lite × $0.075 = $0.004
- **Total: $2.44/month**

**Savings:** $57.56/month = **$690/year** (per 1M tokens)

**If you use 10M tokens/month:**
- Before: $600/month
- After: $24.40/month
- **Savings: $575/month = $6,900/year**

---

## 💎 WANT THIS AUTOMATED?

This decision tree is great.

But VIP members get:
✅ Pre-configured routing (no thinking required)
✅ My exact openclaw.json (copy-paste)
✅ Conditional logic (auto-route based on task)
✅ Cost monitoring (alerts when spend spikes)
✅ Direct support (I fix your config)

**Result:** Save 60-80% without thinking about it

[Join VIP](https://whop.com/clawtv-community)

---

## 📝 QUICK ACTION CHECKLIST

- [ ] Save this decision tree
- [ ] Identify your most common tasks
- [ ] Map tasks to models
- [ ] Test for 1 week
- [ ] Track savings
- [ ] Join VIP for automation

---

**Questions?** Drop in #questions (Discord)

— n0body ◼️
