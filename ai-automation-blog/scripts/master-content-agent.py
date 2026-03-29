#!/usr/bin/env python3
"""
Master Content Agent V3 - Unified SEO-first Blog Post Generator
Integrates keyword research, competitor analysis, SEO optimization, and quality scoring
into ONE intelligent content generation workflow.

Author: AI Automation Builder
Version: 3.0.0
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
import time
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_DIR = WORKSPACE / "blog"
POSTS_DIR = BLOG_DIR / "posts"
TEMPLATE = WORKSPACE / "templates" / "post.html"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"
STATE_DIR = WORKSPACE / ".state"
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"

# State files
STATE_FILE = STATE_DIR / "published-posts.json"
FINGERPRINT_FILE = STATE_DIR / "content-fingerprints.json"
SEO_CACHE = DATA_DIR / "seo-research-cache.json"

# Create directories
for directory in [STATE_DIR, DATA_DIR, LOGS_DIR, POSTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging
LOG_FILE = LOGS_DIR / f"master-agent-{datetime.now().strftime('%Y-%m')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Model Configuration
WRITING_MODEL = "anthropic/claude-sonnet-4"  # For content generation
ANALYSIS_MODEL = "anthropic/claude-3.7-sonnet"  # For SEO/scoring (cheaper)

# Tunables
MIN_QUALITY_SCORE = 70
TARGET_QUALITY_SCORE = 85
MAX_REGENERATION_ATTEMPTS = 2
MIN_NEWSLETTER_SCORE = 30
REQUEST_TIMEOUT = 120
COST_PER_POST_LIMIT = 0.06  # USD

# Author persona
AUTHOR_NAME = "Alex Chen"
AUTHOR_BIO = "AI automation consultant helping solopreneurs build profitable systems"

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SEOResearch:
    """SEO research results for a topic"""
    primary_keyword: str
    secondary_keywords: List[str]
    search_intent: str  # informational, commercial, transactional, navigational
    competitor_gaps: List[str]
    internal_link_opportunities: List[Dict[str, str]]
    suggested_title: str
    suggested_meta_description: str
    
@dataclass
class QualityScore:
    """Content quality scoring breakdown"""
    specific_examples: int  # 0-20
    real_data: int  # 0-15
    personal_voice: int  # 0-15
    actionable_content: int  # 0-20
    proper_structure: int  # 0-10
    no_ai_patterns: int  # 0-10
    seo_optimization: int  # 0-10
    total: int  # 0-100
    feedback: List[str]
    
@dataclass
class GeneratedContent:
    """Generated blog post with metadata"""
    html_content: str
    title: str
    excerpt: str
    quality_score: QualityScore
    seo_research: SEOResearch
    word_count: int
    read_time: int
    internal_links_added: int

# ============================================================================
# UTILITIES
# ============================================================================

def load_json(filepath: Path, default=None):
    """Load JSON with fallback"""
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default if default is not None else {}
    return default if default is not None else {}

def save_json(filepath: Path, data):
    """Save JSON atomically"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    temp = filepath.with_suffix('.tmp')
    with open(temp, 'w') as f:
        json.dump(data, f, indent=2)
    temp.replace(filepath)

def content_fingerprint(text: str) -> str:
    """Generate content fingerprint for duplicate detection"""
    normalized = re.sub(r'[^\w\s]', '', text.lower())
    words = sorted(set(normalized.split()))[:100]
    return hashlib.md5(' '.join(words).encode()).hexdigest()

def is_duplicate(title: str, summary: str) -> bool:
    """Check if content is duplicate"""
    fingerprint = content_fingerprint(title + " " + summary)
    fingerprints = load_json(FINGERPRINT_FILE, [])
    return fingerprint in fingerprints

def save_fingerprint(title: str, summary: str):
    """Save content fingerprint"""
    fingerprint = content_fingerprint(title + " " + summary)
    fingerprints = load_json(FINGERPRINT_FILE, [])
    if fingerprint not in fingerprints:
        fingerprints.append(fingerprint)
        save_json(FINGERPRINT_FILE, fingerprints)

