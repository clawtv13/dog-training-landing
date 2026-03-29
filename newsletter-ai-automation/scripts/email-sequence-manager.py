#!/usr/bin/env python3
"""
Email Sequence Manager - Automated email funnel engine for Beehiiv
Handles sequence delivery, personalization, triggers, and A/B testing
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from pathlib import Path

class EmailSequenceManager:
    def __init__(self, db_path: str = "email_sequences.db", beehiiv_api_key: str = None):
        self.db_path = db_path
        self.api_key = beehiiv_api_key or os.getenv("BEEHIIV_API_KEY")
        self.base_url = "https://api.beehiiv.com/v2"
        self.init_db()
        
    def init_db(self):
        """Initialize SQLite database for sequence tracking"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Subscribers table
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT PRIMARY KEY,
            subscription_id TEXT,
            first_name TEXT,
            last_name TEXT,
            subscribed_at TEXT,
            segment TEXT,
            engagement_score REAL DEFAULT 0,
            last_opened TEXT,
            last_clicked TEXT,
            conversion_status TEXT DEFAULT 'lead',
            ltv REAL DEFAULT 0
        )''')
        
        # Sequence enrollment table
        c.execute('''CREATE TABLE IF NOT EXISTS sequence_enrollment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            sequence_name TEXT,
            enrolled_at TEXT,
            current_step INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            variant TEXT,
            FOREIGN KEY (email) REFERENCES subscribers(email)
        )''')
        
        # Email tracking table
        c.execute('''CREATE TABLE IF NOT EXISTS email_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            sequence_name TEXT,
            email_step INTEGER,
            subject_line TEXT,
            sent_at TEXT,
            opened INTEGER DEFAULT 0,
            clicked INTEGER DEFAULT 0,
            converted INTEGER DEFAULT 0,
            variant TEXT,
            FOREIGN KEY (email) REFERENCES subscribers(email)
        )''')
        
        # Triggers table
        c.execute('''CREATE TABLE IF NOT EXISTS triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            trigger_type TEXT,
            trigger_data TEXT,
            fired_at TEXT,
            action_taken TEXT
        )''')
        
        conn.commit()
        conn.close()
        
    def load_sequence(self, sequence_path: str) -> Dict:
        """Load email sequence from JSON file"""
        with open(sequence_path, 'r') as f:
            return json.load(f)
    
    def enroll_subscriber(self, email: str, sequence_name: str, variant: str = "A"):
        """Enroll subscriber in email sequence"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Check if already enrolled
        c.execute('''SELECT id FROM sequence_enrollment 
                     WHERE email = ? AND sequence_name = ? AND completed = 0''',
                  (email, sequence_name))
        
        if c.fetchone():
            conn.close()
            return {"status": "already_enrolled"}
        
        # Enroll subscriber
        enrolled_at = datetime.now().isoformat()
        c.execute('''INSERT INTO sequence_enrollment 
                     (email, sequence_name, enrolled_at, variant) 
                     VALUES (?, ?, ?, ?)''',
                  (email, sequence_name, enrolled_at, variant))
        
        conn.commit()
        conn.close()
        
        return {"status": "enrolled", "sequence": sequence_name, "variant": variant}
    
    def process_sequences(self):
        """Process all active sequences and send due emails"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get all active enrollments
        c.execute('''SELECT e.id, e.email, e.sequence_name, e.current_step, 
                            e.enrolled_at, e.variant, s.first_name
                     FROM sequence_enrollment e
                     JOIN subscribers s ON e.email = s.email
                     WHERE e.completed = 0''')
        
        enrollments = c.fetchall()
        results = []
        
        for enrollment_id, email, sequence_name, current_step, enrolled_at, variant, first_name in enrollments:
            # Load sequence
            sequence_path = f"../sequences/{sequence_name}.json"
            if not os.path.exists(sequence_path):
                continue
                
            sequence = self.load_sequence(sequence_path)
            
            # Check if next email is due
            enrolled_date = datetime.fromisoformat(enrolled_at)
            current_email = sequence['emails'][current_step]
            days_delay = current_email.get('day', 0)
            
            send_date = enrolled_date + timedelta(days=days_delay)
            
            if datetime.now() >= send_date:
                # Send email
                result = self.send_email(
                    email=email,
                    sequence_name=sequence_name,
                    step=current_step,
                    email_data=current_email,
                    variant=variant,
                    personalization={'first_name': first_name or 'there'}
                )
                
                results.append(result)
                
                # Update enrollment
                next_step = current_step + 1
                if next_step >= len(sequence['emails']):
                    # Sequence complete
                    c.execute('''UPDATE sequence_enrollment 
                                 SET completed = 1, current_step = ? 
                                 WHERE id = ?''',
                              (next_step, enrollment_id))
                else:
                    c.execute('''UPDATE sequence_enrollment 
                                 SET current_step = ? 
                                 WHERE id = ?''',
                              (next_step, enrollment_id))
                
                conn.commit()
        
        conn.close()
        return results
    
    def send_email(self, email: str, sequence_name: str, step: int, 
                   email_data: Dict, variant: str, personalization: Dict) -> Dict:
        """Send individual email via Beehiiv API or manual trigger"""
        
        # Get variant subject and body if A/B testing
        subject = email_data.get(f'subject_{variant}', email_data.get('subject'))
        body = email_data.get(f'body_{variant}', email_data.get('body'))
        
        # Personalize content
        for key, value in personalization.items():
            subject = subject.replace(f'{{{{{key}}}}}', str(value))
            body = body.replace(f'{{{{{key}}}}}', str(value))
        
        # Track send
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO email_tracking 
                     (email, sequence_name, email_step, subject_line, sent_at, variant)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (email, sequence_name, step, subject, datetime.now().isoformat(), variant))
        conn.commit()
        conn.close()
        
        # Note: Beehiiv automation API requires setting up automations in UI
        # This returns content for manual sending or webhook integration
        return {
            "status": "ready_to_send",
            "email": email,
            "subject": subject,
            "body": body,
            "sequence": sequence_name,
            "step": step,
            "variant": variant
        }
    
    def track_open(self, email: str, sequence_name: str, step: int):
        """Track email open"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE email_tracking 
                     SET opened = 1 
                     WHERE email = ? AND sequence_name = ? AND email_step = ?''',
                  (email, sequence_name, step))
        
        c.execute('''UPDATE subscribers 
                     SET last_opened = ?, engagement_score = engagement_score + 1
                     WHERE email = ?''',
                  (datetime.now().isoformat(), email))
        
        conn.commit()
        conn.close()
    
    def track_click(self, email: str, sequence_name: str, step: int, url: str):
        """Track email click and trigger follow-up sequences"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE email_tracking 
                     SET clicked = 1 
                     WHERE email = ? AND sequence_name = ? AND email_step = ?''',
                  (email, sequence_name, step))
        
        c.execute('''UPDATE subscribers 
                     SET last_clicked = ?, engagement_score = engagement_score + 3
                     WHERE email = ?''',
                  (datetime.now().isoformat(), email))
        
        # Log trigger
        trigger_data = json.dumps({"url": url, "sequence": sequence_name, "step": step})
        c.execute('''INSERT INTO triggers 
                     (email, trigger_type, trigger_data, fired_at)
                     VALUES (?, ?, ?, ?)''',
                  (email, "click", trigger_data, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Check for triggered sequences
        self.check_triggers(email, "click", {"url": url})
    
    def track_conversion(self, email: str, product: str, amount: float):
        """Track conversion and update LTV"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE subscribers 
                     SET conversion_status = 'customer', ltv = ltv + ?
                     WHERE email = ?''',
                  (amount, email))
        
        # Mark all related emails as converted
        c.execute('''UPDATE email_tracking 
                     SET converted = 1 
                     WHERE email = ?''',
                  (email,))
        
        conn.commit()
        conn.close()
    
    def check_triggers(self, email: str, trigger_type: str, data: Dict):
        """Check and fire triggered sequences"""
        # Example: If clicked pricing link, enroll in abandoned cart sequence
        if trigger_type == "click" and "pricing" in data.get("url", "").lower():
            self.enroll_subscriber(email, "abandoned-cart", variant="A")
        
        # If downloaded lead magnet, enroll in upsell sequence
        if trigger_type == "click" and "download" in data.get("url", "").lower():
            self.enroll_subscriber(email, "upsell", variant="A")
    
    def segment_subscribers(self):
        """Automatically segment subscribers based on engagement"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Active: engagement_score >= 10, opened in last 7 days
        cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
        c.execute('''UPDATE subscribers 
                     SET segment = 'active' 
                     WHERE engagement_score >= 10 AND last_opened > ?''',
                  (cutoff_date,))
        
        # Warm: engagement_score >= 5, opened in last 30 days
        cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
        c.execute('''UPDATE subscribers 
                     SET segment = 'warm' 
                     WHERE engagement_score >= 5 AND engagement_score < 10 
                     AND last_opened > ?''',
                  (cutoff_date,))
        
        # Cold: low engagement or no recent opens
        c.execute('''UPDATE subscribers 
                     SET segment = 'cold' 
                     WHERE segment IS NULL OR (engagement_score < 5 AND 
                     (last_opened IS NULL OR last_opened < ?))''',
                  (cutoff_date,))
        
        conn.commit()
        conn.close()
    
    def get_performance_report(self, sequence_name: str) -> Dict:
        """Generate performance report for a sequence"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT 
                        email_step,
                        variant,
                        COUNT(*) as sent,
                        SUM(opened) as opens,
                        SUM(clicked) as clicks,
                        SUM(converted) as conversions
                     FROM email_tracking
                     WHERE sequence_name = ?
                     GROUP BY email_step, variant
                     ORDER BY email_step, variant''',
                  (sequence_name,))
        
        results = c.fetchall()
        conn.close()
        
        report = {
            "sequence": sequence_name,
            "steps": []
        }
        
        for step, variant, sent, opens, clicks, conversions in results:
            report["steps"].append({
                "step": step,
                "variant": variant,
                "sent": sent,
                "open_rate": round(opens / sent * 100, 2) if sent > 0 else 0,
                "click_rate": round(clicks / sent * 100, 2) if sent > 0 else 0,
                "conversion_rate": round(conversions / sent * 100, 2) if sent > 0 else 0
            })
        
        return report


