#!/usr/bin/env python3
"""
AI Automation Blog - Prompt Optimizer
Weekly script to analyze best posts and evolve prompts through A/B testing

Algorithm:
1. Query top performers (last 30 days)
2. Extract patterns (word count, structure, tone)
3. Generate prompt candidates via OpenRouter
4. Setup A/B test configuration
5. Evaluate results after 7 days
"""

import os
import sys
import json
import sqlite3
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import Counter
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_DIR = WORKSPACE / "blog" / "md"
PROMPTS_DIR = WORKSPACE / "prompts"
CANDIDATES_DIR = PROMPTS_DIR / "candidates"
DB_PATH = WORKSPACE / "scripts" / "blog.db"
LOGS_DIR = WORKSPACE / "logs"

# Ensure directories exist
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Files
CURRENT_PROMPT_FILE = PROMPTS_DIR / "blog-generation.txt"
AB_TEST_FILE = PROMPTS_DIR / "ab-test.json"
LOG_FILE = LOGS_DIR / f"prompt-optimizer-{datetime.now().strftime('%Y-%m')}.log"

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LLM_MODEL = "anthropic/claude-3.7-sonnet"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Analysis parameters
TOP_N_POSTS = 10
MIN_POSTS_FOR_ANALYSIS = 3
QUALITY_IMPROVEMENT_THRESHOLD = 5
AB_TEST_DURATION_DAYS = 7
NUM_CANDIDATES = 5

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class PostAnalysis:
    """Analyzed post data"""
    slug: str
    title: str
    date: str
    word_count: int
    section_count: int
    intro_phrase: str
    quality_score: float
    technical_markers: int
    casual_markers: int
    
@dataclass
class PatternSummary:
    """Aggregated patterns from top posts"""
    avg_word_count: int
    avg_sections: int
    common_intros: List[str]
    technical_casual_ratio: float
    structure_notes: str
    tone_analysis: str

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize SQLite database for post tracking"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create posts table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            slug TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            word_count INTEGER,
            quality_score REAL DEFAULT 50.0,
            views INTEGER DEFAULT 0,
            created_at TEXT,
            prompt_variant TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")

# ============================================================================
# STEP 1: QUERY TOP PERFORMERS
# ============================================================================

def get_top_posts(days: int = 30) -> List[Dict[str, Any]]:
    """Query top performing posts from last N days"""
    logger.info(f"📊 Querying top {TOP_N_POSTS} posts from last {days} days...")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    c.execute('''
        SELECT slug, title, date, word_count, quality_score, prompt_variant
        FROM posts
        WHERE date >= ?
        ORDER BY quality_score DESC
        LIMIT ?
    ''', (cutoff_date, TOP_N_POSTS))
    
    rows = c.fetchall()
    conn.close()
    
    posts = []
    for row in rows:
        posts.append({
            'slug': row[0],
            'title': row[1],
            'date': row[2],
            'word_count': row[3],
            'quality_score': row[4],
            'prompt_variant': row[5]
        })
    
    # If database is empty, scan markdown files
    if len(posts) < MIN_POSTS_FOR_ANALYSIS:
        logger.warning("⚠️  Not enough posts in database, scanning markdown files...")
        posts = scan_markdown_files()
    
    logger.info(f"✅ Found {len(posts)} posts for analysis")
    return posts

