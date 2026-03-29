#!/usr/bin/env python3
"""
Process Email Captures from LocalStorage
Run via cron every hour to sync emails from browser localStorage
"""

import json
from pathlib import Path
from datetime import datetime

EMAIL_LOG = Path("/root/.openclaw/workspace/.state/cleverdogmethod-emails.json")

def load_emails():
    """Load existing emails"""
    if EMAIL_LOG.exists():
        with open(EMAIL_LOG, 'r') as f:
            return json.load(f)
    return []

def save_email(email_data):
    """Save new email capture"""
    
    emails = load_emails()
    
    # Check duplicate
    is_duplicate = any(e['email'] == email_data['email'] for e in emails)
    
    if not is_duplicate:
        email_data['captured_at'] = datetime.now().isoformat()
        emails.append(email_data)
        
        EMAIL_LOG.parent.mkdir(exist_ok=True)
        with open(EMAIL_LOG, 'w') as f:
            json.dump(emails, f, indent=2)
        
        print(f"✅ New email: {email_data['email']}")
        print(f"   Resource: {email_data.get('resource', 'general')}")
        print(f"   Total emails: {len(emails)}")
        
        return True
    else:
        print(f"⚠️  Duplicate: {email_data['email']}")
        return False

def export_to_csv():
    """Export emails to CSV for import to Mailchimp/ConvertKit"""
    
    emails = load_emails()
    
    csv_file = EMAIL_LOG.parent / "cleverdogmethod-emails.csv"
    
    with open(csv_file, 'w') as f:
        f.write("Email,Resource,Page,Source,Date\n")
        for e in emails:
            f.write(f"{e['email']},{e.get('resource','')},{e.get('page','')},{e.get('source','')},{e.get('timestamp','')}\n")
    
    print(f"\n✅ Exported {len(emails)} emails to CSV")
    print(f"   File: {csv_file}")

def stats():
    """Show email capture statistics"""
    
    emails = load_emails()
    
    print(f"\n📊 EMAIL CAPTURE STATS")
    print(f"="*50)
    print(f"Total emails: {len(emails)}")
    
    # By resource
    resources = {}
    for e in emails:
        r = e.get('resource', 'unknown')
        resources[r] = resources.get(r, 0) + 1
    
    print(f"\n📁 By Resource:")
    for resource, count in sorted(resources.items(), key=lambda x: x[1], reverse=True):
        print(f"   {resource}: {count}")
    
    # By source
    sources = {}
    for e in emails:
        s = e.get('source', 'unknown')
        sources[s] = sources.get(s, 0) + 1
    
    print(f"\n📍 By Source:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"   {source}: {count}")
    
    # Recent
    print(f"\n🕒 Last 5 Captures:")
    for e in emails[-5:]:
        print(f"   {e['email']} - {e.get('resource', 'general')}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'stats':
            stats()
        elif sys.argv[1] == 'export':
            export_to_csv()
    else:
        # Show current status
        emails = load_emails()
        print(f"📧 Total emails captured: {len(emails)}")
        print(f"📁 File: {EMAIL_LOG}")
        print(f"\nRun with:")
        print(f"  python3 {__file__} stats")
        print(f"  python3 {__file__} export")
