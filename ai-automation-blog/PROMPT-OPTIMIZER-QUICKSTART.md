# 🚀 Prompt Optimizer Quick Start

**Goal**: Get the prompt optimizer running in 5 minutes

---

## Step 1: Set API Key (30 seconds)

```bash
export OPENROUTER_API_KEY="your-key-here"
```

**Don't have a key?** Get one at https://openrouter.ai/

**Make it permanent** (optional):
```bash
echo 'export OPENROUTER_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 2: Run First Optimization (2 minutes)

```bash
cd /root/.openclaw/workspace/ai-automation-blog
python3 scripts/prompt-optimizer.py optimize
```

**Expected output**:
```
🧠 PROMPT OPTIMIZER - Learning Loop for Blog Generation
✅ Database initialized
📊 Querying top 10 posts...
✅ Found 10 posts
🔍 Extracting patterns...
✅ Avg word count: 1744, Avg sections: 13
🤖 Generating prompt candidates...
✅ Generated 5 candidates
🔬 A/B test configured for 7 days
✅ OPTIMIZATION COMPLETE
```

---

## Step 3: Check What Was Created (30 seconds)

```bash
# View generated candidates
ls -lh prompts/candidates/

# View A/B test config
cat prompts/ab-test.json
```

---

## Step 4: Wait 7 Days... ⏳

During this time:
- Run `blog-auto-post-v2.py` normally
- Each post uses either variant A or B (random 50/50)
- Quality scores are tracked automatically

---

## Step 5: Evaluate Results (1 minute)

After 7 days:

```bash
python3 scripts/prompt-optimizer.py evaluate
```

**If variant B wins** (>5 point improvement):
- Automatically promotes to production
- Old prompt archived
- You're now using the improved prompt! 🎉

**If no clear winner**:
- Keep current prompt
- Run another optimization cycle later

---

## 🎯 That's It!

You now have a **self-improving blog system** that continuously optimizes its prompts based on real performance data.

---

## 📊 Check Status Anytime

```bash
python3 scripts/ab-test-integration.py
```

Shows:
- Current A/B test status
- Posts generated per variant
- Average quality scores
- Days remaining

---

## 🔄 Weekly Schedule (Optional Automation)

Add to crontab:

```bash
# Optimize every Sunday at 2 AM
0 2 * * 0 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/prompt-optimizer.py optimize

# Evaluate every Monday at 3 AM
0 3 * * 1 cd /root/.openclaw/workspace/ai-automation-blog && python3 scripts/prompt-optimizer.py evaluate
```

---

## 🐛 Troubleshooting

### "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### "Not enough posts for analysis"
Need at least 3 posts. Run blog generation first:
```bash
python3 scripts/blog-auto-post-v2.py
```

### "Database not found"
It auto-creates on first run. If issues persist:
```bash
python3 scripts/prompt-optimizer.py optimize
```

---

## 📚 More Info

- **Full guide**: `PROMPT-OPTIMIZER-INTEGRATION.md`
- **Complete docs**: `BUILD-GROUP-3-COMPLETE.md`
- **Logs**: `logs/prompt-optimizer-*.log`

---

**Ready?** Run step 1 now! ⚡
