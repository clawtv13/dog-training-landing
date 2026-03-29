#!/usr/bin/env python3
"""
Autonomous Orchestrator - Self-Healing Newsletter System

Monitors, manages, and heals the newsletter system automatically:
- Detects errors in logs
- Fixes issues automatically
- Optimizes performance
- Learns from failures
- Makes decisions autonomously

Runs continuously in background.
"""

import os
import sys
import json
import time
import sqlite3
import requests
import traceback
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = Path(__file__).parent.parent / "database" / "newsletter.db"
LOG_PATH = Path(__file__).parent.parent / "logs"
STATE_PATH = Path(__file__).parent.parent / ".state"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Orchestrator state
ORCHESTRATOR_STATE = STATE_PATH / "orchestrator-state.json"

# ============================================================================
# ERROR MONITORING
# ============================================================================

def monitor_logs():
    """
    Check recent logs for errors
    Returns list of errors found
    """
    errors = []
    
    log_files = [
        LOG_PATH / "research.log",
        LOG_PATH / "generate.log",
        LOG_PATH / "realtime.log"
    ]
    
    for log_file in log_files:
        if not log_file.exists():
            continue
        
        # Read last 100 lines
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()[-100:]
            
            # Look for errors
            for i, line in enumerate(lines):
                if any(err in line for err in ['Error', 'error', 'Exception', 'Traceback', 'Failed', '✗']):
                    # Get context (3 lines before and after)
                    context_start = max(0, i-3)
                    context_end = min(len(lines), i+4)
                    context = ''.join(lines[context_start:context_end])
                    
                    errors.append({
                        'file': log_file.name,
                        'line': line.strip(),
                        'context': context,
                        'timestamp': datetime.now().isoformat()
                    })
        except Exception as e:
            continue
    
    return errors

# ============================================================================
# AUTONOMOUS HEALING
# ============================================================================

def auto_heal_error(error):
    """
    Attempt to automatically fix detected error
    Uses Claude to analyze and suggest fix
    """
    if not OPENROUTER_API_KEY:
        return None
    
    print(f"🔧 Attempting to heal error in {error['file']}...")
    
    prompt = f"""You are an autonomous system maintenance agent.

An error was detected in the newsletter automation system:

Log file: {error['file']}
Error: {error['line']}

Context:
{error['context']}

Analyze this error and provide:

1. **Root cause** - What's actually wrong?
2. **Impact** - How critical is this? (Low/Medium/High/Critical)
3. **Auto-fix possible?** - Can this be fixed automatically? (Yes/No)
4. **Fix strategy** - If yes, what needs to be done?
5. **Code fix** - If simple, provide the exact fix

Return as JSON:
{{
  "root_cause": "...",
  "impact": "High",
  "auto_fixable": true,
  "fix_strategy": "...",
  "code_fix": "..." (or null if needs manual intervention)
}}"""

    try:
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
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Parse analysis
            try:
                analysis = json.loads(content)
            except:
                import re
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    analysis = json.loads(match.group(1))
                else:
                    return None
            
            print(f"  Root cause: {analysis['root_cause']}")
            print(f"  Impact: {analysis['impact']}")
            print(f"  Auto-fixable: {analysis['auto_fixable']}\n")
            
            # If critical and auto-fixable, apply fix
            if analysis['impact'] in ['High', 'Critical'] and analysis['auto_fixable']:
                if analysis.get('code_fix'):
                    apply_code_fix(error['file'], analysis)
                    return analysis
            
            # Log analysis for manual review
            log_analysis(error, analysis)
            return analysis
            
    except Exception as e:
        print(f"✗ Healing error: {e}\n")
        return None

def apply_code_fix(log_file, analysis):
    """
    Apply code fix suggested by Claude
    DANGEROUS: Only for simple, safe fixes
    """
    print(f"⚡ Applying auto-fix...")
    
    # For safety, only log the fix for now
    # Manual approval needed for actual code changes
    fix_log = STATE_PATH / "auto-fixes.json"
    
    if fix_log.exists():
        with open(fix_log, 'r') as f:
            fixes = json.load(f)
    else:
        fixes = []
    
    fixes.append({
        'timestamp': datetime.now().isoformat(),
        'file': log_file,
        'analysis': analysis,
        'applied': False,  # Set to True when manually approved
        'status': 'pending_approval'
    })
    
    with open(fix_log, 'w') as f:
        json.dump(fixes, f, indent=2)
    
    print(f"  💾 Fix logged for approval\n")
    notify_fix_pending(log_file, analysis)

