#!/usr/bin/env python3
"""
Health Check & Self-Healing
Monitors blog automation health and auto-fixes common issues

Features:
- Database connectivity check
- Git repository status
- State file integrity
- Disk space monitoring
- Log file rotation
- Auto-recovery from common failures
"""

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
BLOG_DIR = WORKSPACE / "blog"
STATE_DIR = WORKSPACE / ".state"
LOGS_DIR = WORKSPACE / "logs"
NEWSLETTER_DB = WORKSPACE.parent / "newsletter-ai-automation" / "database" / "newsletter.db"

HEALTH_FILE = STATE_DIR / "health-status.json"
DISK_SPACE_THRESHOLD_MB = 500  # Alert if less than 500MB
LOG_RETENTION_DAYS = 30

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# HEALTH CHECKS
# ============================================================================

class HealthCheck:
    """Health check manager"""
    
    def __init__(self):
        self.checks = []
        self.failures = []
        self.warnings = []
    
    def run_check(self, name: str, check_func):
        """Run a health check"""
        try:
            logger.info(f"🔍 Checking: {name}")
            result = check_func()
            
            if result['status'] == 'pass':
                logger.info(f"   ✅ {result.get('message', 'OK')}")
                self.checks.append({'name': name, 'status': 'pass', 'message': result.get('message')})
            elif result['status'] == 'warning':
                logger.warning(f"   ⚠️  {result.get('message', 'Warning')}")
                self.warnings.append({'name': name, 'message': result.get('message')})
                self.checks.append({'name': name, 'status': 'warning', 'message': result.get('message')})
            else:
                logger.error(f"   ❌ {result.get('message', 'Failed')}")
                self.failures.append({'name': name, 'message': result.get('message')})
                self.checks.append({'name': name, 'status': 'fail', 'message': result.get('message')})
                
        except Exception as e:
            logger.error(f"   ❌ Check failed: {e}")
            self.failures.append({'name': name, 'message': str(e)})
            self.checks.append({'name': name, 'status': 'fail', 'message': str(e)})
    
    def get_overall_status(self):
        """Get overall system health"""
        if self.failures:
            return 'unhealthy'
        elif self.warnings:
            return 'degraded'
        return 'healthy'

# ============================================================================
# CHECK FUNCTIONS
# ============================================================================

def check_database_connectivity():
    """Check newsletter database is accessible"""
    if not NEWSLETTER_DB.exists():
        return {'status': 'fail', 'message': 'Newsletter database not found'}
    
    try:
        conn = sqlite3.connect(NEWSLETTER_DB, timeout=5)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM content_items")
        count = c.fetchone()[0]
        conn.close()
        return {'status': 'pass', 'message': f'Database accessible ({count} items)'}
    except Exception as e:
        return {'status': 'fail', 'message': f'Database error: {e}'}

def check_git_repository():
    """Check git repository status"""
    if not (BLOG_DIR / ".git").exists():
        return {'status': 'warning', 'message': 'Git repository not initialized'}
    
    try:
        os.chdir(BLOG_DIR)
        
        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return {'status': 'fail', 'message': 'Git status check failed'}
        
        uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
        if uncommitted > 10:
            return {'status': 'warning', 'message': f'{uncommitted} uncommitted files'}
        
        return {'status': 'pass', 'message': f'Git OK ({uncommitted} uncommitted)'}
        
    except subprocess.TimeoutExpired:
        return {'status': 'fail', 'message': 'Git command timeout'}
    except Exception as e:
        return {'status': 'fail', 'message': f'Git error: {e}'}

def check_state_files():
    """Check state file integrity"""
    required_files = [
        STATE_DIR / "published-posts.json",
        STATE_DIR / "analytics.json",
        STATE_DIR / "health-status.json"
    ]
    
    missing = []
    corrupted = []
    
    for file_path in required_files:
        if not file_path.exists():
            missing.append(file_path.name)
        else:
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                corrupted.append(file_path.name)
    
    if corrupted:
        return {'status': 'fail', 'message': f'Corrupted files: {", ".join(corrupted)}'}
    
    if missing:
        return {'status': 'warning', 'message': f'Missing files: {", ".join(missing)}'}
    
    return {'status': 'pass', 'message': 'All state files OK'}

def check_disk_space():
    """Check available disk space"""
    try:
        stat = os.statvfs(WORKSPACE)
        available_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
        
        if available_mb < DISK_SPACE_THRESHOLD_MB:
            return {'status': 'warning', 'message': f'Low disk space: {available_mb:.0f}MB'}
        
        return {'status': 'pass', 'message': f'Disk space OK ({available_mb:.0f}MB available)'}
        
    except Exception as e:
        return {'status': 'fail', 'message': f'Disk check failed: {e}'}

