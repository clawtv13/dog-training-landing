#!/bin/bash
# Check HTTPS status for workless.build

echo "🔒 HTTPS STATUS CHECK - workless.build"
echo "========================================"
echo ""

echo "DNS Configuration:"
echo "  A records:"
dig +short workless.build A | sed 's/^/    /'
echo "  CNAME (www):"
dig +short www.workless.build CNAME | sed 's/^/    /'
echo ""

echo "HTTP Status (should work):"
timeout 5 curl -sI http://workless.build | grep "HTTP/" | head -1 | sed 's/^/  /'
echo ""

echo "HTTPS Status:"
timeout 5 curl -sI https://workless.build 2>&1 | grep -E "(HTTP|SSL)" | head -1 | sed 's/^/  /' || echo "  ❌ Certificate not ready"
echo ""

echo "CNAME File in Repo:"
cat /root/.openclaw/workspace/ai-automation-blog/blog/CNAME 2>/dev/null | sed 's/^/  /' || echo "  ❌ Missing"
echo ""

echo "========================================"
echo "ACTION REQUIRED:"
echo "========================================"
echo ""
echo "1. Open: https://github.com/clawtv13/ai-automation-blog/settings/pages"
echo ""
echo "2. Look for:"
echo "   [ ] Enforce HTTPS"
echo ""
echo "3. If grayed out:"
echo "   - Wait 10-60 minutes"
echo "   - GitHub is generating Let's Encrypt certificate"
echo "   - Refresh page every 10 minutes"
echo ""
echo "4. When clickable:"
echo "   - ✅ Check the box"
echo "   - Click Save"
echo "   - Wait 2 minutes"
echo ""
echo "5. Verify:"
echo "   - https://workless.build should load"
echo "   - Green padlock visible"
echo ""
echo "⏰ Estimated time: 10-60 minutes from domain setup"
echo ""
