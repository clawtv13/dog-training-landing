#!/usr/bin/env python3
"""
Engagement Tracker - Monitor subscriber behavior and auto-segment
Tracks opens, clicks, and triggers follow-up sequences
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import os

class EngagementTracker:
    def __init__(self, db_path: str = "email_sequences.db"):
        self.db_path = db_path
        
    def record_open(self, email: str, sequence_name: str, step: int, timestamp: str = None):
        """Record email open and update engagement score"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timestamp = timestamp or datetime.now().isoformat()
        
        # Update email tracking
        c.execute('''UPDATE email_tracking 
                     SET opened = 1 
                     WHERE email = ? AND sequence_name = ? AND email_step = ?''',
                  (email, sequence_name, step))
        
        # Update subscriber engagement
        c.execute('''UPDATE subscribers 
                     SET last_opened = ?, 
                         engagement_score = engagement_score + 1
                     WHERE email = ?''',
                  (timestamp, email))
        
        conn.commit()
        
        # Check for triggers
        self._check_engagement_triggers(email)
        
        conn.close()
        
        return {"status": "recorded", "event": "open", "email": email}
    
    def record_click(self, email: str, sequence_name: str, step: int, 
                    url: str, timestamp: str = None):
        """Record email click and trigger sequences"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timestamp = timestamp or datetime.now().isoformat()
        
        # Update email tracking
        c.execute('''UPDATE email_tracking 
                     SET clicked = 1 
                     WHERE email = ? AND sequence_name = ? AND email_step = ?''',
                  (email, sequence_name, step))
        
        # Update subscriber engagement
        c.execute('''UPDATE subscribers 
                     SET last_clicked = ?, 
                         engagement_score = engagement_score + 3
                     WHERE email = ?''',
                  (timestamp, email))
        
        # Log trigger
        trigger_data = json.dumps({
            "url": url,
            "sequence": sequence_name,
            "step": step,
            "timestamp": timestamp
        })
        
        c.execute('''INSERT INTO triggers 
                     (email, trigger_type, trigger_data, fired_at)
                     VALUES (?, ?, ?, ?)''',
                  (email, "click", trigger_data, timestamp))
        
        conn.commit()
        conn.close()
        
        # Check for triggered sequences
        self._check_click_triggers(email, url)
        
        return {"status": "recorded", "event": "click", "email": email, "url": url}
    
    def record_conversion(self, email: str, product: str, amount: float, 
                         timestamp: str = None):
        """Record conversion and update customer status"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        timestamp = timestamp or datetime.now().isoformat()
        
        # Update subscriber
        c.execute('''UPDATE subscribers 
                     SET conversion_status = 'customer', 
                         ltv = ltv + ?,
                         engagement_score = engagement_score + 20
                     WHERE email = ?''',
                  (amount, email))
        
        # Mark all related emails as converted
        c.execute('''UPDATE email_tracking 
                     SET converted = 1 
                     WHERE email = ?''',
                  (email,))
        
        # Log conversion trigger
        trigger_data = json.dumps({
            "product": product,
            "amount": amount,
            "timestamp": timestamp
        })
        
        c.execute('''INSERT INTO triggers 
                     (email, trigger_type, trigger_data, fired_at, action_taken)
                     VALUES (?, ?, ?, ?, ?)''',
                  (email, "conversion", trigger_data, timestamp, "marked_as_customer"))
        
        conn.commit()
        conn.close()
        
        return {"status": "recorded", "event": "conversion", "email": email, 
                "product": product, "amount": amount}
    
    def _check_engagement_triggers(self, email: str):
        """Check if subscriber's engagement triggers any sequences"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get engagement data
        c.execute('''SELECT engagement_score, segment, last_opened 
                     FROM subscribers WHERE email = ?''', (email,))
        result = c.fetchone()
        
        if not result:
            conn.close()
            return
        
        engagement_score, segment, last_opened = result
        
        # High engagement → Offer upsell
        if engagement_score >= 15 and segment == 'active':
            c.execute('''SELECT id FROM sequence_enrollment 
                         WHERE email = ? AND sequence_name = 'upsell' 
                         AND completed = 0''', (email,))
            if not c.fetchone():
                # Enroll in upsell sequence
                c.execute('''INSERT INTO sequence_enrollment 
                             (email, sequence_name, enrolled_at, variant)
                             VALUES (?, ?, ?, ?)''',
                          (email, 'upsell', datetime.now().isoformat(), 'A'))
        
        conn.commit()
        conn.close()
    
    def _check_click_triggers(self, email: str, url: str):
        """Check if clicked URL triggers any sequences"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Pricing page click → Abandoned cart sequence
        if 'pricing' in url.lower() or 'checkout' in url.lower():
            c.execute('''SELECT id FROM sequence_enrollment 
                         WHERE email = ? AND sequence_name = 'abandoned-cart' 
                         AND completed = 0''', (email,))
            if not c.fetchone():
                c.execute('''INSERT INTO sequence_enrollment 
                             (email, sequence_name, enrolled_at, variant)
                             VALUES (?, ?, ?, ?)''',
                          (email, 'abandoned-cart', datetime.now().isoformat(), 'A'))
        
        # Download link → Upsell sequence
        if 'download' in url.lower() or 'starter-kit' in url.lower():
            c.execute('''SELECT id FROM sequence_enrollment 
                         WHERE email = ? AND sequence_name = 'upsell' 
                         AND completed = 0''', (email,))
            if not c.fetchone():
                c.execute('''INSERT INTO sequence_enrollment 
                             (email, sequence_name, enrolled_at, variant)
                             VALUES (?, ?, ?, ?)''',
                          (email, 'upsell', datetime.now().isoformat(), 'A'))
        
        conn.commit()
        conn.close()
    
    def segment_subscribers(self):
        """Auto-segment subscribers based on behavior"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.now()
        
        # Active: High engagement, recent opens
        cutoff_active = (now - timedelta(days=7)).isoformat()
        c.execute('''UPDATE subscribers 
                     SET segment = 'active' 
                     WHERE engagement_score >= 10 
                     AND last_opened > ?''',
                  (cutoff_active,))
        
        # Warm: Moderate engagement
        cutoff_warm = (now - timedelta(days=30)).isoformat()
        c.execute('''UPDATE subscribers 
                     SET segment = 'warm' 
                     WHERE engagement_score >= 5 
                     AND engagement_score < 10 
                     AND last_opened > ?''',
                  (cutoff_warm,))
        
        # Cold: Low engagement or inactive
        c.execute('''UPDATE subscribers 
                     SET segment = 'cold' 
                     WHERE (engagement_score < 5 OR last_opened < ? OR last_opened IS NULL)
                     AND segment != 'active' AND segment != 'warm' ''',
                  (cutoff_warm,))
        
        # Get counts
        c.execute("SELECT segment, COUNT(*) FROM subscribers GROUP BY segment")
        segments = dict(c.fetchall())
        
        conn.commit()
        conn.close()
        
        return segments
    
    def identify_churning_subscribers(self) -> List[str]:
        """Identify subscribers at risk of churning"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # No opens in 30 days
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        c.execute('''SELECT email FROM subscribers 
                     WHERE (last_opened < ? OR last_opened IS NULL)
                     AND segment = 'cold' 
                     AND conversion_status = 'lead' ''',
                  (cutoff,))
        
        churning = [row[0] for row in c.fetchall()]
        
        conn.close()
        return churning
    
    def enroll_churning_in_reengagement(self):
        """Auto-enroll cold subscribers in re-engagement sequence"""
        churning = self.identify_churning_subscribers()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        enrolled = 0
        for email in churning:
            # Check if already enrolled
            c.execute('''SELECT id FROM sequence_enrollment 
                         WHERE email = ? AND sequence_name = 're-engagement' 
                         AND completed = 0''', (email,))
            
            if not c.fetchone():
                c.execute('''INSERT INTO sequence_enrollment 
                             (email, sequence_name, enrolled_at, variant)
                             VALUES (?, ?, ?, ?)''',
                          (email, 're-engagement', datetime.now().isoformat(), 'A'))
                enrolled += 1
        
        conn.commit()
        conn.close()
        
        return {"churning_count": len(churning), "enrolled": enrolled}
    
    def get_engagement_report(self) -> Dict:
        """Generate engagement report"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Overall stats
        c.execute("SELECT COUNT(*) FROM subscribers")
        total_subscribers = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM subscribers WHERE conversion_status = 'customer'")
        total_customers = c.fetchone()[0]
        
        c.execute("SELECT AVG(engagement_score) FROM subscribers")
        avg_engagement = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(ltv) FROM subscribers")
        total_ltv = c.fetchone()[0] or 0
        
        # Segment breakdown
        c.execute("SELECT segment, COUNT(*) FROM subscribers GROUP BY segment")
        segments = dict(c.fetchall())
        
        # Recent activity (last 7 days)
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()
        c.execute("SELECT COUNT(*) FROM subscribers WHERE last_opened > ?", (cutoff,))
        recent_opens = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM subscribers WHERE last_clicked > ?", (cutoff,))
        recent_clicks = c.fetchone()[0]
        
        conn.close()
        
        return {
            "total_subscribers": total_subscribers,
            "total_customers": total_customers,
            "conversion_rate": round(total_customers / total_subscribers * 100, 2) if total_subscribers > 0 else 0,
            "avg_engagement_score": round(avg_engagement, 2),
            "total_ltv": round(total_ltv, 2),
            "segments": segments,
            "recent_activity": {
                "opens_7d": recent_opens,
                "clicks_7d": recent_clicks
            }
        }
    
    def get_top_performers(self, limit: int = 10) -> List[Dict]:
        """Get top performing subscribers by engagement"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT email, engagement_score, ltv, segment 
                     FROM subscribers 
                     ORDER BY engagement_score DESC 
                     LIMIT ?''', (limit,))
        
        performers = []
        for email, score, ltv, segment in c.fetchall():
            performers.append({
                "email": email,
                "engagement_score": score,
                "ltv": ltv,
                "segment": segment
            })
        
        conn.close()
        return performers


# CLI Interface
if __name__ == "__main__":
    import sys
    
    tracker = EngagementTracker()
    
    if len(sys.argv) < 2:
        print("Usage: engagement-tracker.py [open|click|conversion|segment|report|churn]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "open":
        email = sys.argv[2]
        sequence = sys.argv[3]
        step = int(sys.argv[4])
        result = tracker.record_open(email, sequence, step)
        print(json.dumps(result, indent=2))
    
    elif command == "click":
        email = sys.argv[2]
        sequence = sys.argv[3]
        step = int(sys.argv[4])
        url = sys.argv[5]
        result = tracker.record_click(email, sequence, step, url)
        print(json.dumps(result, indent=2))
    
    elif command == "conversion":
        email = sys.argv[2]
        product = sys.argv[3]
        amount = float(sys.argv[4])
        result = tracker.record_conversion(email, product, amount)
        print(json.dumps(result, indent=2))
    
    elif command == "segment":
        segments = tracker.segment_subscribers()
        print(json.dumps(segments, indent=2))
    
    elif command == "report":
        report = tracker.get_engagement_report()
        print(json.dumps(report, indent=2))
    
    elif command == "churn":
        result = tracker.enroll_churning_in_reengagement()
        print(json.dumps(result, indent=2))
    
    elif command == "top":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        performers = tracker.get_top_performers(limit)
        print(json.dumps(performers, indent=2))
    
    else:
        print(f"Unknown command: {command}")
