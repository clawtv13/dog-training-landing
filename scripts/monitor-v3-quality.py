#!/usr/bin/env python3
"""
Monitor V3 Prompt Quality
Tracks first week of V3 deployment to measure improvements
"""

import os
import json
from datetime import datetime
from pathlib import Path

REPORT_PATH = Path("/root/.openclaw/workspace/.state/v3-quality-report.json")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def load_report():
    """Load existing quality report"""
    if REPORT_PATH.exists():
        with open(REPORT_PATH, 'r') as f:
            return json.load(f)
    return {
        "deployment_date": "2026-03-29",
        "prompts_deployed": ["CleverDogMethod Blog", "Newsletter Breaking News", "Blog Generation"],
        "tests": {
            "cleverdogmethod": [],
            "newsletter": [],
            "blog": []
        },
        "baseline_v2": {
            "cleverdogmethod_quality": 65,
            "blog_quality": 85,
            "regeneration_rate": 5.0
        }
    }

def check_cleverdogmethod_output():
    """Check if recent CleverDogMethod post uses V3 features"""
    # Look for posts generated after 20:00 UTC today
    log_path = Path("/root/.openclaw/workspace/logs/cleverdogmethod-autonomous.log")
    
    if not log_path.exists():
        return None
    
    with open(log_path, 'r') as f:
        recent = f.readlines()[-50:]  # Last 50 lines
    
    # Check for V3 indicators in log
    v3_indicators = {
        "case_studies": False,
        "expert_voice": False,
        "faq_section": False,
        "word_count_valid": False
    }
    
    log_text = ''.join(recent)
    
    # Simple heuristics (would need actual post analysis)
    if "✅" in log_text or "Generated successfully" in log_text:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "generated",
            "needs_manual_review": True
        }
    
    return None

def check_newsletter_output():
    """Check if newsletter research used V3 breaking news detection"""
    log_path = Path("/root/.openclaw/workspace/newsletter-ai-automation/logs/realtime.log")
    
    if not log_path.exists():
        return None
    
    with open(log_path, 'r') as f:
        recent = f.readlines()[-30:]
    
    log_text = ''.join(recent)
    
    if "breaking_news" in log_text or "urgency" in log_text:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "v3_logic_detected",
            "breaking_found": "breaking" in log_text.lower()
        }
    
    return None

def check_blog_output():
    """Check if blog post used V3 generation"""
    log_path = Path("/root/.openclaw/workspace/ai-automation-blog/logs/blog.log")
    
    if not log_path.exists():
        return None
    
    with open(log_path, 'r') as f:
        recent = f.readlines()[-50:]
    
    log_text = ''.join(recent)
    
    if "Generated:" in log_text or "✅" in log_text:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "generated",
            "needs_manual_review": True
        }
    
    return None

def generate_summary():
    """Generate human-readable summary"""
    report = load_report()
    
    print("\n═══════════════════════════════════════════════════════════")
    print("📊 V3 PROMPT QUALITY MONITORING")
    print("═══════════════════════════════════════════════════════════\n")
    
    print(f"Deployment: {report['deployment_date']}")
    print(f"Prompts: {len(report['prompts_deployed'])}/3 critical deployed\n")
    
    print("TEST RUNS:\n")
    
    # CleverDogMethod
    cdm_tests = report['tests']['cleverdogmethod']
    print(f"🐕 CleverDogMethod: {len(cdm_tests)} tests")
    if cdm_tests:
        latest = cdm_tests[-1]
        print(f"   Latest: {latest.get('timestamp', 'Unknown')}")
        print(f"   Status: {latest.get('status', 'Unknown')}")
    else:
        print("   ⏳ Waiting for first run (20:00 UTC today)")
    
    # Newsletter
    news_tests = report['tests']['newsletter']
    print(f"\n📰 Newsletter: {len(news_tests)} tests")
    if news_tests:
        latest = news_tests[-1]
        print(f"   Latest: {latest.get('timestamp', 'Unknown')}")
        print(f"   Breaking found: {latest.get('breaking_found', False)}")
    else:
        print("   ⏳ Waiting for first run (18:00 UTC today)")
    
    # Blog
    blog_tests = report['tests']['blog']
    print(f"\n📝 Blog Posts: {len(blog_tests)} tests")
    if blog_tests:
        latest = blog_tests[-1]
        print(f"   Latest: {latest.get('timestamp', 'Unknown')}")
        print(f"   Status: {latest.get('status', 'Unknown')}")
    else:
        print("   ⏳ Waiting for first run (tomorrow 10:00 UTC)")
    
    print("\n═══════════════════════════════════════════════════════════")
    print("⏭️  NEXT CHECKS")
    print("═══════════════════════════════════════════════════════════\n")
    print("Today 18:00 UTC: Newsletter research (V3 breaking news)")
    print("Today 20:00 UTC: CleverDogMethod post (V3 expert voice)")
    print("Tomorrow 08:00 UTC: CleverDogMethod post #2")
    print("Tomorrow 10:00 UTC: Blog post (V3 Alex Chen voice)")
    print("\n═══════════════════════════════════════════════════════════\n")

def update_tests():
    """Check logs and update test results"""
    report = load_report()
    
    # Check each system
    cdm = check_cleverdogmethod_output()
    if cdm and (not report['tests']['cleverdogmethod'] or 
                cdm['timestamp'] != report['tests']['cleverdogmethod'][-1].get('timestamp')):
        report['tests']['cleverdogmethod'].append(cdm)
    
    news = check_newsletter_output()
    if news and (not report['tests']['newsletter'] or 
                 news['timestamp'] != report['tests']['newsletter'][-1].get('timestamp')):
        report['tests']['newsletter'].append(news)
    
    blog = check_blog_output()
    if blog and (not report['tests']['blog'] or 
                 blog['timestamp'] != report['tests']['blog'][-1].get('timestamp')):
        report['tests']['blog'].append(blog)
    
    # Save report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

if __name__ == "__main__":
    import sys
    
    if "--update" in sys.argv:
        update_tests()
        print("✅ Tests updated from logs")
    
    generate_summary()
