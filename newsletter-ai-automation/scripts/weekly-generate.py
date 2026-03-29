#!/usr/bin/env python3
"""
AI Automation Builder - Weekly Newsletter Generation

Runs every Wednesday at 10:00 UTC to:
1. Pull top content from database (last 7 days)
2. Generate newsletter with Claude
3. Create draft in Beehiiv
4. Notify via Telegram

Edition is saved as draft for manual review before Friday publish.
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"
CONTENT_PATH = Path(__file__).parent.parent / "content"
STATE_PATH = Path(__file__).parent.parent / ".state"

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BEEHIIV_API_KEY = os.getenv("BEEHIIV_API_KEY", "")
BEEHIIV_PUBLICATION_ID = os.getenv("BEEHIIV_PUBLICATION_ID", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Newsletter settings
NEWSLETTER_NAME = "AI Automation Builder"
TARGET_WORD_COUNT = 800  # Approx 5 min read

# ============================================================================
# DATABASE QUERIES
# ============================================================================

def get_top_content(days=7, limit=20):
    """
    Fetch top unfeatured content from last N days
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    c.execute('''
        SELECT 
            id, url, title, source, type, total_score,
            relevance_score, novelty_score, usefulness_score, impact_score,
            summary, newsletter_section, published_date
        FROM content_items
        WHERE featured_in_edition IS NULL
        AND created_at >= ?
        ORDER BY total_score DESC, created_at DESC
        LIMIT ?
    ''', (cutoff_date, limit))
    
    items = []
    for row in c.fetchall():
        items.append({
            'id': row[0],
            'url': row[1],
            'title': row[2],
            'source': row[3],
            'type': row[4],
            'total_score': row[5],
            'relevance_score': row[6],
            'novelty_score': row[7],
            'usefulness_score': row[8],
            'impact_score': row[9],
            'summary': row[10],
            'section': row[11],
            'published': row[12]
        })
    
    conn.close()
    return items

def get_next_edition_number():
    """
    Get next edition number
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT MAX(edition_number) FROM editions')
    last_edition = c.fetchone()[0]
    
    conn.close()
    return (last_edition or 0) + 1

def mark_items_featured(item_ids, edition_number):
    """
    Mark items as featured in edition
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    placeholders = ','.join('?' * len(item_ids))
    c.execute(f'''
        UPDATE content_items
        SET featured_in_edition = ?
        WHERE id IN ({placeholders})
    ''', [edition_number] + item_ids)
    
    conn.commit()
    conn.close()

# ============================================================================
# CLAUDE GENERATION
# ============================================================================

def generate_newsletter_content(items, edition_number):
    """
    Use Claude to write newsletter from curated items
    """
    if not OPENROUTER_API_KEY:
        print("⚠️  OpenRouter API key not set, generating basic template...\n")
        return generate_basic_template(items, edition_number)
    
    print(f"✍️  Generating newsletter #{edition_number} with Claude...\n")
    
    # Organize items by section
    sections = {}
    for item in items:
        section = item.get('section', 'Quick Hit')
        if section not in sections:
            sections[section] = []
        sections[section].append(item)
    
    prompt = f"""Write edition #{edition_number} of "{NEWSLETTER_NAME}", a weekly newsletter for solopreneurs building automated businesses with AI.

**Target length:** ~{TARGET_WORD_COUNT} words (5 min read)

**Tone:**
- Direct, no fluff
- Technical but accessible
- Excited about AI, realistic about challenges
- Like talking to a fellow indie hacker

**Structure:**

1. **Opening (50 words):** Hook with week's biggest story or trend. Personal angle.

2. **🔧 Tool of the Week (200 words):** Deep-dive on ONE tool.
   - What it does
   - Why it matters for solopreneurs
   - Practical use case
   - Pricing
   - Link

3. **⚡ Automation Workflow (150 words):** Step-by-step mini-tutorial.
   - Specific problem it solves
   - Tools needed
   - High-level steps
   - Expected result/time savings

4. **📰 This Week in AI (250 words):** 5-7 quick hits
   - Each: headline + 2-3 sentences + link
   - Mix news, tools, repos, discussions
   - Order by impact

5. **💡 Case Study (100 words):** Real business using AI automation
   - What they built
   - Tech stack
   - Results (revenue/time saved)
   - Key lesson

6. **Closing (50 words):** Quick outro + CTA (reply with your automation wins)

**Content to use:**

{json.dumps([{
    'title': item['title'],
    'url': item['url'],
    'summary': item['summary'],
    'score': item['total_score'],
    'section': item['section']
} for item in items[:15]], indent=2)}

**Guidelines:**
- NO generic AI hype ("game-changer", "revolutionary")
- YES specific benefits ("saves 5 hrs/week", "$200/mo cheaper than")
- Use actual numbers and examples
- Every link should add real value
- Write like you're DMing a founder friend

Output HTML ready for Beehiiv (use <h2>, <p>, <ul>, <a href="">)."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aiautomationbuilder.beehiiv.com"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8192
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            print(f"✅ Generated {len(content)} characters\n")
            return content
        else:
            print(f"✗ Claude API error: {response.status_code}\n")
            return generate_basic_template(items, edition_number)
            
    except Exception as e:
        print(f"✗ Generation error: {e}\n")
        return generate_basic_template(items, edition_number)

def generate_basic_template(items, edition_number):
    """
    Fallback basic template when Claude unavailable
    """
    print("📝 Using basic template...\n")
    
    html = f"""<h1>AI Automation Builder #{edition_number}</h1>

