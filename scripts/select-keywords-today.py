#!/usr/bin/env python3
"""Quick script to select 6 keywords from expansion for today"""
import re
from pathlib import Path

keywords_file = Path("content/cleverdogmethod/KEYWORDS-EXPANSION.md")

with open(keywords_file) as f:
    content = f.read()

keywords = []
for line in content.split('\n'):
    if '|' in line and '⭐' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 5 and parts[1]:
            keyword = parts[1]
            priority = parts[4].count('⭐')
            if keyword and keyword != 'Keyword':
                keywords.append({'keyword': keyword, 'priority': priority})

# Sort by priority
keywords.sort(key=lambda x: x['priority'], reverse=True)

# Select top 6 not yet published
published_file = Path(".state/cleverdogmethod-published.json")
import json
with open(published_file) as f:
    published = json.load(f)

published_slugs = [p['slug'] for p in published]

selected = []
for kw in keywords:
    slug = kw['keyword'].lower().replace(' ', '-')
    if slug not in published_slugs and slug not in [s['slug'] for s in selected]:
        selected.append({'keyword': kw['keyword'], 'slug': slug})
        if len(selected) == 6:
            break

print("✅ KEYWORDS FOR TODAY:")
for i, kw in enumerate(selected, 1):
    print(f"{i}. {kw['keyword']}")
