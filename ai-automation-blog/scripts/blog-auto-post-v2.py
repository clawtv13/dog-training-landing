#!/usr/bin/env python3
"""
AI Automation Builder - Blog Auto-Posting V2
PRODUCTION-GRADE with retry logic, error recovery, analytics, and monitoring

Improvements:
- Exponential backoff retry logic
- Rate limiting
- State recovery
- Comprehensive logging
- Analytics tracking
- Duplicate detection
- Health checks
- Auto-recovery
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_DIR = WORKSPACE / "blog"
POSTS_DIR = BLOG_DIR / "posts"
TEMPLATE = WORKSPACE / "templates" / "post.html"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"
STATE_DIR = WORKSPACE / ".state"
LOGS_DIR = WORKSPACE / "logs"

# State files
STATE_FILE = STATE_DIR / "published-posts.json"
ANALYTICS_FILE = STATE_DIR / "analytics.json"
ERROR_LOG_FILE = STATE_DIR / "errors.json"
QUEUE_FILE = STATE_DIR / "content-queue.json"
HEALTH_FILE = STATE_DIR / "health-status.json"

# Logs
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / f"blog-auto-post-{datetime.now().strftime('%Y-%m')}.log"

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Tunables
POSTS_PER_DAY = 2
MIN_QUALITY_SCORE = 30
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds
RATE_LIMIT_DELAY = 5  # seconds between API calls
REQUEST_TIMEOUT = 120
MAX_SIMILAR_THRESHOLD = 0.85  # Content similarity threshold

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

class ErrorType(Enum):
    API_FAILURE = "api_failure"
    RATE_LIMIT = "rate_limit"
    GENERATION_FAILED = "generation_failed"
    GIT_FAILURE = "git_failure"
    DATABASE_ERROR = "database_error"
    VALIDATION_ERROR = "validation_error"

@dataclass
class PostMetrics:
    """Track post performance"""
    post_slug: str
    title: str
    published_at: str
    word_count: int
    source_score: int
    views: int = 0
    clicks: int = 0
    engagement_score: float = 0.0
    
@dataclass
class ErrorRecord:
    """Track errors for analysis"""
    timestamp: str
    error_type: str
    message: str
    context: Dict[str, Any]
    recovered: bool = False
    retry_count: int = 0

@dataclass
class HealthStatus:
    """System health snapshot"""
    timestamp: str
    status: str  # healthy, degraded, unhealthy
    posts_published_today: int
    last_success: Optional[str]
    last_error: Optional[str]
    uptime_percentage: float
    avg_generation_time: float

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

class StateManager:
    """Manage all persistent state with atomic writes"""
    
    @staticmethod
    def _atomic_write(file_path: Path, data: Any):
        """Write JSON atomically to prevent corruption"""
        temp_file = file_path.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            temp_file.replace(file_path)
        except Exception as e:
            logger.error(f"Atomic write failed for {file_path}: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise
    
    @staticmethod
    def load_json(file_path: Path, default: Any = None) -> Any:
        """Load JSON with fallback"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Corrupted JSON in {file_path}: {e}")
                # Backup corrupted file
                backup = file_path.with_suffix(f'.corrupted.{int(time.time())}')
                file_path.rename(backup)
                logger.info(f"Backed up corrupted file to {backup}")
        return default if default is not None else []
    
    @staticmethod
    def save_json(file_path: Path, data: Any):
        """Save JSON atomically"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        StateManager._atomic_write(file_path, data)

# ============================================================================
# ERROR TRACKING
# ============================================================================

class ErrorTracker:
    """Track and analyze errors"""
    
    @staticmethod
    def log_error(error_type: ErrorType, message: str, context: Dict[str, Any] = None):
        """Log error with context"""
        error = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            error_type=error_type.value,
            message=message,
            context=context or {}
        )
        
        errors = StateManager.load_json(ERROR_LOG_FILE, [])
        errors.append(asdict(error))
        
        # Keep last 100 errors
        errors = errors[-100:]
        StateManager.save_json(ERROR_LOG_FILE, errors)
        
        logger.error(f"[{error_type.value}] {message}")
    
    @staticmethod
    def mark_recovered(error_index: int):
        """Mark error as recovered"""
        errors = StateManager.load_json(ERROR_LOG_FILE, [])
        if 0 <= error_index < len(errors):
            errors[error_index]['recovered'] = True
            errors[error_index]['recovered_at'] = datetime.now().isoformat()
            StateManager.save_json(ERROR_LOG_FILE, errors)

# ============================================================================
# RETRY LOGIC
# ============================================================================

def retry_with_backoff(func, max_retries=MAX_RETRIES, error_type=ErrorType.API_FAILURE):
    """Execute function with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            result = func()
            if attempt > 0:
                logger.info(f"✅ Succeeded after {attempt} retries")
            return result
        except requests.exceptions.Timeout:
            logger.warning(f"⏱️  Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                delay = RETRY_DELAY_BASE ** (attempt + 1)
                logger.info(f"⏳ Waiting {delay}s before retry...")
                time.sleep(delay)
            else:
                ErrorTracker.log_error(error_type, "Max retries exceeded (timeout)")
                raise
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                logger.warning(f"🚫 Rate limited on attempt {attempt + 1}/{max_retries}")
                retry_after = int(e.response.headers.get('Retry-After', 60))
                logger.info(f"⏳ Waiting {retry_after}s (rate limit)...")
                time.sleep(retry_after)
            elif 500 <= e.response.status_code < 600:  # Server error
                logger.warning(f"🔥 Server error {e.response.status_code} on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    delay = RETRY_DELAY_BASE ** (attempt + 1)
                    time.sleep(delay)
                else:
                    ErrorTracker.log_error(error_type, f"Server error: {e}")
                    raise
            else:
                ErrorTracker.log_error(error_type, f"HTTP error: {e}")
                raise
        except Exception as e:
            logger.error(f"❌ Unexpected error on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                delay = RETRY_DELAY_BASE ** (attempt + 1)
                time.sleep(delay)
            else:
                ErrorTracker.log_error(error_type, str(e), {'exception_type': type(e).__name__})
                raise
    
    raise Exception(f"Failed after {max_retries} attempts")

# ============================================================================
# CONTENT DEDUPLICATION
# ============================================================================

def content_fingerprint(text: str) -> str:
    """Generate fingerprint for duplicate detection"""
    # Normalize: lowercase, remove punctuation, split into words
    words = ''.join(c.lower() if c.isalnum() or c.isspace() else ' ' for c in text).split()
    # Use first 100 words for fingerprint
    normalized = ' '.join(sorted(set(words[:100])))
    return hashlib.md5(normalized.encode()).hexdigest()

def is_duplicate_content(title: str, summary: str) -> bool:
    """Check if content is too similar to existing posts"""
    fingerprint = content_fingerprint(title + " " + summary)
    
    published = StateManager.load_json(STATE_FILE, [])
    
    for post in published:
        if 'fingerprint' in post:
            existing_fp = post['fingerprint']
            # Simple duplicate check - exact match
            if fingerprint == existing_fp:
                logger.warning(f"⚠️  Duplicate detected: {title[:50]}...")
                return True
    
    return False

# ============================================================================
# PUBLISHED POSTS MANAGEMENT
# ============================================================================

def load_published_posts() -> List[Dict]:
    """Load list of published posts"""
    return StateManager.load_json(STATE_FILE, [])

def save_published_post(post_data: Dict):
    """Save published post to state"""
    published = load_published_posts()
    
    post_data['published_at'] = datetime.now().isoformat()
    post_data['fingerprint'] = content_fingerprint(
        post_data.get('title', '') + " " + post_data.get('excerpt', '')
    )
    
    published.append(post_data)
    StateManager.save_json(STATE_FILE, published)
    
    logger.info(f"💾 Saved to published state: {post_data.get('title', 'Unknown')[:50]}")

# ============================================================================
# ANALYTICS TRACKING
# ============================================================================

class AnalyticsTracker:
    """Track performance metrics"""
    
    @staticmethod
    def log_post_published(post_slug: str, title: str, word_count: int, source_score: int):
        """Log new post metrics"""
        analytics = StateManager.load_json(ANALYTICS_FILE, {'posts': [], 'summary': {}})
        
        metric = PostMetrics(
            post_slug=post_slug,
            title=title,
            published_at=datetime.now().isoformat(),
            word_count=word_count,
            source_score=source_score
        )
        
        analytics['posts'].append(asdict(metric))
        
        # Update summary
        analytics['summary'] = {
            'total_posts': len(analytics['posts']),
            'avg_word_count': sum(p['word_count'] for p in analytics['posts']) / len(analytics['posts']),
            'last_updated': datetime.now().isoformat()
        }
        
        StateManager.save_json(ANALYTICS_FILE, analytics)
        logger.info(f"📊 Analytics updated: {post_slug}")
    
    @staticmethod
    def get_best_performing_posts(limit: int = 10) -> List[Dict]:
        """Get top performing posts by engagement score"""
        analytics = StateManager.load_json(ANALYTICS_FILE, {'posts': []})
        posts = analytics.get('posts', [])
        
        # Sort by engagement score (would be updated by external analytics)
        sorted_posts = sorted(posts, key=lambda p: p.get('engagement_score', 0), reverse=True)
        return sorted_posts[:limit]
    
    @staticmethod
    def get_posts_today() -> int:
        """Count posts published today"""
        analytics = StateManager.load_json(ANALYTICS_FILE, {'posts': []})
        today = datetime.now().date()
        
        count = sum(1 for p in analytics.get('posts', [])
                   if datetime.fromisoformat(p['published_at']).date() == today)
        return count

# ============================================================================
# CONTENT SELECTION
# ============================================================================

def get_unpublished_content() -> List[Dict]:
    """Get high-quality unpublished items from newsletter database"""
    if not NEWSLETTER_DB.exists():
        logger.error("⚠️  Newsletter database not found")
        ErrorTracker.log_error(ErrorType.DATABASE_ERROR, "Newsletter DB missing")
        return []
    
    try:
        conn = sqlite3.connect(NEWSLETTER_DB)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, title, url, summary, source, total_score, created_at
            FROM content_items
            WHERE total_score >= ?
            AND featured_in_edition IS NULL
            ORDER BY total_score DESC, created_at DESC
            LIMIT 30
        ''', (MIN_QUALITY_SCORE,))
        
        items = []
        for row in c.fetchall():
            items.append({
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'summary': row[3],
                'source': row[4],
                'score': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        
        # Filter out already published
        published = load_published_posts()
        published_urls = {p['url'] for p in published}
        
        # Filter out duplicates by URL and content similarity
        unpublished = []
        for item in items:
            if item['url'] in published_urls:
                continue
            if is_duplicate_content(item['title'], item['summary']):
                logger.info(f"⏭️  Skipping duplicate: {item['title'][:50]}")
                continue
            unpublished.append(item)
        
        logger.info(f"📚 Found {len(unpublished)} unique unpublished items")
        return unpublished
        
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        ErrorTracker.log_error(ErrorType.DATABASE_ERROR, str(e))
        return []

# ============================================================================
# BLOG POST GENERATION
# ============================================================================

def generate_blog_post(item: Dict) -> Optional[str]:
    """Generate blog post with retry logic and rate limiting"""
    if not OPENROUTER_API_KEY:
        logger.error("⚠️  OpenRouter API key missing")
        return None
    
    logger.info(f"📝 Generating: {item['title'][:60]}...")
    
    start_time = time.time()
    
    prompt = f"""You are writing for "AI Automation Builder" - a blog for solopreneurs learning AI automation.

Write a detailed, practical blog post based on this source:

Title: {item['title']}
URL: {item['url']}
Summary: {item['summary']}
Source: {item['source']}

Requirements:
- 800-1200 words
- Practical and actionable (not just news reporting)
- Include specific use cases for solopreneurs
- Add "How to use this" section if it's a tool
- Add "Why this matters" section for news
- Conversational but professional tone
- Include external link to source
- SEO optimized (keywords naturally integrated)

Format as clean HTML (no <html> or <body> tags, just content):
- Use <h2> for main sections
- Use <h3> for subsections
- Use <p> for paragraphs
- Use <ul> and <ol> for lists
- Use <strong> and <em> for emphasis
- Use <code> for technical terms
- Use <a href="..."> for links

Start with a compelling intro paragraph, then break into sections.

Return ONLY the HTML content (no markdown, no code blocks, no explanations)."""

    def make_api_call():
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        response.raise_for_status()
        return response.json()
    
    try:
        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)
        
        # API call with retry
        data = retry_with_backoff(make_api_call, error_type=ErrorType.API_FAILURE)
        
        content = data['choices'][0]['message']['content']
        content = content.replace('```html', '').replace('```', '').strip()
        
        generation_time = time.time() - start_time
        logger.info(f"✅ Generated in {generation_time:.1f}s")
        
        # Validate content
        if len(content) < 500:
            logger.warning("⚠️  Generated content too short")
            ErrorTracker.log_error(ErrorType.VALIDATION_ERROR, "Content too short", {'length': len(content)})
            return None
        
        return content
        
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}")
        ErrorTracker.log_error(ErrorType.GENERATION_FAILED, str(e), {'item_id': item.get('id')})
        return None

# ============================================================================
# POST PUBLISHING
# ============================================================================

def create_blog_post(item: Dict, content: str) -> Optional[str]:
    """Create blog post file and update index"""
    try:
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate slug
        slug = item['title'].lower()
        slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
        slug = '-'.join(slug.split())[:80]
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        post_slug = f"{date_str}-{slug}"
        post_file = POSTS_DIR / f"{post_slug}.html"
        
        # Read template
        with open(TEMPLATE, 'r') as f:
            template = f.read()
        
        # Calculate metrics
        word_count = len(content.split())
        read_time = max(1, round(word_count / 200))
        
        # Generate excerpt
        excerpt = item['summary'][:200] + "..."
        
        # Generate keywords
        keywords = f"AI automation, {', '.join(item['title'].split()[:5])}, solopreneur tools"
        
        # Fill template
        html = template.replace('{{TITLE}}', item['title'])
        html = html.replace('{{EXCERPT}}', excerpt)
        html = html.replace('{{KEYWORDS}}', keywords)
        html = html.replace('{{URL}}', f"https://aiautomationbuilder.com/posts/{post_slug}.html")
        html = html.replace('{{DATE}}', datetime.now().strftime('%B %d, %Y'))
        html = html.replace('{{READ_TIME}}', str(read_time))
        html = html.replace('{{CONTENT}}', content)
        
        # Save post
        with open(post_file, 'w') as f:
            f.write(html)
        
        logger.info(f"✅ Created: {post_file.name}")
        
        # Update index
        update_posts_index(post_slug, item, excerpt, read_time)
        
        # Track analytics
        AnalyticsTracker.log_post_published(
            post_slug=post_slug,
            title=item['title'],
            word_count=word_count,
            source_score=item['score']
        )
        
        # Mark as published
        save_published_post({
            'url': f"/posts/{post_slug}.html",
            'title': item['title'],
            'source_id': item['id'],
            'excerpt': excerpt,
            'word_count': word_count
        })
        
        # Generate AI-optimized versions (.txt and .md)
        try:
            logger.info("🤖 Generating AI-optimized versions...")
            import subprocess
            result = subprocess.run(
                ['python3', 'scripts/generate-ai-versions.py'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(BLOG_DIR.parent)
            )
            if result.returncode == 0:
                logger.info("✅ AI versions generated (.txt + .md)")
                
                # Update sitemap to include new formats
                try:
                    sitemap_result = subprocess.run(
                        ['python3', 'scripts/update-sitemap.py'],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=str(BLOG_DIR.parent)
                    )
                    if sitemap_result.returncode == 0:
                        logger.info("✅ Sitemap updated with AI versions")
                except Exception as se:
                    logger.warning(f"⚠️  Sitemap update failed: {se}")
            else:
                logger.warning(f"⚠️  AI version generation failed: {result.stderr[:200]}")
        except Exception as e:
            logger.warning(f"⚠️  Could not generate AI versions: {e}")
        
        return post_slug
        
    except Exception as e:
        logger.error(f"❌ Post creation failed: {e}")
        ErrorTracker.log_error(ErrorType.VALIDATION_ERROR, f"Post creation failed: {e}")
        return None

def update_posts_index(post_slug: str, item: Dict, excerpt: str, read_time: int):
    """Update posts/index.json"""
    index_file = BLOG_DIR / "posts" / "index.json"
    
    posts = StateManager.load_json(index_file, [])
    
    posts.insert(0, {
        'title': item['title'],
        'url': f"/posts/{post_slug}.html",
        'excerpt': excerpt,
        'date': datetime.now().strftime('%B %d, %Y'),
        'readTime': read_time
    })
    
    # Keep last 50 posts in index
    posts = posts[:50]
    
    StateManager.save_json(index_file, posts)

# ============================================================================
# GIT DEPLOYMENT
# ============================================================================

def deploy_to_github() -> bool:
    """Deploy to GitHub with error handling"""
    os.chdir(BLOG_DIR)
    
    def run_git_command(cmd: List[str], check=True):
        """Run git command with retry"""
        def execute():
            result = subprocess.run(cmd, capture_output=True, text=True, check=check, timeout=60)
            return result
        return retry_with_backoff(execute, error_type=ErrorType.GIT_FAILURE)
    
    try:
        # Check if git repo exists
        if not (BLOG_DIR / ".git").exists():
            logger.warning("🔧 Git repo not initialized")
            return False
        
        # Stage changes
        run_git_command(["git", "add", "."])
        
        # Commit
        commit_msg = f"Auto-post: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = run_git_command(["git", "commit", "-m", commit_msg], check=False)
        
        if "nothing to commit" in result.stdout:
            logger.info("✓ No changes to deploy")
            return True
        
        # Push with retry
        run_git_command(["git", "push", "origin", "main"])
        
        logger.info("✅ Deployed to GitHub Pages")
        return True
        
    except Exception as e:
        logger.error(f"❌ Git deployment failed: {e}")
        ErrorTracker.log_error(ErrorType.GIT_FAILURE, str(e))
        return False

# ============================================================================
# HEALTH MONITORING
# ============================================================================

def update_health_status(success: bool, posts_created: int):
    """Update system health metrics"""
    health = StateManager.load_json(HEALTH_FILE, {
        'total_runs': 0,
        'successful_runs': 0,
        'failed_runs': 0,
        'last_success': None,
        'last_error': None
    })
    
    health['total_runs'] = health.get('total_runs', 0) + 1
    health['last_run'] = datetime.now().isoformat()
    
    if success:
        health['successful_runs'] = health.get('successful_runs', 0) + 1
        health['last_success'] = datetime.now().isoformat()
    else:
        health['failed_runs'] = health.get('failed_runs', 0) + 1
        health['last_error'] = datetime.now().isoformat()
    
    health['uptime_percentage'] = (health['successful_runs'] / health['total_runs']) * 100
    health['posts_today'] = AnalyticsTracker.get_posts_today()
    
    StateManager.save_json(HEALTH_FILE, health)

# ============================================================================
# NOTIFICATIONS
# ============================================================================

def send_telegram_notification(posts_created: List[Dict], errors: List[str] = None):
    """Send notification with status"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    if posts_created:
        message = f"""🤖 **AI Automation Blog - Auto-Post**

✅ Published {len(posts_created)} post(s):

"""
        for post in posts_created:
            message += f"• {post['title']}\n"
    else:
        message = "⚠️ **AI Automation Blog - No Posts Created**\n\n"
    
    if errors:
        message += f"\n⚠️ Errors encountered:\n"
        for err in errors[:3]:
            message += f"• {err}\n"
    
    health = StateManager.load_json(HEALTH_FILE, {})
    message += f"\n📊 Health: {health.get('uptime_percentage', 0):.1f}% uptime"
    message += f"\n📝 Posts today: {health.get('posts_today', 0)}"
    message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main workflow with error recovery"""
    logger.info("=" * 60)
    logger.info("AI AUTOMATION BUILDER - BLOG AUTO-POSTING V2")
    logger.info(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 60)
    
    posts_created = []
    errors_encountered = []
    
    try:
        # Get unpublished content
        logger.info("🔍 Fetching unpublished content...")
        items = get_unpublished_content()
        
        if not items:
            logger.info("✓ No new content to publish")
            update_health_status(success=True, posts_created=0)
            return
        
        logger.info(f"📊 Found {len(items)} unpublished items")
        logger.info(f"🎯 Publishing top {POSTS_PER_DAY} today")
        
        # Select best items
        selected = items[:POSTS_PER_DAY]
        
        for item in selected:
            logger.info(f"\n📝 Processing: {item['title'][:60]}...")
            logger.info(f"   Score: {item['score']} | Source: {item['source']}")
            
            try:
                # Generate post
                content = generate_blog_post(item)
                
                if not content:
                    logger.warning("✗ Generation failed, skipping")
                    errors_encountered.append(f"Generation failed: {item['title'][:40]}")
                    continue
                
                # Create HTML file
                post_slug = create_blog_post(item, content)
                
                if not post_slug:
                    logger.warning("✗ Post creation failed, skipping")
                    errors_encountered.append(f"Creation failed: {item['title'][:40]}")
                    continue
                
                posts_created.append({
                    'title': item['title'],
                    'slug': post_slug,
                    'score': item['score']
                })
                
                logger.info(f"✅ Published: {post_slug}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process item: {e}")
                errors_encountered.append(f"Error: {item['title'][:40]}")
                continue
        
        # Deploy if any posts created
        if posts_created:
            logger.info(f"\n✅ Created {len(posts_created)} posts")
            logger.info("🚀 Deploying to GitHub...")
            
            deployed = deploy_to_github()

            
            # Run post-deploy QA tests
            if deployed:
                logger.info("🧪 Running post-deploy QA tests...")
                try:
                    import subprocess
                    qa_result = subprocess.run(
                        ['bash', 'scripts/post-deploy-qa.sh'],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    if qa_result.returncode == 0:
                        logger.info("✅ All QA tests passed")
                    else:
                        logger.warning("⚠️  QA found issues (auto-fix attempted)")
                except Exception as e:
                    logger.error(f"QA test error: {e}")
            
            if deployed:
                send_telegram_notification(posts_created, errors_encountered if errors_encountered else None)
                logger.info("✅ AUTOMATION COMPLETE")
                update_health_status(success=True, posts_created=len(posts_created))
            else:
                logger.error("⚠️  Posts created but deployment failed")
                send_telegram_notification(posts_created, ["Deployment failed"])
                update_health_status(success=False, posts_created=len(posts_created))
        else:
            logger.info("✓ No posts created this run")
            update_health_status(success=True, posts_created=0)
            
    except Exception as e:
        logger.error(f"❌ FATAL ERROR: {e}")
        ErrorTracker.log_error(ErrorType.API_FAILURE, f"Fatal error: {e}")
        update_health_status(success=False, posts_created=0)
        send_telegram_notification([], [f"Fatal error: {str(e)[:100]}"])
        sys.exit(1)

if __name__ == "__main__":
    main()
