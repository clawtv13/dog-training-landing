"""Video composition module using MoviePy - Full Featured Version"""
from pathlib import Path

# Fix Pillow 10+ compatibility with MoviePy 1.x
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, CompositeAudioClip
)
from config import VIDEO_SETTINGS, SUBTITLE_STYLES, OUTPUT_DIR, TEMP_DIR
from .subtitles import SubtitleSegment, create_animated_subtitles, group_words_into_lines
from .effects import apply_effect, apply_random_effect, EFFECT_PRESETS
from .transitions import concatenate_with_transitions, TRANSITION_PRESETS
from .music import mix_with_music_sync


def compose_video(
    video_clips: list[Path],
    audio_path: Path,
    subtitles: list[SubtitleSegment] = None,
    word_timings: list[dict] = None,
    scenes: list[dict] = None,
    output_name: str = "output",
    aspect_ratio: str = "9:16",
    subtitle_style: str = "bold",
    animated_subtitles: bool = True,
    subtitle_animation: str = "karaoke",
    add_effects: bool = True,
    effect_preset: str = "subtle_ken_burns",
    add_transitions: bool = True,
    transition_type: str = "fade",
    transition_duration: float = 0.4,
    add_music: bool = False,
    music_mood: str = "calm",
    logo_path: Path = None,
    use_images: bool = False,
) -> Path:
    """
    Compose final video from clips, audio, and subtitles.
    
    Args:
        video_clips: List of paths to video clip files
        audio_path: Path to narration audio
        subtitles: List of SubtitleSegment objects (for static subtitles)
        word_timings: Word timing data from TTS (for animated subtitles)
        scenes: Scene data with durations
        output_name: Name for output file
        aspect_ratio: "9:16", "16:9", or "1:1"
        subtitle_style: Style from SUBTITLE_STYLES (for static)
        animated_subtitles: Use animated word-by-word subtitles
        subtitle_animation: "karaoke", "bounce", "highlight_box", "wave"
        add_effects: Apply Ken Burns/pan effects to clips
        effect_preset: Preset from EFFECT_PRESETS
        add_transitions: Add transitions between clips
        transition_type: "fade", "slide", "zoom", "swipe", "random"
        transition_duration: Duration of transitions in seconds
        add_music: Add background music
        music_mood: Mood for music selection
        logo_path: Optional logo to add as watermark
    
    Returns:
        Path to final video
    """
    
    settings = VIDEO_SETTINGS[aspect_ratio]
    target_width = settings["width"]
    target_height = settings["height"]
    style_config = SUBTITLE_STYLES.get(subtitle_style, SUBTITLE_STYLES["bold"])
    
    # Load audio to get total duration
    audio = AudioFileClip(str(audio_path))
    total_duration = audio.duration
    
    # Process video clips or images
    processed_clips = []
    current_time = 0
    
    for i, clip_path in enumerate(video_clips):
        scene_duration = scenes[i]["duration"] if scenes and i < len(scenes) else 3.0
        
        # Load clip (video or image)
        clip_path_str = str(clip_path)
        
        if use_images or clip_path_str.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # It's an image - create ImageClip with duration
            from moviepy.editor import ImageClip
            clip = ImageClip(clip_path_str).set_duration(scene_duration)
        else:
            # It's a video
            clip = VideoFileClip(clip_path_str)
        
        # Resize to fit target dimensions
        clip = resize_and_crop(clip, target_width, target_height)
        
        # Set duration
        if clip.duration < scene_duration:
            clip = clip.loop(duration=scene_duration)
        else:
            clip = clip.subclip(0, scene_duration)
        
        # Apply effects (Ken Burns, pan, etc.)
        if add_effects:
            try:
                clip = apply_effect(clip, effect_preset.split("_")[0] if "_" in effect_preset else "ken_burns")
            except Exception as e:
                print(f"Warning: Could not apply effect to clip {i}: {e}")
        
        processed_clips.append(clip)
        current_time += scene_duration
    
    # Extend last clip if needed
    if current_time < total_duration and processed_clips:
        remaining = total_duration - current_time
        last_clip = processed_clips[-1]
        extension = last_clip.loop(duration=remaining)
        processed_clips.append(extension)
    
    # Concatenate clips with or without transitions
    if processed_clips:
        if add_transitions and len(processed_clips) > 1:
            try:
                video = concatenate_with_transitions(
                    processed_clips, 
                    transition_type=transition_type,
                    duration=transition_duration
                )
            except Exception as e:
                print(f"Warning: Transitions failed, using simple concat: {e}")
                video = concatenate_videoclips(processed_clips, method="compose")
        else:
            video = concatenate_videoclips(processed_clips, method="compose")
    else:
        # Fallback: black background
        video = ColorClip(
            size=(target_width, target_height),
            color=(0, 0, 0),
            duration=total_duration
        )
    
    # Ensure video matches audio duration
    if video.duration > total_duration:
        video = video.subclip(0, total_duration)
    elif video.duration < total_duration:
        # Extend with last frame
        video = video.loop(duration=total_duration)
    
    # Handle audio (with optional music)
    if add_music:
        try:
            mixed_audio_path = mix_with_music_sync(
                narration_path=audio_path,
                mood=music_mood,
                use_ducking=True
            )
            if mixed_audio_path and mixed_audio_path.exists():
                final_audio = AudioFileClip(str(mixed_audio_path))
            else:
                final_audio = audio
        except Exception as e:
            print(f"Warning: Music mixing failed: {e}")
            final_audio = audio
    else:
        final_audio = audio
    
    video = video.set_audio(final_audio)
    
    # Add subtitles
    if animated_subtitles and word_timings:
        try:
            subtitle_clips = create_animated_subtitles(
                word_timings=word_timings,
                style=subtitle_animation,
                video_size=(target_width, target_height)
            )
            if subtitle_clips:
                video = CompositeVideoClip([video] + subtitle_clips)
        except Exception as e:
            print(f"Warning: Animated subtitles failed, using static: {e}")
            if subtitles:
                subtitle_clips = create_static_subtitle_clips(
                    subtitles, target_width, target_height, style_config
                )
                video = CompositeVideoClip([video] + subtitle_clips)
    elif subtitles:
        subtitle_clips = create_static_subtitle_clips(
            subtitles, target_width, target_height, style_config
        )
        if subtitle_clips:
            video = CompositeVideoClip([video] + subtitle_clips)
    
    # Add logo/watermark if provided
    if logo_path and logo_path.exists():
        try:
            video = add_logo_watermark(video, logo_path, target_width, target_height)
        except Exception as e:
            print(f"Warning: Could not add logo: {e}")
    
    # Output path
    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    
    # Export
    video.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="medium",
        threads=4,
        logger=None
    )
    
    # Cleanup
    video.close()
    audio.close()
    for clip in processed_clips:
        try:
            clip.close()
        except:
            pass
    
    return output_path


