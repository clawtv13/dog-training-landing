#!/bin/bash
# AI Automation Builder - Quick Setup Script

echo "=========================================="
echo "AI AUTOMATION BUILDER - SETUP"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p content/{editions,drafts,assets}
mkdir -p templates
mkdir -p .state
echo "✓ Directories created"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✓ .env created - EDIT THIS FILE WITH YOUR API KEYS"
    echo ""
fi

# Test database
echo "🗄️  Testing database..."
python3 -c "import sqlite3; conn = sqlite3.connect('database/newsletter.db'); print('✓ Database accessible')"
echo ""

# Check current status
echo "📊 Current Status:"
python3 << EOF
import sqlite3
conn = sqlite3.connect('database/newsletter.db')
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM editions')
editions = c.fetchone()[0]
print(f"   Editions published: {editions}")

c.execute('SELECT COUNT(*) FROM content_items')
items = c.fetchone()[0]
print(f"   Content items: {items}")

c.execute('SELECT MAX(total_subscribers) FROM subscriber_stats')
subs = c.fetchone()[0] or 0
print(f"   Current subscribers: {subs}")

conn.close()
EOF

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env with your API keys:"
echo "   nano .env"
echo ""
echo "2. Test the research script:"
echo "   python3 scripts/daily-research.py"
echo ""
echo "3. Generate a test edition:"
echo "   python3 scripts/weekly-generate.py"
echo ""
echo "4. Read documentation:"
echo "   cat docs/GETTING-STARTED.md"
echo ""
echo "=========================================="
