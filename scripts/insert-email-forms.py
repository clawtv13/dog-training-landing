#!/usr/bin/env python3
"""
Insert email capture forms into all blog posts
Adds form after ~30% of content
"""

from pathlib import Path
from bs4 import BeautifulSoup

BLOG_DIR = Path("/root/.openclaw/workspace/dog-training-landing-clean/blog")
EMAIL_FORM_PATH = Path("/root/.openclaw/workspace/dog-training-landing-clean/email-capture.html")

# Read email form template
with open(EMAIL_FORM_PATH, 'r') as f:
    email_form_html = f.read()

def insert_email_form(html_file):
    """Insert email form after 30% of content"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all paragraphs in main content
    paragraphs = soup.find_all('p')
    
    if len(paragraphs) < 3:
        print(f"⚠️  {html_file.name}: Too short, skipping")
        return False
    
    # Insert after paragraph ~30% through
    insert_after_index = len(paragraphs) // 3
    insert_after_p = paragraphs[insert_after_index]
    
    # Check if form already exists
    if soup.find(class_='email-capture-inline'):
        print(f"✓ {html_file.name}: Form already exists")
        return False
    
    # Insert form
    form_soup = BeautifulSoup(email_form_html, 'html.parser')
    insert_after_p.insert_after(form_soup)
    
    # Save
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✅ {html_file.name}: Form inserted after paragraph {insert_after_index}")
    return True

def main():
    print("📧 Inserting email capture forms into blog posts...\n")
    
    inserted = 0
    skipped = 0
    
    for html_file in BLOG_DIR.glob("*.html"):
        if html_file.name == 'index.html':
            continue
        
        if insert_email_form(html_file):
            inserted += 1
        else:
            skipped += 1
    
    print(f"\n📊 Summary:")
    print(f"   Forms inserted: {inserted}")
    print(f"   Skipped: {skipped}")

if __name__ == '__main__':
    main()
