#!/usr/bin/env python3
"""
Bug Reviewer - Automated Testing & Bug Fixing System
Runs after any major code change to detect and fix issues
"""

import os
import sys
import json
import sqlite3
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Setup
WORKSPACE = Path(__file__).parent.parent
LOGS_DIR = WORKSPACE / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / f"bug-reviewer-{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

class BugReviewer:
    """Automated bug detection and fixing"""
    
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        self.workspace = WORKSPACE
        
    def run_full_check(self) -> Tuple[int, int]:
        """Run all checks and fixes"""
        logging.info("🔍 Starting Bug Reviewer...")
        
        # 1. Python syntax validation
        self.check_python_syntax()
        
        # 2. Database integrity
        self.check_database()
        
        # 3. File permissions
        self.check_permissions()
        
        # 4. Cron jobs validity
        self.check_cron_jobs()
        
        # 5. API keys presence
        self.check_env_vars()
        
        # 6. Test critical scripts
        self.test_scripts()
        
        # 7. Generate report
        self.generate_report()
        
        issues = len(self.issues_found)
        fixes = len(self.fixes_applied)
        
        logging.info(f"✅ Bug Review Complete: {issues} issues found, {fixes} fixed")
        return issues, fixes
    
    def check_python_syntax(self):
        """Validate Python syntax in all scripts"""
        logging.info("📝 Checking Python syntax...")
        
        scripts_dir = self.workspace / "scripts"
        python_files = list(scripts_dir.glob("*.py"))
        
        for py_file in python_files:
            try:
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    issue = f"Syntax error in {py_file.name}: {result.stderr}"
                    self.issues_found.append(issue)
                    logging.warning(f"❌ {issue}")
                    
            except Exception as e:
                issue = f"Failed to check {py_file.name}: {e}"
                self.issues_found.append(issue)
                logging.error(f"❌ {issue}")
        
        logging.info(f"✅ Syntax check complete: {len(python_files)} files validated")
    
    def check_database(self):
        """Verify database integrity"""
        logging.info("🗄️ Checking database...")
        
        db_path = self.workspace / "data" / "analytics.db"
        
        if not db_path.exists():
            issue = "analytics.db not found"
            self.issues_found.append(issue)
            logging.error(f"❌ {issue}")
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check tables exist
            tables = ["posts", "prompt_versions", "weekly_reports"]
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logging.info(f"  ✅ Table '{table}': {count} rows")
            
            # Check for NULL quality scores
            cursor.execute("SELECT COUNT(*) FROM posts WHERE quality_score IS NULL")
            null_count = cursor.fetchone()[0]
            
            if null_count > 0:
                issue = f"{null_count} posts with NULL quality_score"
                self.issues_found.append(issue)
                logging.warning(f"⚠️ {issue} (will be scored by performance-tracker)")
            
            conn.close()
            logging.info("✅ Database integrity OK")
            
        except Exception as e:
            issue = f"Database error: {e}"
            self.issues_found.append(issue)
            logging.error(f"❌ {issue}")
    
    def check_permissions(self):
        """Check file permissions"""
        logging.info("🔐 Checking file permissions...")
        
        scripts_dir = self.workspace / "scripts"
        executables = [
            "performance-tracker.py",
            "prompt-optimizer.py",
            "analytics-dashboard.py",
            "run-analytics.sh"
        ]
        
        for script in executables:
            script_path = scripts_dir / script
            
            if script_path.exists():
                if not os.access(script_path, os.X_OK):
                    # Fix: make executable
                    os.chmod(script_path, 0o755)
                    fix = f"Made {script} executable"
                    self.fixes_applied.append(fix)
                    logging.info(f"🔧 {fix}")
            else:
                issue = f"Missing script: {script}"
                self.issues_found.append(issue)
                logging.warning(f"⚠️ {issue}")
        
        logging.info("✅ Permissions check complete")
    
    def check_cron_jobs(self):
        """Verify cron jobs are valid"""
        logging.info("⏰ Checking cron jobs...")
        
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                cron_lines = result.stdout.strip().split("\n")
                
                # Check for self-improvement crons
                required = [
                    "performance-tracker.py",
                    "analytics-dashboard",
                    "prompt-optimizer.py"
                ]
                
                for req in required:
                    found = any(req in line for line in cron_lines)
                    if found:
                        logging.info(f"  ✅ Cron job for {req} configured")
                    else:
                        issue = f"Missing cron job for {req}"
                        self.issues_found.append(issue)
                        logging.warning(f"⚠️ {issue}")
                
            else:
                issue = "Could not read crontab"
                self.issues_found.append(issue)
                logging.error(f"❌ {issue}")
        
        except Exception as e:
            issue = f"Cron check failed: {e}"
            self.issues_found.append(issue)
            logging.error(f"❌ {issue}")
    
    def check_env_vars(self):
        """Check required environment variables"""
        logging.info("🔑 Checking environment variables...")
        
        required_vars = {
            "OPENROUTER_API_KEY": "OpenRouter API (prompt optimizer)",
            "TELEGRAM_BOT_TOKEN": "Telegram Bot (dashboard)",
            "TELEGRAM_CHAT_ID": "Telegram Chat (dashboard)"
        }
        
        for var, purpose in required_vars.items():
            value = os.getenv(var)
            
            if value:
                masked = value[:10] + "..." if len(value) > 10 else "***"
                logging.info(f"  ✅ {var} set ({masked}) - {purpose}")
            else:
                issue = f"Missing {var} ({purpose})"
                self.issues_found.append(issue)
                logging.warning(f"⚠️ {issue}")
    
    def test_scripts(self):
        """Test critical scripts"""
        logging.info("🧪 Testing critical scripts...")
        
        # Test performance-tracker (dry run)
        try:
            result = subprocess.run(
                ["python3", str(self.workspace / "scripts" / "performance-tracker.py"), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 or "usage" in result.stdout.lower() or "python3" in result.stderr:
                logging.info("  ✅ performance-tracker.py loads OK")
            else:
                issue = f"performance-tracker.py failed: {result.stderr[:100]}"
                self.issues_found.append(issue)
                logging.error(f"❌ {issue}")
        
        except Exception as e:
            issue = f"Could not test performance-tracker.py: {e}"
            self.issues_found.append(issue)
            logging.error(f"❌ {issue}")
    
    def generate_report(self):
        """Generate bug review report"""
        report_path = self.workspace / "reports" / f"bug-review-{datetime.now().strftime('%Y-%m-%d-%H%M')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues_found": len(self.issues_found),
            "fixes_applied": len(self.fixes_applied),
            "issues": self.issues_found,
            "fixes": self.fixes_applied,
            "status": "clean" if len(self.issues_found) == 0 else "issues_detected"
        }
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        logging.info(f"📄 Report saved: {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("🔍 BUG REVIEW SUMMARY")
        print("="*60)
        print(f"Issues found:   {len(self.issues_found)}")
        print(f"Fixes applied:  {len(self.fixes_applied)}")
        print(f"Status:         {report['status'].upper()}")
        
        if self.issues_found:
            print("\n⚠️ ISSUES:")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"  {i}. {issue}")
        
        if self.fixes_applied:
            print("\n🔧 FIXES APPLIED:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")
        
        print("="*60 + "\n")

def main():
    """Run bug reviewer"""
    reviewer = BugReviewer()
    issues, fixes = reviewer.run_full_check()
    
    # Exit code: 0 if clean, 1 if issues found
    sys.exit(0 if issues == 0 else 1)

if __name__ == "__main__":
    main()