def resize_and_crop(clip: VideoFileClip, target_width: int, target_height: int) -> VideoFileClip:
    """Resize and crop video to target dimensions while maintaining aspect ratio"""
    
    try:
        target_ratio = target_width / target_height
        clip_ratio = clip.w / clip.h
        
        if clip_ratio > target_ratio:
            # Video is wider, resize by height and crop width
            new_height = target_height
            new_width = int(clip_ratio * new_height)
            clip = clip.resize(newsize=(new_width, new_height))
            
            # Center crop
            x1 = (new_width - target_width) // 2
            x2 = x1 + target_width
            clip = clip.crop(x1=x1, x2=x2, y1=0, y2=target_height)
        else:
            # Video is taller, resize by width and crop height
            new_width = target_width
            new_height = int(new_width / clip_ratio)
            clip = clip.resize(newsize=(new_width, new_height))
            
            # Center crop
            y1 = (new_height - target_height) // 2
            y2 = y1 + target_height
            clip = clip.crop(x1=0, x2=target_width, y1=y1, y2=y2)
        
        return clip
    except Exception as e:
        print(f"Warning: resize_and_crop failed ({e}), returning original clip")
        return clip


def create_static_subtitle_clips(
    subtitles: list[SubtitleSegment],
    width: int,
    height: int,
    style: dict
) -> list[TextClip]:
    """Create static TextClip objects for each subtitle"""
    
    clips = []
    y_position = int(height * style["position"][1])
    
    for sub in subtitles:
        try:
            txt_clip = TextClip(
                sub.text,
                fontsize=style["fontsize"],
                color=style["color"],
                font=style.get("font", "Arial"),
                stroke_color=style.get("stroke_color"),
                stroke_width=style.get("stroke_width", 0),
                method="caption",
                size=(width - 80, None),
                align="center"
            )
            
            txt_clip = txt_clip.set_position(("center", y_position))
            txt_clip = txt_clip.set_start(sub.start)
            txt_clip = txt_clip.set_duration(sub.end - sub.start)
            
            clips.append(txt_clip)
        except Exception as e:
            print(f"Warning: Could not create subtitle clip: {e}")
            continue
    
    return clips


def add_logo_watermark(
    video: CompositeVideoClip,
    logo_path: Path,
    video_width: int,
    video_height: int,
    position: str = "bottom_right",
    opacity: float = 0.7,
    size_ratio: float = 0.15
) -> CompositeVideoClip:
    """Add logo watermark to video"""
    from moviepy.editor import ImageClip
    
    logo = ImageClip(str(logo_path))
    
    # Resize logo
    logo_width = int(video_width * size_ratio)
    logo = logo.resize(width=logo_width)
    
    # Set position
    margin = 20
    if position == "bottom_right":
        pos = (video_width - logo.w - margin, video_height - logo.h - margin)
    elif position == "bottom_left":
        pos = (margin, video_height - logo.h - margin)
    elif position == "top_right":
        pos = (video_width - logo.w - margin, margin)
    elif position == "top_left":
        pos = (margin, margin)
    else:
        pos = ("center", "center")
    
    logo = logo.set_position(pos)
    logo = logo.set_duration(video.duration)
    logo = logo.set_opacity(opacity)
    
    return CompositeVideoClip([video, logo])


def cleanup_temp_files():
    """Remove temporary files"""
    for file in TEMP_DIR.glob("*"):
        try:
            file.unlink()
        except Exception:
            pass
