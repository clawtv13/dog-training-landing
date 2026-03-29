#!/usr/bin/env python3
"""
Product Creator Agent - Automated Digital Product Generation
Analyzes blog content and generates high-value digital products
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

class ProductCreatorAgent:
    def __init__(self, workspace_dir: str = "/root/.openclaw/workspace/ai-automation-blog"):
        self.workspace = Path(workspace_dir)
        self.blog_dir = self.workspace / "blog" / "content" / "posts"
        self.products_dir = self.workspace / "products"
        self.data_dir = self.workspace / "data"
        
        # Ensure directories exist
        self.products_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Product tiers and pricing
        self.tiers = {
            "low_ticket": {
                "price_range": (20, 50),
                "types": ["ebook", "template_pack", "cheat_sheet", "swipe_file"],
                "effort": "low",
                "time_to_create": "1-3 days"
            },
            "mid_ticket": {
                "price_range": (100, 500),
                "types": ["video_course", "workshop", "implementation_guide", "tool_bundle"],
                "effort": "medium",
                "time_to_create": "1-2 weeks"
            },
            "high_ticket": {
                "price_range": (500, 2000),
                "types": ["cohort_course", "consulting", "done_for_you", "agency_system"],
                "effort": "high",
                "time_to_create": "2-4 weeks"
            }
        }
    
    def analyze_blog_content(self) -> Dict:
        """Analyze all blog posts to identify product opportunities"""
        print("📊 Analyzing blog content...")
        
        content_analysis = {
            "total_posts": 0,
            "total_words": 0,
            "topics": {},
            "clusters": [],
            "best_performers": []
        }
        
        if not self.blog_dir.exists():
            print(f"⚠️  Blog directory not found: {self.blog_dir}")
            return content_analysis
        
        # Analyze each post
        for post_file in self.blog_dir.glob("*.md"):
            try:
                content = post_file.read_text(encoding='utf-8')
                
                # Extract frontmatter
                frontmatter = self._extract_frontmatter(content)
                body = self._extract_body(content)
                
                word_count = len(body.split())
                content_analysis["total_posts"] += 1
                content_analysis["total_words"] += word_count
                
                # Extract topics/tags
                tags = frontmatter.get("tags", [])
                category = frontmatter.get("category", "uncategorized")
                
                for tag in tags + [category]:
                    if tag not in content_analysis["topics"]:
                        content_analysis["topics"][tag] = []
                    content_analysis["topics"][tag].append({
                        "file": post_file.name,
                        "title": frontmatter.get("title", post_file.stem),
                        "words": word_count
                    })
                
            except Exception as e:
                print(f"⚠️  Error analyzing {post_file.name}: {e}")
        
        # Identify content clusters (3+ related posts)
        for topic, posts in content_analysis["topics"].items():
            if len(posts) >= 3:
                total_words = sum(p["words"] for p in posts)
                content_analysis["clusters"].append({
                    "topic": topic,
                    "posts": posts,
                    "total_words": total_words,
                    "product_potential": self._score_product_potential(topic, posts)
                })
        
        # Sort clusters by product potential
        content_analysis["clusters"].sort(key=lambda x: x["product_potential"], reverse=True)
        
        return content_analysis
    
    def _extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown"""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return {}
        
        frontmatter = {}
        yaml_content = match.group(1)
        
        # Simple YAML parsing (good enough for our needs)
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Handle arrays
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                
                frontmatter[key] = value
        
        return frontmatter
    
    def _extract_body(self, content: str) -> str:
        """Extract body content (without frontmatter)"""
        match = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
        if match:
            return content[match.end():]
        return content
    
    def _score_product_potential(self, topic: str, posts: List[Dict]) -> float:
        """Score product potential (0-100)"""
        score = 0.0
        
        # More posts = better
        score += min(len(posts) * 10, 40)
        
        # More words = better
        total_words = sum(p["words"] for p in posts)
        score += min(total_words / 1000 * 5, 30)
        
        # High-value keywords
        high_value_keywords = ["automation", "ai", "workflow", "template", "system", "framework"]
        if any(kw in topic.lower() for kw in high_value_keywords):
            score += 30
        
        return min(score, 100)
    
    def generate_product_ideas(self, analysis: Dict) -> List[Dict]:
        """Generate product ideas from content analysis"""
        print("💡 Generating product ideas...")
        
        ideas = []
        
        # Generate from top clusters
        for cluster in analysis["clusters"][:5]:  # Top 5 clusters
            topic = cluster["topic"]
            posts = cluster["posts"]
            total_words = cluster["total_words"]
            
            # Tier 1: Ebook (if enough content)
            if total_words >= 4000:
                ideas.append({
                    "name": f"{topic.title()} Mastery Guide",
                    "type": "ebook",
                    "tier": "low_ticket",
                    "price": 29,
                    "source_posts": [p["file"] for p in posts],
                    "description": f"Complete guide to {topic} with real-world examples and actionable strategies",
                    "estimated_pages": total_words // 250,
                    "time_to_create": "2-3 days"
                })
            
            # Tier 1: Template Pack
            if "automation" in topic.lower() or "workflow" in topic.lower():
                ideas.append({
                    "name": f"{topic.title()} Template Pack",
                    "type": "template_pack",
                    "tier": "low_ticket",
                    "price": 19,
                    "source_posts": [p["file"] for p in posts],
                    "description": f"Ready-to-use templates and workflows for {topic}",
                    "includes": ["Notion templates", "Automation scripts", "Checklists", "Examples"],
                    "time_to_create": "1-2 days"
                })
            
            # Tier 2: Video Course (if 5+ posts)
            if len(posts) >= 5:
                ideas.append({
                    "name": f"{topic.title()} Masterclass",
                    "type": "video_course",
                    "tier": "mid_ticket",
                    "price": 197,
                    "source_posts": [p["file"] for p in posts],
                    "description": f"Comprehensive video course on {topic} with step-by-step implementation",
                    "modules": len(posts),
                    "estimated_videos": len(posts) * 2,
                    "time_to_create": "2-3 weeks"
                })
        
        # Priority products (Month 1)
        priority_ideas = [
            {
                "name": "AI Automation Starter Kit",
                "type": "ebook",
                "tier": "low_ticket",
                "price": 29,
                "priority": "HIGH",
                "status": "ready_to_launch",
                "source": "lead-magnets/ai-automation-lead-magnet.md",
                "description": "Complete starter guide to AI automation for solopreneurs",
                "estimated_pages": 25,
                "time_to_create": "DONE (expand existing lead magnet)",
                "launch_date": "Week 1"
            },
            {
                "name": "100 ChatGPT Prompts for Solopreneurs",
                "type": "swipe_file",
                "tier": "low_ticket",
                "price": 19,
                "priority": "HIGH",
                "description": "Curated collection of high-value prompts for automation and productivity",
                "includes": ["Content creation prompts", "Business prompts", "Automation prompts", "Analysis prompts"],
                "time_to_create": "2-3 days",
                "launch_date": "Week 2"
            }
        ]
        
        return priority_ideas + ideas
    
    def create_product_spec(self, product_idea: Dict) -> Dict:
        """Create detailed product specification"""
        print(f"📋 Creating spec for: {product_idea['name']}")
        
        spec = {
            "product_id": self._generate_product_id(product_idea['name']),
            "name": product_idea['name'],
            "type": product_idea['type'],
            "tier": product_idea['tier'],
            "price": product_idea['price'],
            "status": product_idea.get('status', 'idea'),
            "created": datetime.now().isoformat(),
            
            # Content
            "description": product_idea['description'],
            "source_content": product_idea.get('source_posts', []),
            
            # Deliverables
            "deliverables": self._define_deliverables(product_idea),
            
            # Marketing
            "target_audience": "Solopreneurs and indie hackers building automated businesses",
            "pain_points": self._identify_pain_points(product_idea),
            "value_proposition": self._create_value_prop(product_idea),
            
            # Production
            "production_steps": self._define_production_steps(product_idea),
            "time_estimate": product_idea.get('time_to_create', 'TBD'),
            
            # Launch
            "launch_strategy": "email_sequence",
            "pricing_strategy": "value_based",
            "upsells": self._suggest_upsells(product_idea)
        }
        
        return spec
    
    def _generate_product_id(self, name: str) -> str:
        """Generate product ID from name"""
        return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    def _define_deliverables(self, product: Dict) -> List[str]:
        """Define what customer gets"""
        ptype = product['type']
        
        deliverables_map = {
            "ebook": [
                "PDF ebook (DRM-free)",
                "EPUB format",
                "Notion template version",
                "Bonus: Quick reference cheat sheet"
            ],
            "template_pack": [
                "Notion templates (duplicate links)",
                "Automation scripts",
                "Setup guide PDF",
                "Video walkthrough (10-15 min)"
            ],
            "swipe_file": [
                "PDF with all prompts",
                "Editable Notion database",
                "Usage guide",
                "Bonus: Prompt engineering tips"
            ],
            "video_course": [
                "HD video lessons (lifetime access)",
                "Course workbook PDF",
                "Templates and resources",
                "Private community access",
                "Certificate of completion"
            ]
        }
        
        return deliverables_map.get(ptype, ["Main product file", "Setup guide", "Support access"])
    
    def _identify_pain_points(self, product: Dict) -> List[str]:
        """Identify pain points this solves"""
        return [
            "Wasting time on repetitive tasks",
            "Don't know where to start with AI automation",
            "Tried automation tools but got overwhelmed",
            "Need proven templates and systems that actually work"
        ]
    
    def _create_value_prop(self, product: Dict) -> str:
        """Create value proposition"""
        name = product['name']
        return f"{name} gives you battle-tested systems to automate your business without the learning curve. Skip months of trial and error."
    
    def _define_production_steps(self, product: Dict) -> List[str]:
        """Define production steps"""
        ptype = product['type']
        
        steps_map = {
            "ebook": [
                "Compile content from source posts",
                "Structure into chapters",
                "Add examples and case studies",
                "Design PDF layout",
                "Proofread and edit",
                "Convert to EPUB",
                "Create cheat sheet bonus"
            ],
            "template_pack": [
                "Build Notion templates",
                "Test each template",
                "Write setup guide",
                "Record video walkthrough",
                "Package everything"
            ],
            "swipe_file": [
                "Collect and categorize prompts",
                "Test each prompt",
                "Write usage instructions",
                "Design PDF layout",
                "Build Notion database"
            ]
        }
        
        return steps_map.get(ptype, ["Define scope", "Create content", "Design", "Test", "Package"])
    
    def _suggest_upsells(self, product: Dict) -> List[Dict]:
        """Suggest upsell products"""
        tier = product['tier']
        
        if tier == "low_ticket":
            return [
                {"name": "Video Masterclass", "price": 197, "discount": "50% for existing customers"},
                {"name": "Product Bundle", "price": 149, "savings": "$96"}
            ]
        elif tier == "mid_ticket":
            return [
                {"name": "1-on-1 Implementation Call", "price": 297},
                {"name": "Cohort Course", "price": 497, "includes": "Group coaching"}
            ]
        
        return []
    
    def save_product_spec(self, spec: Dict):
        """Save product specification"""
        product_id = spec['product_id']
        output_file = self.products_dir / f"{product_id}.json"
        
        with open(output_file, 'w') as f:
            json.dump(spec, f, indent=2)
        
        print(f"✅ Saved: {output_file}")
        
        # Also create markdown version
        md_file = self.products_dir / f"{product_id}.md"
        self._create_markdown_spec(spec, md_file)
    
    def _create_markdown_spec(self, spec: Dict, output_file: Path):
        """Create markdown version of spec"""
        md_content = f"""# {spec['name']}

**Product ID:** {spec['product_id']}  
**Type:** {spec['type']}  
**Tier:** {spec['tier']}  
**Price:** ${spec['price']}  
**Status:** {spec['status']}

## Description

{spec['description']}

## Target Audience

{spec['target_audience']}

## Pain Points Solved

{chr(10).join('- ' + p for p in spec['pain_points'])}

## Value Proposition

{spec['value_proposition']}

## Deliverables

{chr(10).join('- ' + d for d in spec['deliverables'])}

## Production Steps

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(spec['production_steps']))}

**Time Estimate:** {spec['time_estimate']}

## Marketing Strategy

- **Launch:** {spec['launch_strategy']}
- **Pricing:** {spec['pricing_strategy']}

## Upsells

{chr(10).join(f"- **{u['name']}** - ${u['price']}" for u in spec['upsells'])}

## Source Content

{chr(10).join('- ' + s for s in spec.get('source_content', ['TBD']))}

---
*Generated: {spec['created']}*
"""
        
        output_file.write_text(md_content)
        print(f"📄 Markdown spec: {output_file}")
    
    def generate_roadmap(self, product_ideas: List[Dict]) -> Dict:
        """Generate 90-day product roadmap"""
        print("🗓️  Generating 90-day roadmap...")
        
        roadmap = {
            "month_1": {
                "focus": "Quick wins - Launch first 2 products",
                "products": [],
                "revenue_target": 500,
                "subscriber_target": 100
            },
            "month_2": {
                "focus": "Scale - Video course + bundle",
                "products": [],
                "revenue_target": 3000,
                "subscriber_target": 500
            },
            "month_3": {
                "focus": "Premium - Cohort course + consulting",
                "products": [],
                "revenue_target": 10000,
                "subscriber_target": 1000
            }
        }
        
        # Assign products to months
        for idea in product_ideas:
            priority = idea.get('priority', 'NORMAL')
            tier = idea['tier']
            
            if priority == 'HIGH' or tier == 'low_ticket':
                roadmap['month_1']['products'].append(idea)
            elif tier == 'mid_ticket':
                roadmap['month_2']['products'].append(idea)
            else:
                roadmap['month_3']['products'].append(idea)
        
        return roadmap
    
    def run(self):
        """Run full product creation pipeline"""
        print("🚀 Product Creator Agent Starting...")
        print("=" * 60)
        
        # Step 1: Analyze content
        analysis = self.analyze_blog_content()
        print(f"\n📊 Analysis Complete:")
        print(f"   - Total posts: {analysis['total_posts']}")
        print(f"   - Total words: {analysis['total_words']:,}")
        print(f"   - Content clusters: {len(analysis['clusters'])}")
        
        # Save analysis
        analysis_file = self.data_dir / "content-analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"   - Saved: {analysis_file}")
        
        # Step 2: Generate product ideas
        ideas = self.generate_product_ideas(analysis)
        print(f"\n💡 Generated {len(ideas)} product ideas")
        
        # Step 3: Create specs for priority products
        print(f"\n📋 Creating product specifications...")
        for idea in ideas[:5]:  # Top 5 products
            spec = self.create_product_spec(idea)
            self.save_product_spec(spec)
        
        # Step 4: Generate roadmap
        roadmap = self.generate_roadmap(ideas)
        roadmap_file = self.products_dir / "roadmap.json"
        with open(roadmap_file, 'w') as f:
            json.dump(roadmap, f, indent=2)
        print(f"\n🗓️  Roadmap saved: {roadmap_file}")
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PRODUCT CREATOR AGENT COMPLETE")
        print("=" * 60)
        print(f"📦 Products ready: {len(ideas)}")
        print(f"🎯 Priority products: {len([i for i in ideas if i.get('priority') == 'HIGH'])}")
        print(f"💰 Month 1 revenue target: ${roadmap['month_1']['revenue_target']}")
        print(f"🚀 First product ready: {ideas[0]['name']}")
        print("=" * 60)

if __name__ == "__main__":
    agent = ProductCreatorAgent()
    agent.run()
