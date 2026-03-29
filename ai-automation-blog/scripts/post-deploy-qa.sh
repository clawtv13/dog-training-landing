#!/bin/bash
# Post-Deploy QA Workflow
# Runs after every blog deployment to verify everything works

set -e

echo "============================================================"
echo "🤖 POST-DEPLOY QA WORKFLOW"
echo "============================================================"
echo ""

cd "$(dirname "$0")/.."

# Step 1: Run QA tests
echo "📋 Step 1: Running QA tests..."
python3 scripts/qa-agent.py

QA_EXIT=$?

if [ $QA_EXIT -eq 0 ]; then
    echo ""
    echo "✅ All tests passed - no fixes needed"
    exit 0
fi

# Step 2: Bugs found, attempt auto-fix
echo ""
echo "🔧 Step 2: Bugs detected, attempting auto-fix..."
python3 scripts/qa-autofix.py

# Step 3: Re-run QA to verify fixes
echo ""
echo "🔄 Step 3: Re-running QA tests after fixes..."
sleep 120  # Wait for GitHub Pages to rebuild

python3 scripts/qa-agent.py

FINAL_EXIT=$?

if [ $FINAL_EXIT -eq 0 ]; then
    echo ""
    echo "✅ All bugs fixed automatically!"
    exit 0
else
    echo ""
    echo "⚠️  Some bugs remain - manual intervention needed"
    echo "Check: .state/qa-bugs.json"
    exit 1
fi
