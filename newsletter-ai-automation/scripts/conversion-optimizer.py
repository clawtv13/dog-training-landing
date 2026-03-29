#!/usr/bin/env python3
"""
Conversion Optimizer - A/B testing, subject line optimization, send time analysis
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict
import statistics

class ConversionOptimizer:
    def __init__(self, db_path: str = "email_sequences.db"):
        self.db_path = db_path
    
    def analyze_sequence_performance(self, sequence_name: str) -> Dict:
        """Analyze performance metrics for a specific sequence"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT 
                        email_step,
                        variant,
                        subject_line,
                        COUNT(*) as sent,
                        SUM(opened) as opens,
                        SUM(clicked) as clicks,
                        SUM(converted) as conversions
                     FROM email_tracking
                     WHERE sequence_name = ?
                     GROUP BY email_step, variant, subject_line
                     ORDER BY email_step, variant''',
                  (sequence_name,))
        
        results = c.fetchall()
        conn.close()
        
        analysis = {
            "sequence": sequence_name,
            "steps": [],
            "overall": {
                "total_sent": 0,
                "total_opens": 0,
                "total_clicks": 0,
                "total_conversions": 0
            }
        }
        
        for step, variant, subject, sent, opens, clicks, conversions in results:
            step_data = {
                "step": step,
                "variant": variant,
                "subject_line": subject,
                "sent": sent,
                "opens": opens,
                "clicks": clicks,
                "conversions": conversions,
                "open_rate": round(opens / sent * 100, 2) if sent > 0 else 0,
                "click_rate": round(clicks / sent * 100, 2) if sent > 0 else 0,
                "conversion_rate": round(conversions / sent * 100, 2) if sent > 0 else 0,
                "click_to_open": round(clicks / opens * 100, 2) if opens > 0 else 0
            }
            
            analysis["steps"].append(step_data)
            
            # Update overall
            analysis["overall"]["total_sent"] += sent
            analysis["overall"]["total_opens"] += opens
            analysis["overall"]["total_clicks"] += clicks
            analysis["overall"]["total_conversions"] += conversions
        
        # Calculate overall rates
        total_sent = analysis["overall"]["total_sent"]
        if total_sent > 0:
            analysis["overall"]["avg_open_rate"] = round(
                analysis["overall"]["total_opens"] / total_sent * 100, 2
            )
            analysis["overall"]["avg_click_rate"] = round(
                analysis["overall"]["total_clicks"] / total_sent * 100, 2
            )
            analysis["overall"]["avg_conversion_rate"] = round(
                analysis["overall"]["total_conversions"] / total_sent * 100, 2
            )
        
        return analysis
    
    def compare_variants(self, sequence_name: str, step: int) -> Dict:
        """Compare A/B test variants for a specific email"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT 
                        variant,
                        subject_line,
                        COUNT(*) as sent,
                        SUM(opened) as opens,
                        SUM(clicked) as clicks,
                        SUM(converted) as conversions
                     FROM email_tracking
                     WHERE sequence_name = ? AND email_step = ?
                     GROUP BY variant, subject_line''',
                  (sequence_name, step))
        
        results = c.fetchall()
        conn.close()
        
        if len(results) < 2:
            return {"error": "Not enough variants to compare"}
        
        variants = []
        for variant, subject, sent, opens, clicks, conversions in results:
            variants.append({
                "variant": variant,
                "subject_line": subject,
                "sent": sent,
                "open_rate": round(opens / sent * 100, 2) if sent > 0 else 0,
                "click_rate": round(clicks / sent * 100, 2) if sent > 0 else 0,
                "conversion_rate": round(conversions / sent * 100, 2) if sent > 0 else 0
            })
        
        # Determine winner
        winner = max(variants, key=lambda x: x["conversion_rate"])
        
        return {
            "sequence": sequence_name,
            "step": step,
            "variants": variants,
            "winner": winner["variant"],
            "winning_subject": winner["subject_line"],
            "improvement": round(winner["conversion_rate"] - 
                               min(v["conversion_rate"] for v in variants), 2)
        }
    
    def analyze_send_times(self) -> Dict:
        """Analyze best send times based on open rates"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT sent_at, opened 
                     FROM email_tracking 
                     WHERE sent_at IS NOT NULL''')
        
        results = c.fetchall()
        conn.close()
        
        if not results:
            return {"error": "No send time data available"}
        
        # Group by hour and day of week
        hourly_performance = defaultdict(lambda: {"sent": 0, "opened": 0})
        daily_performance = defaultdict(lambda: {"sent": 0, "opened": 0})
        
        for sent_at, opened in results:
            try:
                dt = datetime.fromisoformat(sent_at)
                hour = dt.hour
                day = dt.strftime("%A")
                
                hourly_performance[hour]["sent"] += 1
                daily_performance[day]["sent"] += 1
                
                if opened:
                    hourly_performance[hour]["opened"] += 1
                    daily_performance[day]["opened"] += 1
            except:
                continue
        
        # Calculate rates
        hourly_rates = {}
        for hour, data in hourly_performance.items():
            if data["sent"] > 0:
                hourly_rates[hour] = {
                    "sent": data["sent"],
                    "open_rate": round(data["opened"] / data["sent"] * 100, 2)
                }
        
        daily_rates = {}
        for day, data in daily_performance.items():
            if data["sent"] > 0:
                daily_rates[day] = {
                    "sent": data["sent"],
                    "open_rate": round(data["opened"] / data["sent"] * 100, 2)
                }
        
        # Find best times
        best_hour = max(hourly_rates.items(), key=lambda x: x[1]["open_rate"]) if hourly_rates else None
        best_day = max(daily_rates.items(), key=lambda x: x[1]["open_rate"]) if daily_rates else None
        
        return {
            "by_hour": dict(sorted(hourly_rates.items())),
            "by_day": daily_rates,
            "recommendations": {
                "best_hour": f"{best_hour[0]}:00" if best_hour else None,
                "best_day": best_day[0] if best_day else None
            }
        }
    
    def identify_drop_off_points(self, sequence_name: str) -> Dict:
        """Identify where subscribers drop off in a sequence"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT 
                        email_step,
                        COUNT(*) as sent,
                        SUM(opened) as opens
                     FROM email_tracking
                     WHERE sequence_name = ?
                     GROUP BY email_step
                     ORDER BY email_step''',
                  (sequence_name,))
        
        results = c.fetchall()
        conn.close()
        
        if not results:
            return {"error": "No data for this sequence"}
        
        drop_offs = []
        prev_opens = None
        
        for step, sent, opens in results:
            open_rate = round(opens / sent * 100, 2) if sent > 0 else 0
            
            if prev_opens is not None:
                drop = prev_opens - opens
                drop_pct = round((drop / prev_opens * 100), 2) if prev_opens > 0 else 0
                
                drop_offs.append({
                    "from_step": step - 1,
                    "to_step": step,
                    "subscribers_lost": drop,
                    "drop_percentage": drop_pct,
                    "open_rate": open_rate
                })
            
            prev_opens = opens
        
        # Identify biggest drop
        biggest_drop = max(drop_offs, key=lambda x: x["drop_percentage"]) if drop_offs else None
        
        return {
            "sequence": sequence_name,
            "drop_offs": drop_offs,
            "biggest_drop": biggest_drop,
            "recommendation": f"Review email at step {biggest_drop['to_step']}" if biggest_drop else None
        }
    
    def calculate_email_roi(self) -> Dict:
        """Calculate ROI for email sequences"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total LTV from conversions
        c.execute("SELECT SUM(ltv) FROM subscribers WHERE conversion_status = 'customer'")
        total_revenue = c.fetchone()[0] or 0
        
        # Total emails sent
        c.execute("SELECT COUNT(*) FROM email_tracking")
        total_emails = c.fetchone()[0] or 0
        
        # Conversions
        c.execute("SELECT COUNT(*) FROM subscribers WHERE conversion_status = 'customer'")
        total_conversions = c.fetchone()[0] or 0
        
        # Revenue by sequence
        c.execute('''SELECT 
                        e.sequence_name,
                        COUNT(DISTINCT e.email) as unique_recipients,
                        SUM(s.ltv) as revenue
                     FROM email_tracking e
                     JOIN subscribers s ON e.email = s.email
                     WHERE s.conversion_status = 'customer'
                     GROUP BY e.sequence_name''')
        
        sequence_revenue = []
        for seq, recipients, revenue in c.fetchall():
            sequence_revenue.append({
                "sequence": seq,
                "unique_recipients": recipients,
                "revenue": round(revenue, 2),
                "revenue_per_recipient": round(revenue / recipients, 2) if recipients > 0 else 0
            })
        
        conn.close()
        
        # Estimated costs (assumes $0.001 per email sent)
        email_cost = total_emails * 0.001
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_conversions": total_conversions,
            "total_emails_sent": total_emails,
            "estimated_cost": round(email_cost, 2),
            "roi": round((total_revenue - email_cost) / email_cost * 100, 2) if email_cost > 0 else 0,
            "revenue_per_email": round(total_revenue / total_emails, 2) if total_emails > 0 else 0,
            "by_sequence": sorted(sequence_revenue, key=lambda x: x["revenue"], reverse=True)
        }
    
    def get_subject_line_insights(self) -> Dict:
        """Analyze subject line patterns"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT 
                        subject_line,
                        COUNT(*) as sent,
                        SUM(opened) as opens
                     FROM email_tracking
                     GROUP BY subject_line
                     HAVING sent >= 10
                     ORDER BY opens DESC''')
        
        results = c.fetchall()
        conn.close()
        
        if not results:
            return {"error": "Not enough data"}
        
        # Analyze patterns
        emoji_subjects = []
        question_subjects = []
        urgency_subjects = []
        plain_subjects = []
        
        for subject, sent, opens in results:
            open_rate = round(opens / sent * 100, 2) if sent > 0 else 0
            data = {"subject": subject, "sent": sent, "open_rate": open_rate}
            
            if any(char in subject for char in "🎁🚀⚡🔥💰📈🎯⏰"):
                emoji_subjects.append(data)
            if "?" in subject:
                question_subjects.append(data)
            if any(word in subject.lower() for word in ["urgent", "last chance", "expires", "today", "now"]):
                urgency_subjects.append(data)
            else:
                plain_subjects.append(data)
        
        # Calculate average open rates
        avg_emoji = statistics.mean([s["open_rate"] for s in emoji_subjects]) if emoji_subjects else 0
        avg_question = statistics.mean([s["open_rate"] for s in question_subjects]) if question_subjects else 0
        avg_urgency = statistics.mean([s["open_rate"] for s in urgency_subjects]) if urgency_subjects else 0
        avg_plain = statistics.mean([s["open_rate"] for s in plain_subjects]) if plain_subjects else 0
        
        return {
            "patterns": {
                "emoji": {"count": len(emoji_subjects), "avg_open_rate": round(avg_emoji, 2)},
                "question": {"count": len(question_subjects), "avg_open_rate": round(avg_question, 2)},
                "urgency": {"count": len(urgency_subjects), "avg_open_rate": round(avg_urgency, 2)},
                "plain": {"count": len(plain_subjects), "avg_open_rate": round(avg_plain, 2)}
            },
            "top_performing": sorted(
                [{"subject": s, "sent": sent, "open_rate": round(opens/sent*100, 2)} 
                 for s, sent, opens in results[:10]],
                key=lambda x: x["open_rate"],
                reverse=True
            )
        }
    
    def generate_optimization_recommendations(self) -> List[str]:
        """Generate actionable optimization recommendations"""
        recommendations = []
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Check overall open rates
        c.execute('''SELECT 
                        COUNT(*) as sent,
                        SUM(opened) as opens
                     FROM email_tracking''')
        sent, opens = c.fetchone()
        
        if sent > 0:
            open_rate = opens / sent * 100
            if open_rate < 20:
                recommendations.append("⚠️ Low open rate (<20%). Test different subject lines and sender names.")
            elif open_rate < 30:
                recommendations.append("📊 Moderate open rate (20-30%). Run A/B tests to improve.")
            else:
                recommendations.append("✅ Good open rate (>30%). Continue current strategy.")
        
        # Check click rates
        c.execute('''SELECT 
                        SUM(opened) as opens,
                        SUM(clicked) as clicks
                     FROM email_tracking''')
        opens, clicks = c.fetchone()
        
        if opens > 0:
            ctr = clicks / opens * 100
            if ctr < 5:
                recommendations.append("⚠️ Low click rate (<5%). Improve CTA clarity and placement.")
            elif ctr < 10:
                recommendations.append("📊 Moderate click rate (5-10%). Test different CTA copy.")
            else:
                recommendations.append("✅ Good click rate (>10%). CTAs are working well.")
        
        # Check conversion rates
        c.execute("SELECT COUNT(*) FROM subscribers")
        total_subs = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM subscribers WHERE conversion_status = 'customer'")
        customers = c.fetchone()[0]
        
        if total_subs > 0:
            conv_rate = customers / total_subs * 100
            if conv_rate < 1:
                recommendations.append("⚠️ Low conversion rate (<1%). Review offer and sales copy.")
            elif conv_rate < 3:
                recommendations.append("📊 Moderate conversion rate (1-3%). Test pricing and guarantees.")
            else:
                recommendations.append("✅ Good conversion rate (>3%). Funnel is performing well.")
        
        # Check segmentation
        c.execute("SELECT segment, COUNT(*) FROM subscribers GROUP BY segment")
        segments = dict(c.fetchall())
        
        cold_pct = segments.get('cold', 0) / total_subs * 100 if total_subs > 0 else 0
        if cold_pct > 40:
            recommendations.append("⚠️ Too many cold subscribers (>40%). Run re-engagement campaigns.")
        
        conn.close()
        
        return recommendations