# ============================================================================
# API WRAPPER
# ============================================================================

def call_llm(prompt: str, model: str = WRITING_MODEL, system: str = None) -> str:
    """Call LLM with retry logic"""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "user", "content": prompt}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 8192
    }
    
    for attempt in range(3):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        except Exception as e:
            if attempt == 2:
                raise
            logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
            time.sleep(2 ** attempt)
    
    raise Exception("API call failed after retries")

# ============================================================================
# PHASE 1: PRE-GENERATION (SEO Research)
# ============================================================================

def conduct_seo_research(source_item: Dict) -> SEOResearch:
    """
    Conduct comprehensive SEO research for topic
    Includes keyword research, competitor analysis, search intent mapping
    """
    logger.info("🔍 Phase 1: Conducting SEO research...")
    
    title = source_item['title']
    summary = source_item['summary']
    
    # Check cache first
    cache_key = content_fingerprint(title + summary)
    cache = load_json(SEO_CACHE, {})
    
    if cache_key in cache:
        logger.info("✓ Using cached SEO research")
        return SEOResearch(**cache[cache_key])
    
    # Load existing posts for internal linking
    published = load_json(STATE_FILE, [])
    existing_titles = [p['title'] for p in published[-20:]]  # Last 20 posts
    
    prompt = f"""You are an SEO expert conducting pre-publication research for a blog post.

SOURCE MATERIAL:
Title: {title}
Summary: {summary}
Source URL: {source_item.get('url', 'N/A')}

EXISTING BLOG POSTS (for internal linking):
{chr(10).join(f"- {t}" for t in existing_titles)}

YOUR TASK: Conduct comprehensive SEO research and return a JSON object with:

1. **primary_keyword**: The main keyword to target (2-4 words, high search volume + low competition)
2. **secondary_keywords**: Array of 3-5 related keywords to naturally integrate
3. **search_intent**: Classification (informational/commercial/transactional/navigational)
4. **competitor_gaps**: Array of 3-5 things competitors miss that we should cover
5. **internal_link_opportunities**: Array of objects with {{title, anchor_text}} for 2-3 internal links to related existing posts
6. **suggested_title**: SEO-optimized title (60 chars max, includes primary keyword)
7. **suggested_meta_description**: Compelling meta description (155 chars max, includes call-to-action)

REQUIREMENTS:
- Keywords must be specific to AI automation for solopreneurs
- Title must be click-worthy AND keyword-rich
- Meta description must drive clicks from search results
- Internal links must be genuinely relevant (or empty array if none fit)

Return ONLY valid JSON, no explanation."""

    try:
        result = call_llm(prompt, model=ANALYSIS_MODEL)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            research = SEOResearch(**data)
            
            # Cache the result
            cache[cache_key] = asdict(research)
            save_json(SEO_CACHE, cache)
            
            logger.info(f"✓ SEO research complete")
            logger.info(f"  Primary keyword: {research.primary_keyword}")
            logger.info(f"  Search intent: {research.search_intent}")
            logger.info(f"  Internal links: {len(research.internal_link_opportunities)}")
            
            return research
        else:
            raise ValueError("No JSON found in response")
    
    except Exception as e:
        logger.error(f"SEO research failed: {e}")
        # Fallback to basic research
        return SEOResearch(
            primary_keyword=title.split()[:3],
            secondary_keywords=[],
            search_intent="informational",
            competitor_gaps=[],
            internal_link_opportunities=[],
            suggested_title=title[:60],
            suggested_meta_description=summary[:155]
        )

# ============================================================================
# PHASE 2: CONTENT GENERATION (SEO-Aware)
# ============================================================================