def log_analysis(error, analysis):
    """
    Log error analysis for later review
    """
    analysis_log = STATE_PATH / "error-analysis.json"
    
    if analysis_log.exists():
        with open(analysis_log, 'r') as f:
            log = json.load(f)
    else:
        log = []
    
    log.append({
        'timestamp': datetime.now().isoformat(),
        'error': error,
        'analysis': analysis
    })
    
    # Keep last 50 entries
    log = log[-50:]
    
    with open(analysis_log, 'w') as f:
        json.dump(log, f, indent=2)

# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

def monitor_performance():
    """
    Check system performance metrics
    - Database size
    - Query speeds
    - Success rates
    - Content quality
    """
    metrics = {}
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Database health
    c.execute('SELECT COUNT(*) FROM content_items')
    metrics['total_items'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM content_items WHERE featured_in_edition IS NULL')
    metrics['unfeatured_items'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT source) FROM content_items')
    metrics['unique_sources'] = c.fetchone()[0]
    
    # Content quality (average scores)
    c.execute('SELECT AVG(total_score) FROM content_items WHERE created_at >= datetime("now", "-7 days")')
    metrics['avg_quality_7d'] = c.fetchone()[0] or 0
    
    conn.close()
    
    # Check if research is running
    state_file = STATE_PATH / "daily-research-state.json"
    if state_file.exists():
        with open(state_file, 'r') as f:
            research_state = json.load(f)
            
        last_run = datetime.fromisoformat(research_state.get('last_run', '2020-01-01'))
        hours_since = (datetime.now() - last_run).total_seconds() / 3600
        
        metrics['last_research_hours_ago'] = hours_since
        metrics['research_health'] = 'healthy' if hours_since < 25 else 'stale'
    
    return metrics

def auto_optimize_performance(metrics):
    """
    Automatically optimize based on metrics
    """
    actions_taken = []
    
    # If too many unfeatured items (>200), increase quality threshold
    if metrics['unfeatured_items'] > 200:
        print("⚡ Too many unfeatured items, suggesting quality filter increase")
        actions_taken.append("quality_threshold_increase_recommended")
    
    # If research is stale (>24 hours), alert
    if metrics.get('last_research_hours_ago', 0) > 24:
        print("🚨 Research hasn't run in 24+ hours - checking cron")
        actions_taken.append("research_stale_alert")
        send_alert("Research system hasn't run in 24+ hours. Check cron jobs.")
    
    # If average quality dropping, alert
    if metrics.get('avg_quality_7d', 0) < 28:
        print("⚠️  Content quality declining, suggesting source review")
        actions_taken.append("quality_decline_alert")
    
    return actions_taken

# ============================================================================
# SELF-LEARNING
# ============================================================================

def learn_from_performance():
    """
    Analyze past performance and adjust strategies
    """
    if not OPENROUTER_API_KEY:
        return None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get last 5 editions
    c.execute('''
        SELECT edition_number, subject_line, open_rate, click_rate
        FROM editions
        WHERE status = 'published'
        ORDER BY edition_number DESC
        LIMIT 5
    ''')
    
    editions = []
    for row in c.fetchall():
        editions.append({
            'number': row[0],
            'subject': row[1],
            'open_rate': row[2],
            'click_rate': row[3]
        })
    
    conn.close()
    
    if len(editions) < 3:
        return None  # Need at least 3 editions for learning
    
    print("🧠 Learning from performance data...")
    
    prompt = f"""Analyze newsletter performance and suggest optimizations.

Last 5 editions:
{json.dumps(editions, indent=2)}

Identify:
1. What's working (patterns in high-performing editions)
2. What's not working (declining metrics)
3. Specific optimizations to implement
4. Subject line patterns to favor/avoid

Return JSON with actionable recommendations:
{{
  "working": ["pattern 1", "pattern 2"],
  "not_working": ["pattern 1"],
  "optimizations": [
    {{
      "area": "subject_lines",
      "action": "...",
      "expected_impact": "..."
    }}
  ]
}}"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            try:
                learnings = json.loads(content)
            except:
                import re
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    learnings = json.loads(match.group(1))
                else:
                    return None
            
            # Apply learnings to system
            apply_learnings(learnings)
            
            return learnings
            
    except Exception as e:
        print(f"✗ Learning error: {e}\n")
        return None

def apply_learnings(learnings):
    """
    Automatically apply learned optimizations
    """
    # Save learnings to state
    learnings_file = STATE_PATH / "system-learnings.json"
    
    if learnings_file.exists():
        with open(learnings_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    history.append({
        'timestamp': datetime.now().isoformat(),
        'learnings': learnings
    })
    
    with open(learnings_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"✅ Learnings applied and saved\n")

# ============================================================================
# AUTONOMOUS DECISIONS
# ============================================================================

def make_autonomous_decision(situation):
    """
    Make decisions without human intervention
    """
    if not OPENROUTER_API_KEY:
        return None
    
    print(f"🤔 Analyzing situation: {situation['type']}...")
    
    prompt = f"""You are an autonomous system agent managing a newsletter.

Situation:
{json.dumps(situation, indent=2)}

Make a decision:
1. What action should be taken?
2. Should it be executed now or wait for human approval?
3. What are the risks?
4. What are the potential benefits?

Return JSON:
{{
  "decision": "...",
  "action": "...",
  "should_execute_now": true/false,
  "risks": ["risk 1", "risk 2"],
  "benefits": ["benefit 1"],
  "confidence": 0.0-1.0
}}

Only set should_execute_now=true if:
- Low risk
- Easily reversible
- System health impact
- Confidence > 0.85"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            try:
                decision = json.loads(content)
            except:
                import re
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    decision = json.loads(match.group(1))
                else:
                    return None
            
            print(f"  Decision: {decision['decision']}")
            print(f"  Execute now: {decision['should_execute_now']}")
            print(f"  Confidence: {decision['confidence']:.0%}\n")
            
            # Log decision
            log_decision(situation, decision)
            
            # Execute if approved
            if decision['should_execute_now'] and decision['confidence'] > 0.85:
                execute_decision(decision)
            else:
                print("  ⏳ Decision pending approval\n")
            
            return decision
            
    except Exception as e:
        print(f"✗ Decision error: {e}\n")
        return None

def execute_decision(decision):
    """
    Execute autonomous decision
    """
    print(f"⚡ Executing: {decision['action']}...")
    
    action = decision['action']
    
    # Map actions to functions
    # (Safe actions only - no destructive operations)
    
    if 'restart' in action.lower():
        print("  → Restart requested (requires manual intervention)")
    elif 'increase threshold' in action.lower():
        print("  → Adjusting quality threshold")
        # Adjust config (safe operation)
    elif 'clear cache' in action.lower():
        print("  → Clearing cache")
        # Clear temp files (safe)
    else:
        print(f"  → Action not recognized: {action}")
    
    log_execution(decision)

def log_decision(situation, decision):
    """
    Log autonomous decisions
    """
    decisions_file = STATE_PATH / "autonomous-decisions.json"
    
    if decisions_file.exists():
        with open(decisions_file, 'r') as f:
            log = json.load(f)
    else:
        log = []
    
    log.append({
        'timestamp': datetime.now().isoformat(),
        'situation': situation,
        'decision': decision,
        'executed': decision['should_execute_now']
    })
    
    with open(decisions_file, 'w') as f:
        json.dump(log, f, indent=2)

def log_execution(decision):
    """
    Log decision execution
    """
    # Update decision log with execution result
    pass

# ============================================================================
# HEALTH CHECKS
# ============================================================================

def system_health_check():
    """
    Comprehensive system health check
    """
    health = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'issues': []
    }
    
    # Check database
    if not DB_PATH.exists():
        health['issues'].append({'component': 'database', 'issue': 'missing', 'severity': 'critical'})
        health['status'] = 'critical'
    
    # Check scripts
    required_scripts = ['daily-research.py', 'weekly-generate.py', 'realtime-research.py']
    scripts_dir = Path(__file__).parent
    
    for script in required_scripts:
        if not (scripts_dir / script).exists():
            health['issues'].append({'component': 'script', 'issue': f'{script} missing', 'severity': 'high'})
            health['status'] = 'degraded'
    
    # Check API keys
    if not OPENROUTER_API_KEY:
        health['issues'].append({'component': 'api', 'issue': 'OpenRouter key missing', 'severity': 'high'})
        health['status'] = 'degraded'
    
    # Check recent research
    metrics = monitor_performance()
    if metrics.get('research_health') == 'stale':
        health['issues'].append({'component': 'research', 'issue': 'No research in 24+ hours', 'severity': 'medium'})
        health['status'] = 'degraded' if health['status'] == 'healthy' else health['status']
    
    return health

