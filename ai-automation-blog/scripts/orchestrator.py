#!/usr/bin/env python3
"""
Blog Automation Orchestrator
Master controller that runs health checks, syncs, and posts

Run modes:
- health: Health check only
- sync: Sync newsletter-blog only  
- post: Generate and publish posts
- full: Health + Sync + Post (default)
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
SCRIPTS_DIR = WORKSPACE / "scripts"
STATE_DIR = WORKSPACE / ".state"
LOGS_DIR = WORKSPACE / "logs"

# Scripts
HEALTH_CHECK_SCRIPT = SCRIPTS_DIR / "health-check.py"
SYNC_SCRIPT = SCRIPTS_DIR / "newsletter-blog-sync.py"
POST_SCRIPT = SCRIPTS_DIR / "blog-auto-post-v2.py"

# State
ORCHESTRATOR_STATE = STATE_DIR / "orchestrator-state.json"

# Logging
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / f"orchestrator-{datetime.now().strftime('%Y-%m')}.log"

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
# ORCHESTRATION
# ============================================================================

def run_script(script_path: Path, name: str) -> bool:
    """Run a Python script and return success status"""
    logger.info(f"🚀 Running: {name}")
    logger.info(f"   Script: {script_path.name}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=WORKSPACE
        )
        
        # Log output
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                logger.info(f"   {line}")
        
        if result.returncode == 0:
            logger.info(f"✅ {name} completed successfully")
            return True
        else:
            logger.error(f"❌ {name} failed (exit code {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split('\n'):
                    logger.error(f"   {line}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {name} timed out")
        return False
    except Exception as e:
        logger.error(f"❌ {name} error: {e}")
        return False

def update_orchestrator_state(mode: str, success: bool, steps: dict):
    """Update orchestrator state"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    state = {}
    if ORCHESTRATOR_STATE.exists():
        try:
            with open(ORCHESTRATOR_STATE, 'r') as f:
                state = json.load(f)
        except:
            state = {}
    
    state['last_run'] = datetime.now().isoformat()
    state['last_mode'] = mode
    state['last_success'] = success
    state['steps'] = steps
    state['total_runs'] = state.get('total_runs', 0) + 1
    
    if success:
        state['successful_runs'] = state.get('successful_runs', 0) + 1
    else:
        state['failed_runs'] = state.get('failed_runs', 0) + 1
    
    with open(ORCHESTRATOR_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def orchestrate(mode: str = 'full'):
    """Main orchestration logic"""
    logger.info("=" * 70)
    logger.info("🤖 BLOG AUTOMATION ORCHESTRATOR")
    logger.info(f"Mode: {mode.upper()}")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 70)
    
    steps = {}
    overall_success = True
    
    # Step 1: Health Check
    if mode in ['health', 'full']:
        logger.info("\n" + "=" * 70)
        logger.info("STEP 1: HEALTH CHECK")
        logger.info("=" * 70)
        
        health_success = run_script(HEALTH_CHECK_SCRIPT, "Health Check")
        steps['health_check'] = {'success': health_success, 'timestamp': datetime.now().isoformat()}
        
        if not health_success and mode == 'full':
            logger.warning("⚠️  Health check failed, but continuing...")
            # Don't abort - health check warnings shouldn't stop automation
    
    # Step 2: Newsletter Sync
    if mode in ['sync', 'full']:
        logger.info("\n" + "=" * 70)
        logger.info("STEP 2: NEWSLETTER-BLOG SYNC")
        logger.info("=" * 70)
        
        sync_success = run_script(SYNC_SCRIPT, "Newsletter Sync")
        steps['newsletter_sync'] = {'success': sync_success, 'timestamp': datetime.now().isoformat()}
        
        if not sync_success:
            overall_success = False
            logger.error("❌ Sync failed")
    
    # Step 3: Post Generation
    if mode in ['post', 'full']:
        logger.info("\n" + "=" * 70)
        logger.info("STEP 3: BLOG POST GENERATION")
        logger.info("=" * 70)
        
        post_success = run_script(POST_SCRIPT, "Blog Posting")
        steps['blog_posting'] = {'success': post_success, 'timestamp': datetime.now().isoformat()}
        
        if not post_success:
            overall_success = False
            logger.error("❌ Post generation failed")
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("ORCHESTRATION SUMMARY")
    logger.info("=" * 70)
    
    for step_name, step_data in steps.items():
        status = "✅" if step_data['success'] else "❌"
        logger.info(f"{status} {step_name.replace('_', ' ').title()}: {'Success' if step_data['success'] else 'Failed'}")
    
    if overall_success:
        logger.info("\n✅ ALL STEPS COMPLETED SUCCESSFULLY")
    else:
        logger.error("\n❌ ORCHESTRATION FAILED - SEE ERRORS ABOVE")
    
    logger.info("=" * 70)
    
    # Update state
    update_orchestrator_state(mode, overall_success, steps)
    
    return 0 if overall_success else 1

# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point"""
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    
    valid_modes = ['health', 'sync', 'post', 'full']
    
    if mode not in valid_modes:
        print(f"Usage: {sys.argv[0]} [mode]")
        print(f"Modes: {', '.join(valid_modes)}")
        print(f"\nDefault: full")
        sys.exit(1)
    
    exit_code = orchestrate(mode)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
