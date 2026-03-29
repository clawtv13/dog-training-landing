#!/usr/bin/env python3
"""
Monetization Agent - Automated Sponsor Outreach & Revenue Generation
Handles sponsor prospecting, email automation, deal tracking, and CRM
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MonetizationAgent:
    def __init__(self, workspace_dir: str = "."):
        self.workspace = Path(workspace_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / "sponsors.db"
        self.init_database()
        
    def init_database(self):
        """Initialize sponsor CRM database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Prospects table
        c.execute('''CREATE TABLE IF NOT EXISTS prospects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT,
            email TEXT UNIQUE NOT NULL,
            website TEXT,
            category TEXT,
            tier TEXT,
            status TEXT DEFAULT 'new',
            last_contact DATE,
            next_followup DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Outreach history
        c.execute('''CREATE TABLE IF NOT EXISTS outreach_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER,
            email_type TEXT,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            opened BOOLEAN DEFAULT 0,
            replied BOOLEAN DEFAULT 0,
            response TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )''')
        
        # Deals table
        c.execute('''CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id INTEGER,
            amount REAL,
            mrr REAL,
            contract_start DATE,
            contract_end DATE,
            status TEXT DEFAULT 'negotiating',
            payment_terms TEXT,
            deliverables TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        )''')
        
        # Revenue tracking
        c.execute('''CREATE TABLE IF NOT EXISTS revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            type TEXT,
            deal_id INTEGER,
            notes TEXT,
            FOREIGN KEY (deal_id) REFERENCES deals(id)
        )''')
        
        conn.commit()
        conn.close()
        
    def load_prospects(self, prospect_file: str):
        """Load prospects from JSON file into database"""
        with open(prospect_file) as f:
            prospects = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for p in prospects:
            try:
                c.execute('''INSERT OR IGNORE INTO prospects 
                    (company_name, contact_name, email, website, category, tier, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (p['company'], p.get('contact'), p['email'], 
                     p['website'], p['category'], p.get('tier', 'bronze'), 'new'))
            except Exception as e:
                print(f"Error loading {p['company']}: {e}")
        
        conn.commit()
        conn.close()
        print(f"Loaded {len(prospects)} prospects")
        
    def get_prospects_for_outreach(self, status: str = 'new', limit: int = 10) -> List[Dict]:
        """Get prospects ready for outreach"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT * FROM prospects 
                     WHERE status = ? 
                     ORDER BY tier DESC, created_at ASC 
                     LIMIT ?''', (status, limit))
        
        prospects = [dict(row) for row in c.fetchall()]
        conn.close()
        return prospects
    
    def get_followup_due(self) -> List[Dict]:
        """Get prospects due for follow-up"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        today = datetime.now().date()
        c.execute('''SELECT * FROM prospects 
                     WHERE next_followup <= ? 
                     AND status IN ('contacted', 'replied', 'interested')
                     ORDER BY next_followup ASC''', (today,))
        
        prospects = [dict(row) for row in c.fetchall()]
        conn.close()
        return prospects
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   template_vars: Dict = None, dry_run: bool = True) -> bool:
        """Send outreach email (set dry_run=False to actually send)"""
        
        if template_vars:
            body = body.format(**template_vars)
            subject = subject.format(**template_vars)
        
        if dry_run:
            print(f"\n{'='*60}")
            print(f"DRY RUN - Email to: {to_email}")
            print(f"Subject: {subject}")
            print(f"{'='*60}")
            print(body)
            print(f"{'='*60}\n")
            return True
        
        # TODO: Configure SMTP settings
        # smtp_server = os.getenv('SMTP_SERVER')
        # smtp_port = os.getenv('SMTP_PORT', 587)
        # smtp_user = os.getenv('SMTP_USER')
        # smtp_pass = os.getenv('SMTP_PASS')
        
        # msg = MIMEMultipart()
        # msg['From'] = smtp_user
        # msg['To'] = to_email
        # msg['Subject'] = subject
        # msg.attach(MIMEText(body, 'plain'))
        
        # try:
        #     server = smtplib.SMTP(smtp_server, smtp_port)
        #     server.starttls()
        #     server.login(smtp_user, smtp_pass)
        #     server.send_message(msg)
        #     server.quit()
        #     return True
        # except Exception as e:
        #     print(f"Error sending email: {e}")
        #     return False
        
        print("Set dry_run=False and configure SMTP to actually send")
        return False
    
    def log_outreach(self, prospect_id: int, email_type: str):
        """Log outreach attempt"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO outreach_history (prospect_id, email_type)
                     VALUES (?, ?)''', (prospect_id, email_type))
        
        # Update prospect status
        next_followup = datetime.now() + timedelta(days=3 if email_type == 'initial' else 5)
        c.execute('''UPDATE prospects 
                     SET status = ?, last_contact = ?, next_followup = ?
                     WHERE id = ?''',
                  ('contacted', datetime.now().date(), next_followup.date(), prospect_id))
        
        conn.commit()
        conn.close()
    
    def create_deal(self, prospect_id: int, amount: float, duration_months: int = 3):
        """Create a sponsorship deal"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        mrr = amount / duration_months
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=duration_months * 30)
        
        c.execute('''INSERT INTO deals 
                     (prospect_id, amount, mrr, contract_start, contract_end, status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (prospect_id, amount, mrr, start_date, end_date, 'negotiating'))
        
        deal_id = c.lastrowid
        
        # Update prospect status
        c.execute('UPDATE prospects SET status = ? WHERE id = ?', ('customer', prospect_id))
        
        conn.commit()
        conn.close()
        return deal_id
    
    def log_revenue(self, source: str, amount: float, revenue_type: str, 
                    deal_id: Optional[int] = None, notes: str = None):
        """Log revenue entry"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO revenue (source, amount, date, type, deal_id, notes)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (source, amount, datetime.now().date(), revenue_type, deal_id, notes))
        
        conn.commit()
        conn.close()
    
    def get_mrr(self) -> float:
        """Calculate current Monthly Recurring Revenue"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT SUM(mrr) FROM deals 
                     WHERE status = 'active' 
                     AND contract_end >= date('now')''')
        
        result = c.fetchone()[0]
        conn.close()
        return result or 0.0
    
    def get_revenue_summary(self, days: int = 30) -> Dict:
        """Get revenue summary for last N days"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        c.execute('''SELECT type, SUM(amount) as total 
                     FROM revenue 
                     WHERE date >= ? 
                     GROUP BY type''', (cutoff_date,))
        
        by_type = {row[0]: row[1] for row in c.fetchall()}
        
        c.execute('''SELECT SUM(amount) FROM revenue WHERE date >= ?''', (cutoff_date,))
        total = c.fetchone()[0] or 0.0
        
        conn.close()
        
        return {
            'total': total,
            'by_type': by_type,
            'mrr': self.get_mrr(),
            'period_days': days
        }
    
    def get_pipeline_status(self) -> Dict:
        """Get current sales pipeline status"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT status, COUNT(*) FROM prospects GROUP BY status')
        status_counts = {row[0]: row[1] for row in c.fetchall()}
        
        c.execute('SELECT COUNT(*) FROM prospects WHERE next_followup <= date("now")')
        followups_due = c.fetchone()[0]
        
        c.execute('SELECT status, COUNT(*), SUM(amount) FROM deals GROUP BY status')
        deals = {row[0]: {'count': row[1], 'value': row[2] or 0} for row in c.fetchall()}
        
        conn.close()
        
        return {
            'prospects_by_status': status_counts,
            'followups_due': followups_due,
            'deals': deals
        }
    
    def run_daily_automation(self, max_outreach: int = 5):
        """Run daily automation tasks"""
        print("🤖 Running Daily Monetization Automation...")
        
        # 1. Send follow-ups
        followups = self.get_followup_due()
        print(f"\n📧 {len(followups)} follow-ups due")
        
        # 2. Send new outreach
        new_prospects = self.get_prospects_for_outreach('new', max_outreach)
        print(f"🎯 {len(new_prospects)} new prospects to contact")
        
        # 3. Pipeline status
        pipeline = self.get_pipeline_status()
        print(f"\n📊 Pipeline Status:")
        for status, count in pipeline['prospects_by_status'].items():
            print(f"  {status}: {count}")
        
        # 4. Revenue summary
        revenue = self.get_revenue_summary(30)
        print(f"\n💰 Revenue (Last 30 days): ${revenue['total']:.2f}")
        print(f"   MRR: ${revenue['mrr']:.2f}")
        
        return {
            'followups': followups,
            'new_outreach': new_prospects,
            'pipeline': pipeline,
            'revenue': revenue
        }


def main():
    agent = MonetizationAgent("/root/.openclaw/workspace/ai-automation-blog")
    
    # Load prospects if file exists
    prospects_file = agent.workspace / "data" / "sponsor-prospects.json"
    if prospects_file.exists():
        agent.load_prospects(str(prospects_file))
    
    # Run daily automation
    results = agent.run_daily_automation()
    
    print("\n✅ Monetization agent ready!")
    print("Configure SMTP settings to enable email automation")


if __name__ == "__main__":
    main()