<p>Hey builders 👋</p>

<p>This week: {len(items)} curated tools, workflows, and insights for building automated businesses with AI.</p>

<h2>🔧 Top Picks This Week</h2>

<ul>
"""
    
    for item in items[:7]:
        html += f"""<li><strong><a href="{item['url']}">{item['title']}</a></strong> - {item['summary']}</li>\n"""
    
    html += """</ul>

<h2>⚡ Quick Hits</h2>

<ul>
"""
    
    for item in items[7:12]:
        html += f"""<li><a href="{item['url']}">{item['title']}</a></li>\n"""
    
    html += """</ul>

<p><strong>Reply to this email</strong> with what you're automating this week. I read every response 📬</p>

<p>— n0mad</p>
"""
    
    return html

def generate_subject_lines(items):
    """
    Generate 5 subject line options with Claude
    """
    if not OPENROUTER_API_KEY:
        return [
            f"AI Automation Builder - {items[0]['title'][:30]}...",
            f"This week: {len(items)} AI automation tools",
            f"New AI tools for solopreneurs",
            f"Weekly AI automation roundup",
            f"Build smarter, not harder"
        ]
    
    print("📧 Generating subject lines...\n")
    
    top_5_titles = [item['title'] for item in items[:5]]
    
    prompt = f"""Generate 5 subject line options for this AI automation newsletter edition.

Top stories this week:
{json.dumps(top_5_titles, indent=2)}

Requirements:
- 40-60 characters
- Curiosity gap but not clickbait
- Include specific benefit or number when possible
- Professional tone (no ALL CAPS or excessive punctuation)
- Avoid: "game-changer", "revolutionary", generic hype

Examples of good subject lines:
- "3 AI workflows that saved me 10 hrs this week"
- "The $29/mo tool replacing my $500/mo dev"
- "Building a $2K/mo SaaS with no-code + AI"

Return JSON array of 5 strings, ranked by predicted open rate (best first)."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            subject_lines = json.loads(content)
            
            print(f"✅ Generated {len(subject_lines)} subject lines\n")
            return subject_lines
        else:
            return generate_basic_subjects(items)
            
    except Exception as e:
        print(f"✗ Subject line error: {e}\n")
        return generate_basic_subjects(items)

def generate_basic_subjects(items):
    """Fallback subject lines"""
    return [
        f"AI tools & automation tips (Edition #{get_next_edition_number()})",
        f"This week in AI automation",
        f"New: {items[0]['title'][:40]}...",
        f"Weekly automation roundup",
        f"Build smarter with AI"
    ]

# ============================================================================
# BEEHIIV INTEGRATION
# ============================================================================

