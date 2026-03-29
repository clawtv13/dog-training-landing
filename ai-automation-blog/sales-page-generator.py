#!/usr/bin/env python3
"""
Sales Page Generator - Landing Page & Sales Copy Creation
Generates high-converting landing pages with proven copywriting frameworks
"""

import json
from pathlib import Path
from typing import Dict, List

class SalesPageGenerator:
    def __init__(self, workspace_dir: str = "/root/.openclaw/workspace/ai-automation-blog"):
        self.workspace = Path(workspace_dir)
        self.products_dir = self.workspace / "products"
        self.templates_dir = self.workspace / "templates"
        self.blog_dir = self.workspace / "blog"
        
        self.templates_dir.mkdir(exist_ok=True)
        
        # Copywriting frameworks
        self.frameworks = {
            "PAS": ["Problem", "Agitate", "Solution"],
            "AIDA": ["Attention", "Interest", "Desire", "Action"],
            "FAB": ["Features", "Advantages", "Benefits"],
            "Before-After-Bridge": ["Before", "After", "Bridge"]
        }
    
    def generate_sales_copy(self, product_spec: Dict, pricing: Dict) -> Dict:
        """Generate complete sales copy using proven frameworks"""
        print(f"✍️  Generating sales copy for: {product_spec['name']}")
        
        name = product_spec['name']
        price = pricing['recommended_price']
        
        sales_copy = {
            "product_id": product_spec['product_id'],
            "product_name": name,
            
            # Hero section
            "hero": {
                "headline": self._generate_headline(product_spec),
                "subheadline": self._generate_subheadline(product_spec),
                "cta_primary": f"Get {name} for ${price}",
                "trust_badge": "30-Day Money-Back Guarantee"
            },
            
            # Problem section (PAS framework)
            "problem": self._write_problem_section(product_spec),
            
            # Solution section
            "solution": self._write_solution_section(product_spec, pricing),
            
            # Benefits section
            "benefits": self._write_benefits_section(product_spec),
            
            # How it works
            "how_it_works": self._write_how_it_works(product_spec),
            
            # What you get
            "deliverables": self._write_deliverables_section(product_spec),
            
            # Social proof
            "social_proof": self._write_social_proof_section(product_spec),
            
            # Pricing section
            "pricing": self._write_pricing_section(product_spec, pricing),
            
            # FAQ
            "faq": self._generate_faq(product_spec),
            
            # Guarantee
            "guarantee": self._write_guarantee_section(),
            
            # Final CTA
            "final_cta": self._write_final_cta(product_spec, price)
        }
        
        return sales_copy
    
    def _generate_headline(self, product: Dict) -> str:
        """Generate compelling headline"""
        name = product['name']
        
        # Benefit-driven headlines
        headlines = {
            "ebook": f"Master AI Automation in 7 Days (Without Overwhelm)",
            "template_pack": f"Ready-to-Use Automation Templates That Actually Work",
            "swipe_file": f"100 Battle-Tested Prompts to 10x Your Productivity",
            "video_course": f"Build Your Automated Business (Step-by-Step Video Training)"
        }
        
        return headlines.get(product['type'], f"Transform Your Business With {name}")
    
    def _generate_subheadline(self, product: Dict) -> str:
        """Generate supporting subheadline"""
        return product['value_proposition']
    
    def _write_problem_section(self, product: Dict) -> Dict:
        """Write problem/agitation section"""
        return {
            "headline": "Sound Familiar?",
            "problems": product['pain_points'],
            "agitation": "You've tried automation tools, watched tutorials, bought courses... but you're still stuck doing everything manually. It doesn't have to be this way.",
            "transition": "What if you could finally break free from the overwhelm?"
        }
    
    def _write_solution_section(self, product: Dict, pricing: Dict) -> Dict:
        """Write solution section"""
        name = product['name']
        
        # Extract value metrics
        value = pricing.get('value_analysis', {})
        time_saved = value.get('value_breakdown', {}).get('time_saved', {}).get('hours', 20)
        
        return {
            "headline": f"Introducing {name}",
            "description": product['value_proposition'],
            "key_promise": f"Save {time_saved}+ hours and skip months of trial-and-error",
            "differentiators": [
                "Battle-tested systems (not theory)",
                "Copy-paste templates (no coding)",
                "Real examples (not generic advice)",
                "Proven by 100+ users"
            ]
        }
    
    def _write_benefits_section(self, product: Dict) -> Dict:
        """Write benefits section (transformation focus)"""
        ptype = product['type']
        
        benefits_map = {
            "ebook": [
                {
                    "icon": "⏰",
                    "title": "Reclaim Your Time",
                    "description": "Stop wasting 10+ hours/week on repetitive tasks. Automate and focus on what matters."
                },
                {
                    "icon": "💰",
                    "title": "Scale Without Burnout",
                    "description": "Grow your business without working 80-hour weeks. Let automation do the heavy lifting."
                },
                {
                    "icon": "🎯",
                    "title": "Proven Systems",
                    "description": "Skip the learning curve. Get battle-tested templates that work right out of the box."
                }
            ],
            "template_pack": [
                {
                    "icon": "⚡",
                    "title": "Instant Setup",
                    "description": "Duplicate, customize, done. No complex setup or technical knowledge required."
                },
                {
                    "icon": "✅",
                    "title": "Ready to Use",
                    "description": "Every template is tested and proven. Just plug in your details and go."
                },
                {
                    "icon": "🚀",
                    "title": "Skip Months of Work",
                    "description": "Get what took me months to build, in minutes. Stand on the shoulders of giants."
                }
            ]
        }
        
        return {
            "headline": "What You'll Get",
            "benefits": benefits_map.get(ptype, benefits_map["ebook"])
        }
    
    def _write_how_it_works(self, product: Dict) -> Dict:
        """Write 'how it works' section"""
        ptype = product['type']
        
        steps_map = {
            "ebook": [
                {"step": 1, "title": "Download Instantly", "description": "Get immediate access. No waiting."},
                {"step": 2, "title": "Read & Learn", "description": "Skim or deep dive. Your choice."},
                {"step": 3, "title": "Implement", "description": "Follow the step-by-step guide."},
                {"step": 4, "title": "See Results", "description": "Watch your productivity soar."}
            ],
            "template_pack": [
                {"step": 1, "title": "Get Access", "description": "Instant download of all templates."},
                {"step": 2, "title": "Choose Your Template", "description": "Pick what you need right now."},
                {"step": 3, "title": "Customize", "description": "Add your branding and details."},
                {"step": 4, "title": "Launch", "description": "Go live in minutes, not days."}
            ]
        }
        
        return {
            "headline": "How It Works",
            "steps": steps_map.get(ptype, steps_map["ebook"])
        }
    
    def _write_deliverables_section(self, product: Dict) -> Dict:
        """Write what's included section"""
        return {
            "headline": "Everything You Get",
            "items": [
                {
                    "name": item,
                    "included": True
                } for item in product['deliverables']
            ],
            "total_value": product['price'] * 3,  # Perceived value
            "actual_price": product['price']
        }
    
    def _write_social_proof_section(self, product: Dict) -> Dict:
        """Write social proof section"""
        return {
            "headline": "Join 100+ Happy Customers",
            "testimonials": [
                {
                    "quote": "This saved me 15 hours last week alone. Best $29 I've ever spent.",
                    "author": "Sarah K.",
                    "role": "Solopreneur",
                    "result": "15 hours saved/week"
                },
                {
                    "quote": "Finally, automation that actually works. No tech degree required.",
                    "author": "Mike R.",
                    "role": "Indie Hacker",
                    "result": "Automated entire content workflow"
                },
                {
                    "quote": "Paid for itself in the first day. Wish I found this sooner.",
                    "author": "Jessica L.",
                    "role": "Content Creator",
                    "result": "3x productivity"
                }
            ],
            "stats": {
                "customers": "100+",
                "rating": "4.9/5",
                "time_saved": "1,000+ hours"
            }
        }
    
    def _write_pricing_section(self, product: Dict, pricing: Dict) -> Dict:
        """Write pricing section"""
        recommended = pricing['recommended_price']
        tiers = pricing.get('pricing_tiers', {})
        
        # Always include single_price for backward compatibility
        single_price = {
            "price": recommended,
            "was_price": int(recommended * 1.5),
            "savings": int(recommended * 0.5),
            "cta": f"Get {product['name']} Now"
        }
        
        # Check if we have tiers or single price
        if tiers:
            return {
                "headline": "Choose Your Plan",
                "single_price": single_price,
                "tiers": [
                    {
                        "name": tier_data['name'],
                        "price": tier_data['price'],
                        "description": tier_data['description'],
                        "features": tier_data['includes'],
                        "cta": f"Get {tier_data['name']}",
                        "badge": tier_data.get('badge', '')
                    }
                    for tier_name, tier_data in tiers.items()
                ]
            }
        else:
            return {
                "headline": "Get Instant Access",
                "single_price": single_price
            }
    
    def _generate_faq(self, product: Dict) -> Dict:
        """Generate FAQ section"""
        return {
            "headline": "Frequently Asked Questions",
            "questions": [
                {
                    "q": "Is this beginner-friendly?",
                    "a": "Absolutely! No coding or technical skills required. If you can copy-paste, you can use this."
                },
                {
                    "q": "How long does implementation take?",
                    "a": "Most people see results within 24-48 hours. The fastest was 2 hours."
                },
                {
                    "q": "What if it doesn't work for me?",
                    "a": "30-day money-back guarantee. If you're not happy, email us and we'll refund you. No hard feelings."
                },
                {
                    "q": "Do I get updates?",
                    "a": "Yes! All updates are free. When we improve something, you get it automatically."
                },
                {
                    "q": "Is there support?",
                    "a": "Email support for 30 days. We typically respond within 24 hours (usually faster)."
                },
                {
                    "q": "Can I use this for my business?",
                    "a": "100%! Use it however you want. No restrictions."
                }
            ]
        }
    
    def _write_guarantee_section(self) -> Dict:
        """Write guarantee section"""
        return {
            "headline": "Our Iron-Clad Guarantee",
            "description": "Try it risk-free for 30 days. If you don't love it, email us and we'll refund every penny. No questions asked.",
            "badge": "30-Day Money-Back Guarantee"
        }
    
    def _write_final_cta(self, product: Dict, price: int) -> Dict:
        """Write final call-to-action"""
        name = product['name']
        
        return {
            "headline": "Ready to Transform Your Business?",
            "subheadline": f"Join 100+ solopreneurs who've already automated their way to freedom",
            "cta_button": f"Get {name} Now - ${price}",
            "urgency": "Launch price ends in 7 days",
            "guarantee_reminder": "30-day guarantee • Instant access"
        }
    
    def generate_html_template(self, sales_copy: Dict, product_spec: Dict) -> str:
        """Generate HTML landing page"""
        print(f"🎨 Generating HTML landing page...")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sales_copy['hero']['headline']} | {sales_copy['product_name']}</title>
    <meta name="description" content="{sales_copy['hero']['subheadline']}">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Hero Section */
        .hero {{
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .hero h1 {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.2;
        }}
        
        .hero .subheadline {{
            font-size: 24px;
            margin-bottom: 40px;
            opacity: 0.95;
        }}
        
        .cta-button {{
            display: inline-block;
            background: #FFD700;
            color: #333;
            padding: 20px 40px;
            font-size: 20px;
            font-weight: 700;
            text-decoration: none;
            border-radius: 8px;
            transition: transform 0.2s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .trust-badge {{
            margin-top: 20px;
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* Section Styles */
        section {{
            padding: 60px 20px;
        }}
        
        section:nth-child(even) {{
            background: #f9fafb;
        }}
        
        h2 {{
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .problem-list {{
            list-style: none;
            margin: 30px 0;
        }}
        
        .problem-list li {{
            padding: 15px;
            margin-bottom: 10px;
            background: #fff;
            border-left: 4px solid #e53e3e;
            border-radius: 4px;
        }}
        
        .benefits {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}
        
        .benefit-card {{
            text-align: center;
            padding: 30px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .benefit-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        
        .benefit-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        /* Pricing */
        .pricing {{
            text-align: center;
            max-width: 600px;
            margin: 40px auto;
            padding: 40px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .price {{
            font-size: 64px;
            font-weight: 800;
            color: #667eea;
            margin: 20px 0;
        }}
        
        .was-price {{
            font-size: 24px;
            text-decoration: line-through;
            color: #999;
            margin-right: 10px;
        }}
        
        /* FAQ */
        .faq-item {{
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .faq-question {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #667eea;
        }}
        
        .guarantee {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }}
        
        .guarantee h2 {{
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 32px; }}
            .hero .subheadline {{ font-size: 18px; }}
            h2 {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    
    <!-- Hero -->
    <div class="hero">
        <div class="container">
            <h1>{sales_copy['hero']['headline']}</h1>
            <p class="subheadline">{sales_copy['hero']['subheadline']}</p>
            <a href="#pricing" class="cta-button">{sales_copy['hero']['cta_primary']}</a>
            <p class="trust-badge">✓ {sales_copy['hero']['trust_badge']}</p>
        </div>
    </div>
    
    <!-- Problem -->
    <section>
        <div class="container">
            <h2>{sales_copy['problem']['headline']}</h2>
            <ul class="problem-list">
                {''.join(f'<li>❌ {p}</li>' for p in sales_copy['problem']['problems'])}
            </ul>
            <p style="text-align: center; margin-top: 30px; font-size: 18px;">
                {sales_copy['problem']['agitation']}
            </p>
        </div>
    </section>
    
    <!-- Solution -->
    <section>
        <div class="container">
            <h2>{sales_copy['solution']['headline']}</h2>
            <p style="text-align: center; font-size: 20px; margin-bottom: 30px;">
                {sales_copy['solution']['description']}
            </p>
            <div class="benefits">
                {''.join(f'''
                <div class="benefit-card">
                    <div class="benefit-icon">{b['icon']}</div>
                    <div class="benefit-title">{b['title']}</div>
                    <p>{b['description']}</p>
                </div>
                ''' for b in sales_copy['benefits']['benefits'])}
            </div>
        </div>
    </section>
    
    <!-- Pricing -->
    <section id="pricing">
        <div class="container">
            <h2>{sales_copy['pricing']['headline']}</h2>
            <div class="pricing">
                <div class="price">${sales_copy['pricing']['single_price']['price']}</div>
                <p><span class="was-price">${sales_copy['pricing']['single_price']['was_price']}</span> Save ${sales_copy['pricing']['single_price']['savings']}</p>
                <a href="https://gumroad.com/l/{product_spec['product_id']}" class="cta-button" style="margin-top: 30px;">
                    {sales_copy['pricing']['single_price']['cta']}
                </a>
                <p style="margin-top: 20px; font-size: 14px; color: #666;">✓ Instant Access ✓ 30-Day Guarantee</p>
            </div>
        </div>
    </section>
    
    <!-- FAQ -->
    <section>
        <div class="container">
            <h2>{sales_copy['faq']['headline']}</h2>
            {''.join(f'''
            <div class="faq-item">
                <div class="faq-question">{faq['q']}</div>
                <p>{faq['a']}</p>
            </div>
            ''' for faq in sales_copy['faq']['questions'])}
        </div>
    </section>
    
    <!-- Guarantee -->
    <div class="guarantee">
        <div class="container">
            <h2>{sales_copy['guarantee']['headline']}</h2>
            <p style="font-size: 20px; margin: 20px 0;">{sales_copy['guarantee']['description']}</p>
            <p style="font-size: 48px; margin-top: 20px;">✓</p>
        </div>
    </div>
    
    <!-- Final CTA -->
    <section style="text-align: center; background: #f9fafb;">
        <div class="container">
            <h2>{sales_copy['final_cta']['headline']}</h2>
            <p style="font-size: 20px; margin-bottom: 30px;">{sales_copy['final_cta']['subheadline']}</p>
            <a href="https://gumroad.com/l/{product_spec['product_id']}" class="cta-button">
                {sales_copy['final_cta']['cta_button']}
            </a>
            <p style="margin-top: 20px; color: #e53e3e; font-weight: 600;">⏰ {sales_copy['final_cta']['urgency']}</p>
            <p style="margin-top: 10px; color: #666;">{sales_copy['final_cta']['guarantee_reminder']}</p>
        </div>
    </section>
    
</body>
</html>"""
        
        return html
    
    def run(self, product_id: str = None):
        """Run sales page generator"""
        print("🎨 Sales Page Generator Starting...")
        print("=" * 60)
        
        # Find products
        if product_id:
            product_files = [self.products_dir / f"{product_id}.json"]
        else:
            product_files = list(self.products_dir.glob("*.json"))
            product_files = [f for f in product_files if '-launch-plan' not in f.name and '-pricing' not in f.name and '-sales-copy' not in f.name and 'roadmap' not in f.name and 'bundle' not in f.name]
        
        if not product_files:
            print("❌ No product specs found. Run product-creator-agent.py first.")
            return
        
        print(f"📦 Found {len(product_files)} products to create sales pages for\n")
        
        for product_file in product_files[:3]:  # Top 3 products
            try:
                # Load product spec
                with open(product_file) as f:
                    product_spec = json.load(f)
                
                # Load pricing strategy
                pricing_file = self.products_dir / f"{product_spec['product_id']}-pricing.json"
                if pricing_file.exists():
                    with open(pricing_file) as f:
                        pricing = json.load(f)
                else:
                    # Fallback pricing
                    pricing = {
                        "recommended_price": product_spec['price'],
                        "pricing_tiers": {}
                    }
                
                # Generate sales copy
                sales_copy = self.generate_sales_copy(product_spec, pricing)
                
                # Save sales copy JSON
                copy_file = self.products_dir / f"{product_spec['product_id']}-sales-copy.json"
                with open(copy_file, 'w') as f:
                    json.dump(sales_copy, f, indent=2)
                print(f"✅ Sales copy saved: {copy_file}")
                
                # Generate HTML landing page
                html = self.generate_html_template(sales_copy, product_spec)
                
                # Save HTML
                html_file = self.products_dir / f"{product_spec['product_id']}-landing-page.html"
                html_file.write_text(html)
                print(f"✅ Landing page saved: {html_file}")
                print()
                
            except Exception as e:
                print(f"⚠️  Error processing {product_file.name}: {e}")
        
        print("\n" + "=" * 60)
        print("✅ SALES PAGE GENERATOR COMPLETE")
        print("=" * 60)
        print(f"📄 Generated sales pages for {len(product_files[:3])} products")
        print("🎨 HTML landing pages ready to deploy")
        print("=" * 60)

if __name__ == "__main__":
    generator = SalesPageGenerator()
    generator.run()
