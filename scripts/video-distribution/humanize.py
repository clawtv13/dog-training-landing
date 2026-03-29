#!/usr/bin/env python3
"""
Humanize AI-generated text
Usage: python humanize.py <text>
"""
import sys
import subprocess

def humanize(text):
    """Run humanize-ai-text transform"""
    
    result = subprocess.run(
        [
            "python3",
            "/root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py",
            "-q",  # Quiet mode
            "-a"   # Aggressive mode
        ],
        input=text.encode(),
        capture_output=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Humanize failed: {result.stderr.decode()}")
    
    return result.stdout.decode().strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        text = sys.stdin.read()
    else:
        text = sys.argv[1]
    
    try:
        humanized = humanize(text)
        print(humanized)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