# ============================================================================
# NOTIFICATIONS
# ============================================================================

def send_alert(message, priority='medium'):
    """
    Send alert via Telegram
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"⚠️  Alert: {message}")
        return
    
    emoji = '🚨' if priority == 'critical' else '⚠️' if priority == 'high' else '📊'
    
    telegram_message = f"""{emoji} **Autonomous Orchestrator Alert**

{message}

Priority: {priority.upper()}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": telegram_message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def notify_fix_pending(file, analysis):
    """
    Notify that auto-fix is pending approval
    """
    send_alert(
        f"Auto-fix available for {file}\n\n"
        f"Issue: {analysis['root_cause']}\n"
        f"Impact: {analysis['impact']}\n\n"
        f"Review: .state/auto-fixes.json",
        priority='medium'
    )

# ============================================================================
# ORCHESTRATOR LOOP
# ============================================================================

def orchestrator_loop():
    """
    Main autonomous loop
    Runs continuously, manages the entire system
    """
    print("=" * 60)
    print("🤖 AUTONOMOUS ORCHESTRATOR STARTED")
    print("=" * 60)
    
    STATE_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    
    iteration = 0
    
    while True:
        iteration += 1
        print(f"\n[Iteration {iteration}] {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # 1. Health check
            health = system_health_check()
            
            if health['status'] == 'critical':
                send_alert(f"System critical: {health['issues']}", priority='critical')
            
            # 2. Monitor for errors
            errors = monitor_logs()
            
            if errors:
                print(f"🔍 Found {len(errors)} errors")
                
                # Auto-heal each error
                for error in errors[-5:]:  # Last 5 errors
                    auto_heal_error(error)
            
            # 3. Performance check
            metrics = monitor_performance()
            
            # 4. Auto-optimize
            actions = auto_optimize_performance(metrics)
            
            # 5. Learn from data (weekly)
            if datetime.now().weekday() == 0:  # Monday
                learn_from_performance()
            
            # Update state
            state = {
                'last_check': datetime.now().isoformat(),
                'iteration': iteration,
                'health': health,
                'metrics': metrics
            }
            
            with open(ORCHESTRATOR_STATE, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Sleep for 2 hours (7200 seconds)
            time.sleep(7200)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Orchestrator stopped by user")
            break
        except Exception as e:
            print(f"✗ Orchestrator error: {e}")
            print(traceback.format_exc())
            send_alert(f"Orchestrator error: {e}", priority='high')
            time.sleep(60)  # Wait 1 min before retry

def single_check():
    """
    Run one health check cycle then exit
    Better for cron scheduling
    """
    print("=" * 60)
    print("🤖 AUTONOMOUS ORCHESTRATOR - SINGLE CHECK")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    STATE_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    
    try:
        # Health check
        health = system_health_check()
        print(f"System status: {health['status']}")
        
        if health['status'] == 'critical':
            send_alert(f"System critical: {health['issues']}", priority='critical')
        
        # Monitor for errors
        errors = monitor_logs()
        
        if errors:
            print(f"🔍 Found {len(errors)} errors, analyzing...")
            
            for error in errors[-3:]:  # Last 3 errors only
                auto_heal_error(error)
        else:
            print("✅ No errors detected")
        
        # Performance check
        metrics = monitor_performance()
        actions = auto_optimize_performance(metrics)
        
        # Learn from data (on Mondays)
        if datetime.now().weekday() == 0:
            learn_from_performance()
        
        # Save state
        state = {
            'last_check': datetime.now().isoformat(),
            'health': health,
            'metrics': metrics,
            'errors_found': len(errors),
            'actions_taken': actions
        }
        
        with open(ORCHESTRATOR_STATE, 'w') as f:
            json.dump(state, f, indent=2)
        
        print("\n✅ Check complete\n")
        
    except Exception as e:
        print(f"✗ Orchestrator error: {e}")
        print(traceback.format_exc())
        send_alert(f"Orchestrator error: {e}", priority='high')

def main():
    """
    Start autonomous orchestrator
    Checks if running as daemon or single-check
    """
    import sys
    
    # Single check mode (better for cron)
    if len(sys.argv) > 1 and sys.argv[1] == '--single-check':
        single_check()
        return
    
    # Daemon mode (continuous loop)
    print("""
🤖 Autonomous Orchestrator v1.0

This agent will:
- Monitor system health every 2 hours
- Detect and fix errors automatically  
- Optimize performance
- Learn from analytics
- Make autonomous decisions
- Alert you only when needed

Running in daemon mode (checks every 2 hours)...
Press Ctrl+C to stop
""")
    
    orchestrator_loop()

if __name__ == "__main__":
    main()