def scan_markdown_files() -> List[Dict[str, Any]]:
    """Fallback: scan markdown files and populate database"""
    posts = []
    
    if not BLOG_DIR.exists():
        logger.error(f"❌ Blog directory not found: {BLOG_DIR}")
        return posts
    
    md_files = sorted(BLOG_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for md_file in md_files[:TOP_N_POSTS]:
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # Extract metadata
            slug = md_file.stem
            title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            date_match = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
            
            title = title_match.group(1).strip() if title_match else slug
            date = date_match.group(1).strip() if date_match else md_file.stat().st_mtime
            
            # Count words (excluding frontmatter)
            body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            word_count = len(body.split())
            
            # Calculate basic quality score (can be refined later)
            quality_score = min(100, 50 + (word_count / 50))  # Base 50, +1 per 50 words
            
            post = {
                'slug': slug,
                'title': title,
                'date': str(date),
                'word_count': word_count,
                'quality_score': quality_score,
                'prompt_variant': 'current'
            }
            
            posts.append(post)
            
            # Insert into database
            c.execute('''
                INSERT OR REPLACE INTO posts (slug, title, date, word_count, quality_score, created_at, prompt_variant)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (slug, title, str(date), word_count, quality_score, datetime.now().isoformat(), 'current'))
            
        except Exception as e:
            logger.error(f"❌ Error processing {md_file}: {e}")
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Scanned {len(posts)} markdown files")
    return posts

# ============================================================================
# STEP 2: EXTRACT PATTERNS
# ============================================================================

def analyze_post(md_file: Path) -> Optional[PostAnalysis]:
    """Analyze a single markdown file for patterns"""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Extract metadata
        slug = md_file.stem
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        date_match = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
        
        title = title_match.group(1).strip() if title_match else slug
        date = date_match.group(1).strip() if date_match else ""
        
        # Remove frontmatter
        body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Word count
        words = body.split()
        word_count = len(words)
        
        # Section count (headers)
        sections = re.findall(r'^#{1,3}\s+', body, re.MULTILINE)
        section_count = len(sections)
        
        # Extract intro (first 100 words after title)
        intro_text = ' '.join(words[:100])
        intro_phrase = intro_text[:200] if len(intro_text) > 200 else intro_text
        
        # Tone analysis (simple keyword counting)
        technical_keywords = ['algorithm', 'implementation', 'architecture', 'API', 'framework', 'optimization', 'performance', 'database', 'infrastructure']
        casual_keywords = ['you', 'your', 'we', 'us', 'our', "I'm", "you're", 'simply', 'just', 'really', 'actually']
        
        body_lower = body.lower()
        technical_count = sum(body_lower.count(kw.lower()) for kw in technical_keywords)
        casual_count = sum(body_lower.count(kw.lower()) for kw in casual_keywords)
        
        # Quality score (basic calculation)
        quality_score = min(100, 50 + (word_count / 50))
        
        return PostAnalysis(
            slug=slug,
            title=title,
            date=date,
            word_count=word_count,
            section_count=section_count,
            intro_phrase=intro_phrase,
            quality_score=quality_score,
            technical_markers=technical_count,
            casual_markers=casual_count
        )
        
    except Exception as e:
        logger.error(f"❌ Error analyzing {md_file}: {e}")
        return None

def extract_patterns(posts: List[Dict[str, Any]]) -> PatternSummary:
    """Extract common patterns from top posts"""
    logger.info("🔍 Extracting patterns from top posts...")
    
    analyses = []
    
    for post in posts:
        md_file = BLOG_DIR / f"{post['slug']}.md"
        if md_file.exists():
            analysis = analyze_post(md_file)
            if analysis:
                analyses.append(analysis)
    
    if not analyses:
        logger.error("❌ No posts available for analysis")
        return None
    
    # Calculate averages
    avg_word_count = int(sum(a.word_count for a in analyses) / len(analyses))
    avg_sections = int(sum(a.section_count for a in analyses) / len(analyses))
    
    # Find common intro patterns
    intro_words = []
    for a in analyses:
        first_sentence = a.intro_phrase.split('.')[0].strip()
        intro_words.append(first_sentence[:100])
    
    # Technical/casual ratio
    total_technical = sum(a.technical_markers for a in analyses)
    total_casual = sum(a.casual_markers for a in analyses)
    tech_casual_ratio = total_technical / max(total_casual, 1)
    
    # Determine tone
    if tech_casual_ratio > 1.5:
        tone = "technical and formal"
    elif tech_casual_ratio < 0.5:
        tone = "casual and conversational"
    else:
        tone = "balanced technical-casual"
    
    pattern_summary = PatternSummary(
        avg_word_count=avg_word_count,
        avg_sections=avg_sections,
        common_intros=intro_words[:5],
        technical_casual_ratio=tech_casual_ratio,
        structure_notes=f"Average {avg_sections} sections, {avg_word_count} words",
        tone_analysis=tone
    )
    
    logger.info(f"✅ Pattern extraction complete:")
    logger.info(f"   • Avg word count: {avg_word_count}")
    logger.info(f"   • Avg sections: {avg_sections}")
    logger.info(f"   • Tone: {tone}")
    logger.info(f"   • Tech/Casual ratio: {tech_casual_ratio:.2f}")
    
    return pattern_summary

# ============================================================================
# STEP 3: GENERATE PROMPT CANDIDATES
# ============================================================================

def read_current_prompt() -> str:
    """Read current prompt or create default"""
    if CURRENT_PROMPT_FILE.exists():
        return CURRENT_PROMPT_FILE.read_text(encoding='utf-8')
    
    # Create default prompt
    default_prompt = """You are an expert tech blogger writing for solopreneurs interested in AI automation.

Write a comprehensive, engaging blog post that:
- Provides actionable insights and practical advice
- Uses clear examples and real-world scenarios
- Maintains a professional yet accessible tone
- Includes concrete steps or recommendations
- Structures content with clear sections and headers

Focus on helping solopreneurs save time and scale their businesses using AI."""
    
    CURRENT_PROMPT_FILE.write_text(default_prompt, encoding='utf-8')
    logger.info("✅ Created default prompt file")
    return default_prompt

def generate_prompt_candidates(patterns: PatternSummary, current_prompt: str) -> List[str]:
    """Generate improved prompt variations using LLM"""
    logger.info("🤖 Generating prompt candidates via OpenRouter...")
    
    if not OPENROUTER_API_KEY:
        logger.error("❌ OPENROUTER_API_KEY not set")
        return []
    
    analysis_text = f"""
Based on analysis of top-performing blog posts:

- Average word count: {patterns.avg_word_count}
- Average sections: {patterns.avg_sections}
- Tone: {patterns.tone_analysis}
- Technical/Casual ratio: {patterns.technical_casual_ratio:.2f}
- Structure: {patterns.structure_notes}

Sample introductions from best posts:
{chr(10).join(f"  - {intro[:150]}..." for intro in patterns.common_intros[:3])}

Current prompt:
{current_prompt}
"""
    
    prompt = f"""You are a prompt engineering expert. Analyze these patterns from top-performing blog posts and generate {NUM_CANDIDATES} improved prompt variations.

{analysis_text}

Each prompt should:
1. Incorporate successful patterns from the analysis
2. Be clear and specific
3. Maintain the core purpose (helping solopreneurs with AI automation)
4. Optimize for the discovered word count, structure, and tone
5. Be distinctly different from each other

Return ONLY the 5 prompts, separated by "---PROMPT---" markers. No other text."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Split into separate prompts
        candidates = [p.strip() for p in content.split('---PROMPT---') if p.strip()]
        
        # Ensure we have exactly NUM_CANDIDATES
        candidates = candidates[:NUM_CANDIDATES]
        
        logger.info(f"✅ Generated {len(candidates)} prompt candidates")
        return candidates
        
    except Exception as e:
        logger.error(f"❌ Failed to generate prompts: {e}")
        return []

def save_prompt_candidates(candidates: List[str]):
    """Save prompt candidates to files"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    for i, candidate in enumerate(candidates, 1):
        filename = CANDIDATES_DIR / f"v{timestamp}-{i}.txt"
        filename.write_text(candidate, encoding='utf-8')
        logger.info(f"💾 Saved candidate {i}: {filename.name}")

# ============================================================================
# STEP 4: SETUP A/B TEST
# ============================================================================

def setup_ab_test(candidate_file: str):
    """Create A/B test configuration"""
    logger.info("🔬 Setting up A/B test...")
    
    test_config = {
        "test_id": f"test_{datetime.now().strftime('%Y%m%d')}",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=AB_TEST_DURATION_DAYS)).isoformat(),
        "variants": {
            "A": "blog-generation.txt",  # Current prompt
            "B": candidate_file  # Best candidate
        },
        "results": {
            "A": {"posts": 0, "total_quality": 0, "avg_quality": 0},
            "B": {"posts": 0, "total_quality": 0, "avg_quality": 0}
        },
        "status": "active"
    }
    
    with open(AB_TEST_FILE, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    logger.info(f"✅ A/B test configured: {test_config['test_id']}")
    logger.info(f"   Duration: {AB_TEST_DURATION_DAYS} days")
    logger.info(f"   Variant A: {test_config['variants']['A']}")
    logger.info(f"   Variant B: {test_config['variants']['B']}")

# ============================================================================
# STEP 5: EVALUATE A/B TEST
# ============================================================================

def evaluate_ab_test():
    """Evaluate A/B test results and promote winner if significant"""
    logger.info("📈 Evaluating A/B test results...")
    
    if not AB_TEST_FILE.exists():
        logger.warning("⚠️  No active A/B test found")
        return
    
    with open(AB_TEST_FILE, 'r') as f:
        test_config = json.load(f)
    
    if test_config.get('status') != 'active':
        logger.info("ℹ️  A/B test is not active")
        return
    
    # Check if test duration has passed
    end_date = datetime.fromisoformat(test_config['end_date'])
    if datetime.now() < end_date:
        days_left = (end_date - datetime.now()).days
        logger.info(f"⏳ A/B test still running ({days_left} days remaining)")
        return
    
    # Calculate results from database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    start_date = test_config['start_date']
    
    # Get stats for variant A
    c.execute('''
        SELECT COUNT(*), AVG(quality_score)
        FROM posts
        WHERE date >= ? AND prompt_variant = ?
    ''', (start_date, 'A'))
    
    a_count, a_avg = c.fetchone()
    a_avg = a_avg or 0
    
    # Get stats for variant B
    c.execute('''
        SELECT COUNT(*), AVG(quality_score)
        FROM posts
        WHERE date >= ? AND prompt_variant = ?
    ''', (start_date, 'B'))
    
    b_count, b_avg = c.fetchone()
    b_avg = b_avg or 0
    
    conn.close()
    
    # Update results
    test_config['results']['A'] = {'posts': a_count or 0, 'avg_quality': round(a_avg, 2)}
    test_config['results']['B'] = {'posts': b_count or 0, 'avg_quality': round(b_avg, 2)}
    
    logger.info(f"📊 Results:")
    logger.info(f"   Variant A: {a_count} posts, avg quality {a_avg:.2f}")
    logger.info(f"   Variant B: {b_count} posts, avg quality {b_avg:.2f}")
    
    # Determine winner
    if b_avg > a_avg + QUALITY_IMPROVEMENT_THRESHOLD:
        logger.info(f"🏆 Variant B wins! (+{b_avg - a_avg:.2f} points)")
        promote_winner(test_config['variants']['B'])
        test_config['status'] = 'completed'
        test_config['winner'] = 'B'
    elif a_avg > b_avg + QUALITY_IMPROVEMENT_THRESHOLD:
        logger.info(f"🏆 Variant A wins! Current prompt is better")
        test_config['status'] = 'completed'
        test_config['winner'] = 'A'
    else:
        logger.info(f"🤝 No clear winner (difference < {QUALITY_IMPROVEMENT_THRESHOLD} points)")
        test_config['status'] = 'inconclusive'
        test_config['winner'] = None
    
    # Save updated test results
    with open(AB_TEST_FILE, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    logger.info("✅ A/B test evaluation complete")

def promote_winner(candidate_filename: str):
    """Promote winning candidate to production"""
    logger.info(f"🚀 Promoting winner to production...")
    
    candidate_path = CANDIDATES_DIR / candidate_filename
    
    if not candidate_path.exists():
        logger.error(f"❌ Candidate file not found: {candidate_path}")
        return
    
    # Archive current prompt
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    archive_path = PROMPTS_DIR / f"blog-generation-{timestamp}-archived.txt"
    
    if CURRENT_PROMPT_FILE.exists():
        current_content = CURRENT_PROMPT_FILE.read_text(encoding='utf-8')
        archive_path.write_text(current_content, encoding='utf-8')
        logger.info(f"📦 Archived old prompt: {archive_path.name}")
    
    # Promote new prompt
    new_content = candidate_path.read_text(encoding='utf-8')
    CURRENT_PROMPT_FILE.write_text(new_content, encoding='utf-8')
    
    logger.info(f"✅ New prompt promoted to production!")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow"""
    logger.info("=" * 70)
    logger.info("🧠 PROMPT OPTIMIZER - Learning Loop for Blog Generation")
    logger.info("=" * 70)
    
    # Initialize database
    init_database()
    
    # Parse command line argument
    mode = sys.argv[1] if len(sys.argv) > 1 else 'optimize'
    
    if mode == 'evaluate':
        # Evaluate existing A/B test
        evaluate_ab_test()
    
    elif mode == 'optimize':
        # Step 1: Get top posts
        top_posts = get_top_posts(days=30)
        
        if len(top_posts) < MIN_POSTS_FOR_ANALYSIS:
            logger.warning(f"⚠️  Only {len(top_posts)} posts available (need {MIN_POSTS_FOR_ANALYSIS})")
            logger.info("Run this script after generating more posts")
            return
        
        # Step 2: Extract patterns
        patterns = extract_patterns(top_posts)
        
        if not patterns:
            logger.error("❌ Failed to extract patterns")
            return
        
        # Step 3: Generate candidates
        current_prompt = read_current_prompt()
        candidates = generate_prompt_candidates(patterns, current_prompt)
        
        if not candidates:
            logger.error("❌ Failed to generate candidates")
            return
        
        save_prompt_candidates(candidates)
        
        # Step 4: Setup A/B test with best candidate
        best_candidate = CANDIDATES_DIR / sorted(CANDIDATES_DIR.glob("v*.txt"))[-1].name
        setup_ab_test(best_candidate.name)
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ OPTIMIZATION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Generated {len(candidates)} prompt candidates")
        logger.info(f"A/B test configured for {AB_TEST_DURATION_DAYS} days")
        logger.info(f"Run 'python {Path(__file__).name} evaluate' after test period")
        logger.info("")
    
    else:
        logger.error(f"❌ Unknown mode: {mode}")
        logger.info("Usage: python prompt-optimizer.py [optimize|evaluate]")
        sys.exit(1)

if __name__ == "__main__":
    main()
