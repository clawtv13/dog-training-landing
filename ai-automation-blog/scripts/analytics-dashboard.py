#!/usr/bin/env python3
"""
AI Automation Blog - Analytics Dashboard
Weekly Telegram report with charts and insights
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
STATE_DIR = WORKSPACE / ".state"
REPORTS_DIR = WORKSPACE / "reports"
PROMPTS_DIR = WORKSPACE / "prompts"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"

ANALYTICS_FILE = STATE_DIR / "analytics.json"
PUBLISHED_FILE = STATE_DIR / "published-posts.json"
AB_TEST_FILE = PROMPTS_DIR / "ab-test.json"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8116230130")

# ============================================================================
# DATA LOADING
# ============================================================================

def load_json(path: Path, default=None):
    """Load JSON file with fallback"""
    if not path.exists():
        return default or {}
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default or {}

def load_analytics():
    """Load analytics data"""
    data = load_json(ANALYTICS_FILE, {"posts": [], "summary": {}})
    return data.get("posts", [])

def load_published_posts():
    """Load published posts"""
    return load_json(PUBLISHED_FILE, [])

def load_ab_test():
    """Load A/B test config if exists"""
    return load_json(AB_TEST_FILE, None)

def load_content_items():
    """Load content items from newsletter DB"""
    if not NEWSLETTER_DB.exists():
        return []
    
    try:
        conn = sqlite3.connect(NEWSLETTER_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all content items used for blog
        cursor.execute("""
            SELECT id, url, title, source, type, total_score, 
                   relevance_score, novelty_score, usefulness_score, impact_score,
                   summary, newsletter_section, published_date, created_at, blog_used
            FROM content_items
            WHERE blog_used = 1
            ORDER BY created_at DESC
        """)
        
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items
    except Exception as e:
        print(f"⚠️ Error loading content items: {e}")
        return []

# ============================================================================
# ANALYTICS CALCULATIONS
# ============================================================================

def calculate_week_stats(posts, days=7):
    """Calculate stats for the last N days"""
    cutoff = datetime.now() - timedelta(days=days)
    
    week_posts = [
        p for p in posts 
        if datetime.fromisoformat(p['published_at'].replace('Z', '+00:00')) > cutoff
    ]
    
    if not week_posts:
        return {
            'count': 0,
            'avg_score': 0,
            'avg_word_count': 0,
            'total_engagement': 0
        }
    
    return {
        'count': len(week_posts),
        'avg_score': sum(p.get('source_score', 0) for p in week_posts) / len(week_posts),
        'avg_word_count': sum(p.get('word_count', 0) for p in week_posts) / len(week_posts),
        'total_engagement': sum(p.get('engagement_score', 0) for p in week_posts)
    }

def get_top_performers(posts, limit=5, days=7):
    """Get top performing posts by quality score"""
    cutoff = datetime.now() - timedelta(days=days)
    
    week_posts = [
        p for p in posts 
        if datetime.fromisoformat(p['published_at'].replace('Z', '+00:00')) > cutoff
    ]
    
    # Sort by source_score (quality indicator from HN)
    sorted_posts = sorted(week_posts, key=lambda x: x.get('source_score', 0), reverse=True)
    
    return sorted_posts[:limit]

def classify_topic(title):
    """Simple topic classification based on keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['claude', 'chatgpt', 'openai', 'ai', 'llm', 'gpt']):
        return 'AI Tools'
    elif any(word in title_lower for word in ['code', 'coding', 'programming', 'software', 'developer']):
        return 'Development'
    elif any(word in title_lower for word in ['founder', 'business', 'startup', 'solo', 'entrepreneur']):
        return 'Business'
    elif any(word in title_lower for word in ['security', 'privacy', 'facial', 'police']):
        return 'Security/Privacy'
    elif any(word in title_lower for word in ['windows', 'system', 'file']):
        return 'Systems'
    else:
        return 'Other'

def get_topic_distribution(posts, days=7):
    """Get distribution of topics"""
    cutoff = datetime.now() - timedelta(days=days)
    
    week_posts = [
        p for p in posts 
        if datetime.fromisoformat(p['published_at'].replace('Z', '+00:00')) > cutoff
    ]
    
    topics = [classify_topic(p['title']) for p in week_posts]
    return Counter(topics)

