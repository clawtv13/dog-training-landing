#!/usr/bin/env python3
"""
Affiliate Manager - Auto-embed affiliate links and track conversions
Manages affiliate programs, link insertion, and revenue attribution
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sqlite3

class AffiliateManager:
    def __init__(self, workspace_dir: str = "."):
        self.workspace = Path(workspace_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / "affiliates.db"
        self.init_database()
        
    def init_database(self):
        """Initialize affiliate tracking database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Affiliate programs
        c.execute('''CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT,
            commission_rate REAL,
            commission_type TEXT,
            cookie_duration INTEGER,
            min_payout REAL,
            status TEXT DEFAULT 'active',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Products/services
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER,
            name TEXT NOT NULL,
            category TEXT,
            base_url TEXT,
            affiliate_link TEXT NOT NULL,
            commission_rate REAL,
            recommended BOOLEAN DEFAULT 0,
            keywords TEXT,
            notes TEXT,
            FOREIGN KEY (program_id) REFERENCES programs(id)
        )''')
        
        # Link placements
        c.execute('''CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            post_path TEXT NOT NULL,
            link_text TEXT,
            context TEXT,
            placement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            revenue REAL DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')
        
        # Conversions
        c.execute('''CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placement_id INTEGER,
            conversion_date DATE NOT NULL,
            amount REAL,
            status TEXT DEFAULT 'pending',
            payout_date DATE,
            notes TEXT,
            FOREIGN KEY (placement_id) REFERENCES placements(id)
        )''')
        
        conn.commit()
        conn.close()
    
    def load_programs(self, programs_file: str):
        """Load affiliate programs from JSON"""
        with open(programs_file) as f:
            programs = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for prog in programs:
            c.execute('''INSERT OR REPLACE INTO programs 
                (name, url, commission_rate, commission_type, cookie_duration, min_payout, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (prog['name'], prog['url'], prog.get('commission_rate'), 
                 prog.get('commission_type'), prog.get('cookie_duration'),
                 prog.get('min_payout'), prog.get('status', 'active'), prog.get('notes')))
            
            program_id = c.lastrowid
            
            # Load products for this program
            for product in prog.get('products', []):
                c.execute('''INSERT OR REPLACE INTO products 
                    (program_id, name, category, base_url, affiliate_link, commission_rate, recommended, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (program_id, product['name'], product.get('category'),
                     product.get('base_url'), product['affiliate_link'],
                     product.get('commission_rate'), product.get('recommended', False),
                     ','.join(product.get('keywords', []))))
        
        conn.commit()
        conn.close()
        print(f"Loaded {len(programs)} affiliate programs")
    
    def find_opportunities(self, post_content: str, post_path: str) -> List[Dict]:
        """Find affiliate link opportunities in a post"""
        opportunities = []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM products WHERE status != "inactive"')
        products = [dict(row) for row in c.fetchall()]
        conn.close()
        
        for product in products:
            keywords = product.get('keywords', '').split(',')
            
            for keyword in keywords:
                if not keyword.strip():
                    continue
                    
                # Case-insensitive search
                pattern = re.compile(r'\b' + re.escape(keyword.strip()) + r'\b', re.IGNORECASE)
                matches = pattern.finditer(post_content)
                
                for match in matches:
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(post_content), match.end() + 50)
                    context = post_content[context_start:context_end]
                    
                    opportunities.append({
                        'product': product['name'],
                        'product_id': product['id'],
                        'keyword': keyword.strip(),
                        'position': match.start(),
                        'context': context,
                        'affiliate_link': product['affiliate_link'],
                        'recommended': product['recommended']
                    })
        
        return opportunities
    
    def embed_links(self, post_path: str, dry_run: bool = True) -> Dict:
        """Auto-embed affiliate links in a post"""
        post_file = Path(post_path)
        
        if not post_file.exists():
            return {'error': 'Post not found'}
        
        content = post_file.read_text()
        original_content = content
        
        opportunities = self.find_opportunities(content, str(post_path))
        
        # Sort by position (reverse) to maintain correct indices
        opportunities.sort(key=lambda x: x['position'], reverse=True)
        
        embedded = []
        
        for opp in opportunities:
            # Check if already linked
            start = max(0, opp['position'] - 100)
            end = min(len(content), opp['position'] + 100)
            surrounding = content[start:end]
            
            if 'href=' in surrounding or 'http' in surrounding:
                continue  # Already has a link nearby
            
            # Create markdown link
            keyword = opp['keyword']
            link = f"[{keyword}]({opp['affiliate_link']})"
            
            # Replace first occurrence only
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            content = pattern.sub(link, content, count=1)
            
            embedded.append(opp)
            
            # Log placement
            if not dry_run:
                self.log_placement(opp['product_id'], str(post_path), keyword, opp['context'])
        
        if dry_run:
            print(f"\n{'='*60}")
            print(f"DRY RUN - Affiliate Links for: {post_path}")
            print(f"{'='*60}")
            print(f"Found {len(embedded)} opportunities:")
            for e in embedded:
                print(f"  • {e['product']} ({e['keyword']})")
            print(f"{'='*60}\n")
        else:
            if embedded:
                post_file.write_text(content)
                print(f"✅ Embedded {len(embedded)} affiliate links in {post_path}")
        
        return {
            'opportunities': len(opportunities),
            'embedded': len(embedded),
            'post': str(post_path),
            'links': embedded
        }
    
    def log_placement(self, product_id: int, post_path: str, link_text: str, context: str):
        """Log an affiliate link placement"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO placements (product_id, post_path, link_text, context)
                     VALUES (?, ?, ?, ?)''',
                  (product_id, post_path, link_text, context))
        
        conn.commit()
        conn.close()
    
    def log_conversion(self, placement_id: int, amount: float, status: str = 'pending'):
        """Log an affiliate conversion"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO conversions (placement_id, conversion_date, amount, status)
                     VALUES (?, ?, ?, ?)''',
                  (placement_id, datetime.now().date(), amount, status))
        
        # Update placement revenue
        c.execute('''UPDATE placements 
                     SET conversions = conversions + 1, revenue = revenue + ?
                     WHERE id = ?''',
                  (amount, placement_id))
        
        conn.commit()
        conn.close()
    
    def get_top_performers(self, limit: int = 10) -> List[Dict]:
        """Get top performing affiliate products"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT 
                        p.name,
                        COUNT(pl.id) as placements,
                        SUM(pl.clicks) as total_clicks,
                        SUM(pl.conversions) as total_conversions,
                        SUM(pl.revenue) as total_revenue,
                        ROUND(SUM(pl.revenue) / NULLIF(SUM(pl.clicks), 0) * 100, 2) as epc
                     FROM products p
                     LEFT JOIN placements pl ON p.id = pl.product_id
                     GROUP BY p.id
                     ORDER BY total_revenue DESC
                     LIMIT ?''', (limit,))
        
        performers = [dict(row) for row in c.fetchall()]
        conn.close()
        return performers
    
    def get_revenue_summary(self, days: int = 30) -> Dict:
        """Get affiliate revenue summary"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        cutoff = datetime.now().date()
        
        # Total revenue
        c.execute('''SELECT 
                        SUM(amount) as total,
                        COUNT(*) as conversions
                     FROM conversions
                     WHERE status IN ('confirmed', 'paid')''')
        result = c.fetchone()
        total_revenue = result[0] or 0
        total_conversions = result[1] or 0
        
        # Pending revenue
        c.execute('''SELECT SUM(amount) FROM conversions WHERE status = 'pending' ''')
        pending = c.fetchone()[0] or 0
        
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
            'total_revenue': total_revenue,
            'pending_revenue': pending,
            'total_conversions': total_conversions,
            'by_program': by_program
        }
    
    def scan_all_posts(self, posts_dir: str, dry_run: bool = True):
        """Scan all posts for affiliate opportunities"""
        posts_path = Path(posts_dir)
        
        if not posts_path.exists():
            print(f"Posts directory not found: {posts_dir}")
            return
        
        results = []
        
        for post_file in posts_path.glob("**/*.md"):
            result = self.embed_links(str(post_file), dry_run=dry_run)
            if result.get('embedded', 0) > 0:
                results.append(result)
        
        print(f"\n{'='*60}")
        print(f"📊 Scan Complete")
        print(f"{'='*60}")
        print(f"Posts scanned: {len(list(posts_path.glob('**/*.md')))}")
        print(f"Posts with opportunities: {len(results)}")
        total_embedded = sum(r['embedded'] for r in results)
        print(f"Total links embedded: {total_embedded}")
        print(f"{'='*60}\n")
        
        return results


def main():
    manager = AffiliateManager("/root/.openclaw/workspace/ai-automation-blog")
    
    # Load programs if file exists
    programs_file = manager.workspace / "data" / "affiliate-programs.json"
    if programs_file.exists():
        manager.load_programs(str(programs_file))
    
    # Get revenue summary
    summary = manager.get_revenue_summary()
    print("💰 Affiliate Revenue Summary:")
    print(f"  Total: ${summary['total_revenue']:.2f}")
    print(f"  Pending: ${summary['pending_revenue']:.2f}")
    print(f"  Conversions: {summary['total_conversions']}")
    
    # Top performers
    print("\n🏆 Top Performing Products:")
    performers = manager.get_top_performers(5)
    for p in performers:
        print(f"  • {p['name']}: ${p['total_revenue'] or 0:.2f} ({p['total_conversions'] or 0} conversions)")
    
    print("\n✅ Affiliate manager ready!")


if __name__ == "__main__":
    main()