def generate_content(source_item: Dict, seo_research: SEOResearch) -> Tuple[str, int]:
    """
    Generate SEO-optimized content with keywords naturally embedded
    Returns (html_content, word_count)
    """
    logger.info("✍️  Phase 2: Generating SEO-optimized content...")
    
    system_prompt = f"""You are {AUTHOR_NAME}, {AUTHOR_BIO}.

You write for "AI Automation Builder" - a blog helping solopreneurs master AI automation.

WRITING STYLE:
- Conversational but authoritative (like Paul Graham or Derek Sivers)
- Specific examples over generic advice
- Personal anecdotes when relevant
- Action-oriented (readers should DO something after reading)
- No corporate jargon or AI clichés

FORBIDDEN PHRASES (never use):
- "As a [role]..."
- "Imagine..."
- "In today's world..."
- "It's no secret that..."
- "The bottom line is..."
- "At the end of the day..."
- "Leverage", "utilize", "synergy"

YOUR VOICE:
- Use "I" and "you" freely
- Short sentences. Punchy paragraphs.
- Occasional sentence fragments for emphasis.
- Questions to engage readers.
- Concrete numbers and data points."""

    user_prompt = f"""Write a blog post based on this source:

TITLE: {source_item['title']}
SUMMARY: {source_item['summary']}
SOURCE: {source_item.get('url', 'N/A')}

SEO REQUIREMENTS (integrate naturally, don't force):
- Primary keyword: "{seo_research.primary_keyword}"
- Secondary keywords: {', '.join(seo_research.secondary_keywords)}
- Search intent: {seo_research.search_intent}
- Cover these gaps: {', '.join(seo_research.competitor_gaps)}

CONTENT STRUCTURE:
1. Hook (1-2 short paragraphs that grab attention)
2. Context (what is this and why does it matter?)
3. Practical Application (how solopreneurs can use this)
4. Implementation Steps (concrete, actionable)
5. Common Mistakes to Avoid
6. Real Example (specific numbers/results)
7. Call to Action (what to do next)

REQUIREMENTS:
- 1000-1400 words
- Use <h2> for main sections, <h3> for subsections
- Include 1-2 <ul> or <ol> lists
- Bold (<strong>) key points
- Include external link to source with context
- Natural keyword integration (don't stuff)
- Personal voice throughout

FORMAT:
Return ONLY clean HTML (no ```html, no <html>/<body> tags, just content).
Start with the hook paragraph, then use proper heading hierarchy."""

    content = call_llm(user_prompt, model=WRITING_MODEL, system=system_prompt)
    
    # Clean up response
    content = content.replace('```html', '').replace('```', '').strip()
    
    # Count words
    text = re.sub(r'<[^>]+>', '', content)
    word_count = len(re.findall(r'\w+', text))
    
    # Add internal links if available
    links_added = 0
    for link_opp in seo_research.internal_link_opportunities:
        pattern = re.compile(rf'\b{re.escape(link_opp["anchor_text"])}\b', re.IGNORECASE)
        if pattern.search(content) and links_added < 3:
            content = pattern.sub(
                f'<a href="/posts/{link_opp["title"]}.html">{link_opp["anchor_text"]}</a>',
                content,
                count=1
            )
            links_added += 1
    
    logger.info(f"✓ Content generated: {word_count} words, {links_added} internal links")
    
    return content, word_count

# ============================================================================
# PHASE 3: QUALITY SCORING (During Generation)
# ============================================================================

