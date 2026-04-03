#!/usr/bin/env python3
"""
Compact long prompts for CapCut character limits
Target: 2000-3000 chars per platform
"""

import sys
import re
from pathlib import Path

def compact_prompt(text: str) -> str:
    """Compress prompt to essential CapCut instructions"""
    
    lines = text.split('\n')
    compact = []
    
    current_scene = None
    scene_content = []
    
    for line in lines:
        line = line.strip()
        
        # Scene header
        if re.match(r'\*\*SCENE \d+', line):
            # Save previous scene
            if current_scene and scene_content:
                compact.append(f"{current_scene}: {' | '.join(scene_content)}")
            
            # Extract timing
            timing = re.search(r'\((\d+-\d+s)\)', line)
            if timing:
                current_scene = timing.group(1)
            scene_content = []
            continue
        
        # Visual details
        if line.startswith('- ') or line.startswith('* '):
            visual = line[2:].strip()
            # Remove verbose descriptions
            visual = visual.split(':')[-1].strip()
            if visual and len(visual) > 20:
                scene_content.append(visual[:150])
        
        # Audio
        if 'AUDIO:' in line or 'Audio:' in line:
            audio = line.split(':')[-1].strip()
            if audio:
                scene_content.append(f"🔊 {audio[:100]}")
        
        # Text overlay
        if 'TEXT OVERLAY:' in line or 'Text:' in line:
            text_ov = line.split(':')[-1].strip()
            if text_ov:
                scene_content.append(f"📝 {text_ov[:80]}")
    
    # Last scene
    if current_scene and scene_content:
        compact.append(f"{current_scene}: {' | '.join(scene_content)}")
    
    return '\n'.join(compact)

def process_file(input_path: Path):
    """Compress prompt file"""
    
    with open(input_path) as f:
        content = f.read()
    
    # Split by platform if multi-platform
    platforms = {}
    
    for platform in ['TIKTOK', 'INSTAGRAM', 'YOUTUBE']:
        pattern = f'**{platform}:**'
        if pattern in content:
            start = content.find(pattern)
            # Find next platform or end
            next_plat = len(content)
            for other in ['TIKTOK', 'INSTAGRAM', 'YOUTUBE']:
                if other != platform:
                    next_start = content.find(f'**{other}:**', start + 1)
                    if next_start != -1:
                        next_plat = min(next_plat, next_start)
            
            section = content[start:next_plat]
            platforms[platform] = compact_prompt(section)
    
    # Build output
    output = f"# COMPACT PROMPT - {input_path.stem}\n\n"
    
    for platform, compact in platforms.items():
        char_count = len(compact)
        status = "✅" if char_count < 3000 else "⚠️"
        
        output += f"## {platform} ({char_count} chars {status})\n\n"
        output += compact
        output += "\n\n" + "="*60 + "\n\n"
    
    # Save
    output_path = input_path.parent / f"COMPACT-{input_path.name}"
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"✅ Compacted: {output_path.name}")
    print(f"   Original: {len(content)} chars")
    print(f"   Compact: {len(output)} chars")
    print(f"   Savings: {100 - int(len(output)/len(content)*100)}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compact_prompt.py <prompt_file.txt>")
        sys.exit(1)
    
    process_file(Path(sys.argv[1]))
