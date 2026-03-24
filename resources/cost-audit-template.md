# OpenClaw Cost Audit Template

**Use this to find where you're wasting money on OpenClaw**

---

## 📊 YOUR CURRENT SPENDING

**Step 1: Check OpenRouter Dashboard**

Go to: https://openrouter.ai/activity

**Last 30 days spending:** $______

**Most used model:** ________________

**Average cost per request:** $______

---

## 🔍 COST BREAKDOWN ANALYSIS

### **Model Usage (Last 30 Days)**

| Model | Requests | Total Cost | % of Budget |
|-------|----------|------------|-------------|
| Opus 4.5 | ____ | $____ | ___% |
| Sonnet 4.5 | ____ | $____ | ___% |
| Flash-Thinking | ____ | $____ | ___% |
| Flash 2.0 | ____ | $____ | ___% |
| Gemini 2.0 | ____ | $____ | ___% |
| Deepseek R1 | ____ | $____ | ___% |
| Other | ____ | $____ | ___% |

---

## 🚨 RED FLAGS (Check All That Apply)

- [ ] Opus is >30% of my budget
- [ ] I use the same model for everything
- [ ] I don't know what "model tiering" means
- [ ] My context window is always full
- [ ] I have messages from weeks ago still loaded
- [ ] I've never configured message TTL
- [ ] My heartbeat model is Opus or Sonnet
- [ ] I don't use subagents
- [ ] My default model is Opus

**Total red flags:** _____ / 9

---

## 💡 QUICK WINS (Based on Red Flags)

### **If you checked 0-2:** You're doing okay
- Minor optimizations available
- **Potential savings:** $100-300/month

### **If you checked 3-5:** Moderate waste
- Major optimizations needed
- **Potential savings:** $500-1,000/month

### **If you checked 6+:** Massive waste 🚨
- Urgent optimization required
- **Potential savings:** $1,000-2,000/month

---

## 🔧 IMMEDIATE FIXES

### **Fix #1: Change Default Model**

**If your default is Opus:**
```json
"model": "openrouter/anthropic/claude-sonnet-4.5"
```
**Savings:** 20x cheaper for 80% of tasks

---

### **Fix #2: Setup Model Tiering**

**Heartbeats (monitoring):**
```json
"heartbeatModel": "google/gemini-2.5-flash-lite"
```
**Savings:** $300/month → $1/month (300x cheaper)

**Subagents (background work):**
```json
"subAgentModel": "deepseek/deepseek-reasoner"
```
**Savings:** 90% cheaper than Sonnet

---

### **Fix #3: Context Cleanup**

**Set message TTL (auto-delete old messages):**
```json
"messageRetentionHours": 2
```
**Savings:** $200-500/month (smaller context = cheaper)

---

## 📈 YOUR SAVINGS PROJECTION

**Current monthly spend:** $______

**After quick fixes:** $______ (estimate)

**Annual savings:** $______ × 12 = $______

---

## 💎 WANT THE FULL OPTIMIZATION?

This template shows you WHAT to fix.

**VIP members get:**
✅ My exact openclaw.json (pre-configured)
✅ Done-for-you model routing
✅ Advanced context optimization
✅ Auto-monitoring & alerts
✅ Direct support (fix your setup)

**Result:** Most members save 60-80% ($500-2K/month)

**Investment:** $49/month

**ROI:** Pays for itself 10x in Month 1

[Join VIP Here](https://whop.com/clawtv-community)

---

## 📝 NEXT STEPS

1. ✅ Fill out this audit
2. ✅ Implement quick fixes
3. ✅ Track savings for 7 days
4. ✅ Join VIP for full optimization

---

**Questions?** Ask in #questions (Discord)

— n0body ◼️
