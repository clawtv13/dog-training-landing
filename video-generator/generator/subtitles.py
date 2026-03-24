"""Subtitle generation and timing module"""
from pathlib import Path
from dataclasses import dataclass
from typing import Callable
from config import SUBTITLE_STYLES

# Fix Pillow 10+ compatibility
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

# MoviePy imports for animated subtitles
try:
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


@dataclass
class SubtitleSegment:
    text: str
    start: float  # seconds
    end: float    # seconds


def generate_subtitles_from_timings(
    word_timings: list[dict],
    max_words_per_segment: int = 5,
    max_duration: float = 2.5
) -> list[SubtitleSegment]:
    """
    Generate subtitle segments from word timings.
    Groups words into readable chunks.
    """
    
    if not word_timings:
        return []
    
    segments = []
    current_words = []
    current_start = None
    
    for timing in word_timings:
        word = timing["text"]
        start = timing["start"]
        duration = timing.get("duration", 0.3)
        end = start + duration
        
        if current_start is None:
            current_start = start
        
        current_words.append(word)
        current_end = end
        
        # Check if we should create a new segment
        segment_duration = current_end - current_start
        should_break = (
            len(current_words) >= max_words_per_segment or
            segment_duration >= max_duration or
            word.endswith(('.', '!', '?', ','))
        )
        
        if should_break and current_words:
            segments.append(SubtitleSegment(
                text=" ".join(current_words),
                start=current_start,
                end=current_end
            ))
            current_words = []
            current_start = None
    
    # Add remaining words
    if current_words:
        segments.append(SubtitleSegment(
            text=" ".join(current_words),
            start=current_start,
            end=current_end
        ))
    
    return segments


def generate_subtitles_simple(
    text: str,
    total_duration: float,
    words_per_segment: int = 4
) -> list[SubtitleSegment]:
    """
    Generate subtitles with evenly distributed timing.
    Fallback when word timings aren't available.
    """
    
    words = text.split()
    segments = []
    
    # Calculate timing
    words_per_second = len(words) / total_duration
    
    for i in range(0, len(words), words_per_segment):
        chunk = words[i:i + words_per_segment]
        chunk_text = " ".join(chunk)
        
        start = i / words_per_second
        end = min((i + len(chunk)) / words_per_second, total_duration)
        
        segments.append(SubtitleSegment(
            text=chunk_text,
            start=round(start, 2),
            end=round(end, 2)
        ))
    
    return segments


def export_srt(segments: list[SubtitleSegment], output_path: Path) -> Path:
    """Export subtitles to SRT format"""
    
    lines = []
    for i, seg in enumerate(segments, 1):
        start_time = _format_srt_time(seg.start)
        end_time = _format_srt_time(seg.end)
        
        lines.append(f"{i}")
        lines.append(f"{start_time} --> {end_time}")
        lines.append(seg.text)
        lines.append("")
    
    output_path.write_text("\n".join(lines))
    return output_path


def _format_srt_time(seconds: float) -> str:
    """Format seconds to SRT time format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def export_ass(
    segments: list[SubtitleSegment],
    output_path: Path,
    style: str = "bold",
    video_width: int = 1080,
    video_height: int = 1920
) -> Path:
    """Export subtitles to ASS format (better styling support)"""
    
    style_config = SUBTITLE_STYLES.get(style, SUBTITLE_STYLES["bold"])
    
    # ASS header
    header = f"""[Script Info]
Title: Generated Subtitles
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{style_config['fontsize']},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    lines = [header]
    
    for seg in segments:
        start = _format_ass_time(seg.start)
        end = _format_ass_time(seg.end)
        # Escape special characters and add styling
        text = seg.text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
    
    output_path.write_text("\n".join(lines))
    return output_path


