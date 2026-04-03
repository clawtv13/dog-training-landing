#!/bin/bash
echo "═══════════════════════════════════════════════════════════"
echo "📝 EXTRACTING ALL PROMPTS FROM SCRIPTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "1️⃣ BLOG POST GENERATION (blog-auto-post-v2.py):"
echo "════════════════════════════════════════════════════"
grep -A 35 'prompt = f"""You are writing' blog-auto-post-v2.py | head -40
echo ""

echo "2️⃣ RESEARCH BREAKING NEWS (realtime-research.py):"
echo "════════════════════════════════════════════════════"
cd ../../newsletter-ai-automation/scripts 2>/dev/null
grep -A 30 'prompt = f"""You are monitoring' realtime-research.py 2>/dev/null | head -35
echo ""

echo "3️⃣ MASTER CONTENT AGENT:"
echo "════════════════════════════════════════════════════"
cd /root/.openclaw/workspace/ai-automation-blog/scripts
grep -B 2 -A 50 "SEO_RESEARCH_PROMPT\|CONTENT_GEN_PROMPT\|SCORING_PROMPT" master-content-agent.py 2>/dev/null | head -100
echo ""

