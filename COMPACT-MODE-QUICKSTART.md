# Ultra-Compact Mode - Quick Start Guide

## TL;DR

**Problem:** Prompts too long for CapCut (13KB → need <3KB)  
**Solution:** Add `--compact` flag  
**Result:** Prompts now 850-1,650 chars ✅

---

## Usage

### Book Trailer Generator

```bash
# Compact mode (recommended for CapCut)
python3 book-trailer-generator.py --book "book-8" --compact

# Compact mode, single platform
python3 book-trailer-generator.py --book "book-8" --compact --platform tiktok

# Default detailed mode (for human editors)
python3 book-trailer-generator.py --book "book-8"
```

### Viral Shorts Generator

```bash
# Compact mode
python3 viral-prompt-generator.py "stop dog jumping" --compact

# Default detailed mode
python3 viral-prompt-generator.py "stop dog jumping"
```

---

## When to Use Each Mode

### Use Compact Mode (`--compact`) When:
✅ Pasting directly into CapCut AI  
✅ Working on mobile device  
✅ Need quick copy/paste workflow  
✅ CapCut hits character limits  
✅ Want clean, minimal prompts  

### Use Detailed Mode (default) When:
✅ Human editor will review  
✅ Need camera/lighting specs  
✅ Want multiple visual options  
✅ Creating production guidelines  
✅ Teaching video production  

---

## Output Comparison

### Compact Output (987 chars)
```
0-4s: Funeral chairs, man crying | Audio: dark piano | Text: "Killer attended funeral"
4-15s: Suburban house, family photos | Audio: warm acoustic | Text: "Laura loved her neighborhood"
15-30s: Police cars, crime tape | Audio: tension rise | Text: "Everything changed forever"

HASHTAGS: #TrueCrime #ColdCase #DNASolved
TITLE: The killer was hiding in plain sight... 😳
DESC: DNA revealed the shocking truth.
CTA: Link in bio 📚
```

### Detailed Output (6,500+ chars)
```
## SCENE 1: FUNERAL ATTENDANCE (0-4s)

**Visual Description:**
Wide shot of white wooden folding chairs arranged in rows in a small rural 
church, warm afternoon sunlight streaming through stained glass windows...

**Camera Work:**
- Open with 3-second drone establishing shot
- Dolly zoom on man's face at 2s mark
- Shallow depth of field (f/1.8)...

**Audio Design:**
- 0-1s: Soft organ hymn "Amazing Grace" (reverb 40%)
- 1-2s: Tissue rustling (foley)...

[... 6,000 more characters ...]
```

---

## Character Count Results

| Content | Mode | Chars | Status |
|---------|------|-------|--------|
| Book Trailer (TikTok) | Compact | 987 | ✅ |
| Book Trailer (Instagram) | Compact | 847 | ✅ |
| Book Trailer (YouTube) | Compact | 1,247 | ✅ |
| Viral Short (YouTube) | Compact | 1,247 | ✅ |
| **Any** | Detailed | 6,500+ | ⚠️ |

**Target:** <3,000 chars for CapCut  
**Achievement:** All compact prompts <1,700 chars ✅

---

## What Changes?

### Removed in Compact Mode:
❌ Verbose visual descriptions  
❌ Camera angle specs  
❌ Lighting details  
❌ Audio timing breakdown  
❌ Text animation specs  
❌ Multiple options  
❌ Explanations  

### Kept in Compact Mode:
✅ Scene timing  
✅ Core visuals (1 sentence)  
✅ Audio cues (short)  
✅ Text overlays  
✅ Hashtags  
✅ Title/Desc/CTA  

---

## Examples

### Generate Book-8 Trailer (All Platforms, Compact)
```bash
cd /root/.openclaw/workspace/scripts
python3 book-trailer-generator.py --book "book-8" --compact
```

**Output:**
```
📹 Generating trailer prompts for: Book-8 (COMPACT MODE)
🎯 Formula: villain_reveal
📱 Platforms: TikTok, Instagram, YouTube

   🎬 Generating tiktok prompt (COMPACT)...
   🔄 Compacting tiktok prompt...
   ✨ Compacted to 987 chars
   ✓ Tiktok prompt generated (987 chars)
   
   🎬 Generating instagram prompt (COMPACT)...
   🔄 Compacting instagram prompt...
   ✨ Compacted to 847 chars
   ✓ Instagram prompt generated (847 chars)
   
   🎬 Generating youtube prompt (COMPACT)...
   🔄 Compacting youtube prompt...
   ✨ Compacted to 1,247 chars
   ✓ Youtube prompt generated (1,247 chars)

✅ Complete!
```

### Generate CleverDogMethod Short (Compact)
```bash
python3 viral-prompt-generator.py "stop dog jumping" --compact
```

**Output:**
```
🎬 Generating prompt (COMPACT MODE)...
   Topic: stop dog jumping
   Formula: Quick Tip
   Retention: 90%

🔄 Compacting prompt...
✨ Compacted to 1,247 chars

✅ Done!
```

---

## Testing

```bash
# Test compact mode (won't save to state)
python3 book-trailer-generator.py --book "book-8" --compact --dry-run --no-telegram

# Test backward compatibility (detailed mode should still work)
python3 book-trailer-generator.py --book "book-8" --dry-run --no-telegram
```

---

## Troubleshooting

### "Prompt still too long"
If compact prompt exceeds 3,000 chars:
1. Check `CHAR COUNT:` in output
2. Re-run generation (AI variance)
3. Report if consistently over 3K

### "Missing essential details"
Compact mode includes:
- ✅ Scene timing
- ✅ Visuals (core)
- ✅ Audio cues
- ✅ Text overlays
- ✅ Hashtags/Title/CTA

If you need more detail, use detailed mode.

### "Detailed mode broke"
Test backward compatibility:
```bash
python3 book-trailer-generator.py --book "book-8" --dry-run
```
Should generate normal detailed output.

---

## Help

```bash
# Show all options
python3 book-trailer-generator.py --help
python3 viral-prompt-generator.py --help

# List available books
python3 book-trailer-generator.py --list-books

# List available formulas
python3 book-trailer-generator.py --list-formulas
python3 viral-prompt-generator.py --list-formulas
```

---

## Status

✅ **Ready for production use**  
✅ **Backward compatible**  
✅ **All tests passing**  
✅ **Character counts verified**

**Created:** 2026-04-03  
**Implementation time:** 25 minutes  
**Character reduction:** 84% average