def check_api_credentials():
    """Check required API credentials"""
    missing = []
    
    if not os.getenv('OPENROUTER_API_KEY'):
        missing.append('OPENROUTER_API_KEY')
    
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        missing.append('TELEGRAM_BOT_TOKEN')
    
    if not os.getenv('TELEGRAM_CHAT_ID'):
        missing.append('TELEGRAM_CHAT_ID')
    
    if missing:
        return {'status': 'warning', 'message': f'Missing env vars: {", ".join(missing)}'}
    
    return {'status': 'pass', 'message': 'All credentials present'}

def check_recent_activity():
    """Check if system has been active recently"""
    health = {}
    health_file = STATE_DIR / "health-status.json"
    
    if health_file.exists():
        try:
            with open(health_file, 'r') as f:
                health = json.load(f)
        except:
            pass
    
    last_success = health.get('last_success')
    
    if not last_success:
        return {'status': 'warning', 'message': 'No successful runs recorded'}
    
    last_success_dt = datetime.fromisoformat(last_success)
    hours_since = (datetime.now() - last_success_dt).total_seconds() / 3600
    
    if hours_since > 24:
        return {'status': 'warning', 'message': f'Last success {hours_since:.0f}h ago'}
    
    return {'status': 'pass', 'message': f'Last success {hours_since:.1f}h ago'}

# ============================================================================
# AUTO-HEALING
# ============================================================================

def rotate_old_logs():
    """Remove logs older than retention period"""
    if not LOGS_DIR.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
    removed_count = 0
    
    for log_file in LOGS_DIR.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_date.timestamp():
            log_file.unlink()
            removed_count += 1
    
    if removed_count > 0:
        logger.info(f"🧹 Removed {removed_count} old log files")

def fix_missing_state_files():
    """Create missing state files with defaults"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    default_states = {
        'published-posts.json': [],
        'analytics.json': {'posts': [], 'summary': {}},
        'health-status.json': {
            'total_runs': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'uptime_percentage': 100.0
        },
        'errors.json': []
    }
    
    fixed_count = 0
    for filename, default_data in default_states.items():
        file_path = STATE_DIR / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
            logger.info(f"🔧 Created missing state file: {filename}")
            fixed_count += 1
    
    return fixed_count

def repair_corrupted_json(file_path: Path):
    """Attempt to repair corrupted JSON file"""
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True  # Already valid
    except json.JSONDecodeError:
        # Backup corrupted file
        backup = file_path.with_suffix(f'.corrupted.{int(datetime.now().timestamp())}')
        file_path.rename(backup)
        logger.warning(f"🔧 Backed up corrupted file: {file_path.name}")
        
        # Create new empty file
        default_data = [] if 'posts' in file_path.name or 'errors' in file_path.name else {}
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=2)
        
        logger.info(f"🔧 Recreated state file: {file_path.name}")
        return True

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run health checks and auto-healing"""
    logger.info("=" * 60)
    logger.info("HEALTH CHECK & SELF-HEALING")
    logger.info(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 60)
    
    # Auto-healing tasks
    logger.info("\n🔧 Auto-healing tasks...")
    rotate_old_logs()
    fixed_count = fix_missing_state_files()
    
    # Run health checks
    logger.info("\n🏥 Running health checks...")
    checker = HealthCheck()
    
    checker.run_check("Database Connectivity", check_database_connectivity)
    checker.run_check("Git Repository", check_git_repository)
    checker.run_check("State Files", check_state_files)
    checker.run_check("Disk Space", check_disk_space)
    checker.run_check("API Credentials", check_api_credentials)
    checker.run_check("Recent Activity", check_recent_activity)
    
    # Summary
    overall_status = checker.get_overall_status()
    
    logger.info("\n" + "=" * 60)
    logger.info(f"OVERALL STATUS: {overall_status.upper()}")
    
    if checker.failures:
        logger.error(f"❌ {len(checker.failures)} critical issues")
        for failure in checker.failures:
            logger.error(f"   • {failure['name']}: {failure['message']}")
    
    if checker.warnings:
        logger.warning(f"⚠️  {len(checker.warnings)} warnings")
        for warning in checker.warnings:
            logger.warning(f"   • {warning['name']}: {warning['message']}")
    
    if not checker.failures and not checker.warnings:
        logger.info("✅ All checks passed")
    
    logger.info("=" * 60)
    
    # Exit code
    sys.exit(0 if overall_status != 'unhealthy' else 1)

if __name__ == "__main__":
    main()
