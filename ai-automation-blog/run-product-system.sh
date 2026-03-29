#!/bin/bash
# 🚀 Product Development System - Master Execution Script
# Run entire product generation pipeline

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🚀 PRODUCT DEVELOPMENT SYSTEM - AUTOMATED PIPELINE       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

WORKSPACE="/root/.openclaw/workspace/ai-automation-blog"
cd "$WORKSPACE" || exit 1

# Step 1: Product Creator
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 1: Product Creator Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 product-creator-agent.py
if [ $? -ne 0 ]; then
    echo "❌ Product Creator failed. Aborting."
    exit 1
fi
echo ""

# Step 2: Pricing Optimizer
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💰 STEP 2: Pricing Optimizer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 pricing-optimizer.py
if [ $? -ne 0 ]; then
    echo "❌ Pricing Optimizer failed. Aborting."
    exit 1
fi
echo ""

# Step 3: Launch Orchestrator
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 STEP 3: Launch Orchestrator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 launch-orchestrator.py
if [ $? -ne 0 ]; then
    echo "⚠️  Launch Orchestrator had errors (non-critical)"
fi
echo ""

# Step 4: Sales Page Generator
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 STEP 4: Sales Page Generator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 sales-page-generator.py
if [ $? -ne 0 ]; then
    echo "❌ Sales Page Generator failed. Aborting."
    exit 1
fi
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✅ SYSTEM COMPLETE - SUMMARY                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Generated Files:"
echo ""

cd products || exit 1

# Count files
PRODUCT_SPECS=$(ls -1 *[^-].json 2>/dev/null | grep -v "roadmap\|bundle\|launch-plan\|pricing\|sales-copy" | wc -l)
LAUNCH_PLANS=$(ls -1 *-launch-plan.json 2>/dev/null | wc -l)
PRICING_STRATEGIES=$(ls -1 *-pricing.json 2>/dev/null | wc -l)
LANDING_PAGES=$(ls -1 *-landing-page.html 2>/dev/null | wc -l)

echo "   📦 Product Specs: $PRODUCT_SPECS"
echo "   🚀 Launch Plans: $LAUNCH_PLANS"
echo "   💰 Pricing Strategies: $PRICING_STRATEGIES"
echo "   🎨 Landing Pages: $LANDING_PAGES"
echo ""
echo "📁 All files saved to:"
echo "   $WORKSPACE/products/"
echo ""
echo "📋 Next Steps:"
echo ""
echo "   1. Review product specs:"
echo "      cd products/ && cat *.md"
echo ""
echo "   2. View landing pages:"
echo "      open products/*-landing-page.html"
echo ""
echo "   3. Read launch plans:"
echo "      cat products/*-launch-plan.md"
echo ""
echo "   4. Check pricing strategies:"
echo "      cat products/*-pricing.json | jq '.recommended_price'"
echo ""
echo "   5. Review complete strategy:"
echo "      cat PRODUCT-STRATEGY.md"
echo ""
echo "🎯 Ready to Launch!"
echo ""
echo "╚═══════════════════════════════════════════════════════════╝"
