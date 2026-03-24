# AGENTOPS — Monitoring & Analytics

_Last updated: 2026-03-20_

---

## What Is It?

**AgentOps** is an observability platform for AI agents.

- Tracks all API calls (OpenRouter, Replicate, etc)
- Shows real costs per task
- Identifies expensive operations
- Dashboard with agent metrics

**Website:** https://www.agentops.ai/  
**Installed:** ✅

---

## Setup (Pending API Key)

### 1. Get API Key

1. Go to https://www.agentops.ai/
2. Sign up
3. Get API key
4. Add to `.env` or config

### 2. Initialize in Code

```python
import agentops

# Initialize (use API key from env)
agentops.init(api_key="YOUR_API_KEY")

# Your agent code here...

# End session
agentops.end_session("Success")
```

### 3. Environment Variable (Better)

```bash
export AGENTOPS_API_KEY="your-key-here"
```

```python
import agentops
import os

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
```

---

## Integration with OpenClaw

### Option A: Wrapper Script

Create `/root/.openclaw/workspace/scripts/monitor.py`:

```python
import agentops
import os

# Initialize
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

# Track LLM calls automatically
agentops.record_llm_call(
    model="anthropic/claude-sonnet-4.5",
    prompt_tokens=1000,
    completion_tokens=500,
    cost=0.018
)

# Track custom events
agentops.record_event("shopify_api_call", {
    "endpoint": "/products",
    "method": "GET",
    "duration_ms": 234
})

# End session
agentops.end_session("Success")
```

### Option B: Auto-tracking (if supported)

Check if AgentOps has OpenRouter/Anthropic integration:

```python
from agentops.integrations import openrouter

# This might auto-track all calls
openrouter.enable_tracking()
```

---

## What To Track

### API Costs

```python
agentops.record_llm_call(
    model="sonnet",
    prompt_tokens=5000,
    completion_tokens=2000,
    cost=0.126  # Calculate based on pricing
)
```

### Sub-agent Spawns

```python
agentops.record_event("subagent_spawn", {
    "model": "deepseek-reasoner",
    "task": "generate_product_descriptions",
    "count": 5
})
```

### Task Completion Time

```python
import time

start = time.time()
# ... do work ...
duration = time.time() - start

agentops.record_event("task_complete", {
    "task": "generate_ad_copy",
    "duration_seconds": duration
})
```

---

## Dashboard Metrics

Once configured, you'll see:

- **Cost breakdown** by model
- **Token usage** over time
- **Task duration** averages
- **Error rates**
- **Most expensive operations**

---

## Goals

### Week 1:
- [ ] Get API key
- [ ] Configure tracking
- [ ] Verify dashboard works

### Week 2:
- [ ] Track 1 week of usage
- [ ] Identify top 3 expensive operations
- [ ] Optimize based on data

### Long-term:
- [ ] Set cost alerts
- [ ] A/B test model choices
- [ ] Optimize token usage based on real data

---

## Pending

🔑 **Waiting for API key from user**

Once you provide it, I'll:
1. Add to environment
2. Configure tracking
3. Start monitoring all operations