def analyze_ab_test(ab_config, posts):
    """Analyze A/B test performance if active"""
    if not ab_config or not ab_config.get('active'):
        return None
    
    variant_a_posts = [p for p in posts if p.get('prompt_variant') == 'A']
    variant_b_posts = [p for p in posts if p.get('prompt_variant') == 'B']
    
    if not variant_a_posts or not variant_b_posts:
        return {
            'status': 'insufficient_data',
            'variant_a_count': len(variant_a_posts),
            'variant_b_count': len(variant_b_posts)
        }
    
    a_avg_score = sum(p.get('source_score', 0) for p in variant_a_posts) / len(variant_a_posts)
    b_avg_score = sum(p.get('source_score', 0) for p in variant_b_posts) / len(variant_b_posts)
    
    improvement = ((b_avg_score - a_avg_score) / a_avg_score * 100) if a_avg_score > 0 else 0
    
    # Simple significance test: >10% difference with at least 5 samples each
    significant = abs(improvement) > 10 and len(variant_a_posts) >= 5 and len(variant_b_posts) >= 5
    
    return {
        'status': 'active',
        'variant_a': {
            'count': len(variant_a_posts),
            'avg_score': round(a_avg_score, 1)
        },
        'variant_b': {
            'count': len(variant_b_posts),
            'avg_score': round(b_avg_score, 1)
        },
        'improvement': round(improvement, 1),
        'significant': significant,
        'winner': 'B' if b_avg_score > a_avg_score and significant else 'A' if significant else None
    }

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_topic_pie_chart(topic_dist, filename):
    """Generate pie chart for topic distribution"""
    if not topic_dist:
        return None
    
    labels = list(topic_dist.keys())
    sizes = list(topic_dist.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7B8EA']
    
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors[:len(labels)],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    ax.set_title('Topic Distribution (Last 7 Days)', fontsize=16, weight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    return filename

# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_recommendations(stats_current, stats_previous, topic_dist, ab_result):
    """Generate actionable recommendations"""
    recommendations = []
    
    # Quality trend
    if stats_current['avg_score'] > stats_previous['avg_score']:
        improvement = ((stats_current['avg_score'] - stats_previous['avg_score']) / stats_previous['avg_score'] * 100)
        recommendations.append(f"✅ Quality improved by {improvement:.1f}% this week")
    elif stats_current['avg_score'] < stats_previous['avg_score']:
        decline = ((stats_previous['avg_score'] - stats_current['avg_score']) / stats_previous['avg_score'] * 100)
        recommendations.append(f"⚠️ Quality declined by {decline:.1f}% — review content sources")
    
    # Top topic recommendation
    if topic_dist:
        top_topic = topic_dist.most_common(1)[0][0]
        recommendations.append(f"📈 Post more about {top_topic} (best performing topic)")
    
    # A/B test recommendation
    if ab_result and ab_result.get('significant'):
        winner = ab_result['winner']
        improvement = ab_result['improvement']
        recommendations.append(f"🧪 Consider promoting prompt variant {winner} (+{improvement:.1f}% quality)")
    
    # Volume recommendation
    if stats_current['count'] < 14:  # Less than 2 per day on average
        recommendations.append("⏱️ Consider increasing posting frequency (current: ~2/day)")
    
    return recommendations

def generate_text_report(stats_current, stats_previous, top_posts, topic_dist, ab_result, recommendations):
    """Generate text summary for Telegram"""
    
    # Trend indicator
    if stats_current['avg_score'] > stats_previous['avg_score']:
        trend = "↗️ improving"
    elif stats_current['avg_score'] < stats_previous['avg_score']:
        trend = "↘️ declining"
    else:
        trend = "→ stable"
    
    # Format report
    report = f"""📊 **Weekly Analytics Report**
_{datetime.now().strftime('%Y-%m-%d')}_

**📝 Summary Stats**
• Posts this week: {stats_current['count']}
• Avg quality score: {stats_current['avg_score']:.1f} (prev: {stats_previous['avg_score']:.1f})
• Trend: {trend}

**🏆 Top Performers** (this week)
"""
    
    for i, post in enumerate(top_posts[:5], 1):
        topic = classify_topic(post['title'])
        score = post.get('source_score', 0)
        title = post['title'][:60] + '...' if len(post['title']) > 60 else post['title']
        report += f"{i}. {title}\n   Score: {score} | Topic: {topic}\n\n"
    
    # Topic distribution
    if topic_dist:
        report += "\n**📊 Topic Distribution**\n"
        for topic, count in topic_dist.most_common():
            pct = (count / stats_current['count'] * 100) if stats_current['count'] > 0 else 0
            report += f"• {topic}: {count} posts ({pct:.1f}%)\n"
    
    # A/B test results
    if ab_result and ab_result['status'] == 'active':
        report += f"\n**🧪 A/B Test Results**\n"
        report += f"• Variant A: {ab_result['variant_a']['count']} posts, avg score {ab_result['variant_a']['avg_score']}\n"
        report += f"• Variant B: {ab_result['variant_b']['count']} posts, avg score {ab_result['variant_b']['avg_score']}\n"
        
        if ab_result['significant']:
            report += f"• **Winner: Variant {ab_result['winner']}** ({ab_result['improvement']:+.1f}% improvement)\n"
        else:
            report += f"• Difference: {ab_result['improvement']:+.1f}% (not significant yet)\n"
    
    # Recommendations
    if recommendations:
        report += "\n**💡 Recommendations**\n"
        for rec in recommendations:
            report += f"• {rec}\n"
    
    return report

def save_markdown_report(text_report, filename):
    """Save full report to markdown file"""
    with open(filename, 'w') as f:
        f.write(f"# Analytics Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(text_report.replace('**', '##').replace('_', '*'))
    
    return filename

# ============================================================================
# TELEGRAM DELIVERY
# ============================================================================

def send_telegram_message(text):
    """Send text message to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }, timeout=30)
        
        if response.status_code == 200:
            print("✅ Telegram message sent")
            return True
        else:
            print(f"❌ Telegram error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        return False

def send_telegram_photo(photo_path, caption=""):
    """Send photo to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    try:
        with open(photo_path, 'rb') as photo:
            response = requests.post(url, data={
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption
            }, files={
                'photo': photo
            }, timeout=30)
        
        if response.status_code == 200:
            print("✅ Telegram photo sent")
            return True
        else:
            print(f"❌ Telegram photo error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Telegram photo send failed: {e}")
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("📊 Generating Analytics Dashboard...")
    
    # Load data
    posts = load_analytics()
    published = load_published_posts()
    ab_config = load_ab_test()
    
    if not posts:
        print("⚠️ No analytics data found")
        return
    
    # Calculate stats
    stats_current = calculate_week_stats(posts, days=7)
    stats_previous = calculate_week_stats(posts, days=14)  # Previous 7-14 days for comparison
    
    # Adjust previous week to only include days 8-14
    all_posts = posts
    cutoff_week = datetime.now() - timedelta(days=7)
    cutoff_prev = datetime.now() - timedelta(days=14)
    
    prev_week_posts = [
        p for p in all_posts 
        if cutoff_prev < datetime.fromisoformat(p['published_at'].replace('Z', '+00:00')) <= cutoff_week
    ]
    
    if prev_week_posts:
        stats_previous = {
            'count': len(prev_week_posts),
            'avg_score': sum(p.get('source_score', 0) for p in prev_week_posts) / len(prev_week_posts),
            'avg_word_count': sum(p.get('word_count', 0) for p in prev_week_posts) / len(prev_week_posts),
            'total_engagement': sum(p.get('engagement_score', 0) for p in prev_week_posts)
        }
    
    top_posts = get_top_performers(posts, limit=5, days=7)
    topic_dist = get_topic_distribution(posts, days=7)
    ab_result = analyze_ab_test(ab_config, posts)
    
    # Generate recommendations
    recommendations = generate_recommendations(stats_current, stats_previous, topic_dist, ab_result)
    
    # Create visualizations
    chart_file = REPORTS_DIR / f"topic-distribution-{datetime.now().strftime('%Y-%m-%d')}.png"
    if topic_dist:
        create_topic_pie_chart(topic_dist, chart_file)
        print(f"📈 Chart saved: {chart_file}")
    
    # Generate text report
    text_report = generate_text_report(stats_current, stats_previous, top_posts, topic_dist, ab_result, recommendations)
    
    # Save markdown report
    report_file = REPORTS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    save_markdown_report(text_report, report_file)
    print(f"📄 Report saved: {report_file}")
    
    # Send to Telegram
    print("\n📤 Sending to Telegram...")
    send_telegram_message(text_report)
    
    if chart_file.exists():
        send_telegram_photo(chart_file, caption="📊 Topic Distribution")
    
    print("\n✅ Analytics dashboard complete!")
    print(f"📊 {stats_current['count']} posts analyzed")
    print(f"🏆 Top score: {top_posts[0].get('source_score', 0) if top_posts else 0}")

if __name__ == "__main__":
    main()
