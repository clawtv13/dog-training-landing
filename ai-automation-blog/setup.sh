#!/bin/bash
# Quick setup script for monetization infrastructure

set -e

echo "🚀 Setting up AI Automation Blog Monetization Infrastructure..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Initialize databases
echo ""
echo "📊 Initializing databases..."
python3 monetization-agent.py << EOF
quit
EOF

echo "✅ Sponsor CRM database created"

python3 affiliate-manager.py << EOF
quit
EOF

echo "✅ Affiliate tracking database created"

# Check if data loaded
if [ -f "data/sponsors.db" ] && [ -f "data/affiliates.db" ]; then
    echo "✅ Databases initialized successfully"
else
    echo "⚠️  Database initialization may have failed. Check logs."
fi

echo ""
echo "📧 Email templates ready in templates/"
echo "   • email-initial.txt"
echo "   • email-followup-1.txt"
echo "   • email-followup-2.txt"
echo ""
echo "📋 Data files ready:"
echo "   • data/sponsor-prospects.json (50+ prospects)"
echo "   • data/affiliate-programs.json (15+ programs)"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Customize email templates:"
echo "   nano templates/email-initial.txt"
echo ""
echo "2. Update affiliate links with your ref codes:"
echo "   nano data/affiliate-programs.json"
echo ""
echo "3. Run revenue dashboard:"
echo "   python3 revenue-dashboard.py"
echo ""
echo "4. Start sponsor outreach (dry run):"
echo "   python3 monetization-agent.py"
echo ""
echo "5. Scan blog for affiliate opportunities:"
echo "   python3 affiliate-manager.py"
echo ""
echo "📖 Read the complete playbook:"
echo "   cat MONETIZATION-STRATEGY.md"
echo ""
echo "✨ Setup complete! Ready to monetize. 🚀"
