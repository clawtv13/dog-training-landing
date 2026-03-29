#!/usr/bin/env python3
"""
Revenue Dashboard - Real-time monetization metrics and projections
Tracks MRR, revenue by source, and growth projections
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class RevenueDashboard:
    def __init__(self, workspace_dir: str = "."):
        self.workspace = Path(workspace_dir)
        self.data_dir = self.workspace / "data"
        self.sponsors_db = self.data_dir / "sponsors.db"
        self.affiliates_db = self.data_dir / "affiliates.db"
    
    def get_sponsor_revenue(self) -> Dict:
        """Get sponsor revenue data"""
        if not self.sponsors_db.exists():
            return {'mrr': 0, 'arr': 0, 'active_deals': 0, 'total': 0}
        
        conn = sqlite3.connect(self.sponsors_db)
        c = conn.cursor()
        
        # Current MRR from active deals
        c.execute('''SELECT SUM(mrr) FROM deals 
                     WHERE status = 'active' 
                     AND contract_end >= date('now')''')
        mrr = c.fetchone()[0] or 0
        
        # Active deals count
        c.execute('''SELECT COUNT(*) FROM deals 
                     WHERE status = 'active' 
                     AND contract_end >= date('now')''')
        active_deals = c.fetchone()[0]
        
        # Total sponsor revenue (all time)
        c.execute('''SELECT SUM(amount) FROM revenue WHERE type = 'sponsor' ''')
        total = c.fetchone()[0] or 0
        
        # Revenue this month
        first_day = datetime.now().replace(day=1).date()
        c.execute('''SELECT SUM(amount) FROM revenue 
                     WHERE type = 'sponsor' AND date >= ?''', (first_day,))
        this_month = c.fetchone()[0] or 0
        
        # Revenue last 30 days
        cutoff = datetime.now().date() - timedelta(days=30)
        c.execute('''SELECT SUM(amount) FROM revenue 
                     WHERE type = 'sponsor' AND date >= ?''', (cutoff,))
        last_30_days = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'mrr': mrr,
            'arr': mrr * 12,
            'active_deals': active_deals,
            'total': total,
            'this_month': this_month,
            'last_30_days': last_30_days
        }
    
    def get_affiliate_revenue(self) -> Dict:
        """Get affiliate revenue data"""
        if not self.affiliates_db.exists():
            return {'total': 0, 'pending': 0, 'conversions': 0, 'this_month': 0}
        
        conn = sqlite3.connect(self.affiliates_db)
        c = conn.cursor()
        
        # Total confirmed/paid revenue
        c.execute('''SELECT SUM(amount), COUNT(*) FROM conversions 
                     WHERE status IN ('confirmed', 'paid')''')
        result = c.fetchone()
        total = result[0] or 0
        conversions = result[1] or 0
        
        # Pending revenue
        c.execute('''SELECT SUM(amount) FROM conversions WHERE status = 'pending' ''')
        pending = c.fetchone()[0] or 0
        
        # This month
        first_day = datetime.now().replace(day=1).date()
        c.execute('''SELECT SUM(amount) FROM conversions 
                     WHERE status IN ('confirmed', 'paid') AND conversion_date >= ?''', 
                  (first_day,))
        this_month = c.fetchone()[0] or 0
        
        # Last 30 days
        cutoff = datetime.now().date() - timedelta(days=30)
        c.execute('''SELECT SUM(amount) FROM conversions 
                     WHERE status IN ('confirmed', 'paid') AND conversion_date >= ?''', 
                  (cutoff,))
        last_30_days = c.fetchone()[0] or 0
        
        # By program
        c.execute('''SELECT 
                        prog.name,
                        SUM(c.amount) as revenue,
                        COUNT(c.id) as conversions
                     FROM conversions c
                     JOIN placements pl ON c.placement_id = pl.id
                     JOIN products p ON pl.product_id = p.id
                     JOIN programs prog ON p.program_id = prog.id
                     WHERE c.status IN ('confirmed', 'paid')
                     GROUP BY prog.id
                     ORDER BY revenue DESC''')
        
        by_program = [{'program': row[0], 'revenue': row[1], 'conversions': row[2]} 
                      for row in c.fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'pending': pending,
            'conversions': conversions,
            'this_month': this_month,
            'last_30_days': last_30_days,
            'by_program': by_program
        }
    
    def get_ad_revenue(self) -> Dict:
        """Get ad revenue data (placeholder - integrate with ad network)"""
        # TODO: Integrate with Carbon Ads / Ethical Ads API
        return {
            'total': 0,
            'this_month': 0,
            'rpm': 0,  # Revenue per mille (1000 impressions)
            'impressions': 0
        }
    
    def get_total_revenue(self) -> Dict:
        """Get combined revenue from all sources"""
        sponsors = self.get_sponsor_revenue()
        affiliates = self.get_affiliate_revenue()
        ads = self.get_ad_revenue()
        
        total = sponsors['total'] + affiliates['total'] + ads['total']
        this_month = sponsors['this_month'] + affiliates['this_month'] + ads['this_month']
        last_30_days = sponsors['last_30_days'] + affiliates['last_30_days']
        
        return {
            'total': total,
            'this_month': this_month,
            'last_30_days': last_30_days,
            'mrr': sponsors['mrr'],
            'arr': sponsors['arr'],
            'by_source': {
                'sponsors': sponsors['total'],
                'affiliates': affiliates['total'],
                'ads': ads['total']
            }
        }
    
    def calculate_projections(self, months: int = 6) -> List[Dict]:
        """Project revenue growth based on current trajectory"""
        current_mrr = self.get_sponsor_revenue()['mrr']
        affiliate_monthly = self.get_affiliate_revenue()['last_30_days']
        
        # Assume 20% monthly growth (conservative)
        growth_rate = 0.20
        
        projections = []
        
        for month in range(1, months + 1):
            date = datetime.now() + timedelta(days=month * 30)
            
            # Sponsors grow through MRR
            projected_mrr = current_mrr * (1 + growth_rate) ** month
            
            # Affiliates grow with traffic
            projected_affiliate = affiliate_monthly * (1 + growth_rate * 0.5) ** month
            
            # Ads start when traffic hits 5K/month
            projected_ads = 0
            if month >= 2:  # Assume ads start month 2
                projected_ads = 100 * (1 + growth_rate) ** (month - 1)
            
            total = projected_mrr + projected_affiliate + projected_ads
            
            projections.append({
                'month': date.strftime('%Y-%m'),
                'sponsors': round(projected_mrr, 2),
                'affiliates': round(projected_affiliate, 2),
                'ads': round(projected_ads, 2),
                'total': round(total, 2)
            })
        
        return projections
    
    def get_funnel_metrics(self) -> Dict:
        """Get sales funnel metrics"""
        if not self.sponsors_db.exists():
            return {}
        
        conn = sqlite3.connect(self.sponsors_db)
        c = conn.cursor()
        
        # Prospects by status
        c.execute('SELECT status, COUNT(*) FROM prospects GROUP BY status')
        funnel = {row[0]: row[1] for row in c.fetchall()}
        
        # Conversion rates
        total_prospects = sum(funnel.values())
        contacted = funnel.get('contacted', 0) + funnel.get('replied', 0) + funnel.get('interested', 0) + funnel.get('customer', 0)
        replied = funnel.get('replied', 0) + funnel.get('interested', 0) + funnel.get('customer', 0)
        customers = funnel.get('customer', 0)
        
        contact_rate = (contacted / total_prospects * 100) if total_prospects > 0 else 0
        reply_rate = (replied / contacted * 100) if contacted > 0 else 0
        close_rate = (customers / replied * 100) if replied > 0 else 0
        
        conn.close()
        
        return {
            'funnel': funnel,
            'total_prospects': total_prospects,
            'contact_rate': round(contact_rate, 1),
            'reply_rate': round(reply_rate, 1),
            'close_rate': round(close_rate, 1)
        }
    
    def print_dashboard(self):
        """Print formatted revenue dashboard"""
        print("\n" + "="*70)
        print("💰 REVENUE DASHBOARD".center(70))
        print("="*70)
        
        # Overall metrics
        total_rev = self.get_total_revenue()
        sponsors = self.get_sponsor_revenue()
        affiliates = self.get_affiliate_revenue()
        
        print("\n📊 CURRENT METRICS:")
        print(f"  Total Revenue:        ${total_rev['total']:>10,.2f}")
        print(f"  This Month:           ${total_rev['this_month']:>10,.2f}")
        print(f"  Last 30 Days:         ${total_rev['last_30_days']:>10,.2f}")
        print(f"  Current MRR:          ${total_rev['mrr']:>10,.2f}")
        print(f"  Projected ARR:        ${total_rev['arr']:>10,.2f}")
        
        print("\n💼 BY SOURCE:")
        print(f"  Sponsors:             ${sponsors['total']:>10,.2f} ({sponsors['active_deals']} active)")
        print(f"  Affiliates:           ${affiliates['total']:>10,.2f} ({affiliates['conversions']} conversions)")
        print(f"  Pending:              ${affiliates['pending']:>10,.2f}")
        
        # Top affiliate programs
        if affiliates['by_program']:
            print("\n🏆 TOP AFFILIATE PROGRAMS:")
            for prog in affiliates['by_program'][:5]:
                print(f"  • {prog['program']:<25} ${prog['revenue']:>8,.2f}")
        
        # Funnel metrics
        funnel = self.get_funnel_metrics()
        if funnel:
            print("\n📈 SALES FUNNEL:")
            print(f"  Total Prospects:      {funnel['total_prospects']:>5}")
            print(f"  Contact Rate:         {funnel['contact_rate']:>5.1f}%")
            print(f"  Reply Rate:           {funnel['reply_rate']:>5.1f}%")
            print(f"  Close Rate:           {funnel['close_rate']:>5.1f}%")
        
        # Projections
        print("\n🎯 6-MONTH PROJECTIONS:")
        projections = self.calculate_projections(6)
        
        print(f"  {'Month':<12} {'Sponsors':<12} {'Affiliates':<12} {'Ads':<10} {'Total':<10}")
        print("  " + "-"*60)
        for p in projections:
            print(f"  {p['month']:<12} ${p['sponsors']:<11,.0f} ${p['affiliates']:<11,.0f} ${p['ads']:<9,.0f} ${p['total']:<9,.0f}")
        
        # Goal tracking
        goal = 10000
        current_mrr = total_rev['mrr']
        months_to_goal = 0
        
        if current_mrr > 0:
            growth_needed = goal / current_mrr
            months_to_goal = round(growth_needed / 1.20, 1)  # 20% monthly growth
        
        print("\n🎯 GOAL TRACKING:")
        print(f"  Goal:                 ${goal:>10,.2f}/month")
        print(f"  Current MRR:          ${current_mrr:>10,.2f}")
        print(f"  Progress:             {(current_mrr/goal*100):>10.1f}%")
        if months_to_goal > 0:
            print(f"  Est. Time to Goal:    {months_to_goal:>10.1f} months @ 20% growth")
        
        print("\n" + "="*70 + "\n")
        
        # Save snapshot
        snapshot = {
            'date': datetime.now().isoformat(),
            'total_revenue': total_rev,
            'sponsors': sponsors,
            'affiliates': affiliates,
            'projections': projections,
            'funnel': funnel
        }
        
        snapshot_file = self.data_dir / "revenue_snapshot.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"📸 Snapshot saved to {snapshot_file}")


def main():
    dashboard = RevenueDashboard("/root/.openclaw/workspace/ai-automation-blog")
    dashboard.print_dashboard()


if __name__ == "__main__":
    main()
