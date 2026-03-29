#!/usr/bin/env python3
"""
Generate PDF from Markdown - Puppy Perfect Blueprint
Uses ReportLab for professional PDF generation
"""

import os
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor
import markdown

INPUT_FILE = Path("/root/.openclaw/workspace/content/cleverdogmethod/puppy-blueprint-content.md")
OUTPUT_FILE = Path("/root/.openclaw/workspace/content/cleverdogmethod/puppy-blueprint.pdf")

# Brand colors
BRAND_PURPLE = HexColor('#667eea')
BRAND_DARK = HexColor('#333333')
BRAND_GRAY = HexColor('#666666')

def create_pdf():
    """Generate the PDF from markdown content"""
    
    # Read markdown
    with open(INPUT_FILE, 'r') as f:
        md_content = f.read()
    
    # Convert to HTML (intermediate step)
    html_content = markdown.markdown(md_content)
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=BRAND_PURPLE,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=BRAND_GRAY,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=BRAND_PURPLE,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=BRAND_DARK,
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=BRAND_DARK,
        spaceAfter=12,
        leading=16,
        fontName='Helvetica'
    )
    
    checkbox_style = ParagraphStyle(
        'Checkbox',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=BRAND_DARK,
        leftIndent=20,
        spaceAfter=8,
        fontName='Helvetica'
    )
    
    # Build PDF content
    story = []
    
    # Cover page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("🐾", title_style))
    story.append(Paragraph("The 30-Day Puppy Perfect Blueprint", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Transform Your Puppy Into a Well-Behaved Dog in Just One Month", subtitle_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("By Clever Dog Method™", body_style))
    story.append(Paragraph(f"© {datetime.now().year} | cleverdogmethod.com", body_style))
    story.append(PageBreak())
    
    # Parse markdown and convert to PDF elements
    lines = md_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # Headings
        if line.startswith('# '):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], heading2_style))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], heading3_style))
        
        # Checkboxes
        elif line.startswith('☐') or line.startswith('- ☐'):
            story.append(Paragraph(f"☐ {line.replace('☐', '').replace('- ', '')}", checkbox_style))
        
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(f"• {line[2:]}", body_style))
        
        # Bold markers
        elif line.startswith('**'):
            cleaned = line.replace('**', '')
            story.append(Paragraph(f"<b>{cleaned}</b>", body_style))
        
        # Regular text
        elif line and not line.startswith('#') and not line.startswith('---'):
            story.append(Paragraph(line, body_style))
        
        # Horizontal rules
        elif line.startswith('---'):
            story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    print("📄 Generating PDF...")
    doc.build(story)
    print(f"✅ PDF created: {OUTPUT_FILE}")
    print(f"📊 Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")

def main():
    if not INPUT_FILE.exists():
        print(f"❌ Input file not found: {INPUT_FILE}")
        return
    
    try:
        create_pdf()
        print("\n✅ Success! PDF is ready for delivery.")
        print(f"\nNext steps:")
        print(f"1. Review PDF: {OUTPUT_FILE}")
        print(f"2. Test email delivery")
        print(f"3. Deploy email capture form to blog")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Install required package:")
        print("  pip3 install reportlab markdown")

if __name__ == '__main__':
    main()