# CLI Interface
if __name__ == "__main__":
    import sys
    
    manager = EmailSequenceManager()
    
    if len(sys.argv) < 2:
        print("Usage: email-sequence-manager.py [enroll|process|track|report|segment]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "enroll":
        email = sys.argv[2]
        sequence = sys.argv[3]
        variant = sys.argv[4] if len(sys.argv) > 4 else "A"
        result = manager.enroll_subscriber(email, sequence, variant)
        print(json.dumps(result, indent=2))
    
    elif command == "process":
        results = manager.process_sequences()
        print(json.dumps(results, indent=2))
    
    elif command == "track-open":
        email = sys.argv[2]
        sequence = sys.argv[3]
        step = int(sys.argv[4])
        manager.track_open(email, sequence, step)
        print(f"Tracked open: {email} - {sequence} step {step}")
    
    elif command == "track-click":
        email = sys.argv[2]
        sequence = sys.argv[3]
        step = int(sys.argv[4])
        url = sys.argv[5]
        manager.track_click(email, sequence, step, url)
        print(f"Tracked click: {email} - {sequence} step {step} - {url}")
    
    elif command == "report":
        sequence = sys.argv[2]
        report = manager.get_performance_report(sequence)
        print(json.dumps(report, indent=2))
    
    elif command == "segment":
        manager.segment_subscribers()
        print("Subscribers segmented successfully")
    
    else:
        print(f"Unknown command: {command}")