def publish_to_beehiiv(content, subject_line, edition_number):
    """
    Create draft edition in Beehiiv
    """
    if not BEEHIIV_API_KEY or not BEEHIIV_PUBLICATION_ID:
        print("⚠️  Beehiiv credentials not set, saving locally only...\n")
        return save_locally(content, subject_line, edition_number)
    
    print(f"📤 Publishing to Beehiiv as draft...\n")
    
    url = f"https://api.beehiiv.com/v2/publications/{BEEHIIV_PUBLICATION_ID}/posts"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": subject_line,
        "content_html": content,
        "status": "draft",
        "platform": "both",  # email + web
        "audience": "free"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 201:
            data = response.json()
            draft_url = data.get('web_url', 'N/A')
            
            print(f"✅ Draft created in Beehiiv\n")
            print(f"🔗 Review at: {draft_url}\n")
            
            return {
                'success': True,
                'draft_url': draft_url,
                'beehiiv_id': data.get('id')
            }
        else:
            print(f"✗ Beehiiv API error: {response.status_code} - {response.text}\n")
            return save_locally(content, subject_line, edition_number)
            
    except Exception as e:
        print(f"✗ Beehiiv error: {e}\n")
        return save_locally(content, subject_line, edition_number)

def save_locally(content, subject_line, edition_number):
    """
    Save draft locally when Beehiiv unavailable
    """
    draft_path = CONTENT_PATH / "drafts" / f"edition-{edition_number:03d}.html"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(draft_path, 'w') as f:
        f.write(f"<!-- Subject: {subject_line} -->\n\n")
        f.write(content)
    
    print(f"💾 Saved locally: {draft_path}\n")
    
    return {
        'success': True,
        'draft_url': str(draft_path),
        'beehiiv_id': None
    }

# ============================================================================
# TELEGRAM NOTIFICATION
# ============================================================================

def send_telegram_notification(edition_number, draft_url, subject_line):
    """
    Notify via Telegram that draft is ready
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials not set, skipping notification\n")
        return
    
    message = f"""📰 **AI Automation Builder #{edition_number}**

✅ Draft ready for review!

**Subject:** {subject_line}

🔗 **Review:** {draft_url}

Schedule for Friday 08:00 UTC after approval."""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Telegram notification sent\n")
        else:
            print(f"✗ Telegram error: {response.status_code}\n")
            
    except Exception as e:
        print(f"✗ Telegram error: {e}\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main weekly generation workflow
    """
    print("=" * 60)
    print("AI AUTOMATION BUILDER - WEEKLY GENERATION")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    # Get next edition number
    edition_number = get_next_edition_number()
    print(f"\n📰 Generating Edition #{edition_number}\n")
    
    # Get top content from last 7 days
    items = get_top_content(days=7, limit=20)
    
    if len(items) < 5:
        print(f"⚠️  Only {len(items)} items available. Need at least 5.")
        print("Run daily-research.py first to collect content.\n")
        return
    
    print(f"📊 Using {len(items)} content items\n")
    
    # Generate newsletter content
    content = generate_newsletter_content(items, edition_number)
    
    # Generate subject lines
    subject_lines = generate_subject_lines(items)
    best_subject = subject_lines[0]
    
    print(f"📧 Best subject line: {best_subject}\n")
    
    # Publish as draft
    result = publish_to_beehiiv(content, best_subject, edition_number)
    
    if result['success']:
        # Mark items as featured
        featured_ids = [item['id'] for item in items[:10]]  # Top 10 featured
        mark_items_featured(featured_ids, edition_number)
        
        # Save edition record to database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO editions (edition_number, publish_date, subject_line, status)
            VALUES (?, ?, ?, 'draft')
        ''', (edition_number, datetime.now().isoformat(), best_subject))
        
        conn.commit()
        conn.close()
        
        # Send Telegram notification
        send_telegram_notification(edition_number, result['draft_url'], best_subject)
        
        # Save state
        state = {
            'last_edition': edition_number,
            'last_run': datetime.now().isoformat(),
            'draft_url': result['draft_url'],
            'subject_line': best_subject,
            'items_featured': len(featured_ids)
        }
        
        with open(STATE_PATH / 'weekly-generate-state.json', 'w') as f:
            json.dump(state, f, indent=2)
        
        print("=" * 60)
        print("✅ WEEKLY GENERATION COMPLETE")
        print(f"Edition #{edition_number} ready for review!")
        print("=" * 60)
    else:
        print("✗ Generation failed, check logs\n")

if __name__ == "__main__":
    main()
