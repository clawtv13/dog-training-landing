# Workflow Rules - n0body AI Assistant

## MANDATORY: Check Skills Before Every Task

### Rule #1: ALWAYS Review Available Skills First

**Before starting ANY task, check:**

```
Available Skills:
- web_search: Real-time web search (Brave API)
- web_fetch: Fetch webpage content
- memory_search: Search memory files
- memory_get: Read memory snippets
- read: Read files
- write: Create/overwrite files
- edit: Precise edits
- exec: Run shell commands
- process: Manage background processes
- sessions_spawn: Spawn subagents
- image: Analyze images
```

### When to Use Each:

**web_search:**
- Research trending topics
- Find current news/cases
- Discover popular content
- Real-time data needed

**web_fetch:**
- Get full article content
- Extract specific information
- Deep dive on URLs

**memory_search:**
- Before answering about past work
- Check decisions made
- Find previous preferences
- Verify dates/details

**exec + process:**
- Automate tasks
- Run scripts
- System operations

**sessions_spawn:**
- Complex multi-step tasks
- Parallel processing
- Specialized agents

### Example Workflow:

**WRONG:**
```
Task: Research trending topics
Action: Use fallback hardcoded list
```

**RIGHT:**
```
Task: Research trending topics
1. Check available skills → web_search exists!
2. Use web_search for real-time data
3. Analyze results
4. Generate output
```

---

## Lessons Learned:

### 2026-03-26:
- Had web_search available all along
- Was using fallback topics instead
- User pointed out: "you have skills for that"
- **ALWAYS CHECK FIRST FROM NOW ON**

---

## Checklist Before Every Task:

- [ ] What skills do I have available?
- [ ] Is there a skill that solves this directly?
- [ ] Am I defaulting to manual when tools exist?
- [ ] Did I check memory before answering?

---

*This rule applies to ALL future sessions*
*Read this file at session start*