def score_content_quality(content: str, title: str, seo_research: SEOResearch) -> QualityScore:
    """
    Score content quality during generation (0-100)
    This allows for regeneration if score is too low
    """
    logger.info("📊 Phase 3: Scoring content quality...")
    
    prompt = f"""You are a content quality auditor for a professional blog.

CONTENT TO AUDIT:
Title: {title}
Content: {content}

SCORING CRITERIA (be strict):

1. **Specific Examples** (0-20 points):
   - 20: Multiple concrete examples with numbers/names
   - 10: Some examples but mostly generic
   - 0: All generic advice

2. **Real Data/Numbers** (0-15 points):
   - 15: 3+ specific numbers, stats, or measurements
   - 8: 1-2 data points
   - 0: No concrete data

3. **Personal Voice** (0-15 points):
   - 15: Unique voice, uses "I/you", conversational
   - 8: Somewhat personal but still corporate
   - 0: Generic AI corporate-speak

4. **Actionable Content** (0-20 points):
   - 20: Clear, specific steps readers can follow
   - 10: Some actionable but vague
   - 0: Just information, no actions

5. **Proper Structure** (0-10 points):
   - 10: Perfect H2/H3 hierarchy, scannable, formatted
   - 5: Basic structure
   - 0: Wall of text

6. **No AI Patterns** (0-10 points):
   - 10: Sounds human, no clichés
   - 5: Few AI patterns detected
   - 0: Full of "As a...", "Imagine...", etc.

7. **SEO Optimization** (0-10 points):
   - 10: Keywords integrated naturally, good meta potential
   - 5: Some SEO elements
   - 0: No SEO consideration

Return JSON:
{{
  "specific_examples": <score>,
  "real_data": <score>,
  "personal_voice": <score>,
  "actionable_content": <score>,
  "proper_structure": <score>,
  "no_ai_patterns": <score>,
  "seo_optimization": <score>,
  "total": <sum>,
  "feedback": ["<specific improvement 1>", "<specific improvement 2>", ...]
}}

Be tough. Most AI content deserves 60-75. Only exceptional content gets 85+."""

    try:
        result = call_llm(prompt, model=ANALYSIS_MODEL)
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        
        if json_match:
            data = json.loads(json_match.group())
            score = QualityScore(**data)
            
            logger.info(f"✓ Quality score: {score.total}/100")
            if score.total < MIN_QUALITY_SCORE:
                logger.warning(f"⚠️  Below minimum ({MIN_QUALITY_SCORE})")
                for feedback in score.feedback:
                    logger.warning(f"  - {feedback}")
            elif score.total >= TARGET_QUALITY_SCORE:
                logger.info(f"✅ Excellent quality (>= {TARGET_QUALITY_SCORE})")
            else:
                logger.info(f"⚠️  Acceptable quality ({MIN_QUALITY_SCORE}-{TARGET_QUALITY_SCORE})")
            
            return score
        else:
            raise ValueError("No JSON in scoring response")
    
    except Exception as e:
        logger.error(f"Scoring failed: {e}")
        # Return minimum passing score
        return QualityScore(
            specific_examples=10,
            real_data=8,
            personal_voice=10,
            actionable_content=12,
            proper_structure=8,
            no_ai_patterns=8,
            seo_optimization=7,
            total=70,
            feedback=["Scoring failed, manual review recommended"]
        )

# ============================================================================
# PHASE 4: REGENERATION LOGIC
# ============================================================================