def _format_ass_time(seconds: float) -> str:
    """Format seconds to ASS time format: H:MM:SS.cc"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int((seconds % 1) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


# =============================================================================
# ANIMATED SUBTITLES (TikTok/CapCut Style)
# =============================================================================

def group_words_into_lines(
    word_timings: list[dict],
    max_words_per_line: int = 4,
    max_chars_per_line: int = 25
) -> list[list[dict]]:
    """
    Group words into lines for display.
    
    Args:
        word_timings: List of word timing dicts with "text", "start", "duration"
        max_words_per_line: Maximum words per line (default 4)
        max_chars_per_line: Maximum characters per line (default 25)
    
    Returns:
        List of lines, where each line is a list of word timing dicts
    """
    if not word_timings:
        return []
    
    lines = []
    current_line = []
    current_chars = 0
    
    for word_info in word_timings:
        word_text = word_info["text"]
        word_len = len(word_text)
        
        # Check if adding this word exceeds limits
        would_exceed_words = len(current_line) >= max_words_per_line
        would_exceed_chars = current_chars + word_len + (1 if current_line else 0) > max_chars_per_line
        
        # Start new line if limits exceeded (but always add at least one word)
        if current_line and (would_exceed_words or would_exceed_chars):
            lines.append(current_line)
            current_line = []
            current_chars = 0
        
        current_line.append(word_info)
        current_chars += word_len + (1 if len(current_line) > 1 else 0)  # +1 for space
        
        # Break on sentence-ending punctuation
        if word_text.rstrip().endswith(('.', '!', '?')):
            lines.append(current_line)
            current_line = []
            current_chars = 0
    
    # Add remaining words
    if current_line:
        lines.append(current_line)
    
    return lines


def create_animated_subtitles(
    word_timings: list[dict],
    style: str = "karaoke",
    active_color: str = "yellow",
    base_color: str = "white",
    font_size: int = 60,
    video_size: tuple = (1080, 1920),
    font: str = "Arial-Bold",
    stroke_color: str = "black",
    stroke_width: int = 3,
    max_words_per_line: int = 4,
    max_chars_per_line: int = 25,
    y_position_ratio: float = 0.72
) -> list:
    """
    Create animated subtitle clips with word-by-word highlighting.
    
    Args:
        word_timings: List of dicts with "text", "start", "duration" keys
        style: Animation style - "karaoke", "bounce", "highlight_box", "wave"
        active_color: Color for the currently spoken word
        base_color: Color for inactive words
        font_size: Base font size
        video_size: Tuple of (width, height)
        font: Font name
        stroke_color: Text outline color
        stroke_width: Text outline width
        max_words_per_line: Max words per line
        max_chars_per_line: Max characters per line
        y_position_ratio: Vertical position (0.0 = top, 1.0 = bottom)
    
    Returns:
        List of MoviePy clips (TextClip or CompositeVideoClip)
    """
    if not MOVIEPY_AVAILABLE:
        raise ImportError(
            "MoviePy is required for animated subtitles. "
            "Install with: pip install moviepy"
        )
    
    if not word_timings:
        return []
    
    video_width, video_height = video_size
    y_position = int(video_height * y_position_ratio)
    
    # Group words into lines
    lines = group_words_into_lines(
        word_timings, 
        max_words_per_line=max_words_per_line,
        max_chars_per_line=max_chars_per_line
    )
    
    all_clips = []
    
    # Get style-specific animation function
    animate_func = _get_animation_function(style)
    
    for line_words in lines:
        if not line_words:
            continue
            
        # Calculate line timing
        line_start = line_words[0]["start"]
        line_end = line_words[-1]["start"] + line_words[-1].get("duration", 0.3)
        
        # Create clips for this line
        line_clips = _create_line_clips(
            line_words=line_words,
            line_start=line_start,
            line_end=line_end,
            style=style,
            active_color=active_color,
            base_color=base_color,
            font_size=font_size,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            video_width=video_width,
            y_position=y_position,
            animate_func=animate_func
        )
        
        all_clips.extend(line_clips)
    
    return all_clips


def _get_animation_function(style: str) -> Callable:
    """Get the animation function for the given style."""
    animations = {
        "karaoke": _animate_karaoke,
        "bounce": _animate_bounce,
        "highlight_box": _animate_highlight_box,
        "wave": _animate_wave,
    }
    return animations.get(style, _animate_karaoke)


def _create_line_clips(
    line_words: list[dict],
    line_start: float,
    line_end: float,
    style: str,
    active_color: str,
    base_color: str,
    font_size: int,
    font: str,
    stroke_color: str,
    stroke_width: int,
    video_width: int,
    y_position: int,
    animate_func: Callable
) -> list:
    """Create clips for a single line of words."""
    
    clips = []
    
    # Pre-calculate word widths for positioning
    word_infos = []
    total_width = 0
    space_width = font_size * 0.3  # Approximate space width
    
    for i, word_data in enumerate(line_words):
        # Create temporary clip to measure width
        temp_clip = TextClip(
            text=word_data["text"],
            font_size=font_size,
            font=font,
            color=base_color
        )
        word_width = temp_clip.size[0]
        temp_clip.close()
        
        word_infos.append({
            **word_data,
            "width": word_width,
            "index": i
        })
        total_width += word_width
        if i < len(line_words) - 1:
            total_width += space_width
    
    # Calculate starting X position (centered)
    start_x = (video_width - total_width) / 2
    current_x = start_x
    
    # Create clips for each word
    for word_info in word_infos:
        word_clips = animate_func(
            word_info=word_info,
            line_words=line_words,
            line_start=line_start,
            line_end=line_end,
            current_x=current_x,
            y_position=y_position,
            active_color=active_color,
            base_color=base_color,
            font_size=font_size,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        clips.extend(word_clips)
        current_x += word_info["width"] + space_width
    
    return clips


def _animate_karaoke(
    word_info: dict,
    line_words: list[dict],
    line_start: float,
    line_end: float,
    current_x: float,
    y_position: int,
    active_color: str,
    base_color: str,
    font_size: int,
    font: str,
    stroke_color: str,
    stroke_width: int
) -> list:
    """
    Karaoke style: word changes color when active.
    Creates two clips - base color and active color - with proper timing.
    """
    word_start = word_info["start"]
    word_end = word_start + word_info.get("duration", 0.3)
    word_text = word_info["text"]
    
    clips = []
    
    # Base color clip (before word is spoken)
    if word_start > line_start:
        base_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        base_clip = base_clip.with_position((current_x, y_position))
        base_clip = base_clip.with_start(line_start)
        base_clip = base_clip.with_duration(word_start - line_start)
        clips.append(base_clip)
    
    # Active color clip (while word is being spoken)
    active_clip = TextClip(
        text=word_text,
        font_size=font_size,
        font=font,
        color=active_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )
    active_clip = active_clip.with_position((current_x, y_position))
    active_clip = active_clip.with_start(word_start)
    active_clip = active_clip.with_duration(word_end - word_start)
    clips.append(active_clip)
    
    # Base color clip (after word is spoken, until line ends)
    if word_end < line_end:
        after_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        after_clip = after_clip.with_position((current_x, y_position))
        after_clip = after_clip.with_start(word_end)
        after_clip = after_clip.with_duration(line_end - word_end)
        clips.append(after_clip)
    
    return clips


def _animate_bounce(
    word_info: dict,
    line_words: list[dict],
    line_start: float,
    line_end: float,
    current_x: float,
    y_position: int,
    active_color: str,
    base_color: str,
    font_size: int,
    font: str,
    stroke_color: str,
    stroke_width: int
) -> list:
    """
    Bounce style: word scales up when active, with color change.
    """
    word_start = word_info["start"]
    word_end = word_start + word_info.get("duration", 0.3)
    word_text = word_info["text"]
    word_duration = word_end - word_start
    
    clips = []
    scale_factor = 1.15  # Scale up 15%
    
    # Base clip (before active)
    if word_start > line_start:
        base_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        base_clip = base_clip.with_position((current_x, y_position))
        base_clip = base_clip.with_start(line_start)
        base_clip = base_clip.with_duration(word_start - line_start)
        clips.append(base_clip)
    
    # Scaled/active clip with bounce effect
    scaled_font_size = int(font_size * scale_factor)
    
    # Create the bouncing clip
    bounce_clip = TextClip(
        text=word_text,
        font_size=scaled_font_size,
        font=font,
        color=active_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )
    
    # Adjust position for larger size (center it properly)
    size_diff_x = (bounce_clip.size[0] - word_info["width"]) / 2
    size_diff_y = (scaled_font_size - font_size) / 2
    
    bounce_clip = bounce_clip.with_position((current_x - size_diff_x, y_position - size_diff_y))
    bounce_clip = bounce_clip.with_start(word_start)
    bounce_clip = bounce_clip.with_duration(word_duration)
    clips.append(bounce_clip)
    
    # After clip (return to base)
    if word_end < line_end:
        after_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        after_clip = after_clip.with_position((current_x, y_position))
        after_clip = after_clip.with_start(word_end)
        after_clip = after_clip.with_duration(line_end - word_end)
        clips.append(after_clip)
    
    return clips


def _animate_highlight_box(
    word_info: dict,
    line_words: list[dict],
    line_start: float,
    line_end: float,
    current_x: float,
    y_position: int,
    active_color: str,
    base_color: str,
    font_size: int,
    font: str,
    stroke_color: str,
    stroke_width: int
) -> list:
    """
    Highlight box style: active word has a colored background box.
    """
    word_start = word_info["start"]
    word_end = word_start + word_info.get("duration", 0.3)
    word_text = word_info["text"]
    word_width = word_info["width"]
    word_duration = word_end - word_start
    
    clips = []
    padding_x = 8
    padding_y = 4
    box_height = font_size + padding_y * 2
    box_width = word_width + padding_x * 2
    
    # Base text clip (shown throughout the line duration)
    base_clip = TextClip(
        text=word_text,
        font_size=font_size,
        font=font,
        color=base_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )
    base_clip = base_clip.with_position((current_x, y_position))
    base_clip = base_clip.with_start(line_start)
    base_clip = base_clip.with_duration(line_end - line_start)
    clips.append(base_clip)
    
    # Highlight box behind active word
    box_clip = ColorClip(
        size=(int(box_width), int(box_height)),
        color=_color_name_to_rgb(active_color)
    )
    box_clip = box_clip.with_opacity(0.7)
    box_clip = box_clip.with_position((current_x - padding_x, y_position - padding_y))
    box_clip = box_clip.with_start(word_start)
    box_clip = box_clip.with_duration(word_duration)
    
    # Active text on top of box (slightly different style)
    active_text = TextClip(
        text=word_text,
        font_size=font_size,
        font=font,
        color="black",  # Dark text on colored background
        stroke_color=None,
        stroke_width=0
    )
    active_text = active_text.with_position((current_x, y_position))
    active_text = active_text.with_start(word_start)
    active_text = active_text.with_duration(word_duration)
    
    # Box should be rendered before text
    clips.insert(0, box_clip)  # Insert at beginning so it renders behind
    clips.append(active_text)
    
    return clips


def _animate_wave(
    word_info: dict,
    line_words: list[dict],
    line_start: float,
    line_end: float,
    current_x: float,
    y_position: int,
    active_color: str,
    base_color: str,
    font_size: int,
    font: str,
    stroke_color: str,
    stroke_width: int
) -> list:
    """
    Wave style: words appear one by one with a fade-in effect.
    Word stays visible in base_color after appearing, then highlights when active.
    """
    word_start = word_info["start"]
    word_end = word_start + word_info.get("duration", 0.3)
    word_text = word_info["text"]
    word_index = word_info["index"]
    
    clips = []
    fade_duration = 0.15  # Quick fade in
    
    # Calculate when this word should appear (slightly before it's spoken)
    appear_time = max(line_start, word_start - 0.1)
    
    # Fade-in clip (word appearing)
    if appear_time < word_start:
        fade_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        fade_clip = fade_clip.with_position((current_x, y_position))
        fade_clip = fade_clip.with_start(appear_time)
        fade_clip = fade_clip.with_duration(word_start - appear_time)
        
        # Apply fade in effect
        fade_clip = fade_clip.with_effects([
            _create_fadein_effect(min(fade_duration, word_start - appear_time))
        ])
        clips.append(fade_clip)
    
    # Active clip (highlighted when spoken)
    active_clip = TextClip(
        text=word_text,
        font_size=font_size,
        font=font,
        color=active_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width
    )
    active_clip = active_clip.with_position((current_x, y_position))
    active_clip = active_clip.with_start(word_start)
    active_clip = active_clip.with_duration(word_end - word_start)
    clips.append(active_clip)
    
    # After clip (visible until line ends)
    if word_end < line_end:
        after_clip = TextClip(
            text=word_text,
            font_size=font_size,
            font=font,
            color=base_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        after_clip = after_clip.with_position((current_x, y_position))
        after_clip = after_clip.with_start(word_end)
        after_clip = after_clip.with_duration(line_end - word_end)
        clips.append(after_clip)
    
    return clips


def _create_fadein_effect(duration: float):
    """Create a fade-in effect for MoviePy 2.x"""
    from moviepy.video.fx import FadeIn
    return FadeIn(duration)


def _color_name_to_rgb(color_name: str) -> tuple:
    """Convert color name to RGB tuple."""
    colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "cyan": (0, 255, 255),
        "lime": (50, 205, 50),
    }
    return colors.get(color_name.lower(), (255, 255, 0))  # Default to yellow


def apply_animated_subtitles(
    video_clip,
    word_timings: list[dict],
    style: str = "karaoke",
    **kwargs
) -> "CompositeVideoClip":
    """
    Apply animated subtitles to an existing video clip.
    
    Args:
        video_clip: The base MoviePy video clip
        word_timings: Word timing information from TTS
        style: Animation style
        **kwargs: Additional arguments for create_animated_subtitles
    
    Returns:
        CompositeVideoClip with subtitles overlaid
    """
    if not MOVIEPY_AVAILABLE:
        raise ImportError("MoviePy is required for animated subtitles")
    
    video_size = video_clip.size
    
    subtitle_clips = create_animated_subtitles(
        word_timings=word_timings,
        style=style,
        video_size=video_size,
        **kwargs
    )
    
    # Combine video with subtitle clips
    all_clips = [video_clip] + subtitle_clips
    return CompositeVideoClip(all_clips)