# CLI Interface
if __name__ == "__main__":
    import sys
    
    optimizer = ConversionOptimizer()
    
    if len(sys.argv) < 2:
        print("Usage: conversion-optimizer.py [analyze|compare|sendtime|dropoff|roi|subjects|recommend]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze":
        sequence = sys.argv[2]
        report = optimizer.analyze_sequence_performance(sequence)
        print(json.dumps(report, indent=2))
    
    elif command == "compare":
        sequence = sys.argv[2]
        step = int(sys.argv[3])
        comparison = optimizer.compare_variants(sequence, step)
        print(json.dumps(comparison, indent=2))
    
    elif command == "sendtime":
        analysis = optimizer.analyze_send_times()
        print(json.dumps(analysis, indent=2))
    
    elif command == "dropoff":
        sequence = sys.argv[2]
        analysis = optimizer.identify_drop_off_points(sequence)
        print(json.dumps(analysis, indent=2))
    
    elif command == "roi":
        analysis = optimizer.calculate_email_roi()
        print(json.dumps(analysis, indent=2))
    
    elif command == "subjects":
        insights = optimizer.get_subject_line_insights()
        print(json.dumps(insights, indent=2))
    
    elif command == "recommend":
        recommendations = optimizer.generate_optimization_recommendations()
        print("\n".join(recommendations))
    
    else:
        print(f"Unknown command: {command}")