def generate_with_quality_check(source_item: Dict, seo_research: SEOResearch) -> GeneratedContent:
    """
    Generate content with automatic regeneration if quality is too low
    """
    logger.info("🎯 Starting content generation with quality checks...")
    
    for attempt in range(MAX_REGENERATION_ATTEMPTS + 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Generation Attempt {attempt + 1}/{MAX_REGENERATION_ATTEMPTS + 1}")
        logger.info(f"{'='*60}\n")
        
        # Generate content
        content, word_count = generate_content(source_item, seo_research)
        
        # Score quality
        quality_score = score_content_quality(
            content,
            seo_research.suggested_title,
            seo_research
        )
        
        # Check if acceptable
        if quality_score.total >= MIN_QUALITY_SCORE:
            logger.info(f"✅ Content accepted (score: {quality_score.total})")
            
            return GeneratedContent(
                html_content=content,
                title=seo_research.suggested_title,
                excerpt=seo_research.suggested_meta_description,
                quality_score=quality_score,
                seo_research=seo_research,
                word_count=word_count,
                read_time=max(1, round(word_count / 200)),
                internal_links_added=len([l for l in seo_research.internal_link_opportunities if l])
            )
        
        # If not acceptable and we have attempts left
        if attempt < MAX_REGENERATION_ATTEMPTS:
            logger.warning(f"⚠️  Quality too low ({quality_score.total}). Regenerating...")
            logger.info("Feedback for improvement:")
            for feedback in quality_score.feedback:
                logger.info(f"  • {feedback}")
            time.sleep(2)  # Brief pause before retry
        else:
            logger.warning(f"⚠️  Max attempts reached. Publishing with score {quality_score.total}")
            
            return GeneratedContent(
                html_content=content,
                title=seo_research.suggested_title,
                excerpt=seo_research.suggested_meta_description,
                quality_score=quality_score,
                seo_research=seo_research,
                word_count=word_count,
                read_time=max(1, round(word_count / 200)),
                internal_links_added=len([l for l in seo_research.internal_link_opportunities if l])
            )
    
    raise Exception("Content generation failed")

# ============================================================================
# PHASE 5: POST-GENERATION (Publishing)
# ============================================================================

def create_blog_post(generated: GeneratedContent, source_item: Dict) -> str:
    """Create HTML file from generated content"""
    logger.info("📝 Phase 5: Creating blog post file...")
    
    # Read template
    with open(TEMPLATE, 'r') as f:
        template = f.read()
    
    # Generate slug
    slug = re.sub(r'[^\w\s-]', '', generated.title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)[:80]
    date_str = datetime.now().strftime('%Y-%m-%d')
    post_slug = f"{date_str}-{slug}"
    
    # Prepare metadata
    now = datetime.now()
    published_iso = now.isoformat()
    
    # Fill template
    html = template.replace('{{TITLE}}', generated.title)
    html = html.replace('{{EXCERPT}}', generated.excerpt)
    html = html.replace('{{KEYWORDS}}', generated.seo_research.primary_keyword + ', ' + ', '.join(generated.seo_research.secondary_keywords[:3]))
    html = html.replace('{{URL}}', f"https://clawtv13.github.io/ai-automation-blog/posts/{post_slug}.html")
    html = html.replace('{{DATE}}', now.strftime('%B %d, %Y'))
    html = html.replace('{{READ_TIME}}', str(generated.read_time))
    html = html.replace('{{CONTENT}}', generated.html_content)
    html = html.replace('{{PUBLISHED_ISO}}', published_iso)
    html = html.replace('{{MODIFIED_ISO}}', published_iso)
    html = html.replace('{{IMAGE_URL}}', f"https://clawtv13.github.io/ai-automation-blog/images/og-default.png")
    html = html.replace('{{AUTHOR}}', AUTHOR_NAME)
    
    # Save post
    post_file = POSTS_DIR / f"{post_slug}.html"
    with open(post_file, 'w') as f:
        f.write(html)
    
    logger.info(f"✓ Post saved: {post_file.name}")
    
    # Update index
    update_posts_index(post_slug, generated)
    
    # Save to state
    published = load_json(STATE_FILE, [])
    published.append({
        'slug': post_slug,
        'title': generated.title,
        'url': f"/posts/{post_slug}.html",
        'source_id': source_item.get('id'),
        'quality_score': generated.quality_score.total,
        'word_count': generated.word_count,
        'published_at': published_iso
    })
    save_json(STATE_FILE, published)
    
    # Save fingerprint
    save_fingerprint(generated.title, generated.excerpt)
    
    logger.info(f"✅ Post published: {post_slug}")
    logger.info(f"   Quality: {generated.quality_score.total}/100")
    logger.info(f"   Words: {generated.word_count}")
    logger.info(f"   Read time: {generated.read_time} min")
    
    return post_slug

def update_posts_index(post_slug: str, generated: GeneratedContent):
    """Update posts/index.json"""
    index_file = POSTS_DIR / "index.json"
    posts = load_json(index_file, [])
    
    posts.insert(0, {
        'title': generated.title,
        'url': f"/posts/{post_slug}.html",
        'excerpt': generated.excerpt,
        'date': datetime.now().strftime('%B %d, %Y'),
        'readTime': generated.read_time,
        'qualityScore': generated.quality_score.total
    })
    
    # Keep last 50
    posts = posts[:50]
    save_json(index_file, posts)

# ============================================================================
# CONTENT SELECTION
# ============================================================================

def get_unpublished_content() -> List[Dict]:
    """Get high-quality unpublished items from newsletter DB"""
    if not NEWSLETTER_DB.exists():
        logger.error("Newsletter database not found")
        return []
    
    try:
        conn = sqlite3.connect(NEWSLETTER_DB)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, title, url, summary, source, total_score
            FROM content_items
            WHERE total_score >= ?
            AND featured_in_edition IS NULL
            ORDER BY total_score DESC, created_at DESC
            LIMIT 30
        ''', (MIN_NEWSLETTER_SCORE,))
        
        items = []
        for row in c.fetchall():
            item = {
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'summary': row[3],
                'source': row[4],
                'score': row[5]
            }
            
            # Skip duplicates
            if not is_duplicate(item['title'], item['summary']):
                items.append(item)
        
        conn.close()
        
        logger.info(f"📚 Found {len(items)} unpublished items (score >= {MIN_NEWSLETTER_SCORE})")
        return items
    
    except Exception as e:
        logger.error(f"Database error: {e}")
        return []

# ============================================================================
# DEPLOYMENT
# ============================================================================

def deploy_to_github() -> bool:
    """Deploy to GitHub Pages"""
    logger.info("🚀 Deploying to GitHub...")
    
    os.chdir(BLOG_DIR)
    
    try:
        # Check git status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            logger.info("✓ No changes to deploy")
            return True
        
        # Stage changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        commit_msg = f"Master Agent V3: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, timeout=60)
        
        logger.info("✅ Deployed to GitHub Pages")
        return True
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        return False

# ============================================================================
# NOTIFICATIONS
# ============================================================================

def send_notification(post_slug: str, generated: GeneratedContent, source_item: Dict):
    """Send Telegram notification"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    message = f"""🤖 **Master Content Agent V3**

✅ **New Post Published**

📝 {generated.title}
🔗 https://clawtv13.github.io/ai-automation-blog/posts/{post_slug}.html

📊 **Quality Metrics:**
• Score: {generated.quality_score.total}/100
• Words: {generated.word_count}
• Read time: {generated.read_time} min
• Internal links: {generated.internal_links_added}

🎯 **SEO:**
• Primary keyword: {generated.seo_research.primary_keyword}
• Search intent: {generated.seo_research.search_intent}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"""

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
    except:
        pass

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Master Content Agent Main Workflow"""
    logger.info("="*70)
    logger.info("🚀 MASTER CONTENT AGENT V3.0 - SEO-First Unified Generation")
    logger.info("="*70)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    try:
        # 1. Get unpublished content
        items = get_unpublished_content()
        
        if not items:
            logger.info("✓ No content to publish")
            return
        
        # 2. Select best item
        item = items[0]
        logger.info(f"\n📌 Selected: {item['title'][:60]}...")
        logger.info(f"   Score: {item['score']} | Source: {item['source']}\n")
        
        # 3. Conduct SEO research
        seo_research = conduct_seo_research(item)
        
        # 4. Generate content with quality checks (includes scoring and regeneration)
        generated = generate_with_quality_check(item, seo_research)
        
        # 5. Publish
        post_slug = create_blog_post(generated, item)
        
        # 6. Deploy
        deployed = deploy_to_github()
        
        # 7. Notify
        if deployed:
            send_notification(post_slug, generated, item)
        
        logger.info("\n" + "="*70)
        logger.info("✅ MASTER CONTENT AGENT COMPLETE")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"\n❌ FATAL ERROR: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
