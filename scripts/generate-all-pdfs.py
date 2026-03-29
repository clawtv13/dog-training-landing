#!/usr/bin/env python3
"""Generate real PDFs from markdown resources"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path
import re

def md_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF"""
    
    # Read markdown
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(str(pdf_file), pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#667eea',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#333',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = styles['BodyText']
    body_style.fontSize = 11
    body_style.leading = 16
    
    story = []
    
    # Parse markdown
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.2*inch))
            continue
        
        # Title (# )
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.3*inch))
        
        # Heading (## )
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading_style))
        
        # Heading (### )
        elif line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(f"<b>{text}</b>", body_style))
        
        # Horizontal rule
        elif line.startswith('---'):
            story.append(Spacer(1, 0.3*inch))
        
        # Checkboxes
        elif line.startswith('- ☐'):
            text = line[4:].strip()
            story.append(Paragraph(f"☐ {text}", body_style))
        
        # Bullets
        elif line.startswith('- '):
            text = line[2:].strip()
            story.append(Paragraph(f"• {text}", body_style))
        
        # Regular text
        elif line and not line.startswith('**') and not line.startswith('['):
            # Remove markdown bold
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            story.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Generated: {pdf_file.name}")

# Generate all PDFs
resources_dir = Path("/root/.openclaw/workspace/content/cleverdogmethod/resources")
output_dir = Path("/root/.openclaw/workspace/dog-training-landing-clean/resources")
output_dir.mkdir(exist_ok=True)

for md_file in sorted(resources_dir.glob("*.md")):
    pdf_file = output_dir / md_file.name.replace('.md', '.pdf')
    try:
        md_to_pdf(md_file, pdf_file)
    except Exception as e:
        print(f"❌ Failed {md_file.name}: {e}")

print(f"\n✅ Done! PDFs in: {output_dir}")
